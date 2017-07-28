# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause
import json
import logging
import uuid

from flask import request
import flask_restful
from flask_restful import abort
from six.moves import http_client

from column.api import backend
from column.api import manager
from column.api.common import utils

LOG = logging.getLogger(__name__)

run_post_schema = {
    "$schema": "http://json-schema.org/schema#",
    "type": "object",
    "properties": {
        "playbook_path": {"type": "string"},
        "inventory_file": {"type": ["string", "null"]},
        "options": {
            "type": "object",
            "properties": {
                "become_method": {"type": ["string", "null"]},
                "become_user": {"type": ["string", "null"]},
                "connection": {"type": ["string", "null"]},
                "extra_vars": {"type": ["object", "null"]},
                "password": {"type": ["string", "null"]},
                "private_key_file": {"type": ["string", "null"]},
                "skip_tags": {"type": ["array", "null"]},
                "subset": {"type": ["string", "null"]},
                "tags": {"type": ["string", "array", "null"]},
                "verbosity": {"type": ["number", "null"]}
            },
            "additionalProperties": False
        }
    },
    "required": ["playbook_path"],
    "additionalProperties": False
}


class Run(flask_restful.Resource):
    """Column api run resource class

    Attributes:
        backend_store (obj): backend interface for retrieving run info
    """

    def __init__(self):
        self.backend_store = backend.get_store()

    def get(self, id):
        """Get run by id"""
        run = self.backend_store.get_run(id)
        if not run:
            return abort(404, message="Run {} doesn't exist".format(id))
        return run


class RunList(flask_restful.Resource):
    """Column api runlist resource class

    Attributes:
        backend_store (obj): backend interface for retrieving run info
        manager (obj): manager interface for calling column library method
                       to run playbook
    """

    def __init__(self):
        self.backend_store = backend.get_store()
        self.manager = manager.get_manager('run')

    def get(self):
        """Get run list"""
        LOG.info('Returning all ansible runs')
        return self.backend_store.list_runs()

    @utils.validator(run_post_schema, http_client.BAD_REQUEST)
    def post(self):
        """Trigger a new run"""
        run_payload = json.loads(request.get_data())
        run_payload['id'] = str(uuid.uuid4())
        LOG.info('Triggering new ansible run %s', run_payload['id'])
        return self.manager.create_run(run_payload)
