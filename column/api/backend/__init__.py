# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from column.api.backend import cache


def get_store():
    return cache.LocalMemoryCache()
