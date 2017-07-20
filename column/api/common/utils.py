# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from flask import request
import jsonschema


def validate_payload(schema, payload):
    try:
        jsonschema.validate(payload, schema)
    except jsonschema.exceptions.ValidationError as e:
        return False, e.message
    return True, ""


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
