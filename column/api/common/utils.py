# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import cerberus
from flask import request


def validate_payload(schema, payload):
    v = cerberus.Validator(schema)
    res = v.validate(payload)
    return res, v.errors


def validator(schema, status_code):
    def decorator(f):
        def wrapper(controller_object):
            payload = request.get_json(silent=True)
            res, errors = validate_payload(schema, payload)
            if not res:
                return errors, status_code
            return f(controller_object)
        return wrapper
    return decorator
