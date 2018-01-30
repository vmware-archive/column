# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Runner(object):

    def __init__(self, inventory_file=None, **kwargs):
        self.inventory_file = inventory_file
        self.custom_opts = kwargs or {}

    @abc.abstractmethod
    def run_playbook(self, playbook_file, inventory_file=None, **kwargs):
        """Runs playbook specified in playbook_file, with inventory from
            inventory_file, as a remote_user. All other ansible parameters
            are passed using kwargs. see ansible-playbook --help or
            lib/ansible/constants.py in ansible source code for details
            on what parameters can be specified.


        :param playbook_file: str: absolute path to playbook file
        :param inventory_file: str: absolute path to inventory file
        :param kwargs: dict: Dictionary for optional parameters
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def run_module(self, module_name='ping', module_args=None, hosts='all',
                   inventory_file=None, **kwargs):
        """Runs ansible module on hosts as remote_user, with optional
            inventory_file, module_name, and module_args
            All other ansible parameters
            are passed using kwargs. see ansible --help or
            lib/ansible/constants.py in ansible source code for details
            on what parameters can be specified.


        :param module_name: str: ansible module to execute
        :param module_args: str: ansible module arguments
        :param hosts: str: hosts filter, all by default
        :param inventory_file: str: absolute path to inventory file
        :param kwargs: dict: Dictionary for optional parameters
        """
        raise NotImplementedError()
