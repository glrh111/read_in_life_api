#!/usr/bin/env python
# coding:utf-8


class BaseControllerError(Exception):
    pass


class DictError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def dump(self):
        return {"code": self.code, "message": self.message}

    def __str__(self):
        return "error_code=%s,%s" % (self.code, self.message)
