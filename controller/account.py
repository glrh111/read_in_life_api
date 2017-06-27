#! /usr/bin/env python
# coding: utf-8

import requests
import json

from lib.web.view.error import LoginInfoNotSatisfy, BadArgument
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
            raise BadArgument(
                'get openid failed from js_code[{}]. try resend js_code or wait some minutes.'.format(js_code)
            )

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
    def check_username_available_by_form(cls, username):
        # username能否被当作username
        return check_field_available(username, [
            validator_f_str_min_length(1),
            validator_str_is_number_or_a_to_z
        ])

    @classmethod
    def check_password_available_by_form(cls, password):
        # password能否被当作password
        return check_field_available(password, [
            validator_f_str_min_length(3),
            validator_str_is_number_or_a_to_z_or_punctuation
        ])

    @classmethod
    def check_username_have_ever_been_used(cls, username):
        # 该用户名是否已经存在在本平台
        spec = { 'username': username }
        return User.find_one(spec)

    @classmethod
    def associate_user(cls, json_info):
        """give me openid, and username, I do """
        stage, username, platform, openid = map(
            lambda x: json_info.get(x),
            ['stage', 'username', 'platform', 'openid']
        )

        if not ( stage and username and platform and openid ):
            raise BadArgument('stage, username, platform, openid is essential')

        # check platform
        stage = int(stage)
        platform = int(platform)

        print PLATFORM.values(), PLATFORM, platform

        if platform not in PLATFORM.values():
            raise BadArgument('platform [{}] not available.'.format(platform))

        # check username
        username_available, username_msg = cls.check_username_available_by_form(username)
        if not username_available:
            raise LoginInfoNotSatisfy('[{}]: {}'.format(username, username_msg))

        user = None
        new_info = {}
        # stage == 1
        if 1 == stage:
            # 若为新用户，通知weapp进入stage=2
            # 若为老用户，通知weapp进入stage=3
            user = cls.check_username_have_ever_been_used(username)
            if user:
                new_stage = 3
            else:
                new_stage = 2
            new_info = {
                'code': 1,
                'stage': new_stage,
            }
        elif 2 == stage:
            # 新用户。设置密码。建立用户记录；建立account记录.
            password = json_info.get('password')
            user = cls.register_user(username, password)
            # add account record
            acc = SNSAccount.add_sns_account(
                user.user_id,
                openid,
                platform
            )
            if not acc:
                raise LoginInfoNotSatisfy('[{}]: {}'.format(username, 'the association between user and openid has been created before.'))

            new_info = {
                'code': 1
            }

        elif 3 == stage:
            # 老用户。查看是否已经关联；
            #      若没有关联，验证密码，进行关联；建立account记录.
            #      若已经关联，提示用户名不可用。
            user = User.find_one({ 'username': username })
            if not user:
                LoginInfoNotSatisfy('[{}]: {}'.format(username, 'could not find user by this username.'))

            # 已经关联
            spec = {
                'user_id': int(user.user_id),
                'openid': str(openid),
                'platform': int(platform)
            }
            acc = SNSAccount.find_one(spec)

            # 没有关联
            if not acc:
                acc = SNSAccount.add_sns_account(
                    user.user_id,
                    openid,
                    platform
                )
                if not acc:
                    raise LoginInfoNotSatisfy(
                        '[{}]: {}'.format(username, 'the association between user and openid has been created before.'))

                new_info = {
                    'code': 1
                }

            else:
                LoginInfoNotSatisfy(
                    '[{}]: {}'.format(username, 'the association between user and openid has been created before.'))

        else:
            raise BadArgument('stage [{}] not available.'.format(stage))

        json_info.update(new_info)
        return user, json_info.to_dict()

    @classmethod
    def register_user(cls, username, password):
        """"""
        # check not null
        if not (username and password):
            raise LoginInfoNotSatisfy('username and password is essential.')

        # check username
        username_available, username_msg = cls.check_username_available_by_form(username)
        if not username_available:
            raise LoginInfoNotSatisfy('[{}]: {}'.format(username, username_msg))

        # check password
        password_available, password_msg = cls.check_password_available_by_form(password)
        if not password_available:
            raise LoginInfoNotSatisfy('[{}]: {}'.format(password, password_msg))

        # check username if unique
        user = User.add_user(username, password)
        if not user:
            raise LoginInfoNotSatisfy('[{}]: {}'.format(username, 'username has been used.'))
        return user


login_handler_dict = {
    LoginType.WEB: AccountController.login_for_web,
    LoginType.ThirdGroup: AccountController.login_for_weapp
}


if __name__ == '__main__':
    js_code = '081kt89e0ScLMy16IK9e0hf19e0kt89a'
    print AccountController.get_openid_by_jscode(js_code)