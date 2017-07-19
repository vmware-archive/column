# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import cerberus


def validate_payload(schema, payload):
    v = cerberus.Validator(schema)
    res = v.validate(payload)
    return res, v.errors
