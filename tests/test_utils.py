# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from mock import patch

from testtools import TestCase

from column import utils


class TestUtils(TestCase):

    def setUp(self):
        super(TestUtils, self).setUp()
        self.vault_password = 'h2RV4pEX2M2TXvLxYhuy'

    @patch('__builtin__.reload')
    def test_reload_log_path(self, mock_reload):
        utils.reload_log_path('log_path')
        self.assertTrue(mock_reload.called)

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    def test_vault_decrypt(self, mock_read_vault_password, mock_reload):
        encrypted_value = (
            '$ANSIBLE_VAULT;1.1;AES256\n'
            '3139663233656537383737613633343638313934'
            '3033363766663532326434386435376639316434\n'
            '3930306333303835316564373530656365376561'
            '356466330a383238373762656238336432373261\n'
            '6230306330646332393932316536323235323561'
            '3038386232636331363931373538626461396364\n'
            '6338336334343366650a35363165316661666236'
            '3637636234666230333764323361643866643863\n'
            '3933\n'
        )
        mock_read_vault_password.return_value = self.vault_password
        self.assertEqual('vmware', utils.vault_decrypt(encrypted_value))
        self.assertTrue(mock_read_vault_password.called)

    @patch('__builtin__.reload')
    @patch('ansible.cli.CLI.read_vault_password_file')
    def test_vault_encrypt(self, mock_read_vault_password, mock_reload):
        mock_read_vault_password.return_value = self.vault_password
        encrypted = utils.vault_encrypt('vmware')
        self.assertTrue(encrypted.startswith('$ANSIBLE_VAULT;1.1;AES256'))
        self.assertTrue(mock_read_vault_password.called)
