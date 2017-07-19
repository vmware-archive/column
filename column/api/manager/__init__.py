# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from column.api.manager import credential_manager
from column.api.manager import run_manager

_managers = {
    'run': run_manager.RunManager(),
    'credential': credential_manager.CredentialManager()
}


def get_manager(manager_type):
    if manager_type in _managers:
        return _managers[manager_type]
    raise NotImplementedError()
