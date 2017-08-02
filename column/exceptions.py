# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: GPL-3.0

import logging

LOG = logging.getLogger(__name__)


class BaseException(Exception):
    """The Base Exception to extend custom exceptions.
    """

    message = "An unknown exception occurred."

    def __init__(self, msg=None, **kwargs):
        if msg:
            self.message = msg
        if kwargs:
            try:
                self.msg = self.message % kwargs
            except KeyError as e:
                LOG.warning("Formatting error: %(e)s. Message: "
                            "%(msg)s. kwargs: %(kwargs)s",
                            {'e': e, 'msg': self.message, 'kwargs': kwargs})
                self.msg = self.message
        else:
            self.msg = self.message
        super(BaseException, self).__init__(self.msg)


class InvalidParameter(BaseException):
    """Invalid parameter given"""
    message = "Invalid type of %(name)s on parameter %(param)s"


class FileNotFound(BaseException):
    """The given file cannot be found"""
    message = "File %(name)s cannot be found"
