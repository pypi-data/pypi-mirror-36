# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
"""Tests for Volume Code."""

import datetime
import ddt
import os
import shutil
import sys
import tempfile
import time
import uuid

import enum
import eventlet
import mock
import os_brick
from oslo_concurrency import processutils
from oslo_config import cfg
from oslo_serialization import jsonutils
from oslo_utils import imageutils
from oslo_utils import importutils
from oslo_utils import timeutils
from oslo_utils import units
import six
from taskflow.engines.action_engine import engine

from cinder.api import common
from cinder.brick.local_dev import lvm as brick_lvm
from cinder.common import constants
from cinder import context
from cinder import coordination
from cinder import db
from cinder import exception
from cinder.image import image_utils
from cinder import keymgr as key_manager
from cinder.message import defined_messages
from cinder.message import resource_types
from cinder import objects
from cinder.objects import fields
import cinder.policy
from cinder import quota
from cinder import test
from cinder.tests import fake_driver
from cinder.tests.unit.api import fakes
from cinder.tests.unit.brick import fake_lvm
from cinder.tests.unit import conf_fixture
from cinder.tests.unit import fake_constants as fake
from cinder.tests.unit import fake_service
from cinder.tests.unit import fake_snapshot
from cinder.tests.unit import fake_volume
from cinder.tests.unit.image import fake as fake_image
from cinder.tests.unit.keymgr import fake as fake_keymgr
from cinder.tests.unit import utils as tests_utils
from cinder.tests.unit import volume as base
from cinder import utils
import cinder.volume
from cinder.volume import api as volume_api
from cinder.volume import configuration as conf
from cinder.volume import driver
from cinder.volume.flows.manager import create_volume as create_volume_manager
from cinder.volume import manager as vol_manager
from cinder.volume import rpcapi as volume_rpcapi
import cinder.volume.targets.tgt
from cinder.volume import utils as volutils
from cinder.volume import volume_types


QUOTAS = quota.QUOTAS

CONF = cfg.CONF

ENCRYPTION_PROVIDER = 'nova.volume.encryptors.cryptsetup.CryptsetupEncryptor'

fake_opt = [
    cfg.StrOpt('fake_opt1', default='fake', help='fake opts')
]


OVER_SNAPSHOT_QUOTA_EXCEPTION = exception.OverQuota(
    overs=['snapshots'],
    usages = {'snapshots': {'reserved': 1, 'in_use': 9}},
    quotas = {'gigabytes': 10, 'snapshots': 10})


def create_snapshot(volume_id, size=1, metadata=None, ctxt=None,
                    **kwargs):
    """Create a snapshot object."""
    metadata = metadata or {}
    snap = objects.Snapshot(ctxt or context.get_admin_context())
    snap.volume_size = size
    snap.user_id = kwargs.get('user_id', fake.USER_ID)
    snap.project_id = kwargs.get('project_id', fake.PROJECT_ID)
    snap.volume_id = volume_id
    snap.status = "creating"
    if metadata is not None:
        snap.metadata = metadata
    snap.update(kwargs)

    snap.create()
    return snap


class FakeImageService(object):
    def __init__(self, db_driver=None, image_service=None):
        pass

    def show(self, context, image_id):
        return {'size': 2 * units.Gi,
                'disk_format': 'raw',
                'container_format': 'bare',
                'status': 'active'}


class AvailabilityZoneTestCase(base.BaseVolumeTestCase):
    def setUp(self):
        super(AvailabilityZoneTestCase, self).setUp()
        self.get_all = self.patch(
            'cinder.db.service_get_all', autospec=True,
            return_value = [{'availability_zone': 'a', 'disabled': False}])

    def test_list_availability_zones_cached(self):
        azs = self.volume_api.list_availability_zones(enable_cache=True)
        self.assertEqual([{"name": 'a', 'available': True}], list(azs))
        self.assertIsNotNone(self.volume_api.availability_zones_last_fetched)
        self.assertTrue(self.get_all.called)
        self.volume_api.list_availability_zones(enable_cache=True)
        self.assertEqual(1, self.get_all.call_count)

    def test_list_availability_zones_no_cached(self):
        azs = self.volume_api.list_availability_zones(enable_cache=False)
        self.assertEqual([{"name": 'a', 'available': True}], list(azs))
        self.assertIsNone(self.volume_api.availability_zones_last_fetched)

        self.get_all.return_value[0]['disabled'] = True
        azs = self.volume_api.list_availability_zones(enable_cache=False)
        self.assertEqual([{"name": 'a', 'available': False}], list(azs))
        self.assertIsNone(self.volume_api.availability_zones_last_fetched)

    @mock.patch('oslo_utils.timeutils.utcnow')
    def test_list_availability_zones_refetched(self, mock_utcnow):
        mock_utcnow.return_value = datetime.datetime.utcnow()
        azs = self.volume_api.list_availability_zones(enable_cache=True)
        self.assertEqual([{"name": 'a', 'available': True}], list(azs))
        self.assertIsNotNone(self.volume_api.availability_zones_last_fetched)
        last_fetched = self.volume_api.availability_zones_last_fetched
        self.assertTrue(self.get_all.called)
        self.volume_api.list_availability_zones(enable_cache=True)
        self.assertEqual(1, self.get_all.call_count)

        # The default cache time is 3600, push past that...
        mock_utcnow.return_value = (timeutils.utcnow() +
                                    datetime.timedelta(0, 3800))
        self.get_all.return_value = [
            {
                'availability_zone': 'a',
                'disabled': False,
            },
            {
                'availability_zone': 'b',
                'disabled': False,
            },
        ]
        azs = self.volume_api.list_availability_zones(enable_cache=True)
        azs = sorted([n['name'] for n in azs])
        self.assertEqual(['a', 'b'], azs)
        self.assertEqual(2, self.get_all.call_count)
        self.assertGreater(self.volume_api.availability_zones_last_fetched,
                           last_fetched)
        mock_utcnow.assert_called_with()

    def test_list_availability_zones_enabled_service(self):
        def sort_func(obj):
            return obj['name']

        self.get_all.return_value = [
            {'availability_zone': 'ping', 'disabled': 0},
            {'availability_zone': 'ping', 'disabled': 1},
            {'availability_zone': 'pong', 'disabled': 0},
            {'availability_zone': 'pung', 'disabled': 1},
        ]

        volume_api = cinder.volume.api.API()
        azs = volume_api.list_availability_zones()
        azs = sorted(azs, key=sort_func)

        expected = sorted([
            {'name': 'pung', 'available': False},
            {'name': 'pong', 'available': True},
            {'name': 'ping', 'available': True},
        ], key=sort_func)

        self.assertEqual(expected, azs)


