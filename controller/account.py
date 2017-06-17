#! /usr/bin/env python
# coding: utf-8

from lib.web.view.error import RegisterInfoNotSatisfy
from model.user import User

class AccountController(object):

    @classmethod
    def register_user(cls, json_info):
        """
        receive: 1. 任选一项 phone + country_code, username, email,
                 2. 密码 password
        """
        # 1. 判断注册方式
        value, field = [''] * 2
        for field in [
            'phone', 'username', 'email'
        ]:
            value = json_info.get(field)
            if value:
                break

        if not value:
            raise RegisterInfoNotSatisfy()

        if 'phone' == field and (not json_info.get('country_code')):
            raise RegisterInfoNotSatisfy('country_code is essential')

        # 2. 判断是否有用户使用同名字段.





        pass

    pass