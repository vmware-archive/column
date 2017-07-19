# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from column.api.backend.cache import local_mem


class LocalMemoryCache(object):

    def __init__(self):
        self.runs_store = local_mem.RunMemoryStore('runs')

    def get_run(self, run_id):
        run = self.runs_store.get_run(run_id)
        return run

    def create_run(self, run_id, run):
        return self.runs_store.add_run(run_id, run)

    def update_run(self, run_id, run):
        return self.runs_store.update_run(run_id, run)

    def list_runs(self):
        run_ids = self.runs_store.keys()
        return [self.get_run(run_id) for run_id in run_ids]
