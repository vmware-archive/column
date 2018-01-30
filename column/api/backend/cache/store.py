# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import logging

LOG = logging.getLogger(__name__)

MAX_STORE_SIZE = 50


class Store(object):
    """Backend store base class

    This is a basic store implementation which is thread safe. Local memory
    store should inherit from this class.

    Attributes:
        name (str): store name
        lock (dict): dict of locks for multi-threaded read and write operations
    """

    def __init__(self, name, lock):
        self.name = name
        self.lock = lock

    def add(self, key, value):
        with self.lock:
            if not self._has_key(key):
                if self._is_full():
                    del_key = self._evict()
                    LOG.debug("Deleted key %s from store %s", del_key,
                              self.name)
                self._add(key, value)
                LOG.debug("Added key %s to store %s", key, self.name)
                return True
            return False

    def delete(self, key):
        with self.lock:
            if self._has_key(key):
                self._del(key)
                LOG.debug("Deleted key %s from store %s", key, self.name)
                return True
            return False

    def get(self, key):
        with self.lock:
            if self._has_key(key):
                LOG.debug("Got key %s from store %s", key, self.name)
                return self._retrieve(key)

    def keys(self):
        with self.lock:
            return self._keys()

    def set(self, key, value):
        with self.lock:
            if self._has_key(key):
                self._save(key, value)
                LOG.debug("Updated key %s from store %s", key, self.name)
                return True
            return False

    def contains(self, key):
        with self.lock:
            return self._has_key(key)

    def _add(self, key, value):
        pass

    def _del(self, key):
        pass

    def _save(self, key, value):
        pass

    def _retrieve(self, key):
        pass

    def _has_key(self, key):
        pass

    def _is_full(self):
        pass

    def _evict(self):
        pass

    def _keys(self):
        pass
