#! /usr/bin/env python
# coding: utf-8

import requests
import json

from lib.web.view.error import OperationNotPermit
from model.user import User
from model.account import SNSAccount, PLATFORM
from model.post import Post
from lib.serve.config import app_config
from lib.helpers import check_field_available, validator_f_str_min_length, validator_str_is_number_or_a_to_z_or_punctuation,\
    validator_str_is_number_or_a_to_z


class PostController(object):

    @classmethod
    def get_all_post(cls, offset, limit, myself_user_id=None):
        """all post DESC by"""
        return Post.get_all_post(
            offset=offset,
            limit=limit
        )

    @classmethod
    def get_post_by_id(cls, post_id, myself_user_id=None):
        """需要判断是不是本人.
        1. 如果是本人, 不用检查权限, 即可返回所有
        2. 如果不是本人, 不对外公开的post不能返回
        """
        pass

    @classmethod
    def new_post(cls, current_user_id):
        if not current_user_id:
            return None
        return Post.add_post(current_user_id)

    @classmethod
    def update_content(cls, post_id, content, current_user_id):
        """just update content"""
        post = Post.get_post_by_id(post_id)

        if post:
            # check permission. could not take info out
            if current_user_id == post.user_id:
                return Post.update_content(post_id, content)

        raise OperationNotPermit