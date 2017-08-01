# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import ConfigParser
import os

from column.api_runner import APIRunner
from column.callback import AnsibleCallback
from column.runner import Runner
from column.subprocess_runner import SubprocessRunner


DEFAULT_CONF_FILE = os.path.join(os.sep, 'etc', 'column', 'column.conf')

__all__ = [
    'APIRunner', 'Runner', 'SubprocessRunner', 'AnsibleCallback'
]


__version__ = '0.4.9'

defaults = {
    'log_file': os.path.join(os.sep, 'var', 'log', 'column.log'),
    'log_level': 'DEBUG',
    'server': '127.0.0.1',
    'port': '48620'
}

cfg = ConfigParser.ConfigParser(defaults)
cfg.read(DEFAULT_CONF_FILE)
