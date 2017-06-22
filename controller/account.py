#! /usr/bin/env python
# coding: utf-8

import requests
import json

from lib.web.view.error import RegisterInfoNotSatisfy, LoginInfoNotSatisfy,\
    PasswordNotMatch, BadArgument
from model.user import User
from model.account import SNSAccount, PLATFORM
from lib.serve.config import app_config
from lib.helpers import check_field_available, validator_f_str_min_length, validator_str_is_number_or_a_to_z_or_punctuation,\
    validator_str_is_number_or_a_to_z


class LoginType:
    WEB = 1
    ThirdGroup = 2


class AccountController(object):

    @classmethod
    def get_login_handler(cls, login_type):
        return login_handler_dict.get(login_type)

    @classmethod
    def login_for_web(cls, json_info):
        """for web login
           if could login, Login user
        """
        err = LoginInfoNotSatisfy('user not exist or password not match')
        username = json_info.username
        password = json_info.password

        if not (username and password):
            raise err

        user = User.find_one({ 'username': username })

        if not user:
            raise err

        if not User.verify_user(user, password):
            raise err

        return user, {'code': 1}

    @classmethod
    def get_openid_by_jscode(cls, js_code):
        """for weapp use
           fail return None;
           success return { openid, session_key };
        """
        response = requests.get(
            app_config.WEAPP_JSCODE2OPENID,
            params={
                'appid': app_config.WEAPP_APPID,
                'secret': app_config.WEAPP_SECRET,
                'js_code': js_code,
                'grant_type': 'authorization_code'
            }
        )
        if 200 == response.status_code:
            content = response.content
            try:
                json_dict = json.loads(content)
                openid = json_dict.get('openid')
                session_key = json_dict.get('session_key')
                if openid and session_key:
                    return {
                        'openid': openid,
                        'session_key': session_key
                    }
            except Exception:
                pass

        return None

    @classmethod
    def get_user_by_openid(cls, openid, platform):
        """get user by openid"""
        spec = {
            'openid': openid,
            'platform': platform
        }

        acc = SNSAccount.find_one(spec)

        if acc:
            user_id = acc.user_id
            user = User.find_one({'user_id': user_id})
            if user:
                return user
            else:
                # delete this acc record
                acc.delete()
        return None

    @classmethod
    def login_for_weapp(cls, json_info):
        """
        1. platform
        2. js_code
        """
        platform = PLATFORM.WEAPP
        js_code = json_info.get('js_code')

        if not js_code:
            raise BadArgument('js code is essential')

        # get openid
        openid_info = cls.get_openid_by_jscode(js_code)
        if not openid_info:
            return {
                'message': 'get openid failed from js_code. try resend js_code or wait some minutes.',
                'code': 3
            }

        # try to get user
        user = cls.get_user_by_openid(
            openid = openid_info.get('openid'),
            platform=PLATFORM.WEAPP
        )

        # 1. code == 1, if find user, login
        if user:
            # update session_key
            return user, { 'code': 1 }

        # 2. code == 2, need associating
        ## TODO: save session_key to redis.
        return None, { 'code': 2, 'openid': openid_info.get('openid') }


    @classmethod
    def check_username_available(cls, username):
        # if username available
        username_available, username_msg = check_field_available(username, [
            validator_f_str_min_length(1),
            validator_str_is_number_or_a_to_z
        ])
        if not username_available:
            raise RegisterInfoNotSatisfy('[{}]: {}'.format(username, msg))
        pass


    @classmethod
    def associate_user(cls, json_info):
        """give me openid, and username, I do """
        stage, username, platform, openid = map(
            lambda x: json_info.get(x),
            ['stage', 'username', 'platform', 'openid']
        )

        if not ( stage and username and platform and openid ):
            raise BadArgument('stage, username, platform, openid is essential')

        # check username

        # stage == 1


        pass

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


login_handler_dict = {
        LoginType.WEB: AccountController.login_for_web,
        LoginType.ThirdGroup: AccountController.login_for_weapp
    }


if __name__ == '__main__':
    js_code = '081kt89e0ScLMy16IK9e0hf19e0kt89a'
    print AccountController.get_openid_by_jscode(js_code)