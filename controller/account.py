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

        # 2. 判断注册字段是否可用.
        if 'phone' == field:
            if json_info.get('country_code'):
                if not User.if_register_field_available({
                    'phone': value,
                    'country_code': json_info.get('country_code')
                }):
                    raise RegisterInfoNotSatisfy('this phone [{}:{}] already be registered is essential'.format(
                        json_info.get('country_code'), value
                    ))
            else:
                raise RegisterInfoNotSatisfy('country_code is essential')

        if not User.if_register_field_available({
            field: value
        }):
            raise RegisterInfoNotSatisfy('this {} already be registered is essential')

        # 3. 实际注册步骤 do register






        pass

    pass