@ddt.ddt
class VolumeTestCase(base.BaseVolumeTestCase):

    def setUp(self):
        super(VolumeTestCase, self).setUp()
        self.patch('cinder.volume.utils.clear_volume', autospec=True)
        self.expected_status = 'available'
        self.service_id = 1
        self.user_context = context.RequestContext(user_id=fake.USER_ID,
                                                   project_id=fake.PROJECT_ID)

    @mock.patch('cinder.manager.CleanableManager.init_host')
    def test_init_host_count_allocated_capacity(self, init_host_mock):
        vol0 = tests_utils.create_volume(
            self.context, size=100, host=CONF.host)
        vol1 = tests_utils.create_volume(
            self.context, size=128,
            host=volutils.append_host(CONF.host, 'pool0'))
        vol2 = tests_utils.create_volume(
            self.context, size=256,
            host=volutils.append_host(CONF.host, 'pool0'))
        vol3 = tests_utils.create_volume(
            self.context, size=512,
            host=volutils.append_host(CONF.host, 'pool1'))
        vol4 = tests_utils.create_volume(
            self.context, size=1024,
            host=volutils.append_host(CONF.host, 'pool2'))
        self.volume.init_host(service_id=self.service_id)
        init_host_mock.assert_called_once_with(
            service_id=self.service_id, added_to_cluster=None)
        stats = self.volume.stats
        self.assertEqual(2020, stats['allocated_capacity_gb'])
        self.assertEqual(
            384, stats['pools']['pool0']['allocated_capacity_gb'])
        self.assertEqual(
            512, stats['pools']['pool1']['allocated_capacity_gb'])
        self.assertEqual(
            1024, stats['pools']['pool2']['allocated_capacity_gb'])

        # NOTE(jdg): On the create we have host='xyz', BUT
        # here we do a db.volume_get, and now the host has
        # been updated to xyz#pool-name.  Note this is
        # done via the managers init, which calls the drivers
        # get_pool method, which in the legacy case is going
        # to be volume_backend_name or None

        vol0.refresh()
        expected_host = volutils.append_host(CONF.host, 'fake')
        self.assertEqual(expected_host, vol0.host)
        self.volume.delete_volume(self.context, vol0)
        self.volume.delete_volume(self.context, vol1)
        self.volume.delete_volume(self.context, vol2)
        self.volume.delete_volume(self.context, vol3)
        self.volume.delete_volume(self.context, vol4)

    @mock.patch('cinder.manager.CleanableManager.init_host')
    def test_init_host_count_allocated_capacity_cluster(self, init_host_mock):
        cluster_name = 'mycluster'
        self.volume.cluster = cluster_name
        # All these volumes belong to the same cluster, so we will calculate
        # the capacity of them all because we query the DB by cluster_name.
        tests_utils.create_volume(self.context, size=100, host=CONF.host,
                                  cluster_name=cluster_name)
        tests_utils.create_volume(
            self.context, size=128, cluster_name=cluster_name,
            host=volutils.append_host(CONF.host, 'pool0'))
        tests_utils.create_volume(
            self.context, size=256, cluster_name=cluster_name,
            host=volutils.append_host(CONF.host + '2', 'pool0'))
        tests_utils.create_volume(
            self.context, size=512, cluster_name=cluster_name,
            host=volutils.append_host(CONF.host + '2', 'pool1'))
        tests_utils.create_volume(
            self.context, size=1024, cluster_name=cluster_name,
            host=volutils.append_host(CONF.host + '3', 'pool2'))

        # These don't belong to the cluster so they will be ignored
        tests_utils.create_volume(
            self.context, size=1024,
            host=volutils.append_host(CONF.host, 'pool2'))
        tests_utils.create_volume(
            self.context, size=1024, cluster_name=cluster_name + '1',
            host=volutils.append_host(CONF.host + '3', 'pool2'))

        self.volume.init_host(service_id=self.service_id)
        init_host_mock.assert_called_once_with(
            service_id=self.service_id, added_to_cluster=None)
        stats = self.volume.stats
        self.assertEqual(2020, stats['allocated_capacity_gb'])
        self.assertEqual(
            384, stats['pools']['pool0']['allocated_capacity_gb'])
        self.assertEqual(
            512, stats['pools']['pool1']['allocated_capacity_gb'])
        self.assertEqual(
            1024, stats['pools']['pool2']['allocated_capacity_gb'])

    @mock.patch.object(driver.BaseVD, "update_provider_info")
    def test_init_host_sync_provider_info(self, mock_update):
        vol0 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host)
        vol1 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host)
        vol2 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host, status='creating')
        snap0 = tests_utils.create_snapshot(self.context, vol0.id)
        snap1 = tests_utils.create_snapshot(self.context, vol1.id)
        # Return values for update_provider_info
        volumes = [{'id': vol0.id, 'provider_id': '1 2 xxxx'},
                   {'id': vol1.id, 'provider_id': '3 4 yyyy'}]
        snapshots = [{'id': snap0.id, 'provider_id': '5 6 xxxx'},
                     {'id': snap1.id, 'provider_id': '7 8 yyyy'}]
        mock_update.return_value = (volumes, snapshots)
        # initialize
        self.volume.init_host(service_id=self.service_id)
        # Grab volume and snapshot objects
        vol0_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol0.id)
        vol1_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol1.id)
        vol2_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol2.id)
        snap0_obj = objects.Snapshot.get_by_id(self.context, snap0.id)
        snap1_obj = objects.Snapshot.get_by_id(self.context, snap1.id)
        # Check updated provider ids
        self.assertEqual('1 2 xxxx', vol0_obj.provider_id)
        self.assertEqual('3 4 yyyy', vol1_obj.provider_id)
        self.assertIsNone(vol2_obj.provider_id)
        self.assertEqual('5 6 xxxx', snap0_obj.provider_id)
        self.assertEqual('7 8 yyyy', snap1_obj.provider_id)
        # Clean up
        self.volume.delete_snapshot(self.context, snap0_obj)
        self.volume.delete_snapshot(self.context, snap1_obj)
        self.volume.delete_volume(self.context, vol0)
        self.volume.delete_volume(self.context, vol1)

    @mock.patch.object(driver.BaseVD, "update_provider_info")
    def test_init_host_sync_provider_info_no_update(self, mock_update):
        vol0 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host)
        vol1 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host)
        snap0 = tests_utils.create_snapshot(self.context, vol0.id)
        snap1 = tests_utils.create_snapshot(self.context, vol1.id)
        mock_update.return_value = ([], [])
        # initialize
        self.volume.init_host(service_id=self.service_id)
        # Grab volume and snapshot objects
        vol0_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol0.id)
        vol1_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol1.id)
        snap0_obj = objects.Snapshot.get_by_id(self.context, snap0.id)
        snap1_obj = objects.Snapshot.get_by_id(self.context, snap1.id)
        # Check provider ids are not changed
        self.assertIsNone(vol0_obj.provider_id)
        self.assertIsNone(vol1_obj.provider_id)
        self.assertIsNone(snap0_obj.provider_id)
        self.assertIsNone(snap1_obj.provider_id)
        # Clean up
        self.volume.delete_snapshot(self.context, snap0_obj)
        self.volume.delete_snapshot(self.context, snap1_obj)
        self.volume.delete_volume(self.context, vol0)
        self.volume.delete_volume(self.context, vol1)

    @mock.patch.object(driver.BaseVD, "update_provider_info")
    def test_init_host_sync_provider_info_no_update_cluster(self, mock_update):
        cluster_name = 'mycluster'
        self.volume.cluster = cluster_name
        vol0 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host, cluster_name=cluster_name)
        vol1 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host + '2',
            cluster_name=cluster_name)
        vol2 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host)
        vol3 = tests_utils.create_volume(
            self.context, size=1, host=CONF.host,
            cluster_name=cluster_name + '2')
        snap0 = tests_utils.create_snapshot(self.context, vol0.id)
        snap1 = tests_utils.create_snapshot(self.context, vol1.id)
        tests_utils.create_snapshot(self.context, vol2.id)
        tests_utils.create_snapshot(self.context, vol3.id)
        mock_update.return_value = ([], [])
        # initialize
        self.volume.init_host(service_id=self.service_id)
        # Grab volume and snapshot objects
        vol0_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol0.id)
        vol1_obj = objects.Volume.get_by_id(context.get_admin_context(),
                                            vol1.id)
        snap0_obj = objects.Snapshot.get_by_id(self.context, snap0.id)
        snap1_obj = objects.Snapshot.get_by_id(self.context, snap1.id)

        self.assertSetEqual({vol0.id, vol1.id},
                            {vol.id for vol in mock_update.call_args[0][0]})
        self.assertSetEqual({snap0.id, snap1.id},
                            {snap.id for snap in mock_update.call_args[0][1]})
        # Check provider ids are not changed
        self.assertIsNone(vol0_obj.provider_id)
        self.assertIsNone(vol1_obj.provider_id)
        self.assertIsNone(snap0_obj.provider_id)
        self.assertIsNone(snap1_obj.provider_id)
        # Clean up
        self.volume.delete_snapshot(self.context, snap0_obj)
        self.volume.delete_snapshot(self.context, snap1_obj)
        self.volume.delete_volume(self.context, vol0)
        self.volume.delete_volume(self.context, vol1)

    @mock.patch('cinder.volume.manager.VolumeManager.'
                '_include_resources_in_cluster')
    def test_init_host_cluster_not_changed(self, include_in_cluster_mock):
        self.volume.init_host(added_to_cluster=False,
                              service_id=self.service_id)
        include_in_cluster_mock.assert_not_called()

    @mock.patch('cinder.objects.snapshot.SnapshotList.get_all',
                return_value=[])
    @mock.patch('cinder.objects.volume.VolumeList.get_all', return_value=[])
    @mock.patch('cinder.objects.volume.VolumeList.include_in_cluster')
    @mock.patch('cinder.objects.consistencygroup.ConsistencyGroupList.'
                'include_in_cluster')
    @mock.patch('cinder.db.image_volume_cache_include_in_cluster')
    def test_init_host_added_to_cluster(self, image_cache_include_mock,
                                        cg_include_mock,
                                        vol_include_mock, vol_get_all_mock,
                                        snap_get_all_mock):
        cluster = str(mock.sentinel.cluster)
        self.mock_object(self.volume, 'cluster', cluster)
        self.volume.init_host(added_to_cluster=True,
                              service_id=self.service_id)

        vol_include_mock.assert_called_once_with(mock.ANY, cluster,
                                                 host=self.volume.host)
        cg_include_mock.assert_called_once_with(mock.ANY, cluster,
                                                host=self.volume.host)
        image_cache_include_mock.assert_called_once_with(mock.ANY, cluster,
                                                         host=self.volume.host)
        vol_get_all_mock.assert_called_once_with(
            mock.ANY, filters={'cluster_name': cluster})
        snap_get_all_mock.assert_called_once_with(
            mock.ANY, filters={'cluster_name': cluster})

    @mock.patch('cinder.objects.service.Service.get_minimum_rpc_version')
    @mock.patch('cinder.objects.service.Service.get_minimum_obj_version')
    @mock.patch('cinder.rpc.LAST_RPC_VERSIONS', {'cinder-scheduler': '1.3'})
    @mock.patch('cinder.rpc.LAST_OBJ_VERSIONS', {'cinder-scheduler': '1.4'})
    def test_reset(self, get_min_obj, get_min_rpc):
        vol_mgr = vol_manager.VolumeManager()

        scheduler_rpcapi = vol_mgr.scheduler_rpcapi
        self.assertEqual('1.3', scheduler_rpcapi.client.version_cap)
        self.assertEqual('1.4',
                         scheduler_rpcapi.client.serializer._base.version_cap)
        get_min_obj.return_value = objects.base.OBJ_VERSIONS.get_current()
        vol_mgr.reset()

        scheduler_rpcapi = vol_mgr.scheduler_rpcapi
        self.assertEqual(get_min_rpc.return_value,
                         scheduler_rpcapi.client.version_cap)
        self.assertEqual(get_min_obj.return_value,
                         scheduler_rpcapi.client.serializer._base.version_cap)
        self.assertIsNone(scheduler_rpcapi.client.serializer._base.manifest)

    @mock.patch.object(vol_manager.VolumeManager,
                       'update_service_capabilities')
    def test_report_filter_goodness_function(self, mock_update):
        manager = vol_manager.VolumeManager()
        manager.driver.set_initialized()
        myfilterfunction = "myFilterFunction"
        mygoodnessfunction = "myGoodnessFunction"
        expected = {'name': 'cinder-volumes',
                    'filter_function': myfilterfunction,
                    'goodness_function': mygoodnessfunction,
                    }
        with mock.patch.object(manager.driver,
                               'get_volume_stats') as m_get_stats:
            with mock.patch.object(manager.driver,
                                   'get_goodness_function') as m_get_goodness:
                with mock.patch.object(manager.driver,
                                       'get_filter_function') as m_get_filter:
                    m_get_stats.return_value = {'name': 'cinder-volumes'}
                    m_get_filter.return_value = myfilterfunction
                    m_get_goodness.return_value = mygoodnessfunction
                    manager._report_driver_status(1)
                    self.assertTrue(m_get_stats.called)
                    mock_update.assert_called_once_with(expected)

    def test_is_working(self):
        # By default we have driver mocked to be initialized...
        self.assertTrue(self.volume.is_working())

        # ...lets switch it and check again!
        self.volume.driver._initialized = False
        self.assertFalse(self.volume.is_working())

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    @mock.patch.object(QUOTAS, 'reserve')
    @mock.patch.object(QUOTAS, 'commit')
    @mock.patch.object(QUOTAS, 'rollback')
    def test_create_driver_not_initialized(self, reserve, commit, rollback,
                                           mock_notify):
        self.volume.driver._initialized = False

        def fake_reserve(context, expire=None, project_id=None, **deltas):
            return ["RESERVATION"]

        def fake_commit_and_rollback(context, reservations, project_id=None):
            pass

        reserve.return_value = fake_reserve
        commit.return_value = fake_commit_and_rollback
        rollback.return_value = fake_commit_and_rollback

        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **self.volume_params)

        volume_id = volume['id']
        self.assertIsNone(volume['encryption_key_id'])
        mock_notify.assert_not_called()
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.create_volume, self.context, volume)

        volume = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual("error", volume.status)
        db.volume_destroy(context.get_admin_context(), volume_id)

    def test_create_driver_not_initialized_rescheduling(self):
        self.volume.driver._initialized = False
        mock_delete = self.mock_object(self.volume.driver, 'delete_volume')

        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **self.volume_params)

        volume_id = volume['id']
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.create_volume,
                          self.context, volume,
                          {'volume_properties': self.volume_params},
                          {'retry': {'num_attempts': 1, 'host': []}})
        # NOTE(dulek): Volume should be rescheduled as we passed request_spec
        # and filter_properties, assert that it wasn't counted in
        # allocated_capacity tracking.
        self.assertEqual({}, self.volume.stats['pools'])

        # NOTE(dulek): As we've rescheduled, make sure delete_volume was
        # called.
        self.assertTrue(mock_delete.called)

        db.volume_destroy(context.get_admin_context(), volume_id)

    def test_create_non_cinder_exception_rescheduling(self):
        params = self.volume_params
        del params['host']
        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **params)

        volume_id = volume['id']
        with mock.patch.object(self.volume.driver, 'create_volume',
                               side_effect=processutils.ProcessExecutionError):
            self.assertRaises(processutils.ProcessExecutionError,
                              self.volume.create_volume,
                              self.context, volume,
                              {'volume_properties': params},
                              {'retry': {'num_attempts': 1, 'host': []}})
        # NOTE(dulek): Volume should be rescheduled as we passed request_spec
        # and filter_properties, assert that it wasn't counted in
        # allocated_capacity tracking.
        self.assertEqual({}, self.volume.stats['pools'])

        db.volume_destroy(context.get_admin_context(), volume_id)

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    @mock.patch.object(QUOTAS, 'rollback')
    @mock.patch.object(QUOTAS, 'commit')
    @mock.patch.object(QUOTAS, 'reserve')
    def test_delete_driver_not_initialized(self, reserve, commit, rollback,
                                           mock_notify):
        self.volume.driver._initialized = False

        def fake_reserve(context, expire=None, project_id=None, **deltas):
            return ["RESERVATION"]

        def fake_commit_and_rollback(context, reservations, project_id=None):
            pass

        reserve.return_value = fake_reserve
        commit.return_value = fake_commit_and_rollback
        rollback.return_value = fake_commit_and_rollback

        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **self.volume_params)

        self.assertIsNone(volume['encryption_key_id'])
        mock_notify.assert_not_called()
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.delete_volume, self.context, volume)

        volume = objects.Volume.get_by_id(self.context, volume.id)
        self.assertEqual("error_deleting", volume.status)
        volume.destroy()

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    @mock.patch('cinder.quota.QUOTAS.rollback', new=mock.Mock())
    @mock.patch('cinder.quota.QUOTAS.commit', new=mock.Mock())
    @mock.patch('cinder.quota.QUOTAS.reserve', return_value=['RESERVATION'])
    def test_create_delete_volume(self, _mock_reserve, mock_notify):
        """Test volume can be created and deleted."""
        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **self.volume_params)
        volume_id = volume['id']

        mock_notify.assert_not_called()

        self.assertIsNone(volume['encryption_key_id'])

        self.volume.create_volume(self.context, volume)

        self.assert_notify_called(mock_notify,
                                  (['INFO', 'volume.create.start'],
                                   ['INFO', 'volume.create.end']))

        self.volume.delete_volume(self.context, volume)
        vol = db.volume_get(context.get_admin_context(read_deleted='yes'),
                            volume_id)
        self.assertEqual(vol['status'], 'deleted')

        self.assert_notify_called(mock_notify,
                                  (['INFO', 'volume.create.start'],
                                   ['INFO', 'volume.create.end'],
                                   ['INFO', 'volume.delete.start'],
                                   ['INFO', 'volume.delete.end']))

        self.assertRaises(exception.NotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_create_delete_volume_with_metadata(self):
        """Test volume can be created with metadata and deleted."""
        test_meta = {'fake_key': 'fake_value'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        self.assertEqual(test_meta, volume.metadata)

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.NotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_delete_volume_frozen(self):
        service = tests_utils.create_service(self.context, {'frozen': True})
        volume = tests_utils.create_volume(self.context, host=service.host)
        self.assertRaises(exception.InvalidInput,
                          self.volume_api.delete, self.context, volume)

    def test_delete_snapshot_frozen(self):
        service = tests_utils.create_service(self.context, {'frozen': True})
        volume = tests_utils.create_volume(self.context, host=service.host)
        snapshot = tests_utils.create_snapshot(self.context, volume.id)
        self.assertRaises(exception.InvalidInput,
                          self.volume_api.delete_snapshot, self.context,
                          snapshot)

    @ddt.data('create_snapshot', 'create_snapshot_force')
    def test_create_snapshot_frozen(self, method):
        service = tests_utils.create_service(self.context, {'frozen': True})
        volume = tests_utils.create_volume(self.context, host=service.host)
        method = getattr(self.volume_api, method)
        self.assertRaises(exception.InvalidInput,
                          method, self.context, volume, 'name', 'desc')

    def test_delete_volume_another_cluster_fails(self):
        """Test delete of volume from another cluster fails."""
        self.volume.cluster = 'mycluster'
        volume = tests_utils.create_volume(self.context, status='available',
                                           size=1, host=CONF.host + 'fake',
                                           cluster_name=self.volume.cluster)
        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.NotFound,
                          db.volume_get,
                          self.context,
                          volume.id)

    @mock.patch('cinder.db.volume_metadata_update')
    def test_create_volume_metadata(self, metadata_update):
        metadata = {'fake_key': 'fake_value'}
        metadata_update.return_value = metadata
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        res = self.volume_api.create_volume_metadata(self.context,
                                                     volume, metadata)
        metadata_update.assert_called_once_with(self.context, volume.id,
                                                metadata, False,
                                                common.METADATA_TYPES.user)
        self.assertEqual(metadata, res)

    @ddt.data('maintenance', 'uploading')
    def test_create_volume_metadata_maintenance(self, status):
        metadata = {'fake_key': 'fake_value'}
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume['status'] = status
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.create_volume_metadata,
                          self.context,
                          volume,
                          metadata)

    def test_update_volume_metadata_with_metatype(self):
        """Test update volume metadata with different metadata type."""
        test_meta1 = {'fake_key1': 'fake_value1'}
        test_meta2 = {'fake_key1': 'fake_value2'}
        FAKE_METADATA_TYPE = enum.Enum('METADATA_TYPES', 'fake_type')
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        self.volume.create_volume(self.context, volume)
        # update user metadata associated with the volume.
        result_meta = self.volume_api.update_volume_metadata(
            self.context,
            volume,
            test_meta2,
            False,
            common.METADATA_TYPES.user)
        self.assertEqual(test_meta2, result_meta)

        # create image metadata associated with the volume.
        result_meta = self.volume_api.update_volume_metadata(
            self.context,
            volume,
            test_meta1,
            False,
            common.METADATA_TYPES.image)
        self.assertEqual(test_meta1, result_meta)

        # update image metadata associated with the volume.
        result_meta = self.volume_api.update_volume_metadata(
            self.context,
            volume,
            test_meta2,
            False,
            common.METADATA_TYPES.image)
        self.assertEqual(test_meta2, result_meta)

        # update volume metadata with invalid metadta type.
        self.assertRaises(exception.InvalidMetadataType,
                          self.volume_api.update_volume_metadata,
                          self.context,
                          volume,
                          test_meta1,
                          False,
                          FAKE_METADATA_TYPE.fake_type)

    def test_update_volume_metadata_maintenance(self):
        """Test update volume metadata with different metadata type."""
        test_meta1 = {'fake_key1': 'fake_value1'}
        FAKE_METADATA_TYPE = enum.Enum('METADATA_TYPES', 'fake_type')
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.update_volume_metadata,
                          self.context,
                          volume,
                          test_meta1,
                          False,
                          FAKE_METADATA_TYPE.fake_type)

    @mock.patch('cinder.db.volume_update')
    def test_update_with_ovo(self, volume_update):
        """Test update volume using oslo_versionedobject."""
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        updates = {'display_name': 'foobbar'}
        self.volume_api.update(self.context, volume, updates)
        volume_update.assert_called_once_with(self.context, volume.id,
                                              updates)
        self.assertEqual('foobbar', volume.display_name)

    def test_delete_volume_metadata_with_metatype(self):
        """Test delete volume metadata with different metadata type."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        test_meta2 = {'fake_key1': 'fake_value1'}
        FAKE_METADATA_TYPE = enum.Enum('METADATA_TYPES', 'fake_type')
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        # delete user metadata associated with the volume.
        self.volume_api.delete_volume_metadata(
            self.context,
            volume,
            'fake_key2',
            common.METADATA_TYPES.user)

        self.assertEqual(test_meta2,
                         db.volume_metadata_get(self.context, volume_id))

        # create image metadata associated with the volume.
        result_meta = self.volume_api.update_volume_metadata(
            self.context,
            volume,
            test_meta1,
            False,
            common.METADATA_TYPES.image)

        self.assertEqual(test_meta1, result_meta)

        # delete image metadata associated with the volume.
        self.volume_api.delete_volume_metadata(
            self.context,
            volume,
            'fake_key2',
            common.METADATA_TYPES.image)

        # parse the result to build the dict.
        rows = db.volume_glance_metadata_get(self.context, volume_id)
        result = {}
        for row in rows:
            result[row['key']] = row['value']
        self.assertEqual(test_meta2, result)

        # delete volume metadata with invalid metadta type.
        self.assertRaises(exception.InvalidMetadataType,
                          self.volume_api.delete_volume_metadata,
                          self.context,
                          volume,
                          'fake_key1',
                          FAKE_METADATA_TYPE.fake_type)

    def test_delete_volume_metadata_maintenance(self):
        """Test delete volume metadata in maintenance."""
        FAKE_METADATA_TYPE = enum.Enum('METADATA_TYPES', 'fake_type')
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.delete_volume_metadata,
                          self.context,
                          volume,
                          'fake_key1',
                          FAKE_METADATA_TYPE.fake_type)

    def test_volume_attach_in_maintenance(self):
        """Test attach the volume in maintenance."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.attach,
                          self.context,
                          volume, None, None, None, None)

    def test_volume_detach_in_maintenance(self):
        """Test detach the volume in maintenance."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.detach,
                          self.context,
                          volume, None)

    def test_initialize_connection_maintenance(self):
        """Test initialize connection in maintenance."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.initialize_connection,
                          self.context,
                          volume,
                          None)

    def test_accept_transfer_maintenance(self):
        """Test accept transfer in maintenance."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.accept_transfer,
                          self.context,
                          volume,
                          None, None)

    def test_copy_volume_to_image_maintenance(self):
        """Test copy volume to image in maintenance."""
        test_meta1 = {'fake_key1': 'fake_value1', 'fake_key2': 'fake_value2'}
        volume = tests_utils.create_volume(self.context, metadata=test_meta1,
                                           **self.volume_params)
        volume['status'] = 'maintenance'
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.copy_volume_to_image,
                          self.context,
                          volume,
                          test_meta1,
                          force=True)

    @mock.patch.object(cinder.volume.api.API, 'list_availability_zones')
    def test_create_volume_uses_default_availability_zone(self, mock_list_az):
        """Test setting availability_zone correctly during volume create."""
        mock_list_az.return_value = ({'name': 'az1', 'available': True},
                                     {'name': 'az2', 'available': True},
                                     {'name': 'default-az', 'available': True})

        volume_api = cinder.volume.api.API()

        # Test backwards compatibility, default_availability_zone not set
        self.override_config('storage_availability_zone', 'az2')
        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description')
        self.assertEqual('az2', volume['availability_zone'])

        self.override_config('default_availability_zone', 'default-az')
        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description')
        self.assertEqual('default-az', volume['availability_zone'])

    @mock.patch('cinder.quota.QUOTAS.rollback', new=mock.MagicMock())
    @mock.patch('cinder.quota.QUOTAS.commit', new=mock.MagicMock())
    @mock.patch('cinder.quota.QUOTAS.reserve', return_value=["RESERVATION"])
    def test_create_volume_with_volume_type(self, _mock_reserve):
        """Test volume creation with default volume type."""
        volume_api = cinder.volume.api.API()

        # Create volume with default volume type while default
        # volume type doesn't exist, volume_type_id should be NULL
        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description')
        self.assertIsNone(volume['volume_type_id'])
        self.assertIsNone(volume['encryption_key_id'])

        # Create default volume type
        vol_type = conf_fixture.def_vol_type
        db.volume_type_create(context.get_admin_context(),
                              {'name': vol_type, 'extra_specs': {}})

        db_vol_type = db.volume_type_get_by_name(context.get_admin_context(),
                                                 vol_type)

        # Create volume with default volume type
        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description')
        self.assertEqual(db_vol_type.get('id'), volume['volume_type_id'])
        self.assertIsNone(volume['encryption_key_id'])

        # Create volume with specific volume type
        vol_type = 'test'
        db.volume_type_create(context.get_admin_context(),
                              {'name': vol_type, 'extra_specs': {}})
        db_vol_type = db.volume_type_get_by_name(context.get_admin_context(),
                                                 vol_type)

        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description',
                                   volume_type=db_vol_type)
        self.assertEqual(db_vol_type.get('id'), volume['volume_type_id'])

    @mock.patch.object(key_manager, 'API', fake_keymgr.fake_api)
    def test_create_volume_with_encrypted_volume_type_aes(self):
        ctxt = context.get_admin_context()

        cipher = 'aes-xts-plain64'
        key_size = 256
        control_location = 'front-end'

        db.volume_type_create(ctxt,
                              {'id': '61298380-0c12-11e3-bfd6-4b48424183be',
                               'name': 'LUKS'})
        db.volume_type_encryption_create(
            ctxt,
            '61298380-0c12-11e3-bfd6-4b48424183be',
            {'control_location': control_location,
             'provider': ENCRYPTION_PROVIDER,
             'cipher': cipher,
             'key_size': key_size})

        volume_api = cinder.volume.api.API()

        db_vol_type = db.volume_type_get_by_name(ctxt, 'LUKS')

        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description',
                                   volume_type=db_vol_type)

        key_manager = volume_api.key_manager
        key = key_manager.get(self.context, volume['encryption_key_id'])
        self.assertEqual(key_size, len(key.get_encoded()) * 8)
        self.assertEqual('aes', key.algorithm)

        metadata = db.volume_encryption_metadata_get(self.context, volume.id)
        self.assertEqual(db_vol_type.get('id'), volume['volume_type_id'])
        self.assertEqual(cipher, metadata.get('cipher'))
        self.assertEqual(key_size, metadata.get('key_size'))
        self.assertIsNotNone(volume['encryption_key_id'])

    @mock.patch.object(key_manager, 'API', fake_keymgr.fake_api)
    def test_create_volume_with_encrypted_volume_type_blowfish(self):
        ctxt = context.get_admin_context()

        cipher = 'blowfish-cbc'
        key_size = 32
        control_location = 'front-end'

        db.volume_type_create(ctxt,
                              {'id': '61298380-0c12-11e3-bfd6-4b48424183be',
                               'name': 'LUKS'})
        db.volume_type_encryption_create(
            ctxt,
            '61298380-0c12-11e3-bfd6-4b48424183be',
            {'control_location': control_location,
             'provider': ENCRYPTION_PROVIDER,
             'cipher': cipher,
             'key_size': key_size})

        volume_api = cinder.volume.api.API()

        db_vol_type = db.volume_type_get_by_name(ctxt, 'LUKS')

        volume = volume_api.create(self.context,
                                   1,
                                   'name',
                                   'description',
                                   volume_type=db_vol_type)

        key_manager = volume_api.key_manager
        key = key_manager.get(self.context, volume['encryption_key_id'])
        self.assertEqual('blowfish', key.algorithm)

        metadata = db.volume_encryption_metadata_get(self.context, volume.id)
        self.assertEqual(db_vol_type.get('id'), volume['volume_type_id'])
        self.assertEqual(cipher, metadata.get('cipher'))
        self.assertEqual(key_size, metadata.get('key_size'))
        self.assertIsNotNone(volume['encryption_key_id'])

    def test_create_volume_with_provider_id(self):
        volume_params_with_provider_id = dict(provider_id=fake.PROVIDER_ID,
                                              **self.volume_params)

        volume = tests_utils.create_volume(self.context,
                                           **volume_params_with_provider_id)

        self.volume.create_volume(self.context, volume)
        self.assertEqual(fake.PROVIDER_ID, volume['provider_id'])

    def test_create_volume_with_admin_metadata(self):
        with mock.patch.object(
                self.volume.driver, 'create_volume',
                return_value={'admin_metadata': {'foo': 'bar'}}):
            volume = tests_utils.create_volume(self.user_context)
            self.volume.create_volume(self.user_context, volume)
            self.assertEqual({'foo': 'bar'}, volume['admin_metadata'])

    @mock.patch.object(key_manager, 'API', new=fake_keymgr.fake_api)
    def test_create_delete_volume_with_encrypted_volume_type(self):
        cipher = 'aes-xts-plain64'
        key_size = 256
        db.volume_type_create(self.context,
                              {'id': fake.VOLUME_TYPE_ID, 'name': 'LUKS'})
        db.volume_type_encryption_create(
            self.context, fake.VOLUME_TYPE_ID,
            {'control_location': 'front-end', 'provider': ENCRYPTION_PROVIDER,
             'cipher': cipher, 'key_size': key_size})

        db_vol_type = db.volume_type_get_by_name(self.context, 'LUKS')

        volume = self.volume_api.create(self.context,
                                        1,
                                        'name',
                                        'description',
                                        volume_type=db_vol_type)

        self.assertIsNotNone(volume.get('encryption_key_id', None))
        self.assertEqual(db_vol_type.get('id'), volume['volume_type_id'])

        volume['host'] = 'fake_host'
        volume['status'] = 'available'
        db.volume_update(self.context, volume['id'], {'status': 'available'})
        self.volume_api.delete(self.context, volume)

        volume = objects.Volume.get_by_id(self.context, volume.id)
        while volume.status == 'available':
            # Must wait for volume_api delete request to process enough to
            # change the volume status.
            time.sleep(0.5)
            volume.refresh()

        self.assertEqual('deleting', volume['status'])

        db.volume_destroy(self.context, volume['id'])
        self.assertRaises(exception.NotFound,
                          db.volume_get,
                          self.context,
                          volume['id'])

    def test_extra_capabilities(self):
        # Test valid extra_capabilities.
        fake_capabilities = {'key1': 1, 'key2': 2}

        with mock.patch.object(jsonutils, 'loads') as mock_loads:
            mock_loads.return_value = fake_capabilities
            manager = vol_manager.VolumeManager()
            manager.stats = {'pools': {}}
            manager.driver.set_initialized()
            manager.publish_service_capabilities(self.context)
            self.assertTrue(mock_loads.called)
            volume_stats = manager.last_capabilities
            self.assertEqual(fake_capabilities['key1'],
                             volume_stats['key1'])
            self.assertEqual(fake_capabilities['key2'],
                             volume_stats['key2'])

    def test_extra_capabilities_fail(self):
        with mock.patch.object(jsonutils, 'loads') as mock_loads:
            mock_loads.side_effect = exception.CinderException('test')
            self.assertRaises(exception.CinderException,
                              vol_manager.VolumeManager)

    def test_delete_busy_volume(self):
        """Test volume survives deletion if driver reports it as busy."""
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)

        with mock.patch.object(self.volume.driver, 'delete_volume',
                               side_effect=exception.VolumeIsBusy(
                                   volume_name='fake')
                               ) as mock_del_vol:
            self.volume.delete_volume(self.context, volume)
            volume_ref = db.volume_get(context.get_admin_context(), volume_id)
            self.assertEqual(volume_id, volume_ref.id)
            self.assertEqual("available", volume_ref.status)
            mock_del_vol.assert_called_once_with(volume)

    def test_get_volume_different_tenant(self):
        """Test can't get volume of another tenant when viewable_admin_meta."""
        volume = tests_utils.create_volume(self.context,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)

        another_context = context.RequestContext('another_user_id',
                                                 'another_project_id',
                                                 is_admin=False)
        self.assertNotEqual(another_context.project_id,
                            self.context.project_id)

        volume_api = cinder.volume.api.API()

        self.assertRaises(exception.VolumeNotFound, volume_api.get,
                          another_context, volume_id, viewable_admin_meta=True)
        self.assertEqual(volume_id,
                         volume_api.get(self.context, volume_id)['id'])

        self.volume.delete_volume(self.context, volume)

    def test_get_all_limit_bad_value(self):
        """Test value of 'limit' is numeric and >= 0"""
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.get_all,
                          self.context,
                          limit="A")
        self.assertRaises(exception.InvalidInput,
                          volume_api.get_all,
                          self.context,
                          limit="-1")

    def test_get_all_tenants_volume_list(self):
        """Validate when the volume list for all tenants is returned"""
        volume_api = cinder.volume.api.API()

        with mock.patch.object(volume_api.db,
                               'volume_get_all_by_project') as by_project:
            with mock.patch.object(volume_api.db,
                                   'volume_get_all') as get_all:
                db_volume = {'volume_type_id': fake.VOLUME_TYPE_ID,
                             'name': 'fake_name',
                             'host': 'fake_host',
                             'id': fake.VOLUME_ID}

                volume = fake_volume.fake_db_volume(**db_volume)
                by_project.return_value = [volume]
                get_all.return_value = [volume]

                volume_api.get_all(self.context, filters={'all_tenants': '0'})
                self.assertTrue(by_project.called)
                by_project.called = False

                self.context.is_admin = False
                volume_api.get_all(self.context, filters={'all_tenants': '1'})
                self.assertTrue(by_project.called)

                # check for volume list of all tenants
                self.context.is_admin = True
                volume_api.get_all(self.context, filters={'all_tenants': '1'})
                self.assertTrue(get_all.called)

    def test_delete_volume_in_error_extending(self):
        """Test volume can be deleted in error_extending stats."""
        # create a volume
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)

        # delete 'error_extending' volume
        db.volume_update(self.context, volume['id'],
                         {'status': 'error_extending'})
        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.NotFound, db.volume_get,
                          self.context, volume['id'])

    @mock.patch.object(db.sqlalchemy.api, 'volume_get',
                       side_effect=exception.VolumeNotFound(
                           volume_id='12345678-1234-5678-1234-567812345678'))
    def test_delete_volume_not_found(self, mock_get_volume):
        """Test delete volume moves on if the volume does not exist."""
        volume_id = '12345678-1234-5678-1234-567812345678'
        volume = objects.Volume(self.context, status='available', id=volume_id)
        self.volume.delete_volume(self.context, volume)
        self.assertTrue(mock_get_volume.called)

    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'create_volume_from_snapshot')
    def test_create_volume_from_snapshot(self, mock_create_from_snap):
        """Test volume can be created from a snapshot."""
        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        snapshot_id = create_snapshot(volume_src['id'],
                                      size=volume_src['size'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snapshot_id)
        self.volume.create_snapshot(self.context, snapshot_obj)
        volume_dst = tests_utils.create_volume(self.context,
                                               snapshot_id=snapshot_id,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_dst)
        self.assertEqual(volume_dst['id'],
                         db.volume_get(
                             context.get_admin_context(),
                             volume_dst['id']).id)
        self.assertEqual(snapshot_id,
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).snapshot_id)

        self.volume.delete_volume(self.context, volume_dst)
        self.volume.delete_snapshot(self.context, snapshot_obj)
        self.volume.delete_volume(self.context, volume_src)

    @mock.patch('cinder.volume.flows.api.create_volume.get_flow')
    def test_create_volume_from_snapshot_with_types(self, _get_flow):
        """Test volume create from snapshot with types including mistmatch."""
        volume_api = cinder.volume.api.API()

        db.volume_type_create(
            context.get_admin_context(),
            {'name': 'foo',
             'extra_specs': {'volume_backend_name': 'dev_1'}})

        db.volume_type_create(
            context.get_admin_context(),
            {'name': 'biz', 'extra_specs': {'volume_backend_name': 'dev_2'}})

        foo_type = db.volume_type_get_by_name(context.get_admin_context(),
                                              'foo')
        biz_type = db.volume_type_get_by_name(context.get_admin_context(),
                                              'biz')

        snapshot = {'id': fake.SNAPSHOT_ID,
                    'status': fields.SnapshotStatus.AVAILABLE,
                    'volume_size': 10,
                    'volume_type_id': biz_type['id']}
        snapshot_obj = fake_snapshot.fake_snapshot_obj(self.context,
                                                       **snapshot)
        # Make sure the case of specifying a type that
        # doesn't match the snapshots type fails
        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          volume_type=foo_type,
                          snapshot=snapshot_obj)

        # Make sure that trying to specify a type
        # when the snapshots type is None fails
        snapshot_obj.volume_type_id = None
        self.assertRaises(exception.InvalidVolumeType,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          volume_type=foo_type,
                          snapshot=snapshot_obj)

        with mock.patch.object(cinder.volume.volume_types,
                               'get_volume_type') as mock_get_type:
            mock_get_type.return_value = biz_type
            snapshot_obj.volume_type_id = foo_type['id']
            volume_api.create(self.context, size=1, name='fake_name',
                              description='fake_desc', volume_type=foo_type,
                              snapshot=snapshot_obj)

        db.volume_type_destroy(context.get_admin_context(),
                               foo_type['id'])
        db.volume_type_destroy(context.get_admin_context(),
                               biz_type['id'])

    @mock.patch('cinder.volume.flows.api.create_volume.get_flow')
    def test_create_volume_from_source_with_types(self, _get_flow):
        """Test volume create from source with types including mistmatch."""
        volume_api = cinder.volume.api.API()

        db.volume_type_create(
            context.get_admin_context(),
            {'name': 'foo',
             'extra_specs': {'volume_backend_name': 'dev_1'}})

        db.volume_type_create(
            context.get_admin_context(),
            {'name': 'biz', 'extra_specs': {'volume_backend_name': 'dev_2'}})

        foo_type = db.volume_type_get_by_name(context.get_admin_context(),
                                              'foo')
        biz_type = db.volume_type_get_by_name(context.get_admin_context(),
                                              'biz')

        source_vol = {'id': fake.VOLUME_ID,
                      'status': 'available',
                      'volume_size': 10,
                      'volume_type': biz_type,
                      'volume_type_id': biz_type['id']}

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          volume_type=foo_type,
                          source_volume=source_vol)

        # Make sure that trying to specify a type
        # when the source type is None fails
        source_vol['volume_type_id'] = None
        source_vol['volume_type'] = None
        self.assertRaises(exception.InvalidVolumeType,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          volume_type=foo_type,
                          source_volume=source_vol)

        with mock.patch.object(cinder.volume.volume_types,
                               'get_volume_type') as mock_get_type:
            mock_get_type.return_value = biz_type
            source_vol['volume_type_id'] = biz_type['id']
            source_vol['volume_type'] = biz_type
            volume_api.create(self.context, size=1, name='fake_name',
                              description='fake_desc', volume_type=biz_type,
                              source_volume=source_vol)

        db.volume_type_destroy(context.get_admin_context(),
                               foo_type['id'])
        db.volume_type_destroy(context.get_admin_context(),
                               biz_type['id'])

    @mock.patch('cinder.volume.flows.api.create_volume.get_flow')
    def test_create_volume_from_source_with_same_backend(self, _get_flow):
        """Test volume create from source with type mismatch same backend."""
        volume_api = cinder.volume.api.API()

        foo_type = {
            'name': 'foo',
            'qos_specs_id': None,
            'deleted': False,
            'created_at': datetime.datetime(2015, 5, 8, 0, 40, 5, 408232),
            'updated_at': None,
            'extra_specs': {'volume_backend_name': 'dev_1'},
            'is_public': True,
            'deleted_at': None,
            'id': '29e43b50-2cd7-4d0c-8ddd-2119daab3a38',
            'description': None}

        biz_type = {
            'name': 'biz',
            'qos_specs_id': None,
            'deleted': False,
            'created_at': datetime.datetime(2015, 5, 8, 0, 20, 5, 408232),
            'updated_at': None,
            'extra_specs': {'volume_backend_name': 'dev_1'},
            'is_public': True,
            'deleted_at': None,
            'id': '34e54c31-3bc8-5c1d-9fff-2225bcce4b59',
            'description': None}

        source_vol = {'id': fake.VOLUME_ID,
                      'status': 'available',
                      'volume_size': 10,
                      'volume_type': biz_type,
                      'volume_type_id': biz_type['id']}

        with mock.patch.object(cinder.volume.volume_types,
                               'get_volume_type') as mock_get_type:
            mock_get_type.return_value = biz_type
            volume_api.create(self.context,
                              size=1,
                              name='fake_name',
                              description='fake_desc',
                              volume_type=foo_type,
                              source_volume=source_vol)

    @mock.patch('cinder.volume.flows.api.create_volume.get_flow')
    def test_create_from_source_and_snap_only_one_backend(self, _get_flow):
        """Test create from source and snap with type mismatch one backend."""
        volume_api = cinder.volume.api.API()

        foo_type = {
            'name': 'foo',
            'qos_specs_id': None,
            'deleted': False,
            'created_at': datetime.datetime(2015, 5, 8, 0, 40, 5, 408232),
            'updated_at': None,
            'extra_specs': {'some_key': 3},
            'is_public': True,
            'deleted_at': None,
            'id': '29e43b50-2cd7-4d0c-8ddd-2119daab3a38',
            'description': None}

        biz_type = {
            'name': 'biz',
            'qos_specs_id': None,
            'deleted': False,
            'created_at': datetime.datetime(2015, 5, 8, 0, 20, 5, 408232),
            'updated_at': None,
            'extra_specs': {'some_other_key': 4},
            'is_public': True,
            'deleted_at': None,
            'id': '34e54c31-3bc8-5c1d-9fff-2225bcce4b59',
            'description': None}

        source_vol = {'id': fake.VOLUME_ID,
                      'status': 'available',
                      'volume_size': 10,
                      'volume_type': biz_type,
                      'volume_type_id': biz_type['id']}

        snapshot = {'id': fake.SNAPSHOT_ID,
                    'status': fields.SnapshotStatus.AVAILABLE,
                    'volume_size': 10,
                    'volume_type_id': biz_type['id']}
        snapshot_obj = fake_snapshot.fake_snapshot_obj(self.context,
                                                       **snapshot)

        with mock.patch('cinder.db.service_get_all') as mock_get_service, \
            mock.patch.object(volume_api,
                              'list_availability_zones') as mock_get_azs:
            mock_get_service.return_value = [{'host': 'foo'}]
            mock_get_azs.return_value = {}
            volume_api.create(self.context,
                              size=1,
                              name='fake_name',
                              description='fake_desc',
                              volume_type=foo_type,
                              source_volume=source_vol)

            volume_api.create(self.context,
                              size=1,
                              name='fake_name',
                              description='fake_desc',
                              volume_type=foo_type,
                              snapshot=snapshot_obj)

    def _test_create_from_source_snapshot_encryptions(
            self, is_snapshot=False):
        volume_api = cinder.volume.api.API()
        foo_type = {
            'name': 'foo',
            'extra_specs': {'volume_backend_name': 'dev_1'},
            'id': fake.VOLUME_TYPE_ID,
            'description': None}

        biz_type = {
            'name': 'foo',
            'extra_specs': {'volume_backend_name': 'dev_1'},
            'id': fake.VOLUME_TYPE2_ID,
            'description': None}
        source_vol = {'id': fake.VOLUME_ID,
                      'status': 'available',
                      'volume_size': 1,
                      'volume_type': biz_type,
                      'volume_type_id': biz_type['id']}

        snapshot = {'id': fake.SNAPSHOT_ID,
                    'status': fields.SnapshotStatus.AVAILABLE,
                    'volume_size': 1,
                    'volume_type_id': biz_type['id']}
        snapshot_obj = fake_snapshot.fake_snapshot_obj(self.context,
                                                       **snapshot)

        with mock.patch.object(
                cinder.volume.volume_types,
                'volume_types_encryption_changed') as mock_encryption_changed:
            mock_encryption_changed.return_value = True
            self.assertRaises(exception.InvalidInput,
                              volume_api.create,
                              self.context,
                              size=1,
                              name='fake_name',
                              description='fake_desc',
                              volume_type=foo_type,
                              source_volume=(
                                  source_vol if not is_snapshot else None),
                              snapshot=snapshot_obj if is_snapshot else None)

    def test_create_from_source_encryption_changed(self):
        self._test_create_from_source_snapshot_encryptions()

    def test_create_from_snapshot_encryption_changed(self):
        self._test_create_from_source_snapshot_encryptions(is_snapshot=True)

    def test_create_snapshot_driver_not_initialized(self):
        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        snapshot_id = create_snapshot(volume_src['id'],
                                      size=volume_src['size'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snapshot_id)

        self.volume.driver._initialized = False

        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.create_snapshot,
                          self.context, snapshot_obj)

        # NOTE(flaper87): The volume status should be error.
        self.assertEqual(fields.SnapshotStatus.ERROR, snapshot_obj.status)

        # lets cleanup the mess
        self.volume.driver._initialized = True
        self.volume.delete_snapshot(self.context, snapshot_obj)
        self.volume.delete_volume(self.context, volume_src)

    def _mock_synchronized(self, name, *s_args, **s_kwargs):
        def inner_sync1(f):
            def inner_sync2(*args, **kwargs):
                self.called.append('lock-%s' % (name))
                ret = f(*args, **kwargs)
                self.called.append('unlock-%s' % (name))
                return ret
            return inner_sync2
        return inner_sync1

    def _fake_execute(self, *cmd, **kwargs):
        pass

    @mock.patch.object(coordination.Coordinator, 'get_lock')
    @mock.patch.object(cinder.tests.fake_driver.FakeLoggingVolumeDriver,
                       'create_volume_from_snapshot')
    def test_create_volume_from_snapshot_check_locks(
            self, mock_lvm_create, mock_lock):
        orig_flow = engine.ActionEngine.run

        def mock_flow_run(*args, **kwargs):
            # ensure the lock has been taken
            mock_lock.assert_called_with('%s-delete_snapshot' % snap_id)
            # now proceed with the flow.
            ret = orig_flow(*args, **kwargs)
            return ret

        # create source volume
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)

        # no lock
        self.volume.create_volume(self.context, src_vol)

        snap_id = create_snapshot(src_vol.id,
                                  size=src_vol['size'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snap_id)
        # no lock
        self.volume.create_snapshot(self.context, snapshot_obj)

        dst_vol = tests_utils.create_volume(self.context,
                                            snapshot_id=snap_id,
                                            **self.volume_params)
        admin_ctxt = context.get_admin_context()

        # mock the flow runner so we can do some checks
        self.mock_object(engine.ActionEngine, 'run', mock_flow_run)

        # locked
        self.volume.create_volume(self.context, dst_vol,
                                  request_spec={'snapshot_id': snap_id})
        mock_lock.assert_called_with('%s-delete_snapshot' % snap_id)
        self.assertEqual(dst_vol.id, db.volume_get(admin_ctxt, dst_vol.id).id)
        self.assertEqual(snap_id,
                         db.volume_get(admin_ctxt, dst_vol.id).snapshot_id)

        # locked
        self.volume.delete_volume(self.context, dst_vol)
        mock_lock.assert_called_with('%s-delete_volume' % dst_vol.id)

        # locked
        self.volume.delete_snapshot(self.context, snapshot_obj)
        mock_lock.assert_called_with('%s-delete_snapshot' % snap_id)

        # locked
        self.volume.delete_volume(self.context, src_vol)
        mock_lock.assert_called_with('%s-delete_volume' % src_vol.id)

        self.assertTrue(mock_lvm_create.called)

    @mock.patch.object(coordination.Coordinator, 'get_lock')
    def test_create_volume_from_volume_check_locks(self, mock_lock):
        # mock the synchroniser so we can record events
        self.mock_object(utils, 'execute', self._fake_execute)

        orig_flow = engine.ActionEngine.run

        def mock_flow_run(*args, **kwargs):
            # ensure the lock has been taken
            mock_lock.assert_called_with('%s-delete_volume' % src_vol_id)
            # now proceed with the flow.
            ret = orig_flow(*args, **kwargs)
            return ret

        # create source volume
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        # no lock
        self.volume.create_volume(self.context, src_vol)
        self.assertEqual(0, mock_lock.call_count)

        dst_vol = tests_utils.create_volume(self.context,
                                            source_volid=src_vol_id,
                                            **self.volume_params)
        dst_vol_id = dst_vol['id']
        admin_ctxt = context.get_admin_context()

        # mock the flow runner so we can do some checks
        self.mock_object(engine.ActionEngine, 'run', mock_flow_run)

        # locked
        self.volume.create_volume(self.context, dst_vol,
                                  request_spec={'source_volid': src_vol_id})
        mock_lock.assert_called_with('%s-delete_volume' % src_vol_id)
        self.assertEqual(dst_vol_id, db.volume_get(admin_ctxt, dst_vol_id).id)
        self.assertEqual(src_vol_id,
                         db.volume_get(admin_ctxt, dst_vol_id).source_volid)

        # locked
        self.volume.delete_volume(self.context, dst_vol)
        mock_lock.assert_called_with('%s-delete_volume' % dst_vol_id)

        # locked
        self.volume.delete_volume(self.context, src_vol)
        mock_lock.assert_called_with('%s-delete_volume' % src_vol_id)

    def test_create_volume_from_volume_delete_lock_taken(self):
        # create source volume
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        # no lock
        self.volume.create_volume(self.context, src_vol)

        dst_vol = tests_utils.create_volume(self.context,
                                            source_volid=src_vol_id,
                                            **self.volume_params)

        orig_elevated = self.context.elevated

        gthreads = []

        def mock_elevated(*args, **kwargs):
            # unset mock so it is only called once
            self.mock_object(self.context, 'elevated', orig_elevated)

            # we expect this to block and then fail
            t = eventlet.spawn(self.volume.create_volume,
                               self.context,
                               volume=dst_vol,
                               request_spec={'source_volid': src_vol_id})
            gthreads.append(t)

            return orig_elevated(*args, **kwargs)

        # mock something from early on in the delete operation and within the
        # lock so that when we do the create we expect it to block.
        self.mock_object(self.context, 'elevated', mock_elevated)

        # locked
        self.volume.delete_volume(self.context, src_vol)

        # we expect the volume create to fail with the following err since the
        # source volume was deleted while the create was locked. Note that the
        # volume is still in the db since it was created by the test prior to
        # calling manager.create_volume.
        with mock.patch('sys.stderr', new=six.StringIO()):
            self.assertRaises(exception.VolumeNotFound, gthreads[0].wait)

    def _raise_metadata_copy_failure(self, method, dst_vol):
        # MetadataCopyFailure exception will be raised if DB service is Down
        # while copying the volume glance metadata
        with mock.patch.object(db, method) as mock_db:
            mock_db.side_effect = exception.MetadataCopyFailure(
                reason="Because of DB service down.")
            self.assertRaises(exception.MetadataCopyFailure,
                              self.volume.create_volume,
                              self.context,
                              dst_vol)

        # ensure that status of volume is 'error'
        vol = db.volume_get(self.context, dst_vol.id)
        self.assertEqual('error', vol['status'])

        # cleanup resource
        db.volume_destroy(self.context, dst_vol.id)

    @mock.patch('cinder.utils.execute')
    def test_create_volume_from_volume_with_glance_volume_metadata_none(
            self, mock_execute):
        # create source volume
        mock_execute.return_value = None
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        self.volume.create_volume(self.context, src_vol)
        # set bootable flag of volume to True
        db.volume_update(self.context, src_vol['id'], {'bootable': True})

        # create volume from source volume
        dst_vol = tests_utils.create_volume(self.context,
                                            source_volid=src_vol_id,
                                            **self.volume_params)
        self.volume.create_volume(self.context, dst_vol)

        self.assertRaises(exception.GlanceMetadataNotFound,
                          db.volume_glance_metadata_copy_from_volume_to_volume,
                          self.context, src_vol_id, dst_vol['id'])

        # ensure that status of volume is 'available'
        vol = db.volume_get(self.context, dst_vol['id'])
        self.assertEqual('available', vol['status'])

        # cleanup resource
        db.volume_destroy(self.context, src_vol_id)
        db.volume_destroy(self.context, dst_vol['id'])

    @mock.patch('cinder.utils.execute')
    def test_create_volume_from_volume_raise_metadata_copy_failure(
            self, mock_execute):
        # create source volume
        mock_execute.return_value = None
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        self.volume.create_volume(self.context, src_vol)
        # set bootable flag of volume to True
        db.volume_update(self.context, src_vol['id'], {'bootable': True})

        # create volume from source volume
        dst_vol = tests_utils.create_volume(self.context,
                                            source_volid=src_vol_id,
                                            **self.volume_params)
        self._raise_metadata_copy_failure(
            'volume_glance_metadata_copy_from_volume_to_volume',
            dst_vol)

        # cleanup resource
        db.volume_destroy(self.context, src_vol_id)

    @mock.patch('cinder.utils.execute')
    def test_create_volume_from_snapshot_raise_metadata_copy_failure(
            self, mock_execute):
        # create source volume
        mock_execute.return_value = None
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        self.volume.create_volume(self.context, src_vol)
        # set bootable flag of volume to True
        db.volume_update(self.context, src_vol['id'], {'bootable': True})

        # create volume from snapshot
        snapshot_id = create_snapshot(src_vol['id'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snapshot_id)
        self.volume.create_snapshot(self.context, snapshot_obj)

        # ensure that status of snapshot is 'available'
        self.assertEqual(fields.SnapshotStatus.AVAILABLE, snapshot_obj.status)

        dst_vol = tests_utils.create_volume(self.context,
                                            snapshot_id=snapshot_id,
                                            **self.volume_params)
        self._raise_metadata_copy_failure(
            'volume_glance_metadata_copy_to_volume',
            dst_vol)

        # cleanup resource
        snapshot_obj.destroy()
        db.volume_destroy(self.context, src_vol_id)

    @mock.patch(
        'cinder.volume.driver.VolumeDriver.create_replica_test_volume')
    @mock.patch('cinder.utils.execute')
    def test_create_volume_from_srcreplica_raise_metadata_copy_failure(
            self, mock_execute, _create_replica_test):
        mock_execute.return_value = None
        _create_replica_test.return_value = None
        # create source volume
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        self.volume.create_volume(self.context, src_vol)
        # set bootable flag of volume to True
        db.volume_update(self.context, src_vol['id'], {'bootable': True})

        # create volume from source volume
        dst_vol = tests_utils.create_volume(self.context,
                                            source_volid=src_vol_id,
                                            **self.volume_params)
        self._raise_metadata_copy_failure(
            'volume_glance_metadata_copy_from_volume_to_volume',
            dst_vol)

        # cleanup resource
        db.volume_destroy(self.context, src_vol_id)

    @mock.patch('cinder.utils.execute')
    def test_create_volume_from_snapshot_with_glance_volume_metadata_none(
            self, mock_execute):
        # create source volume
        mock_execute.return_value = None
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)
        src_vol_id = src_vol['id']

        self.volume.create_volume(self.context, src_vol)
        # set bootable flag of volume to True
        db.volume_update(self.context, src_vol['id'], {'bootable': True})

        volume = db.volume_get(self.context, src_vol_id)

        # create snapshot of volume
        snapshot_id = create_snapshot(volume['id'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snapshot_id)
        self.volume.create_snapshot(self.context, snapshot_obj)

        # ensure that status of snapshot is 'available'
        self.assertEqual(fields.SnapshotStatus.AVAILABLE, snapshot_obj.status)

        # create volume from snapshot
        dst_vol = tests_utils.create_volume(self.context,
                                            snapshot_id=snapshot_id,
                                            **self.volume_params)
        self.volume.create_volume(self.context, dst_vol)

        self.assertRaises(exception.GlanceMetadataNotFound,
                          db.volume_glance_metadata_copy_to_volume,
                          self.context, dst_vol['id'], snapshot_id)

        # ensure that status of volume is 'available'
        vol = db.volume_get(self.context, dst_vol['id'])
        self.assertEqual('available', vol['status'])

        # cleanup resource
        snapshot_obj.destroy()
        db.volume_destroy(self.context, src_vol_id)
        db.volume_destroy(self.context, dst_vol['id'])

    @mock.patch(
        'cinder.volume.driver.VolumeDriver.create_replica_test_volume')
    def test_create_volume_from_srcreplica_with_glance_volume_metadata_none(
            self, _create_replica_test):
        """Test volume can be created from a volume replica."""
        _create_replica_test.return_value = None

        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        db.volume_update(self.context, volume_src['id'], {'bootable': True})

        volume = db.volume_get(self.context, volume_src['id'])
        volume_dst = tests_utils.create_volume(
            self.context,
            **self.volume_params)
        self.volume.create_volume(self.context, volume_dst,
                                  {'source_replicaid': volume.id})

        self.assertRaises(exception.GlanceMetadataNotFound,
                          db.volume_glance_metadata_copy_from_volume_to_volume,
                          self.context, volume_src['id'], volume_dst['id'])

        self.assertEqual('available',
                         db.volume_get(self.context,
                                       volume_dst['id']).status)
        self.assertTrue(_create_replica_test.called)

        # cleanup resource
        db.volume_destroy(self.context, volume_dst['id'])
        db.volume_destroy(self.context, volume_src['id'])

    def test_create_volume_from_snapshot_delete_lock_taken(self):
        # create source volume
        src_vol = tests_utils.create_volume(self.context, **self.volume_params)

        # no lock
        self.volume.create_volume(self.context, src_vol)

        # create snapshot
        snap_id = create_snapshot(src_vol.id,
                                  size=src_vol['size'])['id']
        snapshot_obj = objects.Snapshot.get_by_id(self.context, snap_id)
        # no lock
        self.volume.create_snapshot(self.context, snapshot_obj)

        # create vol from snapshot...
        dst_vol = tests_utils.create_volume(self.context,
                                            snapshot_id=snap_id,
                                            source_volid=src_vol.id,
                                            **self.volume_params)

        orig_elevated = self.context.elevated

        gthreads = []

        def mock_elevated(*args, **kwargs):
            # unset mock so it is only called once
            self.mock_object(self.context, 'elevated', orig_elevated)

            # We expect this to block and then fail
            t = eventlet.spawn(self.volume.create_volume, self.context,
                               volume=dst_vol,
                               request_spec={'snapshot_id': snap_id})
            gthreads.append(t)

            return orig_elevated(*args, **kwargs)

        # mock something from early on in the delete operation and within the
        # lock so that when we do the create we expect it to block.
        self.mock_object(self.context, 'elevated', mock_elevated)

        # locked
        self.volume.delete_snapshot(self.context, snapshot_obj)

        # we expect the volume create to fail with the following err since the
        # snapshot was deleted while the create was locked. Note that the
        # volume is still in the db since it was created by the test prior to
        #  calling manager.create_volume.
        with mock.patch('sys.stderr', new=six.StringIO()):
            self.assertRaises(exception.SnapshotNotFound, gthreads[0].wait)
        # locked
        self.volume.delete_volume(self.context, src_vol)
        # make sure it is gone
        self.assertRaises(exception.VolumeNotFound, db.volume_get,
                          self.context, src_vol.id)

    @mock.patch.object(key_manager, 'API', fake_keymgr.fake_api)
    def test_create_volume_from_snapshot_with_encryption(self):
        """Test volume can be created from a snapshot of an encrypted volume"""
        ctxt = context.get_admin_context()
        cipher = 'aes-xts-plain64'
        key_size = 256

        db.volume_type_create(ctxt,
                              {'id': '61298380-0c12-11e3-bfd6-4b48424183be',
                               'name': 'LUKS'})
        db.volume_type_encryption_create(
            ctxt,
            '61298380-0c12-11e3-bfd6-4b48424183be',
            {'control_location': 'front-end', 'provider': ENCRYPTION_PROVIDER,
             'cipher': cipher, 'key_size': key_size})

        volume_api = cinder.volume.api.API()

        db_vol_type = db.volume_type_get_by_name(context.get_admin_context(),
                                                 'LUKS')
        volume_src = volume_api.create(self.context,
                                       1,
                                       'name',
                                       'description',
                                       volume_type=db_vol_type)

        volume_src['host'] = 'fake_host'
        snapshot_ref = volume_api.create_snapshot_force(self.context,
                                                        volume_src,
                                                        'name',
                                                        'description')
        snapshot_ref['status'] = fields.SnapshotStatus.AVAILABLE
        # status must be available
        volume_dst = volume_api.create(self.context,
                                       1,
                                       'name',
                                       'description',
                                       snapshot=snapshot_ref)
        self.assertEqual(volume_dst['id'],
                         db.volume_get(
                             context.get_admin_context(),
                             volume_dst['id']).id)
        self.assertEqual(snapshot_ref['id'],
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).snapshot_id)

        # ensure encryption keys match
        self.assertIsNotNone(volume_src['encryption_key_id'])
        self.assertIsNotNone(volume_dst['encryption_key_id'])

        key_manager = volume_api.key_manager  # must use *same* key manager
        volume_src_key = key_manager.get(self.context,
                                         volume_src['encryption_key_id'])
        volume_dst_key = key_manager.get(self.context,
                                         volume_dst['encryption_key_id'])
        self.assertEqual(volume_src_key, volume_dst_key)

    def test_create_volume_from_encrypted_volume(self):
        """Test volume can be created from an encrypted volume."""
        self.mock_object(key_manager, 'API', fake_keymgr.fake_api)
        cipher = 'aes-xts-plain64'
        key_size = 256

        volume_api = cinder.volume.api.API()

        ctxt = context.get_admin_context()

        db.volume_type_create(ctxt,
                              {'id': '61298380-0c12-11e3-bfd6-4b48424183be',
                               'name': 'LUKS'})
        db.volume_type_encryption_create(
            ctxt,
            '61298380-0c12-11e3-bfd6-4b48424183be',
            {'control_location': 'front-end', 'provider': ENCRYPTION_PROVIDER,
             'cipher': cipher, 'key_size': key_size})

        db_vol_type = db.volume_type_get_by_name(context.get_admin_context(),
                                                 'LUKS')
        volume_src = volume_api.create(self.context,
                                       1,
                                       'name',
                                       'description',
                                       volume_type=db_vol_type)
        volume_src['status'] = 'available'  # status must be available
        volume_dst = volume_api.create(self.context,
                                       1,
                                       'name',
                                       'description',
                                       source_volume=volume_src)
        self.assertEqual(volume_dst['id'],
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).id)
        self.assertEqual(volume_src['id'],
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).source_volid)

        # ensure encryption keys match
        self.assertIsNotNone(volume_src['encryption_key_id'])
        self.assertIsNotNone(volume_dst['encryption_key_id'])

        km = volume_api.key_manager  # must use *same* key manager
        volume_src_key = km.get(self.context,
                                volume_src['encryption_key_id'])
        volume_dst_key = km.get(self.context,
                                volume_dst['encryption_key_id'])
        self.assertEqual(volume_src_key, volume_dst_key)

    def test_delete_encrypted_volume(self):
        self.volume_params['status'] = 'active'
        volume = tests_utils.create_volume(self.context,
                                           **self.volume_params)
        vol_api = cinder.volume.api.API()
        with mock.patch.object(
                vol_api.key_manager,
                'delete',
                side_effect=Exception):
            self.assertRaises(exception.InvalidVolume,
                              vol_api.delete,
                              self.context, volume)

    def test_create_volume_from_snapshot_fail_bad_size(self):
        """Test volume can't be created from snapshot with bad volume size."""
        volume_api = cinder.volume.api.API()

        snapshot = {'id': fake.SNAPSHOT_ID,
                    'status': fields.SnapshotStatus.AVAILABLE,
                    'volume_size': 10}
        snapshot_obj = fake_snapshot.fake_snapshot_obj(self.context,
                                                       **snapshot)
        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          snapshot=snapshot_obj)

    def test_create_volume_from_snapshot_fail_wrong_az(self):
        """Test volume can't be created from snapshot in a different az."""
        volume_api = cinder.volume.api.API()

        def fake_list_availability_zones(enable_cache=False):
            return ({'name': 'nova', 'available': True},
                    {'name': 'az2', 'available': True})

        self.mock_object(volume_api,
                         'list_availability_zones',
                         fake_list_availability_zones)

        volume_src = tests_utils.create_volume(self.context,
                                               availability_zone='az2',
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        snapshot = create_snapshot(volume_src['id'])

        self.volume.create_snapshot(self.context, snapshot)

        volume_dst = volume_api.create(self.context,
                                       size=1,
                                       name='fake_name',
                                       description='fake_desc',
                                       snapshot=snapshot)
        self.assertEqual('az2', volume_dst['availability_zone'])

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          snapshot=snapshot,
                          availability_zone='nova')

    def test_create_volume_with_invalid_exclusive_options(self):
        """Test volume create with multiple exclusive options fails."""
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          1,
                          'name',
                          'description',
                          snapshot=fake.SNAPSHOT_ID,
                          image_id=fake.IMAGE_ID,
                          source_volume=fake.VOLUME_ID)

    @mock.patch.object(cinder.volume.targets.iscsi.ISCSITarget,
                       '_get_target_chap_auth')
    @mock.patch.object(db, 'volume_admin_metadata_get')
    @mock.patch.object(db.sqlalchemy.api, 'volume_get')
    @mock.patch.object(db, 'volume_update')
    def test_initialize_connection_fetchqos(self,
                                            _mock_volume_update,
                                            _mock_volume_get,
                                            _mock_volume_admin_metadata_get,
                                            mock_get_target):
        """Make sure initialize_connection returns correct information."""
        _fake_admin_meta = [{'key': 'fake-key', 'value': 'fake-value'}]
        _fake_volume = {'volume_type_id': fake.VOLUME_TYPE_ID,
                        'name': 'fake_name',
                        'host': 'fake_host',
                        'id': fake.VOLUME_ID,
                        'volume_admin_metadata': _fake_admin_meta}
        fake_volume_obj = fake_volume.fake_volume_obj(self.context,
                                                      **_fake_volume)

        _mock_volume_get.return_value = _fake_volume
        _mock_volume_update.return_value = _fake_volume
        _mock_volume_admin_metadata_get.return_value = {
            'fake-key': 'fake-value'}

        connector = {'ip': 'IP', 'initiator': 'INITIATOR'}
        qos_values = {'consumer': 'front-end',
                      'specs': {
                          'key1': 'value1',
                          'key2': 'value2'}
                      }

        with mock.patch.object(cinder.volume.volume_types,
                               'get_volume_type_qos_specs') as type_qos, \
            mock.patch.object(cinder.tests.fake_driver.FakeLoggingVolumeDriver,
                              'initialize_connection') as driver_init:
            type_qos.return_value = dict(qos_specs=qos_values)
            driver_init.return_value = {'data': {}}
            mock_get_target.return_value = None
            qos_specs_expected = {'key1': 'value1',
                                  'key2': 'value2'}
            # initialize_connection() passes qos_specs that is designated to
            # be consumed by front-end or both front-end and back-end
            conn_info = self.volume.initialize_connection(
                self.context, fake_volume_obj, connector,)
            self.assertDictEqual(qos_specs_expected,
                                 conn_info['data']['qos_specs'])

            qos_values.update({'consumer': 'both'})
            conn_info = self.volume.initialize_connection(
                self.context, fake_volume_obj, connector)
            self.assertDictEqual(qos_specs_expected,
                                 conn_info['data']['qos_specs'])
            # initialize_connection() skips qos_specs that is designated to be
            # consumed by back-end only
            qos_values.update({'consumer': 'back-end'})
            type_qos.return_value = dict(qos_specs=qos_values)
            conn_info = self.volume.initialize_connection(
                self.context, fake_volume_obj, connector)
            self.assertIsNone(conn_info['data']['qos_specs'])

    @mock.patch.object(fake_driver.FakeLoggingVolumeDriver, 'create_export')
    def test_initialize_connection_export_failure(self,
                                                  _mock_create_export):
        """Test exception path for create_export failure."""
        volume = tests_utils.create_volume(
            self.context, admin_metadata={'fake-key': 'fake-value'},
            volume_type_id=fake.VOLUME_TYPE_ID, **self.volume_params)
        _mock_create_export.side_effect = exception.CinderException

        connector = {'ip': 'IP', 'initiator': 'INITIATOR'}

        self.assertRaises(exception.VolumeBackendAPIException,
                          self.volume.initialize_connection,
                          self.context, volume, connector)

    @ddt.data(False, True)
    def test_run_attach_detach_volume_for_instance(self, volume_object):
        """Make sure volume can be attached and detached from instance."""
        mountpoint = "/dev/sdf"
        # attach volume to the instance then to detach
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume = tests_utils.create_volume(self.user_context,
                                           **self.volume_params)
        with volume.obj_as_admin():
            volume.admin_metadata['readonly'] = True
            volume.save()
        volume_id = volume.id
        self.volume.create_volume(self.user_context,
                                  volume=volume)
        volume_passed = volume if volume_object else None
        attachment = self.volume.attach_volume(self.user_context,
                                               volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro',
                                               volume=volume_passed)
        vol = objects.Volume.get_by_id(self.context, volume_id)
        self.assertEqual("in-use", vol.status)
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment.attach_status)
        self.assertEqual(mountpoint, attachment.mountpoint)
        self.assertEqual(instance_uuid, attachment.instance_uuid)
        self.assertIsNone(attachment.attached_host)
        admin_metadata = vol.volume_admin_metadata
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        volume = volume if volume_object else vol
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume=volume)
        self.volume.detach_volume(self.context, volume_id,
                                  attachment.id,
                                  volume=volume_passed)
        vol = objects.Volume.get_by_id(self.context, volume_id)
        self.assertEqual('available', vol.status)

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    @mock.patch('cinder.volume.manager.LOG', mock.Mock())
    def test_initialize_connection(self):
        volume = mock.Mock(save=mock.Mock(side_effect=Exception))
        with mock.patch.object(self.volume, 'driver') as driver_mock:
            self.assertRaises(exception.ExportFailure,
                              self.volume.initialize_connection, self.context,
                              volume, mock.Mock())
        driver_mock.remove_export.assert_called_once_with(mock.ANY, volume)

    def test_run_attach_detach_2volumes_for_instance(self):
        """Make sure volume can be attached and detached from instance."""
        # attach first volume to the instance
        mountpoint1 = "/dev/vdc"
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume1 = tests_utils.create_volume(
            self.context, admin_metadata={'readonly': 'True'},
            **self.volume_params)
        volume1_id = volume1['id']
        self.volume.create_volume(self.context, volume1)
        attachment = self.volume.attach_volume(self.context, volume1_id,
                                               instance_uuid, None,
                                               mountpoint1, 'ro')
        vol1 = db.volume_get(context.get_admin_context(), volume1_id)
        self.assertEqual("in-use", vol1['status'])
        self.assertEqual('attached', attachment['attach_status'])
        self.assertEqual(mountpoint1, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol1['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume1, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume1)

        # attach 2nd volume to the instance
        mountpoint2 = "/dev/vdd"
        volume2 = tests_utils.create_volume(
            self.context, admin_metadata={'readonly': 'False'},
            **self.volume_params)
        volume2_id = volume2['id']
        self.volume.create_volume(self.context, volume2)
        attachment2 = self.volume.attach_volume(self.context, volume2_id,
                                                instance_uuid, None,
                                                mountpoint2, 'rw')
        vol2 = db.volume_get(context.get_admin_context(), volume2_id)
        self.assertEqual("in-use", vol2['status'])
        self.assertEqual('attached', attachment2['attach_status'])
        self.assertEqual(mountpoint2, attachment2['mountpoint'])
        self.assertEqual(instance_uuid, attachment2['instance_uuid'])
        self.assertIsNone(attachment2['attached_host'])
        admin_metadata = vol2['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='False', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

        connector = {'initiator': 'iqn.2012-07.org.fake:02'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume2, connector)
        self.assertEqual('rw', conn_info['data']['access_mode'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume2)

        # detach first volume and then 2nd volume
        self.volume.detach_volume(self.context, volume1_id, attachment['id'])
        vol1 = db.volume_get(self.context, volume1_id)
        self.assertEqual('available', vol1['status'])

        self.volume.delete_volume(self.context, volume1)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume1_id)

        self.volume.detach_volume(self.context, volume2_id, attachment2['id'])
        vol2 = db.volume_get(self.context, volume2_id)
        self.assertEqual('available', vol2['status'])

        self.volume.delete_volume(self.context, volume2)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume2_id)

    def test_detach_invalid_attachment_id(self):
        """Make sure if the attachment id isn't found we raise."""
        attachment_id = "notfoundid"
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=False,
                                           **self.volume_params)
        self.volume.detach_volume(self.context, volume['id'],
                                  attachment_id)
        volume = db.volume_get(self.context, volume['id'])
        self.assertEqual('available', volume['status'])

        instance_uuid = '12345678-1234-5678-1234-567812345678'
        attached_host = 'fake_host'
        mountpoint = '/dev/fake'
        tests_utils.attach_volume(self.context, volume['id'],
                                  instance_uuid, attached_host,
                                  mountpoint)
        self.volume.detach_volume(self.context, volume['id'],
                                  attachment_id)
        volume = db.volume_get(self.context, volume['id'])
        self.assertEqual('in-use', volume['status'])

    def test_detach_no_attachments(self):
        self.volume_params['status'] = 'detaching'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=False,
                                           **self.volume_params)
        self.volume.detach_volume(self.context, volume['id'])
        volume = db.volume_get(self.context, volume['id'])
        self.assertEqual('available', volume['status'])

    def test_run_attach_detach_volume_for_instance_no_attachment_id(self):
        """Make sure volume can be attached and detached from instance."""
        mountpoint = "/dev/sdf"
        # attach volume to the instance then to detach
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        instance_uuid_2 = '12345678-4321-8765-4321-567812345678'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=True,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        attachment2 = self.volume.attach_volume(self.context, volume_id,
                                                instance_uuid_2, None,
                                                mountpoint, 'ro')

        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])
        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)

        self.assertRaises(exception.InvalidVolume,
                          self.volume.detach_volume,
                          self.context, volume_id)

        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('in-use', vol['status'])

        self.volume.detach_volume(self.context, volume_id, attachment2['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('available', vol['status'])

        attachment = self.volume.attach_volume(self.context, volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro')
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('in-use', vol['status'])
        self.volume.detach_volume(self.context, volume_id)
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('available', vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_detach_multiattach_volume_for_instances(self):
        """Make sure volume can be attached to multiple instances."""
        mountpoint = "/dev/sdf"
        # attach volume to the instance then to detach
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=True,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        instance2_uuid = '12345678-1234-5678-1234-567812345000'
        mountpoint2 = "/dev/sdx"
        attachment2 = self.volume.attach_volume(self.context, volume_id,
                                                instance2_uuid, None,
                                                mountpoint2, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment2['attach_status'])
        self.assertEqual(mountpoint2, attachment2['mountpoint'])
        self.assertEqual(instance2_uuid, attachment2['instance_uuid'])
        self.assertIsNone(attachment2['attached_host'])
        self.assertNotEqual(attachment, attachment2)

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)
        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('in-use', vol['status'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)

        self.volume.detach_volume(self.context, volume_id, attachment2['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('available', vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_twice_multiattach_volume_for_instances(self):
        """Make sure volume can be attached to multiple instances."""
        mountpoint = "/dev/sdf"
        # attach volume to the instance then to detach
        instance_uuid = '12345678-1234-5678-1234-567812345699'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=True,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        mountpoint2 = "/dev/sdx"
        attachment2 = self.volume.attach_volume(self.context, volume_id,
                                                instance_uuid, None,
                                                mountpoint2, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual('attached', attachment2['attach_status'])
        self.assertEqual(mountpoint, attachment2['mountpoint'])
        self.assertEqual(instance_uuid, attachment2['instance_uuid'])
        self.assertIsNone(attachment2['attached_host'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)

    def test_attach_detach_not_multiattach_volume_for_instances(self):
        """Make sure volume can't be attached to more than one instance."""
        mountpoint = "/dev/sdf"
        # attach volume to the instance then to detach
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           multiattach=False,
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id,
                                               instance_uuid, None,
                                               mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertFalse(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        instance2_uuid = '12345678-1234-5678-1234-567812345000'
        mountpoint2 = "/dev/sdx"
        self.assertRaises(exception.InvalidVolume,
                          self.volume.attach_volume,
                          self.context,
                          volume_id,
                          instance2_uuid,
                          None,
                          mountpoint2, 'ro')

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)
        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('available', vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_detach_volume_for_host(self):
        """Make sure volume can be attached and detached from host."""
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(
            self.context,
            admin_metadata={'readonly': 'False'},
            **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id, None,
                                               'fake_host', mountpoint, 'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host', attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='False', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('rw', conn_info['data']['access_mode'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)
        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual("available", vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_detach_multiattach_volume_for_hosts(self):
        """Make sure volume can be attached and detached from hosts."""
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(
            self.context,
            admin_metadata={'readonly': 'False'},
            multiattach=True,
            **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id, None,
                                               'fake_host', mountpoint, 'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host', attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='False', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('rw', conn_info['data']['access_mode'])

        mountpoint2 = "/dev/sdx"
        attachment2 = self.volume.attach_volume(self.context, volume_id, None,
                                                'fake_host2', mountpoint2,
                                                'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment2['attach_status'])
        self.assertEqual(mountpoint2, attachment2['mountpoint'])
        self.assertIsNone(attachment2['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host2', attachment2['attached_host'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)
        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual("in-use", vol['status'])

        self.volume.detach_volume(self.context, volume_id, attachment2['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual("available", vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_twice_multiattach_volume_for_hosts(self):
        """Make sure volume can be attached and detached from hosts."""
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(
            self.context,
            admin_metadata={'readonly': 'False'},
            multiattach=True,
            **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id, None,
                                               'fake_host', mountpoint, 'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertTrue(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host', attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='False', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('rw', conn_info['data']['access_mode'])

        mountpoint2 = "/dev/sdx"
        attachment2 = self.volume.attach_volume(self.context, volume_id, None,
                                                'fake_host', mountpoint2,
                                                'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertEqual('attached', attachment2['attach_status'])
        self.assertEqual(mountpoint, attachment2['mountpoint'])
        self.assertIsNone(attachment2['instance_uuid'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)

    def test_run_attach_detach_not_multiattach_volume_for_hosts(self):
        """Make sure volume can't be attached to more than one host."""
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(
            self.context,
            admin_metadata={'readonly': 'False'},
            multiattach=False,
            **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        attachment = self.volume.attach_volume(self.context, volume_id, None,
                                               'fake_host', mountpoint, 'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertFalse(vol['multiattach'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host', attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='False', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('rw', conn_info['data']['access_mode'])

        mountpoint2 = "/dev/sdx"
        self.assertRaises(exception.InvalidVolume,
                          self.volume.attach_volume,
                          self.context,
                          volume_id,
                          None,
                          'fake_host2',
                          mountpoint2,
                          'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         attachment['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        # sanitized, conforms to RFC-952 and RFC-1123 specs.
        self.assertEqual('fake-host', attachment['attached_host'])

        self.assertRaises(exception.VolumeAttached,
                          self.volume.delete_volume,
                          self.context,
                          volume)
        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        self.assertEqual('available', vol['status'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_attach_detach_volume_with_attach_mode(self):
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           **self.volume_params)
        volume_id = volume['id']
        db.volume_update(self.context, volume_id, {'status': 'available', })
        self.volume.attach_volume(self.context, volume_id, instance_uuid,
                                  None, mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        attachment = vol['volume_attachment'][0]
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         vol['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertEqual(instance_uuid, attachment['instance_uuid'])
        self.assertIsNone(attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)

        self.assertEqual('ro', conn_info['data']['access_mode'])

        self.volume.detach_volume(self.context, volume_id, attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        attachment = vol['volume_attachment']
        self.assertEqual('available', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        self.assertEqual([], attachment)
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(1, len(admin_metadata))
        self.assertEqual('readonly', admin_metadata[0]['key'])
        self.assertEqual('True', admin_metadata[0]['value'])

        self.volume.attach_volume(self.context, volume_id, None,
                                  'fake_host', mountpoint, 'ro')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        attachment = vol['volume_attachment'][0]
        self.assertEqual('in-use', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.ATTACHED,
                         vol['attach_status'])
        self.assertEqual(mountpoint, attachment['mountpoint'])
        self.assertIsNone(attachment['instance_uuid'])
        self.assertEqual('fake-host', attachment['attached_host'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='ro')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)
        connector = {'initiator': 'iqn.2012-07.org.fake:01'}
        conn_info = self.volume.initialize_connection(self.context,
                                                      volume, connector)
        self.assertEqual('ro', conn_info['data']['access_mode'])

        self.volume.detach_volume(self.context, volume_id,
                                  attachment['id'])
        vol = db.volume_get(self.context, volume_id)
        attachment = vol['volume_attachment']
        self.assertEqual('available', vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        self.assertEqual([], attachment)
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(1, len(admin_metadata))
        self.assertEqual('readonly', admin_metadata[0]['key'])
        self.assertEqual('True', admin_metadata[0]['value'])

        self.volume.delete_volume(self.context, volume)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get,
                          self.context,
                          volume_id)

    def test_run_manager_attach_detach_volume_with_wrong_attach_mode(self):
        # Not allow using 'read-write' mode attach readonly volume
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        self.assertRaises(exception.InvalidVolumeAttachMode,
                          self.volume.attach_volume,
                          self.context,
                          volume_id,
                          instance_uuid,
                          None,
                          mountpoint,
                          'rw')

        # Assert a user message was created
        self.volume.message_api.create.assert_called_once_with(
            self.context, defined_messages.EventIds.ATTACH_READONLY_VOLUME,
            self.context.project_id, resource_type=resource_types.VOLUME,
            resource_uuid=volume['id'])

        attachment = objects.VolumeAttachmentList.get_all_by_volume_id(
            context.get_admin_context(), volume_id)[0]
        self.assertEqual(fields.VolumeAttachStatus.ERROR_ATTACHING,
                         attachment.attach_status)
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

        db.volume_update(self.context, volume_id, {'status': 'available'})
        self.assertRaises(exception.InvalidVolumeAttachMode,
                          self.volume.attach_volume,
                          self.context,
                          volume_id,
                          None,
                          'fake_host',
                          mountpoint,
                          'rw')
        attachment = objects.VolumeAttachmentList.get_all_by_volume_id(
            context.get_admin_context(), volume_id)[0]
        self.assertEqual(fields.VolumeAttachStatus.ERROR_ATTACHING,
                         attachment.attach_status)
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(2, len(admin_metadata))
        expected = dict(readonly='True', attached_mode='rw')
        ret = {}
        for item in admin_metadata:
            ret.update({item['key']: item['value']})
        self.assertDictEqual(expected, ret)

    def test_run_api_attach_detach_volume_with_wrong_attach_mode(self):
        # Not allow using 'read-write' mode attach readonly volume
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        mountpoint = "/dev/sdf"
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolumeAttachMode,
                          volume_api.attach,
                          self.context,
                          volume,
                          instance_uuid,
                          None,
                          mountpoint,
                          'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(1, len(admin_metadata))
        self.assertEqual('readonly', admin_metadata[0]['key'])
        self.assertEqual('True', admin_metadata[0]['value'])

        db.volume_update(self.context, volume_id, {'status': 'available'})
        self.assertRaises(exception.InvalidVolumeAttachMode,
                          volume_api.attach,
                          self.context,
                          volume,
                          None,
                          'fake_host',
                          mountpoint,
                          'rw')
        vol = db.volume_get(context.get_admin_context(), volume_id)
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])
        admin_metadata = vol['volume_admin_metadata']
        self.assertEqual(1, len(admin_metadata))
        self.assertEqual('readonly', admin_metadata[0]['key'])
        self.assertEqual('True', admin_metadata[0]['value'])

    def test_detach_volume_while_uploading_to_image_is_in_progress(self):
        # If instance is booted from volume with 'Terminate on Delete' flag
        # set, and when we delete instance then it tries to delete volume
        # even it is in 'uploading' state.
        # It is happening because detach call is setting volume status to
        # 'available'.
        mountpoint = "/dev/sdf"
        # Attach volume to the instance
        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        self.volume.attach_volume(self.context, volume_id, instance_uuid,
                                  None, mountpoint, 'ro')
        # Change volume status to 'uploading'
        db.volume_update(self.context, volume_id, {'status': 'uploading'})
        # Call detach api
        self.volume.detach_volume(self.context, volume_id)
        vol = db.volume_get(self.context, volume_id)
        # Check that volume status is 'uploading'
        self.assertEqual("uploading", vol['status'])
        self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                         vol['attach_status'])

    def test_reserve_volume_success(self):
        volume = tests_utils.create_volume(self.context, status='available')
        cinder.volume.api.API().reserve_volume(self.context, volume)
        volume_db = db.volume_get(self.context, volume.id)
        self.assertEqual('attaching', volume_db.status)
        db.volume_destroy(self.context, volume.id)

    def test_reserve_volume_in_attaching(self):
        self._test_reserve_volume_bad_status('attaching')

    def test_reserve_volume_in_maintenance(self):
        self._test_reserve_volume_bad_status('maintenance')

    def _test_reserve_volume_bad_status(self, status):
        volume = tests_utils.create_volume(self.context, status=status)
        self.assertRaises(exception.InvalidVolume,
                          cinder.volume.api.API().reserve_volume,
                          self.context,
                          volume)
        db.volume_destroy(self.context, volume.id)

    def test_unreserve_volume_success_in_use(self):
        UUID = six.text_type(uuid.uuid4())
        volume = tests_utils.create_volume(self.context, status='attaching')
        tests_utils.attach_volume(self.context, volume.id, UUID,
                                  'attached_host', 'mountpoint', mode='rw')

        cinder.volume.api.API().unreserve_volume(self.context, volume)

        db_volume = db.volume_get(self.context, volume.id)
        self.assertEqual('in-use', db_volume.status)

    def test_unreserve_volume_success_available(self):
        volume = tests_utils.create_volume(self.context, status='attaching')

        cinder.volume.api.API().unreserve_volume(self.context, volume)

        db_volume = db.volume_get(self.context, volume.id)
        self.assertEqual('available', db_volume.status)

    def test_multi_node(self):
        # TODO(termie): Figure out how to test with two nodes,
        # each of them having a different FLAG for storage_node
        # This will allow us to test cross-node interactions
        pass

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    def test_create_delete_snapshot(self, mock_notify):
        """Test snapshot can be created and deleted."""
        volume = tests_utils.create_volume(
            self.context,
            availability_zone=CONF.storage_availability_zone,
            **self.volume_params)

        mock_notify.assert_not_called()

        self.volume.create_volume(self.context, volume)

        self.assert_notify_called(mock_notify,
                                  (['INFO', 'volume.create.start'],
                                   ['INFO', 'volume.create.end']))

        snapshot = create_snapshot(volume['id'], size=volume['size'])
        snapshot_id = snapshot.id
        self.volume.create_snapshot(self.context, snapshot)
        self.assertEqual(
            snapshot_id, objects.Snapshot.get_by_id(self.context,
                                                    snapshot_id).id)

        self.assert_notify_called(mock_notify,
                                  (['INFO', 'volume.create.start'],
                                   ['INFO', 'volume.create.end'],
                                   ['INFO', 'snapshot.create.start'],
                                   ['INFO', 'snapshot.create.end']))

        self.volume.delete_snapshot(self.context, snapshot)
        self.assert_notify_called(mock_notify,
                                  (['INFO', 'volume.create.start'],
                                   ['INFO', 'volume.create.end'],
                                   ['INFO', 'snapshot.create.start'],
                                   ['INFO', 'snapshot.create.end'],
                                   ['INFO', 'snapshot.delete.start'],
                                   ['INFO', 'snapshot.delete.end']))

        snap = objects.Snapshot.get_by_id(context.get_admin_context(
            read_deleted='yes'), snapshot_id)
        self.assertEqual(fields.SnapshotStatus.DELETED, snap.status)
        self.assertRaises(exception.NotFound,
                          db.snapshot_get,
                          self.context,
                          snapshot_id)
        self.volume.delete_volume(self.context, volume)

    def test_create_delete_snapshot_with_metadata(self):
        """Test snapshot can be created with metadata and deleted."""
        test_meta = {'fake_key': 'fake_value'}
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        snapshot = create_snapshot(volume['id'], size=volume['size'],
                                   metadata=test_meta)
        snapshot_id = snapshot.id

        result_dict = snapshot.metadata

        self.assertEqual(test_meta, result_dict)
        self.volume.delete_snapshot(self.context, snapshot)
        self.assertRaises(exception.NotFound,
                          db.snapshot_get,
                          self.context,
                          snapshot_id)

    def test_delete_snapshot_another_cluster_fails(self):
        """Test delete of snapshot from another cluster fails."""
        self.volume.cluster = 'mycluster'
        volume = tests_utils.create_volume(self.context, status='available',
                                           size=1, host=CONF.host + 'fake',
                                           cluster_name=self.volume.cluster)
        snapshot = create_snapshot(volume.id, size=volume.size)

        self.volume.delete_snapshot(self.context, snapshot)
        self.assertRaises(exception.NotFound,
                          db.snapshot_get,
                          self.context,
                          snapshot.id)

    @mock.patch.object(db, 'snapshot_create',
                       side_effect=exception.InvalidSnapshot(
                           'Create snapshot in db failed!'))
    def test_create_snapshot_failed_db_snapshot(self, mock_snapshot):
        """Test exception handling when create snapshot in db failed."""
        test_volume = tests_utils.create_volume(
            self.context,
            status='available',
            host=CONF.host)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidSnapshot,
                          volume_api.create_snapshot,
                          self.context,
                          test_volume,
                          'fake_name',
                          'fake_description')

    def test_create_snapshot_failed_maintenance(self):
        """Test exception handling when create snapshot in maintenance."""
        test_volume = tests_utils.create_volume(
            self.context,
            status='maintenance',
            host=CONF.host)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.create_snapshot,
                          self.context,
                          test_volume,
                          'fake_name',
                          'fake_description')

    @mock.patch.object(QUOTAS, 'commit',
                       side_effect=exception.QuotaError(
                           'Snapshot quota commit failed!'))
    def test_create_snapshot_failed_quota_commit(self, mock_snapshot):
        """Test exception handling when snapshot quota commit failed."""
        test_volume = tests_utils.create_volume(
            self.context,
            status='available',
            host=CONF.host)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.QuotaError,
                          volume_api.create_snapshot,
                          self.context,
                          test_volume,
                          'fake_name',
                          'fake_description')

    @mock.patch.object(QUOTAS, 'reserve',
                       side_effect = OVER_SNAPSHOT_QUOTA_EXCEPTION)
    def test_create_snapshot_failed_quota_reserve(self, mock_reserve):
        """Test exception handling when snapshot quota reserve failed."""
        test_volume = tests_utils.create_volume(
            self.context,
            status='available',
            host=CONF.host)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.SnapshotLimitExceeded,
                          volume_api.create_snapshot,
                          self.context,
                          test_volume,
                          'fake_name',
                          'fake_description')

    @mock.patch.object(QUOTAS, 'reserve',
                       side_effect = OVER_SNAPSHOT_QUOTA_EXCEPTION)
    def test_create_snapshots_in_db_failed_quota_reserve(self, mock_reserve):
        """Test exception handling when snapshot quota reserve failed."""
        test_volume = tests_utils.create_volume(
            self.context,
            status='available',
            host=CONF.host)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.SnapshotLimitExceeded,
                          volume_api.create_snapshots_in_db,
                          self.context,
                          [test_volume],
                          'fake_name',
                          'fake_description',
                          fake.CONSISTENCY_GROUP_ID)

    def test_create_snapshot_failed_host_is_None(self):
        """Test exception handling when create snapshot and host is None."""
        test_volume = tests_utils.create_volume(
            self.context,
            host=None)
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidVolume,
                          volume_api.create_snapshot,
                          self.context,
                          test_volume,
                          'fake_name',
                          'fake_description')

    def test_cannot_delete_volume_in_use(self):
        """Test volume can't be deleted in in-use status."""
        self._test_cannot_delete_volume('in-use')

    def test_cannot_delete_volume_maintenance(self):
        """Test volume can't be deleted in maintenance status."""
        self._test_cannot_delete_volume('maintenance')

    def _test_cannot_delete_volume(self, status):
        """Test volume can't be deleted in invalid stats."""
        # create a volume and assign to host
        volume = tests_utils.create_volume(self.context, CONF.host,
                                           status=status)

        # 'in-use' status raises InvalidVolume
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.delete,
                          self.context,
                          volume)

        # clean up
        self.volume.delete_volume(self.context, volume)

    def test_force_delete_volume(self):
        """Test volume can be forced to delete."""
        # create a volume and assign to host
        self.volume_params['status'] = 'error_deleting'
        volume = tests_utils.create_volume(self.context, **self.volume_params)

        # 'error_deleting' volumes can't be deleted
        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.delete,
                          self.context,
                          volume)

        # delete with force
        self.volume_api.delete(self.context, volume, force=True)

        # status is deleting
        volume = objects.Volume.get_by_id(context.get_admin_context(),
                                          volume.id)
        self.assertEqual('deleting', volume.status)

        # clean up
        self.volume.delete_volume(self.context, volume)

    def test_cannot_force_delete_attached_volume(self):
        """Test volume can't be force delete in attached state."""
        volume = tests_utils.create_volume(self.context, CONF.host,
                                           status='in-use',
                                           attach_status=
                                           fields.VolumeAttachStatus.ATTACHED)

        self.assertRaises(exception.InvalidVolume,
                          self.volume_api.delete,
                          self.context,
                          volume,
                          force=True)

        db.volume_destroy(self.context, volume.id)

    def test_cannot_delete_volume_with_snapshots(self):
        """Test volume can't be deleted with dependent snapshots."""
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)
        snapshot = create_snapshot(volume['id'], size=volume['size'])
        self.volume.create_snapshot(self.context, snapshot)
        self.assertEqual(
            snapshot.id, objects.Snapshot.get_by_id(self.context,
                                                    snapshot.id).id)

        volume['status'] = 'available'
        volume['host'] = 'fakehost'

        volume_api = cinder.volume.api.API()

        self.assertRaises(exception.InvalidVolume,
                          volume_api.delete,
                          self.context,
                          volume)
        self.volume.delete_snapshot(self.context, snapshot)
        self.volume.delete_volume(self.context, volume)

    def test_can_delete_errored_snapshot(self):
        """Test snapshot can be created and deleted."""
        volume = tests_utils.create_volume(self.context, CONF.host)

        snapshot = create_snapshot(volume.id, size=volume['size'],
                                   ctxt=self.context,
                                   status=fields.SnapshotStatus.ERROR)

        self.volume_api.delete_snapshot(self.context, snapshot)

        self.assertEqual(fields.SnapshotStatus.DELETING, snapshot.status)
        self.volume.delete_volume(self.context, volume)

    def test_cannot_delete_snapshot_with_bad_status(self):
        volume = tests_utils.create_volume(self.context, CONF.host)
        snapshot = create_snapshot(volume.id, size=volume['size'],
                                   ctxt=self.context,
                                   status=fields.SnapshotStatus.CREATING)
        self.assertRaises(exception.InvalidSnapshot,
                          self.volume_api.delete_snapshot,
                          self.context,
                          snapshot)

        snapshot.status = fields.SnapshotStatus.ERROR
        snapshot.save()
        self.volume_api.delete_snapshot(self.context, snapshot)

        self.assertEqual(fields.SnapshotStatus.DELETING, snapshot.status)
        self.volume.delete_volume(self.context, volume)

    def test_create_snapshot_force(self):
        """Test snapshot in use can be created forcibly."""

        instance_uuid = '12345678-1234-5678-1234-567812345678'
        # create volume and attach to the instance
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)
        values = {'volume_id': volume['id'],
                  'instance_uuid': instance_uuid,
                  'attach_status': fields.VolumeAttachStatus.ATTACHING, }
        attachment = db.volume_attach(self.context, values)
        db.volume_attached(self.context, attachment['id'], instance_uuid,
                           None, '/dev/sda1')

        volume_api = cinder.volume.api.API()
        volume = volume_api.get(self.context, volume['id'])
        self.assertRaises(exception.InvalidVolume,
                          volume_api.create_snapshot,
                          self.context, volume,
                          'fake_name', 'fake_description')
        snapshot_ref = volume_api.create_snapshot_force(self.context,
                                                        volume,
                                                        'fake_name',
                                                        'fake_description')
        snapshot_ref.destroy()
        db.volume_destroy(self.context, volume['id'])

        # create volume and attach to the host
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)
        values = {'volume_id': volume['id'],
                  'attached_host': 'fake_host',
                  'attach_status': fields.VolumeAttachStatus.ATTACHING, }
        attachment = db.volume_attach(self.context, values)
        db.volume_attached(self.context, attachment['id'], None,
                           'fake_host', '/dev/sda1')

        volume_api = cinder.volume.api.API()
        volume = volume_api.get(self.context, volume['id'])
        self.assertRaises(exception.InvalidVolume,
                          volume_api.create_snapshot,
                          self.context, volume,
                          'fake_name', 'fake_description')
        snapshot_ref = volume_api.create_snapshot_force(self.context,
                                                        volume,
                                                        'fake_name',
                                                        'fake_description')
        snapshot_ref.destroy()
        db.volume_destroy(self.context, volume['id'])

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_snapshot_from_bootable_volume(self, mock_qemu_info):
        """Test create snapshot from bootable volume."""
        # create bootable volume from image
        volume = self._create_volume_from_image()
        volume_id = volume['id']
        self.assertEqual('available', volume['status'])
        self.assertTrue(volume['bootable'])

        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        # get volume's volume_glance_metadata
        ctxt = context.get_admin_context()
        vol_glance_meta = db.volume_glance_metadata_get(ctxt, volume_id)
        self.assertTrue(vol_glance_meta)

        # create snapshot from bootable volume
        snap = create_snapshot(volume_id)
        self.volume.create_snapshot(ctxt, snap)

        # get snapshot's volume_glance_metadata
        snap_glance_meta = db.volume_snapshot_glance_metadata_get(
            ctxt, snap.id)
        self.assertTrue(snap_glance_meta)

        # ensure that volume's glance metadata is copied
        # to snapshot's glance metadata
        self.assertEqual(len(vol_glance_meta), len(snap_glance_meta))
        vol_glance_dict = {x.key: x.value for x in vol_glance_meta}
        snap_glance_dict = {x.key: x.value for x in snap_glance_meta}
        self.assertDictEqual(vol_glance_dict, snap_glance_dict)

        # ensure that snapshot's status is changed to 'available'
        self.assertEqual(fields.SnapshotStatus.AVAILABLE, snap.status)

        # cleanup resource
        snap.destroy()
        db.volume_destroy(ctxt, volume_id)

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_snapshot_from_bootable_volume_fail(self, mock_qemu_info):
        """Test create snapshot from bootable volume.

        But it fails to volume_glance_metadata_copy_to_snapshot.
        As a result, status of snapshot is changed to ERROR.
        """
        # create bootable volume from image
        volume = self._create_volume_from_image()
        volume_id = volume['id']
        self.assertEqual('available', volume['status'])
        self.assertTrue(volume['bootable'])

        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        # get volume's volume_glance_metadata
        ctxt = context.get_admin_context()
        vol_glance_meta = db.volume_glance_metadata_get(ctxt, volume_id)
        self.assertTrue(vol_glance_meta)
        snap = create_snapshot(volume_id)
        snap_stat = snap.status
        self.assertTrue(snap.id)
        self.assertTrue(snap_stat)

        # set to return DB exception
        with mock.patch.object(db, 'volume_glance_metadata_copy_to_snapshot')\
                as mock_db:
            mock_db.side_effect = exception.MetadataCopyFailure(
                reason="Because of DB service down.")
            # create snapshot from bootable volume
            self.assertRaises(exception.MetadataCopyFailure,
                              self.volume.create_snapshot,
                              ctxt,
                              snap)

        # get snapshot's volume_glance_metadata
        self.assertRaises(exception.GlanceMetadataNotFound,
                          db.volume_snapshot_glance_metadata_get,
                          ctxt, snap.id)

        # ensure that status of snapshot is 'error'
        self.assertEqual(fields.SnapshotStatus.ERROR, snap.status)

        # cleanup resource
        snap.destroy()
        db.volume_destroy(ctxt, volume_id)

    def test_create_snapshot_from_bootable_volume_with_volume_metadata_none(
            self):
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume_id = volume['id']

        self.volume.create_volume(self.context, volume)
        # set bootable flag of volume to True
        db.volume_update(self.context, volume_id, {'bootable': True})

        snapshot = create_snapshot(volume['id'])
        self.volume.create_snapshot(self.context, snapshot)
        self.assertRaises(exception.GlanceMetadataNotFound,
                          db.volume_snapshot_glance_metadata_get,
                          self.context, snapshot.id)

        # ensure that status of snapshot is 'available'
        self.assertEqual(fields.SnapshotStatus.AVAILABLE, snapshot.status)

        # cleanup resource
        snapshot.destroy()
        db.volume_destroy(self.context, volume_id)

    def test_delete_busy_snapshot(self):
        """Test snapshot can be created and deleted."""

        self.volume.driver.vg = fake_lvm.FakeBrickLVM('cinder-volumes',
                                                      False,
                                                      None,
                                                      'default')

        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        snapshot = create_snapshot(volume_id, size=volume['size'])
        self.volume.create_snapshot(self.context, snapshot)

        with mock.patch.object(self.volume.driver, 'delete_snapshot',
                               side_effect=exception.SnapshotIsBusy(
                                   snapshot_name='fake')
                               ) as mock_del_snap:
            snapshot_id = snapshot.id
            self.volume.delete_snapshot(self.context, snapshot)
            snapshot_ref = objects.Snapshot.get_by_id(self.context,
                                                      snapshot_id)
            self.assertEqual(snapshot_id, snapshot_ref.id)
            self.assertEqual(fields.SnapshotStatus.AVAILABLE,
                             snapshot_ref.status)
            mock_del_snap.assert_called_once_with(snapshot)

    @test.testtools.skipIf(sys.platform == "darwin", "SKIP on OSX")
    def test_delete_no_dev_fails(self):
        """Test delete snapshot with no dev file fails."""
        self.mock_object(os.path, 'exists', lambda x: False)
        self.volume.driver.vg = fake_lvm.FakeBrickLVM('cinder-volumes',
                                                      False,
                                                      None,
                                                      'default')

        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume_id = volume['id']
        self.volume.create_volume(self.context, volume)
        snapshot = create_snapshot(volume_id)
        snapshot_id = snapshot.id
        self.volume.create_snapshot(self.context, snapshot)

        with mock.patch.object(self.volume.driver, 'delete_snapshot',
                               side_effect=exception.SnapshotIsBusy(
                                   snapshot_name='fake')) as mock_del_snap:
            self.volume.delete_snapshot(self.context, snapshot)
            snapshot_ref = objects.Snapshot.get_by_id(self.context,
                                                      snapshot_id)
            self.assertEqual(snapshot_id, snapshot_ref.id)
            self.assertEqual(fields.SnapshotStatus.AVAILABLE,
                             snapshot_ref.status)
            mock_del_snap.assert_called_once_with(snapshot)

    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'create_cloned_volume')
    @mock.patch('cinder.quota.QUOTAS.rollback')
    @mock.patch('cinder.quota.QUOTAS.commit')
    @mock.patch('cinder.quota.QUOTAS.reserve', return_value=["RESERVATION"])
    def test_clone_image_volume(self, mock_reserve, mock_commit,
                                mock_rollback, mock_cloned_volume):
        vol = tests_utils.create_volume(self.context,
                                        **self.volume_params)
        # unnecessary attributes should be removed from image volume
        vol.consistencygroup = None
        result = self.volume._clone_image_volume(self.context, vol,
                                                 {'id': fake.VOLUME_ID})

        self.assertNotEqual(False, result)
        mock_reserve.assert_called_once_with(self.context, volumes=1,
                                             gigabytes=vol.size)
        mock_commit.assert_called_once_with(self.context, ["RESERVATION"],
                                            project_id=vol.project_id)

    @mock.patch('cinder.quota.QUOTAS.rollback')
    @mock.patch('cinder.quota.QUOTAS.commit')
    @mock.patch('cinder.quota.QUOTAS.reserve', return_value=["RESERVATION"])
    def test_clone_image_volume_creation_failure(self, mock_reserve,
                                                 mock_commit, mock_rollback):
        vol = tests_utils.create_volume(self.context, **self.volume_params)
        with mock.patch.object(objects, 'Volume', side_effect=ValueError):
            self.assertFalse(self.volume._clone_image_volume(
                self.context, vol, {'id': fake.VOLUME_ID}))

        mock_reserve.assert_called_once_with(self.context, volumes=1,
                                             gigabytes=vol.size)
        mock_rollback.assert_called_once_with(self.context, ["RESERVATION"])

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_cloned_status_available(
            self, mock_qemu_info):
        """Test create volume from image via cloning.

        Verify that after cloning image to volume, it is in available
        state and is bootable.
        """
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        volume = self._create_volume_from_image()
        self.assertEqual('available', volume['status'])
        self.assertTrue(volume['bootable'])
        self.volume.delete_volume(self.context, volume)

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_not_cloned_status_available(
            self, mock_qemu_info):
        """Test create volume from image via full copy.

        Verify that after copying image to volume, it is in available
        state and is bootable.
        """
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        volume = self._create_volume_from_image(fakeout_clone_image=True)
        self.assertEqual('available', volume['status'])
        self.assertTrue(volume['bootable'])
        self.volume.delete_volume(self.context, volume)

    def test_create_volume_from_image_exception(self):
        """Test create volume from a non-existing image.

        Verify that create volume from a non-existing image, the volume
        status is 'error' and is not bootable.
        """
        dst_fd, dst_path = tempfile.mkstemp()
        os.close(dst_fd)

        self.mock_object(self.volume.driver, 'local_path', lambda x: dst_path)

        # creating volume testdata
        kwargs = {'display_description': 'Test Desc',
                  'size': 20,
                  'availability_zone': 'fake_availability_zone',
                  'status': 'creating',
                  'attach_status': fields.VolumeAttachStatus.DETACHED,
                  'host': 'dummy'}
        volume = objects.Volume(context=self.context, **kwargs)
        volume.create()

        self.assertRaises(exception.ImageNotFound,
                          self.volume.create_volume,
                          self.context,
                          volume,
                          {'image_id': self.FAKE_UUID})
        volume = objects.Volume.get_by_id(self.context, volume.id)
        self.assertEqual("error", volume['status'])
        self.assertFalse(volume['bootable'])
        # cleanup
        volume.destroy()
        os.unlink(dst_path)

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_copy_exception_rescheduling(
            self, mock_qemu_info):
        """Test create volume with ImageCopyFailure

        This exception should not trigger rescheduling and allocated_capacity
        should be incremented so we're having assert for that here.
        """
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        def fake_copy_image_to_volume(context, volume, image_service,
                                      image_id):
            raise exception.ImageCopyFailure()

        self.mock_object(self.volume.driver, 'copy_image_to_volume',
                         fake_copy_image_to_volume)
        mock_delete = self.mock_object(self.volume.driver, 'delete_volume')
        self.assertRaises(exception.ImageCopyFailure,
                          self._create_volume_from_image)
        # NOTE(dulek): Rescheduling should not occur, so lets assert that
        # allocated_capacity is incremented.
        self.assertDictEqual(self.volume.stats['pools'],
                             {'_pool0': {'allocated_capacity_gb': 1}})
        # NOTE(dulek): As we haven't rescheduled, make sure no delete_volume
        # was called.
        self.assertFalse(mock_delete.called)

    @mock.patch('cinder.utils.brick_get_connector_properties')
    @mock.patch('cinder.utils.brick_get_connector')
    @mock.patch('cinder.volume.driver.BaseVD.secure_file_operations_enabled')
    @mock.patch('cinder.volume.driver.BaseVD._detach_volume')
    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_unavailable(
            self, mock_qemu_info, mock_detach, mock_secure, *args):
        """Test create volume with ImageCopyFailure

        We'll raise an exception inside _connect_device after volume has
        already been attached to confirm that it detaches the volume.
        """
        mock_secure.side_effect = NameError
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        unbound_copy_method = cinder.volume.driver.BaseVD.copy_image_to_volume
        bound_copy_method = unbound_copy_method.__get__(self.volume.driver)
        with mock.patch.object(self.volume.driver, 'copy_image_to_volume',
                               side_effect=bound_copy_method):
            self.assertRaises(exception.ImageCopyFailure,
                              self._create_volume_from_image,
                              fakeout_copy_image_to_volume=False)
        # We must have called detach method.
        self.assertEqual(1, mock_detach.call_count)

    @mock.patch('cinder.utils.brick_get_connector_properties')
    @mock.patch('cinder.utils.brick_get_connector')
    @mock.patch('cinder.volume.driver.BaseVD._connect_device')
    @mock.patch('cinder.volume.driver.BaseVD._detach_volume')
    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_unavailable_no_attach_info(
            self, mock_qemu_info, mock_detach, mock_connect, *args):
        """Test create volume with ImageCopyFailure

        We'll raise an exception on _connect_device call to confirm that it
        detaches the volume even if the exception doesn't have attach_info.
        """
        mock_connect.side_effect = NameError
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        unbound_copy_method = cinder.volume.driver.BaseVD.copy_image_to_volume
        bound_copy_method = unbound_copy_method.__get__(self.volume.driver)
        with mock.patch.object(self.volume.driver, 'copy_image_to_volume',
                               side_effect=bound_copy_method):
            self.assertRaises(exception.ImageCopyFailure,
                              self._create_volume_from_image,
                              fakeout_copy_image_to_volume=False)
        # We must have called detach method.
        self.assertEqual(1, mock_detach.call_count)

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_image_clone_image_volume(self, mock_qemu_info):
        """Test create volume from image via image volume.

        Verify that after cloning image to volume, it is in available
        state and is bootable.
        """
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        volume = self._create_volume_from_image(clone_image_volume=True)
        self.assertEqual('available', volume['status'])
        self.assertTrue(volume['bootable'])
        self.volume.delete_volume(self.context, volume)

    def test_create_volume_from_exact_sized_image(self):
        """Test create volume from an image of the same size.

        Verify that an image which is exactly the same size as the
        volume, will work correctly.
        """
        try:
            volume_id = None
            volume_api = cinder.volume.api.API(
                image_service=FakeImageService())
            volume = volume_api.create(self.context, 2, 'name', 'description',
                                       image_id=self.FAKE_UUID)
            volume_id = volume['id']
            self.assertEqual('creating', volume['status'])

        finally:
            # cleanup
            db.volume_destroy(self.context, volume_id)

    def test_create_volume_from_oversized_image(self):
        """Verify that an image which is too big will fail correctly."""
        class _ModifiedFakeImageService(FakeImageService):
            def show(self, context, image_id):
                return {'size': 2 * units.Gi + 1,
                        'disk_format': 'raw',
                        'container_format': 'bare',
                        'status': 'active'}

        volume_api = cinder.volume.api.API(
            image_service=_ModifiedFakeImageService())

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context, 2,
                          'name', 'description', image_id=1)

    def test_create_volume_with_mindisk_error(self):
        """Verify volumes smaller than image minDisk will cause an error."""
        class _ModifiedFakeImageService(FakeImageService):
            def show(self, context, image_id):
                return {'size': 2 * units.Gi,
                        'disk_format': 'raw',
                        'container_format': 'bare',
                        'min_disk': 5,
                        'status': 'active'}

        volume_api = cinder.volume.api.API(
            image_service=_ModifiedFakeImageService())

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context, 2,
                          'name', 'description', image_id=1)

    def test_create_volume_with_deleted_imaged(self):
        """Verify create volume from image will cause an error."""
        class _ModifiedFakeImageService(FakeImageService):
            def show(self, context, image_id):
                return {'size': 2 * units.Gi,
                        'disk_format': 'raw',
                        'container_format': 'bare',
                        'min_disk': 5,
                        'status': 'deleted'}

        volume_api = cinder.volume.api.API(
            image_service=_ModifiedFakeImageService())

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context, 2,
                          'name', 'description', image_id=1)

    @mock.patch.object(QUOTAS, "rollback")
    @mock.patch.object(QUOTAS, "commit")
    @mock.patch.object(QUOTAS, "reserve", return_value=["RESERVATION"])
    def _do_test_create_volume_with_size(self, size, *_unused_quota_mocks):
        volume_api = cinder.volume.api.API()

        volume = volume_api.create(self.context,
                                   size,
                                   'name',
                                   'description')
        self.assertEqual(int(size), volume['size'])

    def test_create_volume_int_size(self):
        """Test volume creation with int size."""
        self._do_test_create_volume_with_size(2)

    def test_create_volume_string_size(self):
        """Test volume creation with string size."""
        self._do_test_create_volume_with_size('2')

    @mock.patch.object(QUOTAS, "rollback")
    @mock.patch.object(QUOTAS, "commit")
    @mock.patch.object(QUOTAS, "reserve", return_value=["RESERVATION"])
    def test_create_volume_with_bad_size(self, *_unused_quota_mocks):
        volume_api = cinder.volume.api.API()

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          '2Gb',
                          'name',
                          'description')

    def test_create_volume_with_float_fails(self):
        """Test volume creation with invalid float size."""
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          '1.5',
                          'name',
                          'description')

    def test_create_volume_with_zero_size_fails(self):
        """Test volume creation with string size."""
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          '0',
                          'name',
                          'description')

    def test_begin_detaching_fails_available(self):
        volume_api = cinder.volume.api.API()
        volume = tests_utils.create_volume(self.context, status='available')
        # Volume status is 'available'.
        self.assertRaises(exception.InvalidVolume, volume_api.begin_detaching,
                          self.context, volume)

        db.volume_update(self.context, volume.id,
                         {'status': 'in-use',
                          'attach_status':
                              fields.VolumeAttachStatus.DETACHED})
        # Should raise an error since not attached
        self.assertRaises(exception.InvalidVolume, volume_api.begin_detaching,
                          self.context, volume)

        db.volume_update(self.context, volume.id,
                         {'attach_status':
                          fields.VolumeAttachStatus.ATTACHED})
        # Ensure when attached no exception raised
        volume_api.begin_detaching(self.context, volume)

        volume_api.update(self.context, volume, {'status': 'maintenance'})
        self.assertRaises(exception.InvalidVolume, volume_api.begin_detaching,
                          self.context, volume)
        db.volume_destroy(self.context, volume.id)

    def test_begin_roll_detaching_volume(self):
        """Test begin_detaching and roll_detaching functions."""

        instance_uuid = '12345678-1234-5678-1234-567812345678'
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        attachment = db.volume_attach(self.context,
                                      {'volume_id': volume['id'],
                                       'attached_host': 'fake-host'})
        db.volume_attached(self.context, attachment['id'], instance_uuid,
                           'fake-host', 'vdb')
        volume_api = cinder.volume.api.API()
        volume_api.begin_detaching(self.context, volume)
        volume = volume_api.get(self.context, volume['id'])
        self.assertEqual("detaching", volume['status'])
        volume_api.roll_detaching(self.context, volume)
        volume = volume_api.get(self.context, volume['id'])
        self.assertEqual("in-use", volume['status'])

    def test_volume_api_update(self):
        # create a raw vol
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        # use volume.api to update name
        volume_api = cinder.volume.api.API()
        update_dict = {'display_name': 'test update name'}
        volume_api.update(self.context, volume, update_dict)
        # read changes from db
        vol = db.volume_get(context.get_admin_context(), volume['id'])
        self.assertEqual('test update name', vol['display_name'])

    def test_volume_api_update_maintenance(self):
        # create a raw vol
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        volume['status'] = 'maintenance'
        # use volume.api to update name
        volume_api = cinder.volume.api.API()
        update_dict = {'display_name': 'test update name'}
        self.assertRaises(exception.InvalidVolume, volume_api.update,
                          self.context, volume, update_dict)

    def test_volume_api_update_snapshot(self):
        # create raw snapshot
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        snapshot = create_snapshot(volume['id'])
        snapshot_id = snapshot.id
        self.assertIsNone(snapshot.display_name)
        # use volume.api to update name
        volume_api = cinder.volume.api.API()
        update_dict = {'display_name': 'test update name'}
        volume_api.update_snapshot(self.context, snapshot, update_dict)
        # read changes from db
        snap = objects.Snapshot.get_by_id(context.get_admin_context(),
                                          snapshot_id)
        self.assertEqual('test update name', snap.display_name)

    def test_volume_api_get_list_volumes_image_metadata(self):
        """Test get_list_volumes_image_metadata in volume API."""
        ctxt = context.get_admin_context()
        db.volume_create(ctxt, {'id': 'fake1', 'status': 'available',
                                'host': 'test', 'provider_location': '',
                                'size': 1})
        db.volume_glance_metadata_create(ctxt, 'fake1', 'key1', 'value1')
        db.volume_glance_metadata_create(ctxt, 'fake1', 'key2', 'value2')
        db.volume_create(ctxt, {'id': 'fake2', 'status': 'available',
                                'host': 'test', 'provider_location': '',
                                'size': 1})
        db.volume_glance_metadata_create(ctxt, 'fake2', 'key3', 'value3')
        db.volume_glance_metadata_create(ctxt, 'fake2', 'key4', 'value4')
        volume_api = cinder.volume.api.API()
        results = volume_api.get_list_volumes_image_metadata(ctxt, ['fake1',
                                                                    'fake2'])
        expect_results = {'fake1': {'key1': 'value1', 'key2': 'value2'},
                          'fake2': {'key3': 'value3', 'key4': 'value4'}}
        self.assertEqual(expect_results, results)

    @mock.patch.object(QUOTAS, 'limit_check')
    @mock.patch.object(QUOTAS, 'reserve')
    def test_extend_volume(self, reserve, limit_check):
        """Test volume can be extended at API level."""
        # create a volume and assign to host
        volume = tests_utils.create_volume(self.context, size=2,
                                           status='in-use', host=CONF.host)
        volume_api = cinder.volume.api.API()

        # Extend fails when status != available
        self.assertRaises(exception.InvalidVolume,
                          volume_api.extend,
                          self.context,
                          volume,
                          3)

        db.volume_update(self.context, volume.id, {'status': 'available'})
        # Extend fails when new_size < orig_size
        self.assertRaises(exception.InvalidInput,
                          volume_api.extend,
                          self.context,
                          volume,
                          1)

        # Extend fails when new_size == orig_size
        self.assertRaises(exception.InvalidInput,
                          volume_api.extend,
                          self.context,
                          volume,
                          2)

        # works when new_size > orig_size
        reserve.return_value = ["RESERVATION"]
        volume_api.extend(self.context, volume, 3)
        volume.refresh()
        self.assertEqual('extending', volume.status)
        reserve.assert_called_once_with(self.context, gigabytes=1,
                                        project_id=volume.project_id)

        # Test the quota exceeded
        db.volume_update(self.context, volume.id, {'status': 'available'})
        reserve.side_effect = exception.OverQuota(overs=['gigabytes'],
                                                  quotas={'gigabytes': 20},
                                                  usages={'gigabytes':
                                                          {'reserved': 5,
                                                           'in_use': 15}})
        self.assertRaises(exception.VolumeSizeExceedsAvailableQuota,
                          volume_api.extend, self.context,
                          volume, 3)

        limit_check.side_effect = exception.OverQuota(
            overs=['per_volume_gigabytes'], quotas={'per_volume_gigabytes': 2})
        self.assertRaises(exception.VolumeSizeExceedsLimit,
                          volume_api.extend, self.context,
                          volume, 3)

        # Test scheduler path
        limit_check.side_effect = None
        reserve.side_effect = None
        db.volume_update(self.context, volume.id, {'status': 'available'})
        volume_api.scheduler_rpcapi = mock.MagicMock()
        volume_api.scheduler_rpcapi.extend_volume = mock.MagicMock()

        volume_api.extend(self.context, volume, 3)

        request_spec = {
            'volume_properties': volume,
            'volume_type': {},
            'volume_id': volume.id
        }
        volume_api.scheduler_rpcapi.extend_volume.assert_called_once_with(
            self.context, volume, 3, ["RESERVATION"], request_spec)

        # Test direct volume path
        limit_check.side_effect = None
        reserve.side_effect = None
        db.volume_update(self.context, volume.id, {'status': 'available'})
        ext_mock = mock.MagicMock(side_effect=exception.ServiceTooOld)
        volume_api.volume_rpcapi.extend_volume = mock.MagicMock()
        volume_api.scheduler_rpcapi.extend_volume = ext_mock

        volume_api.extend(self.context, volume, 3)

        volume_api.volume_rpcapi.extend_volume.assert_called_once_with(
            self.context, volume, 3, ["RESERVATION"])

        # clean up
        self.volume.delete_volume(self.context, volume)

    def test_extend_volume_driver_not_initialized(self):
        """Test volume can be extended at API level."""
        # create a volume and assign to host
        fake_reservations = ['RESERVATION']
        volume = tests_utils.create_volume(self.context, size=2,
                                           status='available',
                                           host=CONF.host)
        self.volume.create_volume(self.context, volume)

        self.volume.driver._initialized = False

        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.extend_volume,
                          self.context, volume, 3,
                          fake_reservations)

        volume.refresh()
        self.assertEqual('error_extending', volume.status)

        # lets cleanup the mess.
        self.volume.driver._initialized = True
        self.volume.delete_volume(self.context, volume)

    def test_extend_volume_manager(self):
        """Test volume can be extended at the manager level."""
        def fake_extend(volume, new_size):
            volume['size'] = new_size

        fake_reservations = ['RESERVATION']
        volume = tests_utils.create_volume(self.context, size=2,
                                           status='creating', host=CONF.host)
        self.volume.create_volume(self.context, volume)

        # Test driver exception
        with mock.patch.object(self.volume.driver,
                               'extend_volume') as extend_volume:
            extend_volume.side_effect =\
                exception.CinderException('fake exception')
            volume['status'] = 'extending'
            self.volume.extend_volume(self.context, volume, '4',
                                      fake_reservations)
            volume.refresh()
            self.assertEqual(2, volume.size)
            self.assertEqual('error_extending', volume.status)

        # Test driver success
        with mock.patch.object(self.volume.driver,
                               'extend_volume') as extend_volume:
            with mock.patch.object(QUOTAS, 'commit') as quotas_commit:
                extend_volume.return_value = fake_extend
                volume.status = 'extending'
                self.volume.extend_volume(self.context, volume, '4',
                                          fake_reservations)
                volume.refresh()
                self.assertEqual(4, volume.size)
                self.assertEqual('available', volume.status)
                quotas_commit.assert_called_with(
                    self.context,
                    ['RESERVATION'],
                    project_id=volume.project_id)

        # clean up
        self.volume.delete_volume(self.context, volume)

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.extend_volume')
    def test_extend_volume_with_volume_type(self, mock_rpc_extend):
        elevated = context.get_admin_context()
        project_id = self.context.project_id
        db.volume_type_create(elevated, {'name': 'type', 'extra_specs': {}})
        vol_type = db.volume_type_get_by_name(elevated, 'type')

        volume_api = cinder.volume.api.API()
        volume = volume_api.create(self.context, 100, 'name', 'description',
                                   volume_type=vol_type)
        try:
            usage = db.quota_usage_get(elevated, project_id, 'gigabytes_type')
            volumes_in_use = usage.in_use
        except exception.QuotaUsageNotFound:
            volumes_in_use = 0
        self.assertEqual(100, volumes_in_use)
        db.volume_update(self.context, volume.id, {'status': 'available'})

        volume_api.extend(self.context, volume, 200)
        mock_rpc_extend.called_once_with(self.context, volume, 200, mock.ANY)

        try:
            usage = db.quota_usage_get(elevated, project_id, 'gigabytes_type')
            volumes_reserved = usage.reserved
        except exception.QuotaUsageNotFound:
            volumes_reserved = 0

        self.assertEqual(100, volumes_reserved)

    @mock.patch(
        'cinder.volume.driver.VolumeDriver.create_replica_test_volume')
    def test_create_volume_from_sourcereplica(self, _create_replica_test):
        """Test volume can be created from a volume replica."""
        _create_replica_test.return_value = None

        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        volume_dst = tests_utils.create_volume(
            self.context,
            **self.volume_params)
        self.volume.create_volume(self.context, volume_dst,
                                  {'source_replicaid': volume_src.id})
        self.assertEqual('available',
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).status)
        self.assertTrue(_create_replica_test.called)
        self.volume.delete_volume(self.context, volume_dst)
        self.volume.delete_volume(self.context, volume_src)

    def test_create_volume_from_sourcevol(self):
        """Test volume can be created from a source volume."""
        def fake_create_cloned_volume(volume, src_vref):
            pass

        self.mock_object(self.volume.driver, 'create_cloned_volume',
                         fake_create_cloned_volume)
        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)
        volume_dst = tests_utils.create_volume(self.context,
                                               source_volid=volume_src['id'],
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_dst)
        volume_dst.refresh()
        self.assertEqual('available', volume_dst.status)
        self.volume.delete_volume(self.context, volume_dst)
        self.volume.delete_volume(self.context, volume_src)

    @mock.patch('cinder.volume.api.API.list_availability_zones',
                return_value=({'name': 'nova', 'available': True},
                              {'name': 'az2', 'available': True}))
    def test_create_volume_from_sourcevol_fail_wrong_az(self, _mock_laz):
        """Test volume can't be cloned from an other volume in different az."""
        volume_api = cinder.volume.api.API()

        volume_src = tests_utils.create_volume(self.context,
                                               availability_zone='az2',
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_src)

        volume_src = db.volume_get(self.context, volume_src['id'])

        volume_dst = volume_api.create(self.context,
                                       size=1,
                                       name='fake_name',
                                       description='fake_desc',
                                       source_volume=volume_src)
        self.assertEqual('az2', volume_dst['availability_zone'])

        self.assertRaises(exception.InvalidInput,
                          volume_api.create,
                          self.context,
                          size=1,
                          name='fake_name',
                          description='fake_desc',
                          source_volume=volume_src,
                          availability_zone='nova')

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_create_volume_from_sourcevol_with_glance_metadata(
            self, mock_qemu_info):
        """Test glance metadata can be correctly copied to new volume."""
        def fake_create_cloned_volume(volume, src_vref):
            pass

        self.mock_object(self.volume.driver, 'create_cloned_volume',
                         fake_create_cloned_volume)
        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        volume_src = self._create_volume_from_image()
        self.volume.create_volume(self.context, volume_src)
        volume_dst = tests_utils.create_volume(self.context,
                                               source_volid=volume_src['id'],
                                               **self.volume_params)
        self.volume.create_volume(self.context, volume_dst)
        self.assertEqual('available',
                         db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).status)
        src_glancemeta = db.volume_get(context.get_admin_context(),
                                       volume_src['id']).volume_glance_metadata
        dst_glancemeta = db.volume_get(context.get_admin_context(),
                                       volume_dst['id']).volume_glance_metadata
        for meta_src in src_glancemeta:
            for meta_dst in dst_glancemeta:
                if meta_dst.key == meta_src.key:
                    self.assertEqual(meta_src.value, meta_dst.value)
        self.volume.delete_volume(self.context, volume_src)
        self.volume.delete_volume(self.context, volume_dst)

    def test_create_volume_from_sourcevol_failed_clone(self):
        """Test src vol status will be restore by error handling code."""
        def fake_error_create_cloned_volume(volume, src_vref):
            db.volume_update(self.context, src_vref['id'], {'status': 'error'})
            raise exception.CinderException('fake exception')

        self.mock_object(self.volume.driver, 'create_cloned_volume',
                         fake_error_create_cloned_volume)
        volume_src = tests_utils.create_volume(self.context,
                                               **self.volume_params)
        self.assertEqual('creating', volume_src.status)
        self.volume.create_volume(self.context, volume_src)
        self.assertEqual('available', volume_src.status)
        volume_dst = tests_utils.create_volume(self.context,
                                               source_volid=volume_src['id'],
                                               **self.volume_params)
        self.assertEqual('creating', volume_dst.status)
        self.assertRaises(exception.CinderException,
                          self.volume.create_volume,
                          self.context,
                          volume_dst)
        # Source volume's status is still available and dst is set to error
        self.assertEqual('available', volume_src.status)
        self.assertEqual('error', volume_dst.status)
        self.volume.delete_volume(self.context, volume_dst)
        self.volume.delete_volume(self.context, volume_src)

    def test_clean_temporary_volume(self):
        def fake_delete_volume(ctxt, volume):
            volume.destroy()

        fake_volume = tests_utils.create_volume(self.context, size=1,
                                                host=CONF.host,
                                                migration_status='migrating')
        fake_new_volume = tests_utils.create_volume(self.context, size=1,
                                                    host=CONF.host)
        # 1. Only clean the db
        self.volume._clean_temporary_volume(self.context, fake_volume,
                                            fake_new_volume,
                                            clean_db_only=True)
        self.assertRaises(exception.VolumeNotFound,
                          db.volume_get, self.context,
                          fake_new_volume.id)

        # 2. Delete the backend storage
        fake_new_volume = tests_utils.create_volume(self.context, size=1,
                                                    host=CONF.host)
        with mock.patch.object(volume_rpcapi.VolumeAPI, 'delete_volume') as \
                mock_delete_volume:
            mock_delete_volume.side_effect = fake_delete_volume
            self.volume._clean_temporary_volume(self.context,
                                                fake_volume,
                                                fake_new_volume,
                                                clean_db_only=False)
            self.assertRaises(exception.VolumeNotFound,
                              db.volume_get, self.context,
                              fake_new_volume.id)

        # Check when the migrated volume is not in migration
        fake_new_volume = tests_utils.create_volume(self.context, size=1,
                                                    host=CONF.host)
        fake_volume.migration_status = 'non-migrating'
        fake_volume.save()
        self.volume._clean_temporary_volume(self.context, fake_volume,
                                            fake_new_volume)
        volume = db.volume_get(context.get_admin_context(),
                               fake_new_volume.id)
        self.assertIsNone(volume.migration_status)

    def test_check_volume_filters_true(self):
        """Test bootable as filter for true"""
        volume_api = cinder.volume.api.API()
        filters = {'bootable': 'TRUE'}

        # To convert filter value to True or False
        volume_api.check_volume_filters(filters)

        # Confirming converted filter value against True
        self.assertTrue(filters['bootable'])

    def test_check_volume_filters_false(self):
        """Test bootable as filter for false"""
        volume_api = cinder.volume.api.API()
        filters = {'bootable': 'false'}

        # To convert filter value to True or False
        volume_api.check_volume_filters(filters)

        # Confirming converted filter value against False
        self.assertEqual(False, filters['bootable'])

    def test_check_volume_filters_invalid(self):
        """Test bootable as filter"""
        volume_api = cinder.volume.api.API()
        filters = {'bootable': 'invalid'}

        # To convert filter value to True or False
        volume_api.check_volume_filters(filters)

        # Confirming converted filter value against invalid value
        self.assertTrue(filters['bootable'])

    def test_update_volume_readonly_flag(self):
        """Test volume readonly flag can be updated at API level."""
        # create a volume and assign to host
        volume = tests_utils.create_volume(self.context,
                                           admin_metadata={'readonly': 'True'},
                                           **self.volume_params)
        self.volume.create_volume(self.context, volume)
        volume.status = 'in-use'

        def sort_func(obj):
            return obj['name']

        volume_api = cinder.volume.api.API()

        # Update fails when status != available
        self.assertRaises(exception.InvalidVolume,
                          volume_api.update_readonly_flag,
                          self.context,
                          volume,
                          False)

        volume.status = 'available'

        # works when volume in 'available' status
        volume_api.update_readonly_flag(self.context, volume, False)

        volume.refresh()
        self.assertEqual('available', volume.status)
        admin_metadata = volume.volume_admin_metadata
        self.assertEqual(1, len(admin_metadata))
        self.assertEqual('readonly', admin_metadata[0]['key'])
        self.assertEqual('False', admin_metadata[0]['value'])

        # clean up
        self.volume.delete_volume(self.context, volume)

    def test_secure_file_operations_enabled(self):
        """Test secure file operations setting for base driver.

        General, non network file system based drivers do not have
        anything to do with "secure_file_operations". This test verifies that
        calling the method always returns False.
        """
        ret_flag = self.volume.driver.secure_file_operations_enabled()
        self.assertFalse(ret_flag)

    @mock.patch.object(driver.BaseVD, 'secure_file_operations_enabled')
    def test_secure_file_operations_enabled_2(self, mock_secure):
        mock_secure.return_value = True
        vol = tests_utils.create_volume(self.context)
        result = self.volume.secure_file_operations_enabled(self.context,
                                                            vol)
        mock_secure.assert_called_once_with()
        self.assertTrue(result)

    @mock.patch('cinder.volume.flows.common.make_pretty_name',
                new=mock.MagicMock())
    @mock.patch('cinder.scheduler.rpcapi.SchedulerAPI.create_volume',
                return_value=None)
    @mock.patch('cinder.volume.flows.manager.create_volume.'
                'CreateVolumeFromSpecTask.execute',
                side_effect=exception.DriverNotInitialized())
    def test_create_volume_raise_rescheduled_exception(self, mock_execute,
                                                       mock_reschedule):
        # Create source volume
        test_vol = tests_utils.create_volume(self.context,
                                             **self.volume_params)
        test_vol_id = test_vol['id']
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.create_volume,
                          self.context, test_vol,
                          {'volume_properties': self.volume_params},
                          {'retry': {'num_attempts': 1, 'host': []}})
        self.assertTrue(mock_reschedule.called)
        volume = db.volume_get(context.get_admin_context(), test_vol_id)
        self.assertEqual('creating', volume['status'])

    @mock.patch('cinder.volume.flows.manager.create_volume.'
                'CreateVolumeFromSpecTask.execute')
    def test_create_volume_raise_unrescheduled_exception(self, mock_execute):
        # create source volume
        test_vol = tests_utils.create_volume(self.context,
                                             **self.volume_params)
        test_vol_id = test_vol['id']
        mock_execute.side_effect = exception.VolumeNotFound(
            volume_id=test_vol_id)
        self.assertRaises(exception.VolumeNotFound,
                          self.volume.create_volume,
                          self.context, test_vol,
                          {'volume_properties': self.volume_params},
                          {'retry': {'num_attempts': 1, 'host': []}})
        volume = db.volume_get(context.get_admin_context(), test_vol_id)
        self.assertEqual('error', volume['status'])

    def test_cascade_delete_volume_with_snapshots(self):
        """Test volume deletion with dependent snapshots."""
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)
        snapshot = create_snapshot(volume['id'], size=volume['size'])
        self.volume.create_snapshot(self.context, snapshot)
        self.assertEqual(
            snapshot.id, objects.Snapshot.get_by_id(self.context,
                                                    snapshot.id).id)

        volume['status'] = 'available'
        volume['host'] = 'fakehost'

        volume_api = cinder.volume.api.API()

        volume_api.delete(self.context,
                          volume,
                          cascade=True)

    def test_cascade_delete_volume_with_snapshots_error(self):
        """Test volume deletion with dependent snapshots."""
        volume = tests_utils.create_volume(self.context, **self.volume_params)
        self.volume.create_volume(self.context, volume)
        snapshot = create_snapshot(volume['id'], size=volume['size'])
        self.volume.create_snapshot(self.context, snapshot)
        self.assertEqual(
            snapshot.id, objects.Snapshot.get_by_id(self.context,
                                                    snapshot.id).id)

        snapshot.update({'status': fields.SnapshotStatus.CREATING})
        snapshot.save()

        volume['status'] = 'available'
        volume['host'] = 'fakehost'

        volume_api = cinder.volume.api.API()

        self.assertRaises(exception.InvalidVolume,
                          volume_api.delete,
                          self.context,
                          volume,
                          cascade=True)

    def test_cascade_force_delete_volume_with_snapshots_error(self):
        """Test volume force deletion with errored dependent snapshots."""
        volume = tests_utils.create_volume(self.context,
                                           host='fakehost')

        snapshot = create_snapshot(volume.id,
                                   size=volume.size,
                                   status=fields.SnapshotStatus.ERROR_DELETING)
        self.volume.create_snapshot(self.context, snapshot)

        volume_api = cinder.volume.api.API()

        volume_api.delete(self.context, volume, cascade=True, force=True)

        snapshot = objects.Snapshot.get_by_id(self.context, snapshot.id)
        self.assertEqual('deleting', snapshot.status)

        volume = objects.Volume.get_by_id(self.context, volume.id)
        self.assertEqual('deleting', volume.status)

    @mock.patch.object(fake_driver.FakeLoggingVolumeDriver, 'get_volume_stats')
    @mock.patch.object(driver.BaseVD, '_init_vendor_properties')
    def test_get_capabilities(self, mock_init_vendor, mock_get_volume_stats):
        stats = {
            'volume_backend_name': 'lvm',
            'vendor_name': 'Open Source',
            'storage_protocol': 'iSCSI',
            'vendor_prefix': 'abcd'
        }
        expected = stats.copy()
        expected['properties'] = {
            'compression': {
                'title': 'Compression',
                'description': 'Enables compression.',
                'type': 'boolean'},
            'qos': {
                'title': 'QoS',
                'description': 'Enables QoS.',
                'type': 'boolean'},
            'replication_enabled': {
                'title': 'Replication',
                'description': 'Enables replication.',
                'type': 'boolean'},
            'thin_provisioning': {
                'title': 'Thin Provisioning',
                'description': 'Sets thin provisioning.',
                'type': 'boolean'},
        }

        # Test to get updated capabilities
        discover = True
        mock_get_volume_stats.return_value = stats
        mock_init_vendor.return_value = ({}, None)
        capabilities = self.volume.get_capabilities(self.context,
                                                    discover)
        self.assertEqual(expected, capabilities)
        mock_get_volume_stats.assert_called_once_with(True)

        # Test to get existing original capabilities
        mock_get_volume_stats.reset_mock()
        discover = False
        capabilities = self.volume.get_capabilities(self.context,
                                                    discover)
        self.assertEqual(expected, capabilities)
        self.assertFalse(mock_get_volume_stats.called)

        # Normal test case to get vendor unique capabilities
        def init_vendor_properties(self):
            properties = {}
            self._set_property(
                properties,
                "abcd:minIOPS",
                "Minimum IOPS QoS",
                "Sets minimum IOPS if QoS is enabled.",
                "integer",
                minimum=10,
                default=100)
            return properties, 'abcd'

        expected['properties'].update(
            {'abcd:minIOPS': {
                'title': 'Minimum IOPS QoS',
                'description': 'Sets minimum IOPS if QoS is enabled.',
                'type': 'integer',
                'minimum': 10,
                'default': 100}})

        mock_get_volume_stats.reset_mock()
        mock_init_vendor.reset_mock()
        discover = True
        mock_init_vendor.return_value = (
            init_vendor_properties(self.volume.driver))
        capabilities = self.volume.get_capabilities(self.context,
                                                    discover)
        self.assertEqual(expected, capabilities)
        self.assertTrue(mock_get_volume_stats.called)

    @mock.patch.object(fake_driver.FakeLoggingVolumeDriver, 'get_volume_stats')
    @mock.patch.object(driver.BaseVD, '_init_vendor_properties')
    @mock.patch.object(driver.BaseVD, '_init_standard_capabilities')
    def test_get_capabilities_prefix_error(self, mock_init_standard,
                                           mock_init_vendor,
                                           mock_get_volume_stats):

        # Error test case: propety does not match vendor prefix
        def init_vendor_properties(self):
            properties = {}
            self._set_property(
                properties,
                "aaa:minIOPS",
                "Minimum IOPS QoS",
                "Sets minimum IOPS if QoS is enabled.",
                "integer")
            self._set_property(
                properties,
                "abcd:compression_type",
                "Compression type",
                "Specifies compression type.",
                "string")

            return properties, 'abcd'

        expected = {
            'abcd:compression_type': {
                'title': 'Compression type',
                'description': 'Specifies compression type.',
                'type': 'string'}}

        discover = True
        mock_get_volume_stats.return_value = {}
        mock_init_standard.return_value = {}
        mock_init_vendor.return_value = (
            init_vendor_properties(self.volume.driver))
        capabilities = self.volume.get_capabilities(self.context,
                                                    discover)
        self.assertEqual(expected, capabilities['properties'])

    @mock.patch.object(fake_driver.FakeLoggingVolumeDriver, 'get_volume_stats')
    @mock.patch.object(driver.BaseVD, '_init_vendor_properties')
    @mock.patch.object(driver.BaseVD, '_init_standard_capabilities')
    def test_get_capabilities_fail_override(self, mock_init_standard,
                                            mock_init_vendor,
                                            mock_get_volume_stats):

        # Error test case: propety cannot override any standard capabilities
        def init_vendor_properties(self):
            properties = {}
            self._set_property(
                properties,
                "qos",
                "Minimum IOPS QoS",
                "Sets minimum IOPS if QoS is enabled.",
                "integer")
            self._set_property(
                properties,
                "ab::cd:compression_type",
                "Compression type",
                "Specifies compression type.",
                "string")

            return properties, 'ab::cd'

        expected = {
            'ab__cd:compression_type': {
                'title': 'Compression type',
                'description': 'Specifies compression type.',
                'type': 'string'}}

        discover = True
        mock_get_volume_stats.return_value = {}
        mock_init_standard.return_value = {}
        mock_init_vendor.return_value = (
            init_vendor_properties(self.volume.driver))
        capabilities = self.volume.get_capabilities(self.context,
                                                    discover)
        self.assertEqual(expected, capabilities['properties'])

    @mock.patch.object(driver.BaseVD, 'get_backup_device')
    @mock.patch.object(driver.BaseVD, 'secure_file_operations_enabled')
    def test_get_backup_device(self, mock_secure, mock_get_backup):
        vol = tests_utils.create_volume(self.context)
        backup = tests_utils.create_backup(self.context, vol['id'])
        mock_secure.return_value = False
        mock_get_backup.return_value = (vol, False)
        result = self.volume.get_backup_device(self.context,
                                               backup)

        mock_get_backup.assert_called_once_with(self.context, backup)
        mock_secure.assert_called_once_with()
        expected_result = {'backup_device': vol, 'secure_enabled': False,
                           'is_snapshot': False}
        self.assertEqual(expected_result, result)

    @mock.patch.object(driver.BaseVD, 'get_backup_device')
    @mock.patch.object(driver.BaseVD, 'secure_file_operations_enabled')
    def test_get_backup_device_want_objects(self, mock_secure,
                                            mock_get_backup):
        vol = tests_utils.create_volume(self.context)
        backup = tests_utils.create_backup(self.context, vol['id'])
        mock_secure.return_value = False
        mock_get_backup.return_value = (vol, False)
        result = self.volume.get_backup_device(self.context,
                                               backup, want_objects=True)

        mock_get_backup.assert_called_once_with(self.context, backup)
        mock_secure.assert_called_once_with()
        expected_result = objects.BackupDeviceInfo.from_primitive(
            {'backup_device': vol, 'secure_enabled': False,
             'is_snapshot': False},
            self.context)
        self.assertEqual(expected_result, result)

    def test_backup_use_temp_snapshot_config(self):
        local_conf = self.volume.driver.configuration.local_conf
        self.assertFalse(local_conf.backup_use_temp_snapshot)

    @mock.patch.object(QUOTAS, 'reserve',
                       side_effect = OVER_SNAPSHOT_QUOTA_EXCEPTION)
    def test_existing_snapshot_failed_quota_reserve(self, mock_reserve):
        vol = tests_utils.create_volume(self.context)
        snap = tests_utils.create_snapshot(self.context, vol.id)
        with mock.patch.object(
                self.volume.driver,
                'manage_existing_snapshot_get_size') as mock_get_size:
            mock_get_size.return_value = 1
            self.assertRaises(exception.SnapshotLimitExceeded,
                              self.volume.manage_existing_snapshot,
                              self.context,
                              snap)

    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'manage_existing')
    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'manage_existing_get_size')
    @mock.patch('cinder.volume.utils.notify_about_volume_usage')
    def test_manage_volume_with_notify(self, mock_notify, mock_size,
                                       mock_manage):
        elevated = context.get_admin_context()
        vol_type = db.volume_type_create(
            elevated, {'name': 'type1', 'extra_specs': {}})
        # create source volume
        volume_params = {'volume_type_id': vol_type.id, 'status': 'managing'}
        test_vol = tests_utils.create_volume(self.context, **volume_params)
        mock_size.return_value = 1
        mock_manage.return_value = None

        self.volume.manage_existing(self.context, test_vol, 'volume_ref')
        mock_notify.assert_called_with(self.context, test_vol,
                                       'manage_existing.end',
                                       host=test_vol.host)

    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'manage_existing_get_size')
    @mock.patch('cinder.volume.flows.manager.manage_existing.'
                'ManageExistingTask.execute')
    def test_manage_volume_raise_driver_exception(self, mock_execute,
                                                  mock_driver_get_size):
        elevated = context.get_admin_context()
        project_id = self.context.project_id
        db.volume_type_create(elevated, {'name': 'type1', 'extra_specs': {}})
        vol_type = db.volume_type_get_by_name(elevated, 'type1')
        # create source volume
        self.volume_params['volume_type_id'] = vol_type['id']
        self.volume_params['status'] = 'managing'
        test_vol = tests_utils.create_volume(self.context,
                                             **self.volume_params)
        mock_execute.side_effect = exception.VolumeBackendAPIException(
            data="volume driver got exception")
        mock_driver_get_size.return_value = 1
        # Set quota usage
        reserve_opts = {'volumes': 1, 'gigabytes': 1}
        reservations = QUOTAS.reserve(self.context, project_id=project_id,
                                      **reserve_opts)
        QUOTAS.commit(self.context, reservations)
        usage = db.quota_usage_get(self.context, project_id, 'volumes')
        volumes_in_use = usage.in_use
        usage = db.quota_usage_get(self.context, project_id, 'gigabytes')
        gigabytes_in_use = usage.in_use

        self.assertRaises(exception.VolumeBackendAPIException,
                          self.volume.manage_existing,
                          self.context, test_vol,
                          'volume_ref')
        # check volume status
        volume = objects.Volume.get_by_id(context.get_admin_context(),
                                          test_vol.id)
        self.assertEqual('error_managing', volume.status)
        # Delete this volume with 'error_managing_deleting' status in c-vol.
        test_vol.status = 'error_managing_deleting'
        test_vol.save()
        self.volume.delete_volume(self.context, test_vol)
        ctxt = context.get_admin_context(read_deleted='yes')
        volume = objects.Volume.get_by_id(ctxt, test_vol.id)
        self.assertEqual('deleted', volume.status)
        # Get in_use number after deleting error_managing volume
        usage = db.quota_usage_get(self.context, project_id, 'volumes')
        volumes_in_use_new = usage.in_use
        self.assertEqual(volumes_in_use, volumes_in_use_new)
        usage = db.quota_usage_get(self.context, project_id, 'gigabytes')
        gigabytes_in_use_new = usage.in_use
        self.assertEqual(gigabytes_in_use, gigabytes_in_use_new)

    @mock.patch('cinder.volume.drivers.lvm.LVMVolumeDriver.'
                'manage_existing_get_size')
    def test_manage_volume_raise_driver_size_exception(self,
                                                       mock_driver_get_size):
        elevated = context.get_admin_context()
        project_id = self.context.project_id
        db.volume_type_create(elevated, {'name': 'type1', 'extra_specs': {}})
        # create source volume
        test_vol = tests_utils.create_volume(self.context,
                                             **self.volume_params)
        mock_driver_get_size.side_effect = exception.VolumeBackendAPIException(
            data="volume driver got exception")

        # Set quota usage
        reserve_opts = {'volumes': 1, 'gigabytes': 1}
        reservations = QUOTAS.reserve(self.context, project_id=project_id,
                                      **reserve_opts)
        QUOTAS.commit(self.context, reservations)
        usage = db.quota_usage_get(self.context, project_id, 'volumes')
        volumes_in_use = usage.in_use
        usage = db.quota_usage_get(self.context, project_id, 'gigabytes')
        gigabytes_in_use = usage.in_use

        self.assertRaises(exception.VolumeBackendAPIException,
                          self.volume.manage_existing,
                          self.context, test_vol,
                          'volume_ref')
        # check volume status
        volume = objects.Volume.get_by_id(context.get_admin_context(),
                                          test_vol.id)
        self.assertEqual('error_managing', volume.status)
        # Delete this volume with 'error_managing_deleting' status in c-vol.
        test_vol.status = 'error_managing_deleting'
        test_vol.save()
        self.volume.delete_volume(self.context, test_vol)
        ctxt = context.get_admin_context(read_deleted='yes')
        volume = objects.Volume.get_by_id(ctxt, test_vol.id)
        self.assertEqual('deleted', volume.status)
        # Get in_use number after raising exception
        usage = db.quota_usage_get(self.context, project_id, 'volumes')
        volumes_in_use_new = usage.in_use
        self.assertEqual(volumes_in_use, volumes_in_use_new)
        usage = db.quota_usage_get(self.context, project_id, 'gigabytes')
        gigabytes_in_use_new = usage.in_use
        self.assertEqual(gigabytes_in_use, gigabytes_in_use_new)

    @mock.patch('cinder.tests.fake_driver.FakeLoggingVolumeDriver.'
                'SUPPORTS_ACTIVE_ACTIVE', True)
    def test_set_resource_host_different(self):
        manager = vol_manager.VolumeManager(host='localhost-1@ceph',
                                            cluster='mycluster@ceph')
        volume = tests_utils.create_volume(self.user_context,
                                           host='localhost-2@ceph#ceph',
                                           cluster_name='mycluster@ceph')
        manager._set_resource_host(volume)
        volume.refresh()
        self.assertEqual('localhost-1@ceph#ceph', volume.host)

    @mock.patch('cinder.tests.fake_driver.FakeLoggingVolumeDriver.'
                'SUPPORTS_ACTIVE_ACTIVE', True)
    def test_set_resource_host_equal(self):
        manager = vol_manager.VolumeManager(host='localhost-1@ceph',
                                            cluster='mycluster@ceph')
        volume = tests_utils.create_volume(self.user_context,
                                           host='localhost-1@ceph#ceph',
                                           cluster_name='mycluster@ceph')
        with mock.patch.object(volume, 'save') as save_mock:
            manager._set_resource_host(volume)
            save_mock.assert_not_called()


