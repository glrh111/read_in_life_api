#!/usr/bin/env python
# coding:utf-8
from lib.web.view.status_code import STATUS_CODE


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


class UserDisabled(DictError):
    def __init__(self, message=STATUS_CODE.USER_DISABLED.msg):
        self.code = STATUS_CODE.USER_DISABLED.code
        self.message = message


class LoginRequired(DictError):
    def __init__(self):
        self.code = STATUS_CODE.LOGIN_REQUIRED.code
        self.message = STATUS_CODE.LOGIN_REQUIRED.msg


class BadArgument(DictError):
    def __init__(self, msg=''):
        self.code = STATUS_CODE.BAD_ARGUMENT.code
        self.message = "%s  %s" % (STATUS_CODE.BAD_ARGUMENT.msg, msg)


class RegisterInfoNotSatisfy(DictError):
    """login """
    def __init__(self, msg=''):
        self.code = STATUS_CODE.RegisterInfoNotSatisfy.code
        self.message = "%s %s" % (STATUS_CODE.RegisterInfoNotSatisfy.msg, msg)


class LoginInfoNotSatisfy(DictError):

    def __init__(self, msg):
        self.code = STATUS_CODE.LoginInfoNotSatisfy.code
        self.message = "%s %s" % (STATUS_CODE.LoginInfoNotSatisfy.msg, msg)


class PasswordNotMatch(DictError):
    def __init__(self, msg):
        self.code = STATUS_CODE.PASSWORD_NOT_MATCH.code
        self.message = "%s %s" % (STATUS_CODE.PASSWORD_NOT_MATCH.msg, msg)


class PostNotFound(DictError):
    def __init__(self, msg=''):
        self.code = STATUS_CODE.POST_NOT_FOUND.code
        self.message = "%s %s" % (STATUS_CODE.POST_NOT_FOUND.msg, msg)


class OperationNotPermit(DictError):
    def __init__(self, msg=''):
        self.code = STATUS_CODE.OPERATION_NOT_PERMIT.code
        self.message = "%s %s" % (STATUS_CODE.OPERATION_NOT_PERMIT.msg, msg)