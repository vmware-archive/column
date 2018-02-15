# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import copy

from ansible.playbook import play_context


CONTEXT_ATTRIBUTES = copy.deepcopy(play_context.PlayContext._attributes)