@ddt.ddt
class VolumeMigrationTestCase(base.BaseVolumeTestCase):

    def setUp(self):
        super(VolumeMigrationTestCase, self).setUp()
        self._clear_patch = mock.patch('cinder.volume.utils.clear_volume',
                                       autospec=True)
        self._clear_patch.start()
        self.expected_status = 'available'

    def tearDown(self):
        super(VolumeMigrationTestCase, self).tearDown()
        self._clear_patch.stop()

    def test_migrate_volume_driver(self):
        """Test volume migration done by driver."""
        # Mock driver and rpc functions
        self.mock_object(self.volume.driver, 'migrate_volume',
                         lambda x, y, z, new_type_id=None: (
                             True, {'user_id': fake.USER_ID}))

        volume = tests_utils.create_volume(self.context, size=0,
                                           host=CONF.host,
                                           migration_status='migrating')
        host_obj = {'host': 'newhost', 'capabilities': {}}
        self.volume.migrate_volume(self.context, volume, host_obj, False)

        # check volume properties
        volume = objects.Volume.get_by_id(context.get_admin_context(),
                                          volume.id)
        self.assertEqual('newhost', volume.host)
        self.assertEqual('success', volume.migration_status)

    def _fake_create_volume(self, ctxt, volume, req_spec, filters,
                            allow_reschedule=True):
        return db.volume_update(ctxt, volume['id'],
                                {'status': self.expected_status})

    def test_migrate_volume_error(self):
        with mock.patch.object(self.volume.driver, 'migrate_volume') as \
                mock_migrate,\
                mock.patch.object(self.volume.driver, 'create_export') as \
                mock_create_export:

            # Exception case at self.driver.migrate_volume and create_export
            mock_migrate.side_effect = processutils.ProcessExecutionError
            mock_create_export.side_effect = processutils.ProcessExecutionError
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(processutils.ProcessExecutionError,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              False)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              volume.id)
            self.assertEqual('error', volume.migration_status)
            self.assertEqual('available', volume.status)

    @mock.patch('cinder.compute.API')
    @mock.patch('cinder.volume.manager.VolumeManager.'
                'migrate_volume_completion')
    @mock.patch('cinder.db.sqlalchemy.api.volume_get')
    def test_migrate_volume_generic(self, volume_get,
                                    migrate_volume_completion,
                                    nova_api):
        fake_db_new_volume = {'status': 'available', 'id': fake.VOLUME_ID}
        fake_new_volume = fake_volume.fake_db_volume(**fake_db_new_volume)
        new_volume_obj = fake_volume.fake_volume_obj(self.context,
                                                     **fake_new_volume)
        host_obj = {'host': 'newhost', 'capabilities': {}}
        volume_get.return_value = fake_new_volume
        update_server_volume = nova_api.return_value.update_server_volume
        volume = tests_utils.create_volume(self.context, size=1,
                                           host=CONF.host)
        with mock.patch.object(self.volume, '_copy_volume_data') as \
                mock_copy_volume:
            self.volume._migrate_volume_generic(self.context, volume,
                                                host_obj, None)
            mock_copy_volume.assert_called_with(self.context, volume,
                                                new_volume_obj,
                                                remote='dest')
            migrate_volume_completion.assert_called_with(
                self.context, volume, new_volume_obj, error=False)
            self.assertFalse(update_server_volume.called)

    @mock.patch('cinder.compute.API')
    @mock.patch('cinder.volume.manager.VolumeManager.'
                'migrate_volume_completion')
    @mock.patch('cinder.db.sqlalchemy.api.volume_get')
    def test_migrate_volume_generic_attached_volume(self, volume_get,
                                                    migrate_volume_completion,
                                                    nova_api):
        attached_host = 'some-host'
        fake_volume_id = fake.VOLUME_ID
        fake_db_new_volume = {'status': 'available', 'id': fake_volume_id}
        fake_new_volume = fake_volume.fake_db_volume(**fake_db_new_volume)
        host_obj = {'host': 'newhost', 'capabilities': {}}
        fake_uuid = fakes.get_fake_uuid()
        update_server_volume = nova_api.return_value.update_server_volume
        volume_get.return_value = fake_new_volume
        volume = tests_utils.create_volume(self.context, size=1,
                                           host=CONF.host)
        volume_attach = tests_utils.attach_volume(
            self.context, volume['id'], fake_uuid, attached_host, '/dev/vda')
        self.assertIsNotNone(volume_attach['volume_attachment'][0]['id'])
        self.assertEqual(
            fake_uuid, volume_attach['volume_attachment'][0]['instance_uuid'])
        self.assertEqual('in-use', volume_attach['status'])
        self.volume._migrate_volume_generic(self.context, volume,
                                            host_obj, None)
        self.assertFalse(migrate_volume_completion.called)
        update_server_volume.assert_called_with(self.context, fake_uuid,
                                                volume['id'], fake_volume_id)

    @mock.patch('cinder.objects.volume.Volume.save')
    @mock.patch('cinder.volume.rpcapi.VolumeAPI.create_volume')
    @mock.patch('cinder.compute.API')
    @mock.patch('cinder.volume.manager.VolumeManager.'
                'migrate_volume_completion')
    @mock.patch('cinder.db.sqlalchemy.api.volume_get')
    def test_migrate_volume_generic_volume_from_snap(self, volume_get,
                                                     migrate_volume_completion,
                                                     nova_api, create_volume,
                                                     save):
        def fake_create_volume(*args, **kwargs):
            context, volume, request_spec, filter_properties = args
            fake_db = mock.Mock()
            task = create_volume_manager.ExtractVolumeSpecTask(fake_db)
            specs = task.execute(context, volume, {})
            self.assertEqual('raw', specs['type'])

        def fake_copy_volume_data_with_chk_param(*args, **kwargs):
            context, src, dest = args
            self.assertEqual(src['snapshot_id'], dest['snapshot_id'])

        fake_db_new_volume = {'status': 'available', 'id': fake.VOLUME_ID}
        fake_new_volume = fake_volume.fake_db_volume(**fake_db_new_volume)
        host_obj = {'host': 'newhost', 'capabilities': {}}
        volume_get.return_value = fake_new_volume

        volume_from_snap = tests_utils.create_volume(self.context, size=1,
                                                     host=CONF.host)
        volume_from_snap['snapshot_id'] = fake.SNAPSHOT_ID
        create_volume.side_effect = fake_create_volume

        with mock.patch.object(self.volume, '_copy_volume_data') as \
                mock_copy_volume:
            mock_copy_volume.side_effect = fake_copy_volume_data_with_chk_param
            self.volume._migrate_volume_generic(self.context, volume_from_snap,
                                                host_obj, None)

    @mock.patch('cinder.objects.volume.Volume.save')
    @mock.patch('cinder.volume.rpcapi.VolumeAPI.create_volume')
    @mock.patch('cinder.compute.API')
    @mock.patch('cinder.volume.manager.VolumeManager.'
                'migrate_volume_completion')
    @mock.patch('cinder.db.sqlalchemy.api.volume_get')
    def test_migrate_volume_generic_for_clone(self, volume_get,
                                              migrate_volume_completion,
                                              nova_api, create_volume, save):
        def fake_create_volume(*args, **kwargs):
            context, volume, request_spec, filter_properties = args
            fake_db = mock.Mock()
            task = create_volume_manager.ExtractVolumeSpecTask(fake_db)
            specs = task.execute(context, volume, {})
            self.assertEqual('raw', specs['type'])

        def fake_copy_volume_data_with_chk_param(*args, **kwargs):
            context, src, dest = args
            self.assertEqual(src['source_volid'], dest['source_volid'])

        fake_db_new_volume = {'status': 'available', 'id': fake.VOLUME_ID}
        fake_new_volume = fake_volume.fake_db_volume(**fake_db_new_volume)
        host_obj = {'host': 'newhost', 'capabilities': {}}
        volume_get.return_value = fake_new_volume

        clone = tests_utils.create_volume(self.context, size=1,
                                          host=CONF.host)
        clone['source_volid'] = fake.VOLUME2_ID
        create_volume.side_effect = fake_create_volume

        with mock.patch.object(self.volume, '_copy_volume_data') as \
                mock_copy_volume:
            mock_copy_volume.side_effect = fake_copy_volume_data_with_chk_param
            self.volume._migrate_volume_generic(self.context, clone,
                                                host_obj, None)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'update_migrated_volume')
    @mock.patch.object(volume_rpcapi.VolumeAPI, 'delete_volume')
    @mock.patch.object(volume_rpcapi.VolumeAPI, 'create_volume')
    def test_migrate_volume_for_volume_generic(self, create_volume,
                                               rpc_delete_volume,
                                               update_migrated_volume):
        fake_volume = tests_utils.create_volume(self.context, size=1,
                                                previous_status='available',
                                                host=CONF.host)

        host_obj = {'host': 'newhost', 'capabilities': {}}
        with mock.patch.object(self.volume.driver, 'migrate_volume') as \
                mock_migrate_volume,\
                mock.patch.object(self.volume, '_copy_volume_data'),\
                mock.patch.object(self.volume.driver, 'delete_volume') as \
                delete_volume:
            create_volume.side_effect = self._fake_create_volume
            self.volume.migrate_volume(self.context, fake_volume, host_obj,
                                       True)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              fake_volume.id)
            self.assertEqual('newhost', volume.host)
            self.assertEqual('success', volume.migration_status)
            self.assertFalse(mock_migrate_volume.called)
            self.assertFalse(delete_volume.called)
            self.assertTrue(rpc_delete_volume.called)
            self.assertTrue(update_migrated_volume.called)

    def test_migrate_volume_generic_copy_error(self):
        with mock.patch.object(self.volume.driver, 'migrate_volume'),\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'create_volume')\
                as mock_create_volume,\
                mock.patch.object(self.volume, '_copy_volume_data') as \
                mock_copy_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'delete_volume'),\
                mock.patch.object(self.volume, 'migrate_volume_completion'),\
                mock.patch.object(self.volume.driver, 'create_export'):

            # Exception case at migrate_volume_generic
            # source_volume['migration_status'] is 'migrating'
            mock_create_volume.side_effect = self._fake_create_volume
            mock_copy_volume.side_effect = processutils.ProcessExecutionError
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(processutils.ProcessExecutionError,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              True)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              volume.id)
            self.assertEqual('error', volume.migration_status)
            self.assertEqual('available', volume.status)

    @mock.patch('cinder.image.image_utils.qemu_img_info')
    def test_migrate_volume_with_glance_metadata(self, mock_qemu_info):
        volume = self._create_volume_from_image(clone_image_volume=True)
        glance_metadata = volume.glance_metadata

        # We imitate the behavior of rpcapi, by serializing and then
        # deserializing the volume object we created earlier.
        serializer = objects.base.CinderObjectSerializer()
        serialized_volume = serializer.serialize_entity(self.context, volume)
        volume = serializer.deserialize_entity(self.context, serialized_volume)

        image_info = imageutils.QemuImgInfo()
        image_info.virtual_size = '1073741824'
        mock_qemu_info.return_value = image_info

        host_obj = {'host': 'newhost', 'capabilities': {}}
        with mock.patch.object(self.volume.driver,
                               'migrate_volume') as mock_migrate_volume:
            mock_migrate_volume.side_effect = (
                lambda x, y, z, new_type_id=None: (
                    True, {'user_id': fake.USER_ID}))
            self.volume.migrate_volume(self.context, volume, host_obj,
                                       False)
        self.assertEqual('newhost', volume.host)
        self.assertEqual('success', volume.migration_status)
        self.assertEqual(glance_metadata, volume.glance_metadata)

    @mock.patch('cinder.db.volume_update')
    def test_update_migrated_volume(self, volume_update):
        fake_host = 'fake_host'
        fake_new_host = 'fake_new_host'
        fake_update = {'_name_id': fake.VOLUME2_NAME_ID,
                       'provider_location': 'updated_location'}
        fake_elevated = context.RequestContext(fake.USER_ID, self.project_id,
                                               is_admin=True)
        volume = tests_utils.create_volume(self.context, size=1,
                                           status='available',
                                           host=fake_host)
        new_volume = tests_utils.create_volume(
            self.context, size=1,
            status='available',
            provider_location='fake_provider_location',
            _name_id=fake.VOLUME_NAME_ID,
            host=fake_new_host)
        new_volume._name_id = fake.VOLUME_NAME_ID
        new_volume.provider_location = 'fake_provider_location'
        fake_update_error = {'_name_id': new_volume._name_id,
                             'provider_location':
                             new_volume.provider_location}
        expected_update = {'_name_id': volume._name_id,
                           'provider_location': volume.provider_location}
        with mock.patch.object(self.volume.driver,
                               'update_migrated_volume') as migrate_update,\
                mock.patch.object(self.context, 'elevated') as elevated:
            migrate_update.return_value = fake_update
            elevated.return_value = fake_elevated
            self.volume.update_migrated_volume(self.context, volume,
                                               new_volume, 'available')
            volume_update.assert_has_calls((
                mock.call(fake_elevated, new_volume.id, expected_update),
                mock.call(fake_elevated, volume.id, fake_update)))

            # Test the case for update_migrated_volume not implemented
            # for the driver.
            migrate_update.reset_mock()
            volume_update.reset_mock()
            # Reset the volume objects to their original value, since they
            # were changed in the last call.
            new_volume._name_id = fake.VOLUME_NAME_ID
            new_volume.provider_location = 'fake_provider_location'
            migrate_update.side_effect = NotImplementedError
            self.volume.update_migrated_volume(self.context, volume,
                                               new_volume, 'available')
            volume_update.assert_has_calls((
                mock.call(fake_elevated, new_volume.id, fake_update),
                mock.call(fake_elevated, volume.id, fake_update_error)))

    def test_migrate_volume_generic_create_volume_error(self):
        self.expected_status = 'error'

        with mock.patch.object(self.volume.driver, 'migrate_volume'), \
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'create_volume') as mock_create_volume, \
                mock.patch.object(self.volume, '_clean_temporary_volume') as \
                clean_temporary_volume:

            # Exception case at the creation of the new temporary volume
            mock_create_volume.side_effect = self._fake_create_volume
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(exception.VolumeMigrationFailed,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              True)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              volume.id)
            self.assertEqual('error', volume['migration_status'])
            self.assertEqual('available', volume['status'])
            self.assertTrue(clean_temporary_volume.called)
        self.expected_status = 'available'

    def test_migrate_volume_generic_timeout_error(self):
        CONF.set_override("migration_create_volume_timeout_secs", 2)

        with mock.patch.object(self.volume.driver, 'migrate_volume'), \
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'create_volume') as mock_create_volume, \
                mock.patch.object(self.volume, '_clean_temporary_volume') as \
                clean_temporary_volume, \
                mock.patch.object(time, 'sleep'):

            # Exception case at the timeout of the volume creation
            self.expected_status = 'creating'
            mock_create_volume.side_effect = self._fake_create_volume
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(exception.VolumeMigrationFailed,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              True)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              volume.id)
            self.assertEqual('error', volume['migration_status'])
            self.assertEqual('available', volume['status'])
            self.assertTrue(clean_temporary_volume.called)
        self.expected_status = 'available'

    def test_migrate_volume_generic_create_export_error(self):
        with mock.patch.object(self.volume.driver, 'migrate_volume'),\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'create_volume')\
                as mock_create_volume,\
                mock.patch.object(self.volume, '_copy_volume_data') as \
                mock_copy_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'delete_volume'),\
                mock.patch.object(self.volume, 'migrate_volume_completion'),\
                mock.patch.object(self.volume.driver, 'create_export') as \
                mock_create_export:

            # Exception case at create_export
            mock_create_volume.side_effect = self._fake_create_volume
            mock_copy_volume.side_effect = processutils.ProcessExecutionError
            mock_create_export.side_effect = processutils.ProcessExecutionError
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(processutils.ProcessExecutionError,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              True)
            volume = objects.Volume.get_by_id(context.get_admin_context(),
                                              volume.id)
            self.assertEqual('error', volume['migration_status'])
            self.assertEqual('available', volume['status'])

    def test_migrate_volume_generic_migrate_volume_completion_error(self):
        def fake_migrate_volume_completion(ctxt, volume, new_volume,
                                           error=False):
            db.volume_update(ctxt, volume['id'],
                             {'migration_status': 'completing'})
            raise processutils.ProcessExecutionError

        with mock.patch.object(self.volume.driver, 'migrate_volume'),\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'create_volume')\
                as mock_create_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI, 'delete_volume'),\
                mock.patch.object(self.volume, 'migrate_volume_completion')\
                as mock_migrate_compl,\
                mock.patch.object(self.volume.driver, 'create_export'), \
                mock.patch.object(self.volume, '_attach_volume') \
                as mock_attach, \
                mock.patch.object(self.volume, '_detach_volume'), \
                mock.patch.object(os_brick.initiator.connector,
                                  'get_connector_properties') \
                as mock_get_connector_properties, \
                mock.patch.object(volutils, 'copy_volume') as mock_copy, \
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'get_capabilities') \
                as mock_get_capabilities:

            # Exception case at delete_volume
            # source_volume['migration_status'] is 'completing'
            mock_create_volume.side_effect = self._fake_create_volume
            mock_migrate_compl.side_effect = fake_migrate_volume_completion
            mock_get_connector_properties.return_value = {}
            mock_attach.side_effect = [{'device': {'path': 'bar'}},
                                       {'device': {'path': 'foo'}}]
            mock_get_capabilities.return_value = {'sparse_copy_volume': True}
            volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host)
            host_obj = {'host': 'newhost', 'capabilities': {}}
            self.assertRaises(processutils.ProcessExecutionError,
                              self.volume.migrate_volume,
                              self.context,
                              volume,
                              host_obj,
                              True)
            volume = db.volume_get(context.get_admin_context(), volume['id'])
            self.assertEqual('error', volume['migration_status'])
            self.assertEqual('available', volume['status'])
            mock_copy.assert_called_once_with('foo', 'bar', 0, '1M',
                                              sparse=True)

    def fake_attach_volume(self, ctxt, volume, instance_uuid, host_name,
                           mountpoint, mode):
            tests_utils.attach_volume(ctxt, volume.id,
                                      instance_uuid, host_name,
                                      '/dev/vda')

    def _test_migrate_volume_completion(self, status='available',
                                        instance_uuid=None, attached_host=None,
                                        retyping=False,
                                        previous_status='available'):

        initial_status = retyping and 'retyping' or status
        old_volume = tests_utils.create_volume(self.context, size=0,
                                               host=CONF.host,
                                               status=initial_status,
                                               migration_status='migrating',
                                               previous_status=previous_status)
        attachment = None
        if status == 'in-use':
            vol = tests_utils.attach_volume(self.context, old_volume.id,
                                            instance_uuid, attached_host,
                                            '/dev/vda')
            self.assertEqual('in-use', vol['status'])
            attachment = vol['volume_attachment'][0]
        target_status = 'target:%s' % old_volume.id
        new_host = CONF.host + 'new'
        new_volume = tests_utils.create_volume(self.context, size=0,
                                               host=new_host,
                                               migration_status=target_status)
        with mock.patch.object(self.volume, 'detach_volume') as \
                mock_detach_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'delete_volume') as mock_delete_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'attach_volume') as mock_attach_volume,\
                mock.patch.object(volume_rpcapi.VolumeAPI,
                                  'update_migrated_volume'),\
                mock.patch.object(self.volume.driver, 'attach_volume'):
            mock_attach_volume.side_effect = self.fake_attach_volume
            old_volume_host = old_volume.host
            new_volume_host = new_volume.host
            self.volume.migrate_volume_completion(self.context, old_volume,
                                                  new_volume)
            after_new_volume = objects.Volume.get_by_id(self.context,
                                                        new_volume.id)
            after_old_volume = objects.Volume.get_by_id(self.context,
                                                        old_volume.id)
            if status == 'in-use':
                mock_detach_volume.assert_called_with(self.context,
                                                      old_volume.id,
                                                      attachment['id'])
                attachments = db.volume_attachment_get_all_by_instance_uuid(
                    self.context, instance_uuid)
                mock_attach_volume.assert_called_once_with(
                    self.context,
                    old_volume,
                    attachment['instance_uuid'],
                    attachment['attached_host'],
                    attachment['mountpoint'],
                    'rw'
                )
                self.assertIsNotNone(attachments)
                self.assertEqual(attached_host,
                                 attachments[0]['attached_host'])
                self.assertEqual(instance_uuid,
                                 attachments[0]['instance_uuid'])
            else:
                self.assertFalse(mock_detach_volume.called)
            self.assertTrue(mock_delete_volume.called)
            # NOTE(sborkows): the migrate_volume_completion method alters
            # old and new volume objects, so we need to check the equality
            # between the former host value and the actual one.
            self.assertEqual(old_volume_host, after_new_volume.host)
            self.assertEqual(new_volume_host, after_old_volume.host)

    def test_migrate_volume_completion_retype_available(self):
        self._test_migrate_volume_completion('available', retyping=True)

    def test_migrate_volume_completion_retype_in_use(self):
        self._test_migrate_volume_completion(
            'in-use',
            '83c969d5-065e-4c9c-907d-5394bc2e98e2',
            'some-host',
            retyping=True,
            previous_status='in-use')

    def test_migrate_volume_completion_migrate_available(self):
        self._test_migrate_volume_completion()

    def test_migrate_volume_completion_migrate_in_use(self):
        self._test_migrate_volume_completion(
            'in-use',
            '83c969d5-065e-4c9c-907d-5394bc2e98e2',
            'some-host',
            retyping=False,
            previous_status='in-use')

    @ddt.data(False, True)
    def test_api_migrate_volume_completion_from_swap_with_no_migration(
            self, swap_error):
        # This test validates that Cinder properly finishes the swap volume
        # status updates for the case that no migration has occurred
        instance_uuid = '83c969d5-065e-4c9c-907d-5394bc2e98e2'
        attached_host = 'attached-host'
        orig_attached_vol = tests_utils.create_volume(self.context, size=0)
        orig_attached_vol = tests_utils.attach_volume(
            self.context, orig_attached_vol['id'], instance_uuid,
            attached_host, '/dev/vda')
        new_volume = tests_utils.create_volume(self.context, size=0)

        @mock.patch.object(volume_rpcapi.VolumeAPI, 'detach_volume')
        @mock.patch.object(volume_rpcapi.VolumeAPI, 'attach_volume')
        def _run_migration_completion(rpc_attach_volume,
                                      rpc_detach_volume):
            attachment = orig_attached_vol['volume_attachment'][0]
            attachment_id = attachment['id']
            rpc_attach_volume.side_effect = self.fake_attach_volume
            vol_id = volume_api.API().migrate_volume_completion(
                self.context, orig_attached_vol, new_volume, swap_error)
            if swap_error:
                # When swap failed, we don't want to finish attachment
                self.assertFalse(rpc_detach_volume.called)
                self.assertFalse(rpc_attach_volume.called)
            else:
                # When no error, we should be finishing the attachment
                rpc_detach_volume.assert_called_with(self.context,
                                                     orig_attached_vol,
                                                     attachment_id)
                rpc_attach_volume.assert_called_with(
                    self.context, new_volume, attachment['instance_uuid'],
                    attachment['attached_host'], attachment['mountpoint'],
                    'rw')
            self.assertEqual(new_volume['id'], vol_id)

        _run_migration_completion()

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    def test_retype_setup_fail_volume_is_available(self, mock_notify):
        """Verify volume is still available if retype prepare failed."""
        elevated = context.get_admin_context()
        project_id = self.context.project_id

        db.volume_type_create(elevated, {'name': 'old', 'extra_specs': {}})
        old_vol_type = db.volume_type_get_by_name(elevated, 'old')
        db.volume_type_create(elevated, {'name': 'new', 'extra_specs': {}})
        new_vol_type = db.volume_type_get_by_name(elevated, 'new')
        db.quota_create(elevated, project_id, 'volumes_new', 0)

        volume = tests_utils.create_volume(self.context, size=1,
                                           host=CONF.host, status='available',
                                           volume_type_id=old_vol_type['id'])

        api = cinder.volume.api.API()
        self.assertRaises(exception.VolumeLimitExceeded, api.retype,
                          self.context, volume, new_vol_type['id'])

        volume = db.volume_get(elevated, volume.id)
        mock_notify.assert_not_called()
        self.assertEqual('available', volume['status'])

    @mock.patch('cinder.tests.unit.fake_notifier.FakeNotifier._notify')
    def _retype_volume_exec(self, driver, mock_notify,
                            snap=False, policy='on-demand',
                            migrate_exc=False, exc=None, diff_equal=False,
                            replica=False, reserve_vol_type_only=False,
                            encryption_changed=False,
                            replica_new=None):
        elevated = context.get_admin_context()
        project_id = self.context.project_id

        if replica:
            rep_status = 'enabled'
            extra_specs = {'replication_enabled': '<is> True'}
        else:
            rep_status = 'disabled'
            extra_specs = {}

        if replica_new is None:
            replica_new = replica
        new_specs = {'replication_enabled': '<is> True'} if replica_new else {}

        db.volume_type_create(elevated, {'name': 'old',
                                         'extra_specs': extra_specs})
        old_vol_type = db.volume_type_get_by_name(elevated, 'old')

        db.volume_type_create(elevated, {'name': 'new',
                                         'extra_specs': new_specs})
        vol_type = db.volume_type_get_by_name(elevated, 'new')
        db.quota_create(elevated, project_id, 'volumes_new', 10)

        volume = tests_utils.create_volume(self.context, size=1,
                                           host=CONF.host, status='retyping',
                                           volume_type_id=old_vol_type['id'],
                                           replication_status=rep_status)
        volume.previous_status = 'available'
        volume.save()
        if snap:
            create_snapshot(volume.id, size=volume.size,
                            user_id=self.user_context.user_id,
                            project_id=self.user_context.project_id,
                            ctxt=self.user_context)
        if driver or diff_equal:
            host_obj = {'host': CONF.host, 'capabilities': {}}
        else:
            host_obj = {'host': 'newhost', 'capabilities': {}}

        reserve_opts = {'volumes': 1, 'gigabytes': volume.size}
        QUOTAS.add_volume_type_opts(self.context,
                                    reserve_opts,
                                    vol_type['id'])
        if reserve_vol_type_only:
            reserve_opts.pop('volumes')
            reserve_opts.pop('gigabytes')
            try:
                usage = db.quota_usage_get(elevated, project_id, 'volumes')
                total_volumes_in_use = usage.in_use
                usage = db.quota_usage_get(elevated, project_id, 'gigabytes')
                total_gigabytes_in_use = usage.in_use
            except exception.QuotaUsageNotFound:
                total_volumes_in_use = 0
                total_gigabytes_in_use = 0
        reservations = QUOTAS.reserve(self.context,
                                      project_id=project_id,
                                      **reserve_opts)

        old_reserve_opts = {'volumes': -1, 'gigabytes': -volume.size}
        QUOTAS.add_volume_type_opts(self.context,
                                    old_reserve_opts,
                                    old_vol_type['id'])
        old_reservations = QUOTAS.reserve(self.context,
                                          project_id=project_id,
                                          **old_reserve_opts)

        with mock.patch.object(self.volume.driver, 'retype') as _retype,\
                mock.patch.object(volume_types, 'volume_types_diff') as _diff,\
                mock.patch.object(self.volume, 'migrate_volume') as _mig,\
                mock.patch.object(db.sqlalchemy.api, 'volume_get') as _vget,\
                mock.patch.object(context.RequestContext, 'elevated') as _ctx:
            _vget.return_value = volume
            _retype.return_value = driver
            _ctx.return_value = self.context
            returned_diff = {
                'encryption': {},
                'qos_specs': {},
                'extra_specs': {},
            }
            if replica != replica_new:
                returned_diff['extra_specs']['replication_enabled'] = (
                    extra_specs.get('replication_enabled'),
                    new_specs.get('replication_enabled'))
            expected_replica_status = 'enabled' if replica_new else 'disabled'

            if encryption_changed:
                returned_diff['encryption'] = 'fake'
            _diff.return_value = (returned_diff, diff_equal)
            if migrate_exc:
                _mig.side_effect = KeyError
            else:
                _mig.return_value = True

            if not exc:
                self.volume.retype(self.context, volume,
                                   vol_type['id'], host_obj,
                                   migration_policy=policy,
                                   reservations=reservations,
                                   old_reservations=old_reservations)
            else:
                self.assertRaises(exc, self.volume.retype,
                                  self.context, volume,
                                  vol_type['id'], host_obj,
                                  migration_policy=policy,
                                  reservations=reservations,
                                  old_reservations=old_reservations)
            if host_obj['host'] != CONF.host:
                _retype.assert_not_called()

        # get volume/quota properties
        volume = objects.Volume.get_by_id(elevated, volume.id)
        try:
            usage = db.quota_usage_get(elevated, project_id, 'volumes_new')
            volumes_in_use = usage.in_use
        except exception.QuotaUsageNotFound:
            volumes_in_use = 0

        # Get new in_use after retype, it should not be changed.
        if reserve_vol_type_only:
            try:
                usage = db.quota_usage_get(elevated, project_id, 'volumes')
                new_total_volumes_in_use = usage.in_use
                usage = db.quota_usage_get(elevated, project_id, 'gigabytes')
                new_total_gigabytes_in_use = usage.in_use
            except exception.QuotaUsageNotFound:
                new_total_volumes_in_use = 0
                new_total_gigabytes_in_use = 0
            self.assertEqual(total_volumes_in_use, new_total_volumes_in_use)
            self.assertEqual(total_gigabytes_in_use,
                             new_total_gigabytes_in_use)

        # check properties
        if driver or diff_equal:
            self.assertEqual(vol_type['id'], volume.volume_type_id)
            self.assertEqual('available', volume.status)
            self.assertEqual(CONF.host, volume.host)
            self.assertEqual(1, volumes_in_use)
            self.assert_notify_called(mock_notify,
                                      (['INFO', 'volume.retype'],))
        elif not exc:
            self.assertEqual(old_vol_type['id'], volume.volume_type_id)
            self.assertEqual('retyping', volume.status)
            self.assertEqual(CONF.host, volume.host)
            self.assertEqual(1, volumes_in_use)
            self.assert_notify_called(mock_notify,
                                      (['INFO', 'volume.retype'],))
        else:
            self.assertEqual(old_vol_type['id'], volume.volume_type_id)
            self.assertEqual('available', volume.status)
            self.assertEqual(CONF.host, volume.host)
            self.assertEqual(0, volumes_in_use)
            mock_notify.assert_not_called()
        if encryption_changed:
            self.assertTrue(_mig.called)
        self.assertEqual(expected_replica_status, volume.replication_status)

    def test_retype_volume_driver_success(self):
        self._retype_volume_exec(True)

    @ddt.data((False, False), (False, True), (True, False), (True, True))
    @ddt.unpack
    def test_retype_volume_replica(self, replica, replica_new):
        self._retype_volume_exec(True, replica=replica,
                                 replica_new=replica_new)

    def test_retype_volume_migration_bad_policy(self):
        # Test volume retype that requires migration by not allowed
        self._retype_volume_exec(False, policy='never',
                                 exc=exception.VolumeMigrationFailed)

    def test_retype_volume_migration_with_replica(self):
        self._retype_volume_exec(False,
                                 replica=True,
                                 exc=exception.InvalidVolume)

    def test_retype_volume_migration_with_snaps(self):
        self._retype_volume_exec(False, snap=True, exc=exception.InvalidVolume)

    def test_retype_volume_migration_failed(self):
        self._retype_volume_exec(False, migrate_exc=True, exc=KeyError)

    def test_retype_volume_migration_success(self):
        self._retype_volume_exec(False, migrate_exc=False, exc=None)

    def test_retype_volume_migration_equal_types(self):
        self._retype_volume_exec(False, diff_equal=True)

    def test_retype_volume_with_type_only(self):
        self._retype_volume_exec(True, reserve_vol_type_only=True)

    def test_retype_volume_migration_encryption(self):
        self._retype_volume_exec(False, encryption_changed=True)

    def test_migrate_driver_not_initialized(self):
        volume = tests_utils.create_volume(self.context, size=0,
                                           host=CONF.host)
        host_obj = {'host': 'newhost', 'capabilities': {}}

        self.volume.driver._initialized = False
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.migrate_volume,
                          self.context, volume, host_obj, True)

        volume = objects.Volume.get_by_id(context.get_admin_context(),
                                          volume.id)
        self.assertEqual('error', volume.migration_status)

        # lets cleanup the mess.
        self.volume.driver._initialized = True
        self.volume.delete_volume(self.context, volume)

    def test_delete_source_volume_in_migration(self):
        """Test deleting a source volume that is in migration."""
        self._test_delete_volume_in_migration('migrating')

    def test_delete_destination_volume_in_migration(self):
        """Test deleting a destination volume that is in migration."""
        self._test_delete_volume_in_migration('target:vol-id')

    def _test_delete_volume_in_migration(self, migration_status):
        """Test deleting a volume that is in migration."""
        volume = tests_utils.create_volume(self.context, host=CONF.host,
                                           migration_status=migration_status)
        self.volume.delete_volume(self.context, volume=volume)

        # The volume is successfully removed during the volume delete
        # and won't exist in the database any more.
        self.assertRaises(exception.VolumeNotFound, volume.refresh)


