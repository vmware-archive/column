# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json
import time

from six.moves import http_client

from tests.api import controllers


class TestRun(controllers.APITest):

    def _wait_for_run_complete(self, id):
        counter = 0
        while counter < self.counter:
            res = self.app.get('/runs/{}'.format(id))
            res_dict = json.loads(res.data)
            if res_dict['state'] != 'RUNNING':
                break
            time.sleep(self.wait_interval)
            counter += 1

        self.assertNotEqual('RUNNING', res_dict['state'])

    def test_bad_payload(self):
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(inventory_file='localhost,',
                                 options={'connection': 'local'})),
            content_type='application/json')
        self.assertEqual(http_client.BAD_REQUEST, response.status_code)

        pb = 'tests/fixtures/playbooks/hello_world_with_fail.yml'
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(playbook_path=pb,
                                 inventory_file='localhost,',
                                 options={'connection': 'local',
                                          'bad_option': 'bad'})),
            content_type='application/json')
        self.assertEqual(http_client.BAD_REQUEST, response.status_code)

    def test_failed_run(self):
        pb = 'tests/fixtures/playbooks/hello_world_with_fail.yml'
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(playbook_path=pb,
                                 inventory_file='localhost,',
                                 options={'connection': 'local'})),
            content_type='application/json')
        res_dict = json.loads(response.data)
        self._wait_for_run_complete(res_dict['id'])
        response = self.app.get('/runs/{}'.format(res_dict['id']))
        res_dict = json.loads(response.data)
        self.assertEqual('ERROR', res_dict['state'])

    def test_get_run_by_id(self):
        response = self.app.get('/runs/1234')
        self.assertEqual(http_client.NOT_FOUND, response.status_code)

        pb = 'tests/fixtures/playbooks/hello_world.yml'
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(playbook_path=pb,
                                 inventory_file='localhosti,',
                                 options={'connection': 'local'})),
            content_type='application/json')
        res_dict = json.loads(response.data)
        run_id = res_dict['id']
        self.assertEqual(http_client.OK, response.status_code)
        response = self.app.get('/runs/{}'.format(run_id))
        self.assertEqual(http_client.OK, response.status_code)
        self._wait_for_run_complete(run_id)

    def test_get_run_list(self):
        pb = 'tests/fixtures/playbooks/hello_world.yml'
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(playbook_path=pb,
                                 inventory_file='localhost,',
                                 options={'connection': 'local'})),
            content_type='application/json')
        res_dict = json.loads(response.data)
        run_id = res_dict['id']
        self.assertEqual(http_client.OK, response.status_code)
        response = self.app.get('/runs')
        res_list = json.loads(response.data)
        found = False
        for item in res_list:
            if item['id'] == run_id:
                found = True
                break
        self.assertEqual(True, found)
        self._wait_for_run_complete(run_id)

    def test_trigger_run(self):
        pb = 'tests/fixtures/playbooks/hello_world.yml'
        response = self.app.post(
            '/runs',
            data=json.dumps(dict(playbook_path=pb,
                                 inventory_file='localhost,',
                                 options={'connection': 'local'})),
            content_type='application/json')
        res_dict = json.loads(response.data)
        self.assertEqual(http_client.OK, response.status_code)
        self.assertEqual('RUNNING', res_dict['state'])
        self._wait_for_run_complete(res_dict['id'])
        response = self.app.get('/runs/{}'.format(res_dict['id']))
        res_dict = json.loads(response.data)
        self.assertEqual('COMPLETED', res_dict['state'])
