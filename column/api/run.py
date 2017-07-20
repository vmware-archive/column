# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

import logging
import os

import flask
import flask_restful

from column import cfg
from column.api.controller import credential_controller
from column.api.controller import run_controller

app = flask.Flask(__name__)
api = flask_restful.Api(app)

api.add_resource(run_controller.Run, '/runs/<id>')
api.add_resource(run_controller.RunList, '/runs')
api.add_resource(credential_controller.Credential, '/credentials')


if __name__ == '__main__':
    log_file = cfg.get('DEFAULT', 'log_file')
    log_level = cfg.get('DEFAULT', 'log_level')
    if os.access(log_file, os.W_OK):
        logging.basicConfig(filename=log_file,
                            format='%(asctime)s %(levelname)s '
                                   '%(name)s %(message)s',
                            level=log_level)
    else:
        print('Unable to log to the file: %s' % log_file)

    server = cfg.get('DEFAULT', 'server')
    port = cfg.get('DEFAULT', 'port')

    app.run(host=server, port=port)
