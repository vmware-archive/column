# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

from testtools import TestCase

from column import APIRunner


class TestAPIRunner(TestCase):

    def setUp(self):
        super(TestAPIRunner, self).setUp()

    def test_run_module_on_localhost(self):
        api_runner = APIRunner()
        api_runner.run_module('localhost', remote_user=None)

    def test_run_playbook_on_localhost(self):
        api_runner = APIRunner()
        pb_path = './tests/fixtures/playbooks/hello_world.yml'
        result = api_runner.run_playbook(pb_path, 'localhost,',
                                         remote_user=None, connection='local')
        self.assertEqual('', result['error_msg'])
        self.assertEqual(0, len(result['unreachable_hosts']))
        self.assertEqual(0, len(result['failed_hosts']))

    def test_run_playbook_with_fail(self):
        api_runner = APIRunner()
        pb_path = './tests/fixtures/playbooks/hello_world_with_fail.yml'
        result = api_runner.run_playbook(pb_path, 'localhost,',
                                         remote_user=None, connection='local')
        self.assertIsNot('', result['error_msg'])
        self.assertEqual(0, len(result['unreachable_hosts']))
        self.assertEqual(1, len(result['failed_hosts']))
        self.assertEqual(1, len(result['failed_tasks']))
        self.assertEqual('This task will fail', result['failed_tasks'][0])
