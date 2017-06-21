#! /usr/bin/env python
# coding: utf-8

from lib.web.view.error import RegisterInfoNotSatisfy, LoginInfoNotSatisfy,\
    PasswordNotMatch
from model.user import User


class AccountController(object):

    @classmethod
    def register_user(cls, json_info):
        """
        receive: 1. 任选一项 phone + country_code, username, email,
                 2. 密码 password
        """
        # translate json_info to dict
        register_info, password = User.if_register_info_available_for_web(json_info)

        user = User.register_user(register_info, password)
        if user is None:
            raise RegisterInfoNotSatisfy('something bad occur(db transaction error) when registering')

        return user

    @classmethod
    def login_user_from_web(cls, json_info):

        value, field = [''] * 2
        for field in [
            'phone', 'username', 'email'
        ]:
            value = json_info.get(field)
            if value:
                break

        if not value:
            raise LoginInfoNotSatisfy('need log in info')

        login_info = {
            field: value
        }

        if 'phone' == field:
            if not json_info.get('country_code'):
                raise LoginInfoNotSatisfy('country_code is essential')

            login_info.update({
                'country_code': json_info.get('country_code')
            })

        # find user via login_info
        user = User.find_one(login_info)

        password = json_info.get('password')

        if not password:
            raise LoginInfoNotSatisfy('password is essential')

        if not user:
            raise LoginInfoNotSatisfy('could not find user by your info')

        if User.verify_user(user, password):
            return user
        else:
            raise PasswordNotMatch()