@ddt.ddt
class ReplicationTestCase(base.BaseVolumeTestCase):

    @mock.patch('cinder.objects.Service.is_up', True)
    @mock.patch.object(volume_rpcapi.VolumeAPI, 'failover')
    @mock.patch.object(cinder.db, 'conditional_update')
    @mock.patch.object(objects.ServiceList, 'get_all')
    def test_failover(self, mock_get_all, mock_db_update, mock_failover):
        """Test replication failover."""

        service = fake_service.fake_service_obj(self.context,
                                                binary='cinder-volume')
        mock_get_all.return_value = [service]
        mock_db_update.return_value = {'replication_status': 'enabled'}
        volume_api = cinder.volume.api.API()
        volume_api.failover(self.context, host=CONF.host, cluster_name=None)
        mock_failover.assert_called_once_with(self.context, service, None)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'failover')
    @mock.patch.object(cinder.db, 'conditional_update')
    @mock.patch.object(cinder.db, 'service_get_all')
    def test_failover_unexpected_status(self, mock_db_get_all, mock_db_update,
                                        mock_failover):
        """Test replication failover unxepected status."""

        mock_db_get_all.return_value = [fake_service.fake_service_obj(
            self.context,
            binary='cinder-volume')]
        mock_db_update.return_value = None
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.failover,
                          self.context,
                          host=CONF.host,
                          cluster_name=None)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'freeze_host')
    @mock.patch.object(cinder.db, 'conditional_update', return_value=1)
    @mock.patch.object(cinder.objects.ServiceList, 'get_all')
    def test_freeze_host(self, mock_get_all, mock_db_update,
                         mock_freeze):
        """Test replication freeze_host."""

        service = fake_service.fake_service_obj(self.context,
                                                binary='cinder-volume')
        mock_get_all.return_value = [service]
        mock_freeze.return_value = True
        volume_api = cinder.volume.api.API()
        volume_api.freeze_host(self.context, host=CONF.host, cluster_name=None)
        mock_freeze.assert_called_once_with(self.context, service)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'freeze_host')
    @mock.patch.object(cinder.db, 'conditional_update')
    @mock.patch.object(cinder.db, 'service_get_all')
    def test_freeze_host_unexpected_status(self, mock_get_all,
                                           mock_db_update,
                                           mock_freeze):
        """Test replication freeze_host unexpected status."""

        mock_get_all.return_value = [fake_service.fake_service_obj(
            self.context,
            binary='cinder-volume')]
        mock_db_update.return_value = None
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.freeze_host,
                          self.context,
                          host=CONF.host,
                          cluster_name=None)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'thaw_host')
    @mock.patch.object(cinder.db, 'conditional_update', return_value=1)
    @mock.patch.object(cinder.objects.ServiceList, 'get_all')
    def test_thaw_host(self, mock_get_all, mock_db_update,
                       mock_thaw):
        """Test replication thaw_host."""

        service = fake_service.fake_service_obj(self.context,
                                                binary='cinder-volume')
        mock_get_all.return_value = [service]
        mock_thaw.return_value = True
        volume_api = cinder.volume.api.API()
        volume_api.thaw_host(self.context, host=CONF.host, cluster_name=None)
        mock_thaw.assert_called_once_with(self.context, service)

    @mock.patch.object(volume_rpcapi.VolumeAPI, 'thaw_host')
    @mock.patch.object(cinder.db, 'conditional_update')
    @mock.patch.object(cinder.db, 'service_get_all')
    def test_thaw_host_unexpected_status(self, mock_get_all,
                                         mock_db_update,
                                         mock_thaw):
        """Test replication thaw_host unexpected status."""

        mock_get_all.return_value = [fake_service.fake_service_obj(
            self.context,
            binary='cinder-volume')]
        mock_db_update.return_value = None
        volume_api = cinder.volume.api.API()
        self.assertRaises(exception.InvalidInput,
                          volume_api.thaw_host,
                          self.context,
                          host=CONF.host, cluster_name=None)

    @mock.patch('cinder.volume.driver.BaseVD.failover_completed')
    def test_failover_completed(self, completed_mock):
        rep_field = fields.ReplicationStatus
        svc = objects.Service(self.context, host=self.volume.host,
                              binary=constants.VOLUME_BINARY,
                              replication_status=rep_field.ENABLED)
        svc.create()
        self.volume.failover_completed(
            self.context,
            {'active_backend_id': 'secondary',
             'replication_status': rep_field.FAILED_OVER})
        service = objects.Service.get_by_id(self.context, svc.id)
        self.assertEqual('secondary', service.active_backend_id)
        self.assertEqual('failed-over', service.replication_status)
        completed_mock.assert_called_once_with(self.context, 'secondary')

    @mock.patch('cinder.volume.driver.BaseVD.failover_completed', wraps=True)
    def test_failover_completed_driver_failure(self, completed_mock):
        rep_field = fields.ReplicationStatus
        svc = objects.Service(self.context, host=self.volume.host,
                              binary=constants.VOLUME_BINARY,
                              replication_status=rep_field.ENABLED)
        svc.create()
        self.volume.failover_completed(
            self.context,
            {'active_backend_id': 'secondary',
             'replication_status': rep_field.FAILED_OVER})
        service = objects.Service.get_by_id(self.context, svc.id)
        self.assertEqual('secondary', service.active_backend_id)
        self.assertEqual(rep_field.ERROR, service.replication_status)
        self.assertTrue(service.disabled)
        self.assertIsNotNone(service.disabled_reason)
        completed_mock.assert_called_once_with(self.context, 'secondary')

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.failover_completed')
    def test_finish_failover_non_clustered(self, completed_mock):
        svc = mock.Mock(is_clustered=None)
        self.volume.finish_failover(self.context, svc, mock.sentinel.updates)
        svc.update.assert_called_once_with(mock.sentinel.updates)
        svc.save.assert_called_once_with()
        completed_mock.assert_not_called()

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.failover_completed')
    def test_finish_failover_clustered(self, completed_mock):
        svc = mock.Mock(cluster_name='cluster_name')
        updates = {'status': 'error'}
        self.volume.finish_failover(self.context, svc, updates)
        completed_mock.assert_called_once_with(self.context, svc, updates)
        svc.cluster.status = 'error'
        svc.cluster.save.assert_called_once()

    @ddt.data(None, 'cluster_name')
    @mock.patch('cinder.volume.manager.VolumeManager.finish_failover')
    @mock.patch('cinder.volume.manager.VolumeManager._get_my_volumes')
    def test_failover_manager(self, cluster, get_vols_mock, finish_mock):
        """Test manager's failover method for clustered and not clustered."""
        rep_field = fields.ReplicationStatus
        svc = objects.Service(self.context, host=self.volume.host,
                              binary=constants.VOLUME_BINARY,
                              cluster_name=cluster,
                              replication_status=rep_field.ENABLED)
        svc.create()

        vol = objects.Volume(self.context, host=self.volume.host)
        vol.create()

        get_vols_mock.return_value = [vol]

        with mock.patch.object(self.volume, 'driver') as driver:
            called, not_called = driver.failover_host, driver.failover
            if cluster:
                called, not_called = not_called, called

            called.return_value = ('secondary', [{'volume_id': vol.id,
                                   'updates': {'status': 'error'}}])

            self.volume.failover(self.context,
                                 secondary_backend_id='secondary')

        not_called.assert_not_called()
        called.assert_called_once_with(self.context, [vol],
                                       secondary_id='secondary')

        expected_update = {'replication_status': rep_field.FAILED_OVER,
                           'active_backend_id': 'secondary',
                           'disabled': True,
                           'disabled_reason': 'failed-over'}
        finish_mock.assert_called_once_with(self.context, svc, expected_update)

        volume = objects.Volume.get_by_id(self.context, vol.id)
        self.assertEqual('error', volume.status)

    @ddt.data(('host1', None), (None, 'mycluster'))
    @ddt.unpack
    def test_failover_api_fail_multiple_results(self, host, cluster):
        """Fail if we try to failover multiple backends in the same request."""
        rep_field = fields.ReplicationStatus
        clusters = [
            objects.Cluster(self.context,
                            name='mycluster@backend1',
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
            objects.Cluster(self.context,
                            name='mycluster@backend2',
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY)
        ]
        clusters[0].create()
        clusters[1].create()
        services = [
            objects.Service(self.context, host='host1@backend1',
                            cluster_name=clusters[0].name,
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
            objects.Service(self.context, host='host1@backend2',
                            cluster_name=clusters[1].name,
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
        ]
        services[0].create()
        services[1].create()
        self.assertRaises(exception.Invalid,
                          self.volume_api.failover, self.context, host,
                          cluster)

    def test_failover_api_not_found(self):
        self.assertRaises(exception.ServiceNotFound, self.volume_api.failover,
                          self.context, 'host1', None)

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.failover')
    def test_failover_api_success_multiple_results(self, failover_mock):
        """Succeed to failover multiple services for the same backend."""
        rep_field = fields.ReplicationStatus
        cluster_name = 'mycluster@backend1'
        cluster = objects.Cluster(self.context,
                                  name=cluster_name,
                                  replication_status=rep_field.ENABLED,
                                  binary=constants.VOLUME_BINARY)
        cluster.create()
        services = [
            objects.Service(self.context, host='host1@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
            objects.Service(self.context, host='host2@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
        ]
        services[0].create()
        services[1].create()

        self.volume_api.failover(self.context, None, cluster_name,
                                 mock.sentinel.secondary_id)

        for service in services + [cluster]:
            self.assertEqual(rep_field.ENABLED, service.replication_status)
            service.refresh()
            self.assertEqual(rep_field.FAILING_OVER,
                             service.replication_status)

        failover_mock.assert_called_once_with(self.context, mock.ANY,
                                              mock.sentinel.secondary_id)
        self.assertEqual(services[0].id, failover_mock.call_args[0][1].id)

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.failover')
    def test_failover_api_success_multiple_results_not_updated(self,
                                                               failover_mock):
        """Succeed to failover even if a service is not updated."""
        rep_field = fields.ReplicationStatus
        cluster_name = 'mycluster@backend1'
        cluster = objects.Cluster(self.context,
                                  name=cluster_name,
                                  replication_status=rep_field.ENABLED,
                                  binary=constants.VOLUME_BINARY)
        cluster.create()
        services = [
            objects.Service(self.context, host='host1@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ENABLED,
                            binary=constants.VOLUME_BINARY),
            objects.Service(self.context, host='host2@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ERROR,
                            binary=constants.VOLUME_BINARY),
        ]
        services[0].create()
        services[1].create()

        self.volume_api.failover(self.context, None, cluster_name,
                                 mock.sentinel.secondary_id)

        for service in services[:1] + [cluster]:
            service.refresh()
            self.assertEqual(rep_field.FAILING_OVER,
                             service.replication_status)

        services[1].refresh()
        self.assertEqual(rep_field.ERROR, services[1].replication_status)

        failover_mock.assert_called_once_with(self.context, mock.ANY,
                                              mock.sentinel.secondary_id)
        self.assertEqual(services[0].id, failover_mock.call_args[0][1].id)

    @mock.patch('cinder.volume.rpcapi.VolumeAPI.failover')
    def test_failover_api_fail_multiple_results_not_updated(self,
                                                            failover_mock):
        """Fail if none of the services could be updated."""
        rep_field = fields.ReplicationStatus
        cluster_name = 'mycluster@backend1'
        cluster = objects.Cluster(self.context,
                                  name=cluster_name,
                                  replication_status=rep_field.ENABLED,
                                  binary=constants.VOLUME_BINARY)
        cluster.create()
        down_time = timeutils.datetime.datetime(1970, 1, 1)
        services = [
            # This service is down
            objects.Service(self.context, host='host1@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ENABLED,
                            created_at=down_time,
                            updated_at=down_time,
                            modified_at=down_time,
                            binary=constants.VOLUME_BINARY),
            # This service is not with the right replication status
            objects.Service(self.context, host='host2@backend1',
                            cluster_name=cluster_name,
                            replication_status=rep_field.ERROR,
                            binary=constants.VOLUME_BINARY),
        ]
        services[0].create()
        services[1].create()

        self.assertRaises(exception.InvalidInput,
                          self.volume_api.failover, self.context, None,
                          cluster_name, mock.sentinel.secondary_id)

        for service in services:
            svc = objects.Service.get_by_id(self.context, service.id)
            self.assertEqual(service.replication_status,
                             svc.replication_status)

        cluster.refresh()
        self.assertEqual(rep_field.ENABLED, cluster.replication_status)

        failover_mock.assert_not_called()


class CopyVolumeToImageTestCase(base.BaseVolumeTestCase):
    def fake_local_path(self, volume):
        return self.dst_path

    def setUp(self):
        super(CopyVolumeToImageTestCase, self).setUp()
        self.dst_fd, self.dst_path = tempfile.mkstemp()
        self.addCleanup(os.unlink, self.dst_path)

        os.close(self.dst_fd)
        self.mock_object(self.volume.driver, 'local_path',
                         self.fake_local_path)
        self.image_id = '70a599e0-31e7-49b7-b260-868f441e862b'
        self.image_meta = {
            'id': self.image_id,
            'container_format': 'bare',
            'disk_format': 'raw'
        }
        self.volume_id = fake.VOLUME_ID
        self.addCleanup(db.volume_destroy, self.context, self.volume_id)

        self.volume_attrs = {
            'id': self.volume_id,
            'updated_at': datetime.datetime(1, 1, 1, 1, 1, 1),
            'display_description': 'Test Desc',
            'size': 20,
            'status': 'uploading',
            'host': 'dummy'
        }

    def test_copy_volume_to_image_status_available(self):
        # creating volume testdata
        self.volume_attrs['instance_uuid'] = None
        db.volume_create(self.context, self.volume_attrs)

        # start test
        self.volume.copy_volume_to_image(self.context,
                                         self.volume_id,
                                         self.image_meta)

        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume['status'])

    def test_copy_volume_to_image_over_image_quota(self):
        # creating volume testdata
        self.volume_attrs['instance_uuid'] = None
        volume = db.volume_create(self.context, self.volume_attrs)

        with mock.patch.object(self.volume.driver,
                               'copy_volume_to_image') as driver_copy_mock:
            driver_copy_mock.side_effect = exception.ImageLimitExceeded

            # test with image not in queued state
            self.assertRaises(exception.ImageLimitExceeded,
                              self.volume.copy_volume_to_image,
                              self.context,
                              self.volume_id,
                              self.image_meta)
            # Assert a user message was created
            self.volume.message_api.create.assert_called_once_with(
                self.context,
                defined_messages.EventIds.IMAGE_FROM_VOLUME_OVER_QUOTA,
                self.context.project_id, resource_type=resource_types.VOLUME,
                resource_uuid=volume['id'])

    def test_copy_volume_to_image_instance_deleted(self):
        # During uploading volume to image if instance is deleted,
        # volume should be in available status.
        self.image_meta['id'] = 'a440c04b-79fa-479c-bed1-0b816eaec379'
        # Creating volume testdata
        self.volume_attrs['instance_uuid'] = 'b21f957d-a72f-4b93-b5a5-' \
                                             '45b1161abb02'
        db.volume_create(self.context, self.volume_attrs)

        method = 'volume_update_status_based_on_attachment'
        with mock.patch.object(db, method,
                               wraps=getattr(db, method)) as mock_update:
            # Start test
            self.volume.copy_volume_to_image(self.context,
                                             self.volume_id,
                                             self.image_meta)
            # Check 'volume_update_status_after_copy_volume_to_image'
            # is called 1 time
            self.assertEqual(1, mock_update.call_count)

        # Check volume status has changed to available because
        # instance is deleted
        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume['status'])

    def test_copy_volume_to_image_status_use(self):
        self.image_meta['id'] = 'a440c04b-79fa-479c-bed1-0b816eaec379'
        # creating volume testdata
        db.volume_create(self.context, self.volume_attrs)

        # start test
        self.volume.copy_volume_to_image(self.context,
                                         self.volume_id,
                                         self.image_meta)

        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume['status'])

    def test_copy_volume_to_image_exception(self):
        self.image_meta['id'] = self.FAKE_UUID
        # creating volume testdata
        self.volume_attrs['status'] = 'in-use'
        db.volume_create(self.context, self.volume_attrs)

        # start test
        self.assertRaises(exception.ImageNotFound,
                          self.volume.copy_volume_to_image,
                          self.context,
                          self.volume_id,
                          self.image_meta)

        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume['status'])

    def test_copy_volume_to_image_driver_not_initialized(self):
        # creating volume testdata
        db.volume_create(self.context, self.volume_attrs)

        # set initialized to False
        self.volume.driver._initialized = False

        # start test
        self.assertRaises(exception.DriverNotInitialized,
                          self.volume.copy_volume_to_image,
                          self.context,
                          self.volume_id,
                          self.image_meta)

        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume.status)

    def test_copy_volume_to_image_driver_exception(self):
        self.image_meta['id'] = self.image_id

        image_service = fake_image.FakeImageService()
        # create new image in queued state
        queued_image_id = 'd5133f15-f753-41bd-920a-06b8c49275d9'
        queued_image_meta = image_service.show(self.context, self.image_id)
        queued_image_meta['id'] = queued_image_id
        queued_image_meta['status'] = 'queued'
        image_service.create(self.context, queued_image_meta)

        # create new image in saving state
        saving_image_id = '5c6eec33-bab4-4e7d-b2c9-88e2d0a5f6f2'
        saving_image_meta = image_service.show(self.context, self.image_id)
        saving_image_meta['id'] = saving_image_id
        saving_image_meta['status'] = 'saving'
        image_service.create(self.context, saving_image_meta)

        # create volume
        self.volume_attrs['status'] = 'available'
        self.volume_attrs['instance_uuid'] = None
        db.volume_create(self.context, self.volume_attrs)

        with mock.patch.object(self.volume.driver,
                               'copy_volume_to_image') as driver_copy_mock:
            driver_copy_mock.side_effect = exception.VolumeDriverException(
                "Error")

            # test with image not in queued state
            self.assertRaises(exception.VolumeDriverException,
                              self.volume.copy_volume_to_image,
                              self.context,
                              self.volume_id,
                              self.image_meta)
            # Make sure we are passing an OVO instance and not an ORM instance
            # to the driver
            self.assertIsInstance(driver_copy_mock.call_args[0][1],
                                  objects.Volume)
            volume = db.volume_get(self.context, self.volume_id)
            self.assertEqual('available', volume['status'])
            # image shouldn't be deleted if it is not in queued state
            image_service.show(self.context, self.image_id)

            # test with image in queued state
            self.assertRaises(exception.VolumeDriverException,
                              self.volume.copy_volume_to_image,
                              self.context,
                              self.volume_id,
                              queued_image_meta)
            volume = db.volume_get(self.context, self.volume_id)
            self.assertEqual('available', volume['status'])
            # queued image should be deleted
            self.assertRaises(exception.ImageNotFound,
                              image_service.show,
                              self.context,
                              queued_image_id)

            # test with image in saving state
            self.assertRaises(exception.VolumeDriverException,
                              self.volume.copy_volume_to_image,
                              self.context,
                              self.volume_id,
                              saving_image_meta)
            volume = db.volume_get(self.context, self.volume_id)
            self.assertEqual('available', volume['status'])
            # image in saving state should be deleted
            self.assertRaises(exception.ImageNotFound,
                              image_service.show,
                              self.context,
                              saving_image_id)

    @mock.patch.object(QUOTAS, 'reserve')
    @mock.patch.object(QUOTAS, 'commit')
    @mock.patch.object(vol_manager.VolumeManager, 'create_volume')
    @mock.patch.object(fake_driver.FakeLoggingVolumeDriver,
                       'copy_volume_to_image')
    def _test_copy_volume_to_image_with_image_volume(
            self, mock_copy, mock_create, mock_quota_commit,
            mock_quota_reserve):
        self.flags(glance_api_version=2)
        self.volume.driver.configuration.image_upload_use_cinder_backend = True
        self.addCleanup(fake_image.FakeImageService_reset)
        image_service = fake_image.FakeImageService()

        def add_location_wrapper(ctx, id, uri, metadata):
            try:
                volume = db.volume_get(ctx, id)
                self.assertEqual(ctx.project_id,
                                 volume['metadata']['image_owner'])
            except exception.VolumeNotFound:
                pass
            return image_service.add_location_orig(ctx, id, uri, metadata)

        image_service.add_location_orig = image_service.add_location
        image_service.add_location = add_location_wrapper

        image_id = '5c6eec33-bab4-4e7d-b2c9-88e2d0a5f6f2'
        self.image_meta['id'] = image_id
        self.image_meta['status'] = 'queued'
        image_service.create(self.context, self.image_meta)

        # creating volume testdata
        self.volume_attrs['instance_uuid'] = None
        db.volume_create(self.context, self.volume_attrs)

        def fake_create(context, volume, **kwargs):
            db.volume_update(context, volume.id, {'status': 'available'})

        mock_create.side_effect = fake_create

        # start test
        self.volume.copy_volume_to_image(self.context,
                                         self.volume_id,
                                         self.image_meta)

        volume = db.volume_get(self.context, self.volume_id)
        self.assertEqual('available', volume['status'])

        # return create image
        image = image_service.show(self.context, image_id)
        image_service.delete(self.context, image_id)
        return image

    def test_copy_volume_to_image_with_image_volume(self):
        image = self._test_copy_volume_to_image_with_image_volume()
        self.assertTrue(image['locations'][0]['url'].startswith('cinder://'))

    def test_copy_volume_to_image_with_image_volume_qcow2(self):
        self.image_meta['disk_format'] = 'qcow2'
        image = self._test_copy_volume_to_image_with_image_volume()
        self.assertNotIn('locations', image)

    @mock.patch.object(vol_manager.VolumeManager, 'delete_volume')
    @mock.patch.object(fake_image._FakeImageService, 'add_location',
                       side_effect=exception.Invalid)
    def test_copy_volume_to_image_with_image_volume_failure(
            self, mock_add_location, mock_delete):
        image = self._test_copy_volume_to_image_with_image_volume()
        self.assertNotIn('locations', image)
        self.assertTrue(mock_delete.called)


