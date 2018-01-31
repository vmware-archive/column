# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import os

from ansible import cli
from ansible import errors
from ansible.parsing import dataloader
from ansible.parsing import vault
from six.moves import configparser


ANSIBLE_CFG = os.path.join(os.sep, 'etc', 'ansible', 'ansible.cfg')
VAULT_PWD_FILE = os.path.join(os.sep, 'etc', 'column', 'vault_pass.txt')
DEFAULTS = {
    'vault_password_file': VAULT_PWD_FILE
}


def _get_vault_password_file():
    if os.path.exists(ANSIBLE_CFG):
        cfg = configparser.ConfigParser(DEFAULTS)
        cfg.read(ANSIBLE_CFG)
        return cfg.get('defaults', 'vault_password_file')


def vault_decrypt(value):
    vault_password = cli.CLI.read_vault_password_file(
        _get_vault_password_file(), dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    try:
        return this_vault.decrypt(value)
    except errors.AnsibleError:
        return None


def vault_encrypt(value):
    vault_password = cli.CLI.read_vault_password_file(
        _get_vault_password_file(), dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    return this_vault.encrypt(value)
