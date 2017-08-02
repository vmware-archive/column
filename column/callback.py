# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import logging

from ansible.plugins import callback


LOG = logging.getLogger(__name__)


# This is a base class that implements ansible 2.x callbacks. It should NOT
# be used outside. Use AnsibleCallback and implement methods declared there.
class AnsibleCallbackBase(callback.CallbackBase):

    def __init__(self, *args, **kwargs):
        super(AnsibleCallbackBase, self).__init__(*args, **kwargs)

    def v2_on_any(self, *args, **kwargs):
        super(AnsibleCallbackBase, self).v2_on_any(*args, **kwargs)
        self.run_on_any(*args, **kwargs)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        super(AnsibleCallbackBase, self).v2_runner_on_failed(result,
                                                             ignore_errors)
        self.run_on_runner_failed(result, ignore_errors)

    def v2_runner_on_ok(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_ok(result)
        self.run_on_runner_ok(result)

    def v2_runner_on_skipped(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_skipped(result)
        self.run_on_runner_skipped(result)

    def v2_runner_on_unreachable(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_unreachable(result)
        self.run_on_runner_unreachable(result)

    def v2_runner_on_no_hosts(self, task):
        super(AnsibleCallbackBase, self).v2_runner_on_no_hosts(task)
        self.run_on_runner_no_hosts(task)

    def v2_runner_on_async_poll(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_async_poll(result)
        self.run_on_runner_async_poll(result)

    def v2_runner_on_async_ok(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_async_ok(result)
        self.run_on_runner_async_ok(result)

    def v2_runner_on_async_failed(self, result):
        super(AnsibleCallbackBase, self).v2_runner_on_async_failed(result)
        self.run_on_runner_async_failed(result)

    def v2_runner_on_file_diff(self, result, diff):
        super(AnsibleCallbackBase, self).v2_runner_on_file_diff(result, diff)
        self.run_on_runner_file_diff(result, diff)

    def v2_playbook_on_start(self, playbook):
        super(AnsibleCallbackBase, self).v2_playbook_on_start(playbook)
        self.run_on_playbook_start(playbook)

    def v2_playbook_on_notify(self, result, handler):
        super(AnsibleCallbackBase, self).v2_playbook_on_notify(result, handler)
        self.run_on_playbook_notify(result, handler)

    def v2_playbook_on_no_hosts_matched(self):
        super(AnsibleCallbackBase, self).v2_playbook_on_no_hosts_matched()
        self.run_on_playbook_no_hosts_matched()

    def v2_playbook_on_no_hosts_remaining(self):
        super(AnsibleCallbackBase, self).v2_playbook_on_no_hosts_remaining()
        self.run_on_playbook_no_hosts_remaining()

    def v2_playbook_on_task_start(self, task, is_conditional):
        super(AnsibleCallbackBase, self).v2_playbook_on_task_start(
            task, is_conditional
            )
        self.run_on_playbook_task_start(task, is_conditional)

    def v2_playbook_on_cleanup_task_start(self, task):
        super(AnsibleCallbackBase, self).v2_playbook_on_cleanup_task_start(
            task
            )
        self.run_on_playbook_cleanup_task_start(task)

    def v2_playbook_on_handler_task_start(self, task):
        super(AnsibleCallbackBase, self).v2_playbook_on_handler_task_start(
            task
            )
        self.run_on_playbook_handler_task_start(task)

    def v2_playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                   encrypt=None, confirm=False, salt_size=None,
                                   salt=None, default=None):
        super(AnsibleCallbackBase, self).v2_playbook_on_vars_prompt(
            varname, private, prompt, encrypt, confirm, salt_size, salt,
            default
            )
        self.run_on_playbook_vars_prompt(varname, private, prompt, encrypt,
                                         confirm, salt_size, salt, default)

    def v2_playbook_on_setup(self):
        super(AnsibleCallbackBase, self).v2_playbook_on_setup()
        self.run_on_playbook_setup()

    def v2_playbook_on_import_for_host(self, result, imported_file):
        super(AnsibleCallbackBase, self).v2_playbook_on_import_for_host(
            result, imported_file
            )
        self.run_on_playbook_import_for_host(result, imported_file)

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        super(AnsibleCallbackBase, self).v2_playbook_on_not_import_for_host(
            result, missing_file
            )
        self.run_on_playbook_not_import_for_host(result, missing_file)

    def v2_playbook_on_play_start(self, play):
        super(AnsibleCallbackBase, self).v2_playbook_on_play_start(play)
        self.run_on_playbook_play_start(play)

    def v2_playbook_on_stats(self, stats):
        super(AnsibleCallbackBase, self).v2_playbook_on_stats(stats)
        self.run_on_playbook_stats(stats)

    def v2_on_file_diff(self, result):
        super(AnsibleCallbackBase, self).v2_on_file_diff(result)
        self.run_on_file_diff(result)

    def v2_playbook_on_include(self, included_file):
        super(AnsibleCallbackBase, self).v2_playbook_on_include(included_file)
        self.run_on_playbook_include(included_file)

    def v2_runner_item_on_ok(self, result):
        super(AnsibleCallbackBase, self).v2_runner_item_on_ok(result)
        self.run_on_runner_item_ok(result)

    def v2_runner_item_on_failed(self, result):
        super(AnsibleCallbackBase, self).v2_runner_item_on_failed(result)
        self.run_on_runner_item_failed(result)

    def v2_runner_item_on_skipped(self, result):
        super(AnsibleCallbackBase, self).v2_runner_item_on_skipped(result)
        self.run_on_runner_item_skipped(result)

    def v2_runner_retry(self, result):
        super(AnsibleCallbackBase, self).v2_runner_retry(result)
        self.run_on_runner_retry(result)


# Interface class that wraps ansible callback class to make future upgrades
# easier. Derive from this class and implement any subset of methods defined
# here. See examples/callbacks for examples how to use it.
class AnsibleCallback(AnsibleCallbackBase):

    def __init__(self, *args, **kwargs):
        super(AnsibleCallback, self).__init__(*args, **kwargs)

    def run_on_any(self, *args, **kwargs):
        pass

    def run_on_runner_failed(self, result, ignore_errors=False):
        pass

    def run_on_runner_ok(self, result):
        pass

    def run_on_runner_skipped(self, result):
        pass

    def run_on_runner_unreachable(self, result):
        pass

    def run_on_runner_no_hosts(self, result):
        pass

    def run_on_runner_async_poll(self, result):
        pass

    def run_on_runner_async_ok(self, result):
        pass

    def run_on_runner_async_failed(self, result):
        pass

    def run_on_runner_file_diff(self, result, diff):
        pass

    def run_on_playbook_start(self, playbook):
        pass

    def run_on_playbook_notify(self, result, handler):
        pass

    def run_on_playbook_no_hosts_matched(self):
        pass

    def run_on_playbook_no_hosts_remaining(self):
        pass

    def run_on_playbook_task_start(self, task, is_conditional):
        pass

    def run_on_playbook_cleanup_task_start(self, task):
        pass

    def run_on_playbook_handler_task_start(self, task):
        pass

    def run_on_playbook_vars_prompt(self, varname, private=True, prompt=None,
                                    encrypt=None, confirm=False,
                                    salt_size=None, salt=None, default=None):
        pass

    def run_on_playbook_setup(self):
        pass

    def run_on_playbook_import_for_host(self, result, imported_file):
        pass

    def run_on_playbook_not_import_for_host(self, result, missing_file):
        pass

    def run_on_playbook_play_start(self, play):
        pass

    def run_on_playbook_stats(self, stats):
        pass

    def run_on_file_diff(self, result):
        pass

    def run_on_playbook_include(self, included_file):
        pass

    def run_on_runner_item_ok(self, result):
        pass

    def run_on_runner_item_failed(self, result):
        pass

    def run_on_runner_item_skipped(self, result):
        pass

    def run_on_runner_retry(self, result):
        pass
