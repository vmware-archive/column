# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause


from column.api_runner import APIRunner
from column.callback import AnsibleCallback
from column.runner import Runner
from column.subprocess_runner import SubprocessRunner

import ConfigParser

DEFAULT_CONF_FILE = '/etc/column/column.conf'

__all__ = [
    'APIRunner', 'Runner', 'SubprocessRunner', 'AnsibleCallback'
]


__version__ = '0.3.6'

cfg = ConfigParser.ConfigParser(allow_no_value=True)
cfg.read(DEFAULT_CONF_FILE)
