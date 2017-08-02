# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import testtools

from column.api.run import application


class APITest(testtools.TestCase):

    def setUp(self):
        super(APITest, self).setUp()
        application.config['SERVER_NAME'] = '127.0.0.1:48620'
        self.pb_running_time = 60
        self.wait_interval = 5
        self.counter = self.pb_running_time / self.wait_interval
        self.app = application.test_client()