class GetActiveByWindowTestCase(base.BaseVolumeTestCase):
    def setUp(self):
        super(GetActiveByWindowTestCase, self).setUp()
        self.ctx = context.get_admin_context(read_deleted="yes")
        self.db_vol_attrs = [
            {
                'id': fake.VOLUME_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True, 'status': 'deleted',
                'deleted_at': datetime.datetime(1, 2, 1, 1, 1, 1),
            },
            {
                'id': fake.VOLUME2_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True, 'status': 'deleted',
                'deleted_at': datetime.datetime(1, 3, 10, 1, 1, 1),
            },
            {
                'id': fake.VOLUME3_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True, 'status': 'deleted',
                'deleted_at': datetime.datetime(1, 5, 1, 1, 1, 1),
            },
            {
                'id': fake.VOLUME4_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 3, 10, 1, 1, 1),
            },
            {
                'id': fake.VOLUME5_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 5, 1, 1, 1, 1),
            }
        ]

        self.db_snap_attrs = [
            {
                'id': fake.SNAPSHOT_ID,
                'project_id': 'p1',
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True,
                'status': fields.SnapshotStatus.DELETED,
                'deleted_at': datetime.datetime(1, 2, 1, 1, 1, 1),
                'volume_id': fake.VOLUME_ID,
            },

            {
                'id': fake.SNAPSHOT2_ID,
                'project_id': 'p1',
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True,
                'status': fields.SnapshotStatus.DELETED,
                'deleted_at': datetime.datetime(1, 3, 10, 1, 1, 1),
                'volume_id': fake.VOLUME_ID,
            },
            {
                'id': fake.SNAPSHOT3_ID,
                'project_id': 'p1',
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': True,
                'status': fields.SnapshotStatus.DELETED,
                'deleted_at': datetime.datetime(1, 5, 1, 1, 1, 1),
                'volume_id': fake.VOLUME_ID,
            },
            {
                'id': fake.SNAPSHOT_ID,
                'project_id': 'p1',
                'created_at': datetime.datetime(1, 3, 10, 1, 1, 1),
                'volume_id': fake.VOLUME_ID,
            },
            {
                'id': fake.SNAPSHOT2_ID,
                'project_id': 'p1',
                'created_at': datetime.datetime(1, 5, 1, 1, 1, 1),
                'volume_id': fake.VOLUME_ID
            }
        ]

        self.db_back_attrs = [
            {
                'id': fake.BACKUP_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': 1,
                'status': 'deleted',
                'deleted_at': datetime.datetime(1, 2, 1, 1, 1, 1)
            },
            {
                'id': fake.BACKUP2_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': 1,
                'status': 'deleted',
                'deleted_at': datetime.datetime(1, 3, 10, 1, 1, 1)
            },
            {
                'id': fake.BACKUP3_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 1, 1, 1, 1, 1),
                'deleted': 1,
                'status': 'deleted',
                'deleted_at': datetime.datetime(1, 5, 1, 1, 1, 1)
            },
            {
                'id': fake.BACKUP4_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 3, 10, 1, 1, 1),
            },
            {
                'id': fake.BACKUP5_ID,
                'host': 'devstack',
                'project_id': fake.PROJECT_ID,
                'created_at': datetime.datetime(1, 5, 1, 1, 1, 1),
            },
        ]

    def test_volume_get_all_active_by_window(self):
        # Find all all volumes valid within a timeframe window.

        # Not in window
        db.volume_create(self.ctx, self.db_vol_attrs[0])

        # In - deleted in window
        db.volume_create(self.ctx, self.db_vol_attrs[1])

        # In - deleted after window
        db.volume_create(self.ctx, self.db_vol_attrs[2])

        # In - created in window
        db.volume_create(self.context, self.db_vol_attrs[3])

        # Not of window.
        db.volume_create(self.context, self.db_vol_attrs[4])

        volumes = db.volume_get_all_active_by_window(
            self.context,
            datetime.datetime(1, 3, 1, 1, 1, 1),
            datetime.datetime(1, 4, 1, 1, 1, 1),
            project_id=fake.PROJECT_ID)
        self.assertEqual(3, len(volumes))
        self.assertEqual(fake.VOLUME2_ID, volumes[0].id)
        self.assertEqual(fake.VOLUME3_ID, volumes[1].id)
        self.assertEqual(fake.VOLUME4_ID, volumes[2].id)

    def test_snapshot_get_all_active_by_window(self):
        # Find all all snapshots valid within a timeframe window.
        db.volume_create(self.context, {'id': fake.VOLUME_ID})
        for i in range(5):
            self.db_vol_attrs[i]['volume_id'] = fake.VOLUME_ID

        # Not in window
        del self.db_snap_attrs[0]['id']
        snap1 = objects.Snapshot(self.ctx, **self.db_snap_attrs[0])
        snap1.create()

        # In - deleted in window
        del self.db_snap_attrs[1]['id']
        snap2 = objects.Snapshot(self.ctx, **self.db_snap_attrs[1])
        snap2.create()

        # In - deleted after window
        del self.db_snap_attrs[2]['id']
        snap3 = objects.Snapshot(self.ctx, **self.db_snap_attrs[2])
        snap3.create()

        # In - created in window
        del self.db_snap_attrs[3]['id']
        snap4 = objects.Snapshot(self.ctx, **self.db_snap_attrs[3])
        snap4.create()

        # Not of window.
        del self.db_snap_attrs[4]['id']
        snap5 = objects.Snapshot(self.ctx, **self.db_snap_attrs[4])
        snap5.create()

        snapshots = objects.SnapshotList.get_all_active_by_window(
            self.context,
            datetime.datetime(1, 3, 1, 1, 1, 1),
            datetime.datetime(1, 4, 1, 1, 1, 1)).objects
        self.assertEqual(3, len(snapshots))
        self.assertEqual(snap2.id, snapshots[0].id)
        self.assertEqual(fake.VOLUME_ID, snapshots[0].volume_id)
        self.assertEqual(snap3.id, snapshots[1].id)
        self.assertEqual(fake.VOLUME_ID, snapshots[1].volume_id)
        self.assertEqual(snap4.id, snapshots[2].id)
        self.assertEqual(fake.VOLUME_ID, snapshots[2].volume_id)

    def test_backup_get_all_active_by_window(self):
        # Find all backups valid within a timeframe window.
        db.volume_create(self.context, {'id': fake.VOLUME_ID})
        for i in range(5):
            self.db_back_attrs[i]['volume_id'] = fake.VOLUME_ID

        # Not in window
        db.backup_create(self.ctx, self.db_back_attrs[0])

        # In - deleted in window
        db.backup_create(self.ctx, self.db_back_attrs[1])

        # In - deleted after window
        db.backup_create(self.ctx, self.db_back_attrs[2])

        # In - created in window
        db.backup_create(self.ctx, self.db_back_attrs[3])

        # Not of window
        db.backup_create(self.ctx, self.db_back_attrs[4])

        backups = db.backup_get_all_active_by_window(
            self.context,
            datetime.datetime(1, 3, 1, 1, 1, 1),
            datetime.datetime(1, 4, 1, 1, 1, 1),
            project_id=fake.PROJECT_ID
        )
        self.assertEqual(3, len(backups))
        self.assertEqual(fake.BACKUP2_ID, backups[0].id)
        self.assertEqual(fake.BACKUP3_ID, backups[1].id)
        self.assertEqual(fake.BACKUP4_ID, backups[2].id)


