# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause


import logging
import os

from ansible import constants as a_const
from ansible.executor import playbook_executor as pb_exec
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible import inventory
from ansible.parsing import dataloader
from ansible.parsing.splitter import parse_kv
from ansible.playbook.play import Play
from ansible.utils.vars import load_extra_vars
from ansible.vars import VariableManager

from column import callback
from column import exceptions
from column import runner


LOG = logging.getLogger(__name__)


class Namespace(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class ErrorsCallback(callback.AnsibleCallback):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.failed_results = []

    def run_on_runner_failed(self, result, ignore_errors=False):
        if ignore_errors:
            #  We only collect not ignored errors
            return
        self.failed_results.append(result)


class APIRunner(runner.Runner):

    def __init__(self, inventory_file=None, **kwargs):
        super(self.__class__, self).__init__(inventory_file, **kwargs)
        self._callbacks = []

    def run_playbook(self, playbook_file, inventory_file=None, **kwargs):
        if inventory_file is None:
            inventory_file = self.inventory_file

        LOG.debug('Running with inventory file: %s', inventory_file)
        LOG.debug('Running with playbook file: %s', playbook_file)

        conn_pass = None
        if 'conn_pass' in kwargs:
            conn_pass = kwargs['conn_pass']

        become_pass = None
        if 'become_pass' in kwargs:
            become_pass = kwargs['become_pass']

        passwords = {'conn_pass': conn_pass, 'become_pass': become_pass}

        playbooks = [playbook_file]

        options = self._build_opt_dict(inventory_file, **kwargs)

        variable_manager = VariableManager()
        loader = dataloader.DataLoader()
        variable_manager.extra_vars = options.extra_vars

        ansible_inv = inventory.Inventory(loader=loader,
                                          variable_manager=variable_manager,
                                          host_list=options.inventory)
        ansible_inv.set_playbook_basedir(os.path.dirname(playbook_file))
        variable_manager.set_inventory(ansible_inv)
        ansible_inv.subset(options.subset)

        pbex = pb_exec.PlaybookExecutor(playbooks=playbooks,
                                        inventory=ansible_inv,
                                        variable_manager=variable_manager,
                                        loader=loader,
                                        options=options,
                                        passwords=passwords)

        errors_callback = ErrorsCallback()
        self.add_callback(errors_callback)
        # There is no public API for adding callbacks, hence we use private
        # property to add callbacks
        pbex._tqm._callback_plugins.extend(self._callbacks)

        status = pbex.run()
        stats = pbex._tqm._stats
        failed_results = errors_callback.failed_results
        result = self._process_stats(stats, failed_results)
        return result

    def run_module(self, module_name='ping', module_args=None, hosts="all",
                   inventory_file=None, **kwargs):

        if not module_args:
            check_raw = module_name in ('command', 'win_command', 'shell',
                                        'win_shell', 'script', 'raw')
            module_args = parse_kv(a_const.DEFAULT_MODULE_ARGS, check_raw)

        conn_pass = None
        if 'conn_pass' in kwargs:
            conn_pass = kwargs['conn_pass']

        become_pass = None
        if 'become_pass' in kwargs:
            become_pass = kwargs['become_pass']

        passwords = {'conn_pass': conn_pass, 'become_pass': become_pass}

        options = self._build_opt_dict(inventory_file, **kwargs)

        variable_manager = VariableManager()
        loader = dataloader.DataLoader()
        variable_manager.extra_vars = options.extra_vars

        ansible_inv = inventory.Inventory(loader=loader,
                                          variable_manager=variable_manager,
                                          host_list=options.inventory)
        variable_manager.set_inventory(ansible_inv)
        ansible_inv.subset(options.subset)

        play_ds = self._play_ds(hosts, module_name, module_args)
        play = Play().load(play_ds, variable_manager=variable_manager,
                           loader=loader)

        try:
            tqm = TaskQueueManager(
                inventory=ansible_inv,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback='minimal',
                run_additional_callbacks=True
            )

            # There is no public API for adding callbacks, hence we use private
            # property to add callbacks
            tqm._callback_plugins.extend(self._callbacks)

            result = tqm.run(play)
        finally:
            if tqm:
                tqm.cleanup()
            if loader:
                loader.cleanup_all_tmp_files()

        stats = tqm._stats
        result = self._process_stats(stats)
        return result

    def add_callback(self, callback):
        self._callbacks.append(callback)

    def _build_opt_dict(self, inventory_file, **kwargs):
        args = {
            'check': None, 'listtasks': None, 'listhosts': None,
            'listtags': None, 'syntax': None, 'module_path': None,
            'skip_tags': [], 'ssh_common_args': '',
            'sftp_extra_args': '', 'scp_extra_args': '',
            'ssh_extra_args': '', 'become': a_const.DEFAULT_BECOME,
            'become_user': a_const.DEFAULT_BECOME_USER,
            'become_ask_pass': a_const.DEFAULT_BECOME_ASK_PASS,
            'become_method': a_const.DEFAULT_BECOME_METHOD,
            'forks': a_const.DEFAULT_FORKS,
            'inventory': inventory_file,
            'private_key_file': a_const.DEFAULT_PRIVATE_KEY_FILE,
            'extra_vars': {}, 'subset': a_const.DEFAULT_SUBSET,
            'tags': [], 'verbosity': 0,
            'connection': a_const.DEFAULT_TRANSPORT,
            'timeout': a_const.DEFAULT_TIMEOUT
        }
        args.update(self.custom_opts)
        args.update(kwargs)
        # In ansible 2.2, tags can be a string or a list, but only a list
        # is supported in 2.3.
        if isinstance(args['tags'], str):
            args['tags'] = args['tags'].split(',')
        elif not isinstance(args['tags'], list):
            raise exceptions.InvalidParameter(name=type(args['tags']).__name__,
                                              param='tag')
        return Namespace(**args)

    def _play_ds(self, hosts, module_name, module_args):
        return dict(
            name="Ansible module runner",
            hosts=hosts,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args),
                        async=0,
                        poll=a_const.DEFAULT_POLL_INTERVAL)]
        )

    @staticmethod
    def _process_stats(stats, failed_results=[]):
        unreachable_hosts = sorted(stats.dark.keys())
        failed_hosts = sorted(stats.failures.keys())
        error_msg = ''
        failed_tasks = []
        if len(unreachable_hosts) > 0:
            tmpl = "Following nodes were unreachable: {0}\n"
            error_msg += tmpl.format(unreachable_hosts)
        for result in failed_results:
            task_name, msg, host = APIRunner._process_task_result(result)
            failed_tasks.append(task_name)
            tmpl = 'Task "{0}" failed on host "{1}" with message: {2}'
            error_msg += tmpl.format(task_name, host, msg)

        return {"error_msg": error_msg, "unreachable_hosts": unreachable_hosts,
                "failed_hosts": failed_hosts, 'failed_tasks': failed_tasks}

    @staticmethod
    def _process_task_result(task):
        result = task._result
        task_obj = task._task
        host = task._host
        if isinstance(result, dict) and 'msg' in result:
            error_msg = result.get('msg')
        else:
            # task result may be an object with multiple results
            msgs = []
            for res in result.get('results', []):
                if isinstance(res, dict) and 'msg' in res:
                    msgs.append(res.get('result'))
            error_msg = ' '.join(msgs)

        return task_obj.get_name(), error_msg, host.get_name()
