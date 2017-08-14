# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

from collections import defaultdict


def get_progress(run):
    # TODO(ushergod) need to create backend model class and
    # put this fucntion into the model class
    progress = run['api_runner'].get_progress()
    return 0 if progress is None else progress


def format_response(run):
    # TODO(ushergod) need to create backend model class and
    # put this fucntion into the model class
    private_attr = ['become_pass', 'conn_pass', 'private_key_file']
    response = defaultdict(dict)
    for item, value in run.iteritems():
        if item == 'api_runner':
            response['progress'] = get_progress(run)
        elif item == 'options':
            for sub_i, sub_v in value.iteritems():
                if sub_i in private_attr:
                    continue
                else:
                    response[item][sub_i] = sub_v
        else:
            response[item] = value
    return response
