# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause


import os

from ansible import cli
from ansible import constants
from ansible.parsing import dataloader
from ansible.parsing import vault
from ansible.utils import display


def reload_log_path(log_path):
    os.environ['ANSIBLE_LOG_PATH'] = log_path
    reload(constants)
    reload(display)


def vault_decrypt(value):
    reload(constants)
    vault_password = cli.CLI.read_vault_password_file(
        constants.DEFAULT_VAULT_PASSWORD_FILE, dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    return this_vault.decrypt(value)


def vault_encrypt(value):
    reload(constants)
    vault_password = cli.CLI.read_vault_password_file(
        constants.DEFAULT_VAULT_PASSWORD_FILE, dataloader.DataLoader())
    this_vault = vault.VaultLib(vault_password)
    return this_vault.encrypt(value)
