# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import json

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
            payload = uni_to_str(json.loads(request.get_data()))
            res, errors = validate_payload(schema, payload)
            if not res:
                return errors, status_code
            return f(controller_object)
        return wrapper
    return decorator


def uni_to_str(input):
    if isinstance(input, dict):
        return {uni_to_str(key):
                uni_to_str(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [uni_to_str(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input
