# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import json

from mock import patch
from six.moves import http_client

from tests.api import controllers


class TestCredential(controllers.APITest):

    def test_bad_payload(self):
        response = self.app.get('/credentials')
        self.assertEqual(http_client.BAD_REQUEST, response.status_code)
        response = self.app.put('/credentials',
                                data=json.dumps(dict(bad_payload='test',)),
                                content_type='application/json')
        self.assertEqual(http_client.BAD_REQUEST, response.status_code)

    @patch('column.utils.vault_decrypt')
    def test_get_credential(self, mock_vault_decrypt):
        mock_vault_decrypt.return_value = 'TestPassword'
        response = self.app.get('/credentials?value=test')
        self.assertTrue(mock_vault_decrypt.called)
        mock_vault_decrypt.assert_called_with('test')
        self.assertEqual(http_client.OK, response.status_code)

    @patch('column.utils.vault_encrypt')
    def test_update_credential(self, mock_vault_encrypt):
        mock_vault_encrypt.return_value = "test"
        value = 'TestPassword'
        response = self.app.put('/credentials',
                                data=json.dumps(dict(value=value,)),
                                content_type='application/json')
        res_data = json.loads(response.data)
        self.assertTrue(mock_vault_encrypt.called)
        mock_vault_encrypt.assert_called_with(value)
        self.assertEqual(http_client.OK, response.status_code)
        self.assertEqual(mock_vault_encrypt.return_value, res_data)
