# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

from column.api.backend import cache


def get_store():
    return cache.LocalMemoryCache()