class DriverTestCase(test.TestCase):
    """Base Test class for Drivers."""
    driver_name = "cinder.volume.driver.FakeBaseDriver"

    def setUp(self):
        super(DriverTestCase, self).setUp()
        vol_tmpdir = tempfile.mkdtemp()
        self.flags(volume_driver=self.driver_name,
                   volumes_dir=vol_tmpdir)
        self.volume = importutils.import_object(CONF.volume_manager)
        self.context = context.get_admin_context()
        self.output = ""
        self.configuration = conf.Configuration(None)
        self.mock_object(brick_lvm.LVM, '_vg_exists', lambda x: True)

        def _fake_execute(_command, *_args, **_kwargs):
            """Fake _execute."""
            return self.output, None
        exec_patcher = mock.patch.object(self.volume.driver, '_execute',
                                         _fake_execute)
        exec_patcher.start()
        self.addCleanup(exec_patcher.stop)
        self.volume.driver.set_initialized()
        self.addCleanup(self._cleanup)

    def _cleanup(self):
        try:
            shutil.rmtree(CONF.volumes_dir)
        except OSError:
            pass

    def _attach_volume(self):
        """Attach volumes to an instance."""
        return []


@ddt.ddt
class GenericVolumeDriverTestCase(DriverTestCase):
    """Test case for VolumeDriver."""
    driver_name = "cinder.tests.fake_driver.FakeLoggingVolumeDriver"

    @mock.patch.object(utils, 'temporary_chown')
    @mock.patch('six.moves.builtins.open')
    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch.object(db.sqlalchemy.api, 'volume_get')
    def test_backup_volume_available(self, mock_volume_get,
                                     mock_get_connector_properties,
                                     mock_file_open,
                                     mock_temporary_chown):
        vol = tests_utils.create_volume(self.context)
        self.context.user_id = fake.USER_ID
        self.context.project_id = fake.PROJECT_ID
        backup_obj = tests_utils.create_backup(self.context,
                                               vol['id'])
        properties = {}
        attach_info = {'device': {'path': '/dev/null'}}
        backup_service = mock.Mock()

        self.volume.driver._attach_volume = mock.MagicMock()
        self.volume.driver._detach_volume = mock.MagicMock()
        self.volume.driver.terminate_connection = mock.MagicMock()
        self.volume.driver.create_snapshot = mock.MagicMock()
        self.volume.driver.delete_snapshot = mock.MagicMock()

        mock_volume_get.return_value = vol
        mock_get_connector_properties.return_value = properties
        f = mock_file_open.return_value = open('/dev/null', 'rb')

        backup_service.backup(backup_obj, f, None)
        self.volume.driver._attach_volume.return_value = attach_info, vol

        self.volume.driver.backup_volume(self.context, backup_obj,
                                         backup_service)

        mock_volume_get.assert_called_with(self.context, vol['id'])

    def test_create_temp_cloned_volume(self):
        with mock.patch.object(
                self.volume.driver,
                'create_cloned_volume') as mock_create_cloned_volume:
            model_update = {'provider_location': 'dummy'}
            mock_create_cloned_volume.return_value = model_update
            vol = tests_utils.create_volume(self.context,
                                            status='backing-up')
            cloned_vol = self.volume.driver._create_temp_cloned_volume(
                self.context, vol)
            self.assertEqual('dummy', cloned_vol.provider_location)
            self.assertEqual('available', cloned_vol.status)

            mock_create_cloned_volume.return_value = None
            vol = tests_utils.create_volume(self.context,
                                            status='backing-up')
            cloned_vol = self.volume.driver._create_temp_cloned_volume(
                self.context, vol)
            self.assertEqual('available', cloned_vol.status)

    @mock.patch.object(utils, 'temporary_chown')
    @mock.patch('six.moves.builtins.open')
    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch.object(db.sqlalchemy.api, 'volume_get')
    def test_backup_volume_inuse_temp_volume(self, mock_volume_get,
                                             mock_get_connector_properties,
                                             mock_file_open,
                                             mock_temporary_chown):
        vol = tests_utils.create_volume(self.context,
                                        status='backing-up',
                                        previous_status='in-use')
        temp_vol = tests_utils.create_volume(self.context)
        self.context.user_id = fake.USER_ID
        self.context.project_id = fake.PROJECT_ID
        backup_obj = tests_utils.create_backup(self.context,
                                               vol['id'])
        properties = {}
        attach_info = {'device': {'path': '/dev/null'}}
        backup_service = mock.Mock()

        self.volume.driver._attach_volume = mock.MagicMock()
        self.volume.driver._detach_volume = mock.MagicMock()
        self.volume.driver.terminate_connection = mock.MagicMock()
        self.volume.driver._create_temp_snapshot = mock.MagicMock()
        self.volume.driver._delete_temp_snapshot = mock.MagicMock()

        mock_volume_get.return_value = vol
        self.volume.driver._create_temp_snapshot.return_value = temp_vol
        mock_get_connector_properties.return_value = properties
        f = mock_file_open.return_value = open('/dev/null', 'rb')

        backup_service.backup(backup_obj, f, None)
        self.volume.driver._attach_volume.return_value = attach_info, vol
        self.volume.driver.backup_volume(self.context, backup_obj,
                                         backup_service)

        mock_volume_get.assert_called_with(self.context, vol['id'])
        self.volume.driver._create_temp_snapshot.assert_called_once_with(
            self.context, vol)
        self.volume.driver._delete_temp_snapshot.assert_called_once_with(
            self.context, temp_vol)

    @mock.patch.object(utils, 'temporary_chown')
    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch('six.moves.builtins.open')
    def test_restore_backup(self,
                            mock_open,
                            mock_get_connector_properties,
                            mock_temporary_chown):
        dev_null = '/dev/null'
        vol = tests_utils.create_volume(self.context)
        backup = {'volume_id': vol['id'], 'id': 'backup-for-%s' % vol['id']}
        properties = {}
        attach_info = {'device': {'path': dev_null}}

        volume_file = mock.MagicMock()
        mock_open.return_value.__enter__.return_value = volume_file
        mock_get_connector_properties.return_value = properties

        self.volume.driver._attach_volume = mock.MagicMock()
        self.volume.driver._attach_volume.return_value = attach_info, vol
        self.volume.driver._detach_volume = mock.MagicMock()
        self.volume.driver.terminate_connection = mock.MagicMock()
        self.volume.driver.secure_file_operations_enabled = mock.MagicMock()
        self.volume.driver.secure_file_operations_enabled.side_effect = (False,
                                                                         True)
        backup_service = mock.MagicMock()

        self.volume.driver.restore_backup(self.context, backup, vol,
                                          backup_service)
        backup_service.restore.assert_called_with(backup, vol['id'],
                                                  volume_file)
        self.assertEqual(1, backup_service.restore.call_count)

    def test_get_backup_device_available(self):
        vol = tests_utils.create_volume(self.context)
        self.context.user_id = fake.USER_ID
        self.context.project_id = fake.PROJECT_ID
        backup_obj = tests_utils.create_backup(self.context,
                                               vol['id'])
        (backup_device, is_snapshot) = self.volume.driver.get_backup_device(
            self.context, backup_obj)
        volume = objects.Volume.get_by_id(self.context, vol.id)
        self.assertEqual(volume, backup_device)
        self.assertFalse(is_snapshot)
        backup_obj.refresh()
        self.assertIsNone(backup_obj.temp_volume_id)

    def test_get_backup_device_in_use(self):
        vol = tests_utils.create_volume(self.context,
                                        status='backing-up',
                                        previous_status='in-use')
        temp_vol = tests_utils.create_volume(self.context)
        self.context.user_id = fake.USER_ID
        self.context.project_id = fake.PROJECT_ID
        backup_obj = tests_utils.create_backup(self.context,
                                               vol['id'])
        with mock.patch.object(
                self.volume.driver,
                '_create_temp_cloned_volume') as mock_create_temp:
            mock_create_temp.return_value = temp_vol
            (backup_device, is_snapshot) = (
                self.volume.driver.get_backup_device(self.context,
                                                     backup_obj))
            self.assertEqual(temp_vol, backup_device)
            self.assertFalse(is_snapshot)
            backup_obj.refresh()
            self.assertEqual(temp_vol.id, backup_obj.temp_volume_id)

    def test__create_temp_volume_from_snapshot(self):
        volume_dict = {'id': fake.SNAPSHOT_ID,
                       'host': 'fakehost',
                       'cluster_name': 'fakecluster',
                       'availability_zone': 'fakezone',
                       'size': 1}
        vol = fake_volume.fake_volume_obj(self.context, **volume_dict)
        snapshot = fake_snapshot.fake_snapshot_obj(self.context)

        with mock.patch.object(
                self.volume.driver,
                'create_volume_from_snapshot'):
            temp_vol = self.volume.driver._create_temp_volume_from_snapshot(
                self.context,
                vol, snapshot)
            self.assertEqual(fields.VolumeAttachStatus.DETACHED,
                             temp_vol.attach_status)
            self.assertEqual('fakezone', temp_vol.availability_zone)
            self.assertEqual('fakecluster', temp_vol.cluster_name)

    @mock.patch.object(utils, 'brick_get_connector_properties')
    @mock.patch.object(cinder.volume.manager.VolumeManager, '_attach_volume')
    @mock.patch.object(cinder.volume.manager.VolumeManager, '_detach_volume')
    @mock.patch.object(volutils, 'copy_volume')
    @mock.patch.object(volume_rpcapi.VolumeAPI, 'get_capabilities')
    @mock.patch.object(cinder.volume.volume_types,
                       'volume_types_encryption_changed')
    @ddt.data(False, True)
    def test_copy_volume_data_mgr(self,
                                  encryption_changed,
                                  mock_encryption_changed,
                                  mock_get_capabilities,
                                  mock_copy,
                                  mock_detach,
                                  mock_attach,
                                  mock_get_connector):
        """Test function of _copy_volume_data."""

        src_vol = tests_utils.create_volume(self.context, size=1,
                                            host=CONF.host)
        dest_vol = tests_utils.create_volume(self.context, size=1,
                                             host=CONF.host)
        mock_get_connector.return_value = {}
        mock_encryption_changed.return_value = encryption_changed
        self.volume.driver._throttle = mock.MagicMock()

        attach_expected = [
            mock.call(self.context, dest_vol, {},
                      remote=False,
                      attach_encryptor=encryption_changed),
            mock.call(self.context, src_vol, {},
                      remote=False,
                      attach_encryptor=encryption_changed)]

        detach_expected = [
            mock.call(self.context, {'device': {'path': 'bar'}},
                      dest_vol, {}, force=False, remote=False,
                      attach_encryptor=encryption_changed),
            mock.call(self.context, {'device': {'path': 'foo'}},
                      src_vol, {}, force=False, remote=False,
                      attach_encryptor=encryption_changed)]

        attach_volume_returns = [
            {'device': {'path': 'bar'}},
            {'device': {'path': 'foo'}}
        ]

        #  Test case for sparse_copy_volume = False
        mock_attach.side_effect = attach_volume_returns
        mock_get_capabilities.return_value = {}
        self.volume._copy_volume_data(self.context,
                                      src_vol,
                                      dest_vol)

        self.assertEqual(attach_expected, mock_attach.mock_calls)
        mock_copy.assert_called_with('foo', 'bar', 1024, '1M', sparse=False)
        self.assertEqual(detach_expected, mock_detach.mock_calls)

        #  Test case for sparse_copy_volume = True
        mock_attach.reset_mock()
        mock_detach.reset_mock()
        mock_attach.side_effect = attach_volume_returns
        mock_get_capabilities.return_value = {'sparse_copy_volume': True}
        self.volume._copy_volume_data(self.context,
                                      src_vol,
                                      dest_vol)

        self.assertEqual(attach_expected, mock_attach.mock_calls)
        mock_copy.assert_called_with('foo', 'bar', 1024, '1M', sparse=True)
        self.assertEqual(detach_expected, mock_detach.mock_calls)

        # cleanup resource
        db.volume_destroy(self.context, src_vol['id'])
        db.volume_destroy(self.context, dest_vol['id'])

    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch.object(image_utils, 'fetch_to_raw')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_attach_volume')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_detach_volume')
    @mock.patch.object(cinder.utils, 'brick_attach_volume_encryptor')
    @mock.patch.object(cinder.utils, 'brick_detach_volume_encryptor')
    def test_copy_image_to_encrypted_volume(self,
                                            mock_detach_encryptor,
                                            mock_attach_encryptor,
                                            mock_detach_volume,
                                            mock_attach_volume,
                                            mock_fetch_to_raw,
                                            mock_get_connector_properties):
        properties = {}
        volume = tests_utils.create_volume(
            self.context, status='available',
            size=2,
            encryption_key_id=fake.ENCRYPTION_KEY_ID)
        volume_id = volume['id']
        volume = db.volume_get(context.get_admin_context(), volume_id)
        image_service = fake_image.FakeImageService()
        local_path = 'dev/sda'
        attach_info = {'device': {'path': local_path},
                       'conn': {'driver_volume_type': 'iscsi',
                                'data': {}, }}

        mock_get_connector_properties.return_value = properties
        mock_attach_volume.return_value = [attach_info, volume]

        self.volume.driver.copy_image_to_encrypted_volume(
            self.context, volume, image_service, fake.IMAGE_ID)

        encryption = {'encryption_key_id': fake.ENCRYPTION_KEY_ID}
        mock_attach_volume.assert_called_once_with(
            self.context, volume, properties)
        mock_attach_encryptor.assert_called_once_with(
            self.context, attach_info, encryption)
        mock_fetch_to_raw.assert_called_once_with(
            self.context, image_service, fake.IMAGE_ID,
            local_path, '1M', size=2)
        mock_detach_encryptor.assert_called_once_with(
            attach_info, encryption)
        mock_detach_volume.assert_called_once_with(
            self.context, attach_info, volume, properties)

    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch.object(image_utils, 'fetch_to_raw')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_attach_volume')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_detach_volume')
    @mock.patch.object(cinder.utils, 'brick_attach_volume_encryptor')
    @mock.patch.object(cinder.utils, 'brick_detach_volume_encryptor')
    def test_copy_image_to_encrypted_volume_failed_attach_encryptor(
            self,
            mock_detach_encryptor,
            mock_attach_encryptor,
            mock_detach_volume,
            mock_attach_volume,
            mock_fetch_to_raw,
            mock_get_connector_properties):
        properties = {}
        volume = tests_utils.create_volume(
            self.context, status='available',
            size=2,
            encryption_key_id=fake.ENCRYPTION_KEY_ID)
        volume_id = volume['id']
        volume = db.volume_get(context.get_admin_context(), volume_id)
        image_service = fake_image.FakeImageService()
        attach_info = {'device': {'path': 'dev/sda'},
                       'conn': {'driver_volume_type': 'iscsi',
                                'data': {}, }}

        mock_get_connector_properties.return_value = properties
        mock_attach_volume.return_value = [attach_info, volume]
        raised_exception = os_brick.exception.VolumeEncryptionNotSupported(
            volume_id = "123",
            volume_type = "abc")
        mock_attach_encryptor.side_effect = raised_exception

        self.assertRaises(os_brick.exception.VolumeEncryptionNotSupported,
                          self.volume.driver.copy_image_to_encrypted_volume,
                          self.context, volume, image_service, fake.IMAGE_ID)

        encryption = {'encryption_key_id': fake.ENCRYPTION_KEY_ID}
        mock_attach_volume.assert_called_once_with(
            self.context, volume, properties)
        mock_attach_encryptor.assert_called_once_with(
            self.context, attach_info, encryption)
        self.assertFalse(mock_fetch_to_raw.called)
        self.assertFalse(mock_detach_encryptor.called)
        mock_detach_volume.assert_called_once_with(
            self.context, attach_info, volume, properties)

    @mock.patch.object(os_brick.initiator.connector,
                       'get_connector_properties')
    @mock.patch.object(image_utils, 'fetch_to_raw')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_attach_volume')
    @mock.patch.object(cinder.volume.driver.VolumeDriver, '_detach_volume')
    @mock.patch.object(cinder.utils, 'brick_attach_volume_encryptor')
    @mock.patch.object(cinder.utils, 'brick_detach_volume_encryptor')
    def test_copy_image_to_encrypted_volume_failed_fetch(
            self,
            mock_detach_encryptor, mock_attach_encryptor,
            mock_detach_volume, mock_attach_volume, mock_fetch_to_raw,
            mock_get_connector_properties):
        properties = {}
        volume = tests_utils.create_volume(
            self.context, status='available',
            size=2,
            encryption_key_id=fake.ENCRYPTION_KEY_ID)
        volume_id = volume['id']
        volume = db.volume_get(context.get_admin_context(), volume_id)
        image_service = fake_image.FakeImageService()
        local_path = 'dev/sda'
        attach_info = {'device': {'path': local_path},
                       'conn': {'driver_volume_type': 'iscsi',
                                'data': {}, }}

        mock_get_connector_properties.return_value = properties
        mock_attach_volume.return_value = [attach_info, volume]
        raised_exception = exception.ImageUnacceptable(reason='fake',
                                                       image_id=fake.IMAGE_ID)
        mock_fetch_to_raw.side_effect = raised_exception

        encryption = {'encryption_key_id': fake.ENCRYPTION_KEY_ID}
        self.assertRaises(exception.ImageUnacceptable,
                          self.volume.driver.copy_image_to_encrypted_volume,
                          self.context, volume, image_service, fake.IMAGE_ID)

        mock_attach_volume.assert_called_once_with(
            self.context, volume, properties)
        mock_attach_encryptor.assert_called_once_with(
            self.context, attach_info, encryption)
        mock_fetch_to_raw.assert_called_once_with(
            self.context, image_service, fake.IMAGE_ID,
            local_path, '1M', size=2)
        mock_detach_encryptor.assert_called_once_with(
            attach_info, encryption)
        mock_detach_volume.assert_called_once_with(
            self.context, attach_info, volume, properties)


