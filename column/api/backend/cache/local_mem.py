# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from collections import deque  # noqa
import copy
import logging
import threading

from column.api.backend.cache import store


# Shared dictionaries for LocalMemoryCache
_stores = {}
_key_queues = {}
_locks = {}

LOG = logging.getLogger(__name__)


class LocalMemoryStore(store.Store):
    """In memory store base class

    This class inherits basic store class to implment a local memory backend.

    Attributes:
        _store (dict): dict for saving info
        _key_queue (dict): dict for keeping the store size below the
            MAX_STORE_SIZE
    """

    def __init__(self, name):
        self._store = _stores.setdefault(name, {})
        self._key_queue = _key_queues.setdefault(name, deque([]))
        lock = _locks.setdefault(name, threading.Lock())
        super(LocalMemoryStore, self).__init__(name, lock)

    def _has_key(self, key):
        return key in self._store

    def _add(self, key, value):
        self._save(key, value)
        self._key_queue.append(key)

    def _del(self, key):
        del self._store[key]

    def _save(self, key, value):
        self._store[key] = value

    def _retrieve(self, key):
        return self._store[key]

    def _is_full(self):
        return len(self._key_queue) >= store.MAX_STORE_SIZE

    def _evict(self):
        del_key = self._key_queue.popleft()
        self._del[del_key]
        return del_key

    def _keys(self):
        return self._store.keys()


class RunMemoryStore(LocalMemoryStore):
    """Column api service in-memory backend interface class

    This class provides a backend interface and additional logic for
    getting and saving run info.
    """

    def _get_progress(self, run):
        progress = run['api_runner'].get_progress()
        return 0 if progress is None else progress

    def _format_response(self, run):
        run_copy = copy.deepcopy(run)
        if 'options' in run_copy:
            if 'become_pass' in run_copy['options']:
                run_copy['options']['become_pass'] = '***'
            if 'conn_pass' in run_copy['options']:
                run_copy['options']['conn_pass'] = '***'
        # Getting progress only happens in playbook running.
        # After run is done, the api_runner attribute would
        # be deleted
        if 'api_runner' in run_copy:
            run_copy['progress'] = self._get_progress(run_copy)
            del run_copy['api_runner']
        return run_copy

    def get_run(self, run_id):
        run = self.get(run_id)
        if run:
            return self._format_response(run)

    def add_run(self, run_id, run):
        if self.add(run_id, run):
            return self._format_response(run)

    def update_run(self, run_id, run):
        if self.get(run_id):
            self.set(run_id, run)
