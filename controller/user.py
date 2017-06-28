#! /usr/bin/env python
# coding: utf-8

import re

from model.post import Post
from model.user import User
from controller.account import AccountController
from lib.helpers import check_field_available, validator_str_is_email,\
    validator_f_str_min_length


class UserController(object):


    @classmethod
    def update_password(cls, user, old_password, new_password):

        # check old password
        old_password = str(old_password)
        if not User.verify_user(user, old_password):
            return False

        # update
        new_password = str(new_password)
        if not AccountController.check_password_available_by_form(
            new_password
        )[0]:
            return False

        return User.modify_password(user, new_password)

    @staticmethod
    def check_email_by_form(value):
        """check form"""
        return check_field_available(value, [validator_str_is_email])[0]

    @staticmethod
    def check_penname_by_form(value):
        """check form"""
        return check_field_available(value, [validator_f_str_min_length(1)])[0]

    @classmethod
    def update_user_info(cls, user, json_info):
        """the following field could be updated:
        email, penname, avatar,
        motto, brief_introduction, country"""
        field_list = [
            'email', 'penname', 'avatar', 'motto',
            'brief_introduction', 'country'
        ]

        update_info = {

        }
        for field in field_list:
            value = json_info.get(field)
            if value:
                # check
                handler = getattr(cls, 'check_{}_by_form'.format(field), None)
                if handler:
                    check_result = handler(value)
                    if not check_result:
                        continue
                update_info.update({
                    field: value
                })

        return_result = False
        # do update
        if update_info:
            return_result = User.update_user_info(
                user, update_info
            )

        return return_result