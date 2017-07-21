# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import logging
import os

import flask
import flask_restful

from column.api.controller import credential_controller
from column.api.controller import run_controller
from column import cfg


application = flask.Flask(__name__)
api = flask_restful.Api(application)

api.add_resource(run_controller.Run, '/runs/<id>')
api.add_resource(run_controller.RunList, '/runs')
api.add_resource(credential_controller.Credential, '/credentials')

LOG_FILE = cfg.get('DEFAULT', 'log_file')
LOG_LEVEL = cfg.get('DEFAULT', 'log_level')
if os.access(LOG_FILE, os.W_OK):
    logging.basicConfig(filename=LOG_FILE,
                        format='%(asctime)s %(levelname)s '
                               '%(name)s %(message)s',
                        level=LOG_LEVEL)
else:
    print('Unable to log to the file: %s' % LOG_FILE)

SERVER = cfg.get('DEFAULT', 'server')
PORT = cfg.get('DEFAULT', 'port')


if __name__ == '__main__':
    application.run(host=SERVER, port=PORT)