class FibreChannelTestCase(DriverTestCase):
    """Test Case for FibreChannelDriver."""
    driver_name = "cinder.volume.driver.FibreChannelDriver"

    def test_initialize_connection(self):
        self.assertRaises(NotImplementedError,
                          self.volume.driver.initialize_connection, {}, {})

    def test_validate_connector(self):
        """validate_connector() successful use case.

        validate_connector() does not throw an exception when
        wwpns and wwnns are both set and both are not empty.
        """
        connector = {'wwpns': ["not empty"],
                     'wwnns': ["not empty"]}
        self.volume.driver.validate_connector(connector)

    def test_validate_connector_no_wwpns(self):
        """validate_connector() throws exception when it has no wwpns."""
        connector = {'wwnns': ["not empty"]}
        self.assertRaises(exception.InvalidConnectorException,
                          self.volume.driver.validate_connector, connector)

    def test_validate_connector_empty_wwpns(self):
        """validate_connector() throws exception when it has empty wwpns."""
        connector = {'wwpns': [],
                     'wwnns': ["not empty"]}
        self.assertRaises(exception.InvalidConnectorException,
                          self.volume.driver.validate_connector, connector)

    def test_validate_connector_no_wwnns(self):
        """validate_connector() throws exception when it has no wwnns."""
        connector = {'wwpns': ["not empty"]}
        self.assertRaises(exception.InvalidConnectorException,
                          self.volume.driver.validate_connector, connector)

    def test_validate_connector_empty_wwnns(self):
        """validate_connector() throws exception when it has empty wwnns."""
        connector = {'wwnns': [],
                     'wwpns': ["not empty"]}
        self.assertRaises(exception.InvalidConnectorException,
                          self.volume.driver.validate_connector, connector)


