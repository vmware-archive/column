# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import copy
import logging
import threading
import time

from ansible.playbook import play_context

import column
from column import api
from column.api import backend
from column.api.model import run_model
from column.api import objects
from column import exceptions
from column.plugins.callback import progress


LOG = logging.getLogger(__name__)


class RunManager(object):
    """Column api manager class

    The Manager layer is to support additional logic which is needed
    to run ansible playbook.

    Attributes:
        column_manager (obj): column library interface for running ansible
            playbook
    """

    def __init__(self):
        self.column_manager = column.APIRunner()
        self.backend_store = backend.get_store()

    def _build_opts(self, opts):
        column_opts = copy.deepcopy(opts)
        # state attribute is not useful to column runner
        if 'state' in column_opts:
            del column_opts['state']
        # state attribute is not useful to column runner
        if 'id' in column_opts:
            del column_opts['id']
        # api_runner is not useful to column runner
        if 'api_runner' in column_opts:
            del column_opts['api_runner']
        return column_opts

    def _parse_result(self, run_id, result):
        unreachable_hosts = result['unreachable_hosts']
        failed_hosts = result['failed_hosts']
        run = self.backend_store.get_run(run_id)
        if unreachable_hosts:
            error_msg = ("{} failed because the following nodes were "
                         "unreachable: {}.\n".format(run['playbook_path'],
                                                     unreachable_hosts))
            run['state'] = objects.State.ERROR
            run['message'] = error_msg
            self.backend_store.update_run(run_id, run)

        elif failed_hosts:
            error_msg = ("{} failed on the following nodes: {}"
                         .format(run['playbook_path'], failed_hosts))
            run['state'] = objects.State.ERROR
            run['message'] = error_msg
            self.backend_store.update_run(run_id, run)

        else:
            run['state'] = objects.State.COMPLETED
            self.backend_store.update_run(run_id, run)

    def _run_playbook(self, run):
        play_context.PlayContext._attributes = copy.deepcopy(
                api.context_attributes)
        column_opts = self._build_opts(run)
        progress_callback = progress.AnsibleTrackProgress()
        self.column_manager.add_callback(progress_callback)
        inventory_file = column_opts.get('inventory_file', None)
        options = column_opts.get('options', {})
        try:
            result = self.column_manager.run_playbook(
                column_opts['playbook_path'],
                inventory_file,
                **options)
            self._parse_result(run['id'], result)
        except exceptions.FileNotFound as e:
            run = self.backend_store.get_run(run['id'])
            run['state'] = objects.State.ERROR
            run['message'] = e.message
            self.backend_store.update_run(run['id'], run)

    def create_run(self, run):
        run['state'] = objects.State.RUNNING
        run['api_runner'] = self.column_manager
        self.backend_store.create_run(run['id'], run)
        LOG.debug('Triggering a new run with %s',
                run_model.format_response(run))
        t = threading.Thread(target=self._run_playbook, args=[run])
        t.start()
        return run

    def delete_run(self, run):
        timeout = 10
        if (run['state'] == objects.State.COMPLETED or
                run['state'] == objects.State.ERROR or
                run['state'] == objects.State.ABORTED):
            return True
        for i in xrange(timeout):
            if run['api_runner'].tqm:
                run['api_runner'].tqm.terminate()
                run['state'] = objects.State.ABORTED
                run['message'] = "Run Aborted"
                self.backend_store.update_run(run['id'], run)
                return True
            time.sleep(1)
        return False
