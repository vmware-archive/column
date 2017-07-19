import cerberus


def validate_payload(schema, payload):
    v = cerberus.Validator(schema)
    res = v.validate(payload)
    return res, v.errors