class VolumePolicyTestCase(test.TestCase):

    def setUp(self):
        super(VolumePolicyTestCase, self).setUp()

        cinder.policy.init()

        self.context = context.get_admin_context()

    def test_check_policy(self):
        target = {
            'project_id': self.context.project_id,
            'user_id': self.context.user_id,
        }
        with mock.patch.object(cinder.policy, 'enforce') as mock_enforce:
            cinder.volume.api.check_policy(self.context, 'attach')
            mock_enforce.assert_called_once_with(self.context,
                                                 'volume:attach',
                                                 target)

    def test_check_policy_with_target(self):
        target = {
            'project_id': self.context.project_id,
            'user_id': self.context.user_id,
            'id': 2,
        }
        with mock.patch.object(cinder.policy, 'enforce') as mock_enforce:
            cinder.volume.api.check_policy(self.context, 'attach', {'id': 2})
            mock_enforce.assert_called_once_with(self.context,
                                                 'volume:attach',
                                                 target)


class ImageVolumeCacheTestCase(base.BaseVolumeTestCase):

    def setUp(self):
        super(ImageVolumeCacheTestCase, self).setUp()
        self.volume.driver.set_initialized()

    @mock.patch('oslo_utils.importutils.import_object')
    def test_cache_configs(self, mock_import_object):
        opts = {
            'image_volume_cache_enabled': True,
            'image_volume_cache_max_size_gb': 100,
            'image_volume_cache_max_count': 20
        }

        def conf_get(option):
            if option in opts:
                return opts[option]
            else:
                return None

        mock_driver = mock.Mock()
        mock_driver.configuration.safe_get.side_effect = conf_get
        mock_driver.configuration.extra_capabilities = 'null'

        def import_obj(*args, **kwargs):
            return mock_driver

        mock_import_object.side_effect = import_obj

        manager = vol_manager.VolumeManager(volume_driver=mock_driver)
        self.assertIsNotNone(manager)
        self.assertIsNotNone(manager.image_volume_cache)
        self.assertEqual(100, manager.image_volume_cache.max_cache_size_gb)
        self.assertEqual(20, manager.image_volume_cache.max_cache_size_count)

    def test_delete_image_volume(self):
        volume_params = {
            'status': 'creating',
            'host': 'some_host',
            'cluster_name': 'some_cluster',
            'size': 1
        }
        volume_api = cinder.volume.api.API()
        volume = tests_utils.create_volume(self.context, **volume_params)
        volume.status = 'available'
        volume.save()
        image_id = '70a599e0-31e7-49b7-b260-868f441e862b'
        db.image_volume_cache_create(self.context,
                                     volume['host'],
                                     volume_params['cluster_name'],
                                     image_id,
                                     datetime.datetime.utcnow(),
                                     volume['id'],
                                     volume['size'])
        volume_api.delete(self.context, volume)
        entry = db.image_volume_cache_get_by_volume_id(self.context,
                                                       volume['id'])
        self.assertIsNone(entry)

    def test_delete_volume_with_keymanager_exception(self):
        volume_params = {
            'host': 'some_host',
            'size': 1
        }
        volume_api = cinder.volume.api.API()
        volume = tests_utils.create_volume(self.context, **volume_params)

        with mock.patch.object(
                volume_api.key_manager, 'delete') as key_del_mock:
            key_del_mock.side_effect = Exception("Key not found")
            volume_api.delete(self.context, volume)


@ddt.ddt
class DiscardFlagTestCase(base.BaseVolumeTestCase):

    def setUp(self):
        super(DiscardFlagTestCase, self).setUp()
        self.volume.driver = mock.MagicMock()

    @ddt.data(dict(config_discard_flag=True,
                   driver_discard_flag=None,
                   expected_flag=True),
              dict(config_discard_flag=False,
                   driver_discard_flag=None,
                   expected_flag=None),
              dict(config_discard_flag=True,
                   driver_discard_flag=True,
                   expected_flag=True),
              dict(config_discard_flag=False,
                   driver_discard_flag=True,
                   expected_flag=True),
              dict(config_discard_flag=False,
                   driver_discard_flag=False,
                   expected_flag=False),
              dict(config_discard_flag=None,
                   driver_discard_flag=True,
                   expected_flag=True),
              dict(config_discard_flag=None,
                   driver_discard_flag=False,
                   expected_flag=False))
    @ddt.unpack
    def test_initialize_connection_discard_flag(self,
                                                config_discard_flag,
                                                driver_discard_flag,
                                                expected_flag):
        self.volume.driver.create_export.return_value = None
        connector = {'ip': 'IP', 'initiator': 'INITIATOR'}

        conn_info = {
            'driver_volume_type': 'iscsi',
            'data': {'access_mode': 'rw',
                     'encrypted': False}
        }

        if driver_discard_flag is not None:
            conn_info['data']['discard'] = driver_discard_flag

        self.volume.driver.initialize_connection.return_value = conn_info

        def _safe_get(key):
            if key is 'report_discard_supported':
                return config_discard_flag
            else:
                return None

        self.volume.driver.configuration.safe_get.side_effect = _safe_get

        with mock.patch.object(objects, 'Volume') as mock_vol:
            volume = tests_utils.create_volume(self.context)
            volume.volume_type_id = None
            mock_vol.get_by_id.return_value = volume

            conn_info = self.volume.initialize_connection(self.context,
                                                          volume,
                                                          connector)

        self.assertEqual(expected_flag, conn_info['data'].get('discard'))
