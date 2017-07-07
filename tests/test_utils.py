# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import mock
from mock import patch

from ansible import constants
from testtools import TestCase

from column import utils


class TestUtils(TestCase):

    def setUp(self):
        super(TestUtils, self).setUp()

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    @patch('ansible.parsing.vault.VaultLib')
    @patch('ansible.parsing.vault.VaultLib.decrypt')
    @patch('__builtin__.open', mock.mock_open(), create=True)
    def test_get_vault_secret(self, mock_decrypt, mock_vaultlib,
                              mock_read_vault_password_file, mock_reload):
        mock_read_vault_password_file.return_value = 'my_vault_password'
        utils.get_vault_secret('/var/lib/column', 'admin_password')
        self.assertTrue(mock_read_vault_password_file.called)
        mock_vaultlib.assert_called_with('my_vault_password')

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    @patch('ansible.parsing.vault.VaultLib')
    @patch('ansible.parsing.vault.VaultLib.encrypt')
    @patch('__builtin__.open', mock.mock_open(), create=True)
    @patch('os.chmod')
    def test_update_vault_secret(self, mock_chmod, mock_encrypt, mock_vaultlib,
                                 mock_read_vault_password_file, mock_reload):
        mock_read_vault_password_file.return_value = 'my_vault_password'
        utils.update_vault_secret('admin_password', 'pass', '/var/lib/column')
        self.assertTrue(mock_read_vault_password_file.called)
        mock_vaultlib.assert_called_with('my_vault_password')
        self.assertTrue(mock_chmod.called)
