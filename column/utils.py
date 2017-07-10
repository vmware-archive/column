# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause


import logging
import os
import stat

from ansible import cli
from ansible import constants
from ansible.parsing import dataloader
from ansible.parsing import vault
from ansible.utils import display


LOG = logging.getLogger(__name__)


def reload_log_path(log_path):
    os.environ['ANSIBLE_LOG_PATH'] = log_path
    reload(constants)
    reload(display)


def get_vault_secret(secret_file):
    reload(constants)
    vault_password = cli.CLI.read_vault_password_file(
        constants.DEFAULT_VAULT_PASSWORD_FILE, dataloader.DataLoader())

    this_vault = vault.VaultLib(vault_password)

    with open(secret_file) as f:
        return this_vault.decrypt(f.read())


def update_vault_secret(secret_file, value):
    reload(constants)
    vault_password = cli.CLI.read_vault_password_file(
        constants.DEFAULT_VAULT_PASSWORD_FILE, dataloader.DataLoader())

    if vault_password:
        this_vault = vault.VaultLib(vault_password)
        enc_data = this_vault.encrypt(value)

        with open(secret_file, 'wb') as f:
            os.chmod(secret_file, stat.S_IRUSR | stat.S_IWUSR)
            f.write(enc_data)
    else:
        LOG.debug('No vault_password found')
