# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import os

from ansible.parsing import vault
from ansible import release
from six.moves import configparser


ANSIBLE_CFG = os.path.join(os.sep, 'etc', 'ansible', 'ansible.cfg')
VAULT_PWD_FILE = os.path.join(os.sep, 'etc', 'column', 'vault_pass.txt')
DEFAULTS = {
    'vault_password_file': VAULT_PWD_FILE
}


def _read_vault_password_file():
    if os.path.exists(ANSIBLE_CFG):
        cfg = configparser.ConfigParser(DEFAULTS)
        cfg.read(ANSIBLE_CFG)
        password_file = cfg.get('defaults', 'vault_password_file')

        with open(password_file, "rb") as f:
            return f.read().strip()


def vault_decrypt(value):
    this_vault = vault.VaultLib(_read_vault_password_file())
    return this_vault.decrypt(value)


def vault_encrypt(value):
    this_vault = vault.VaultLib(_read_vault_password_file())
    return this_vault.encrypt(value)


def ansible_version():
    return release.__version__
