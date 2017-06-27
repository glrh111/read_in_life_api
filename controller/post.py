#! /usr/bin/env python
# coding: utf-8

from model.post import Post


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
        return Post.get_post_by_id(post_id)

    @classmethod
    def new_post(cls, current_user_id):
        if not current_user_id:
            return None
        return Post.add_post(current_user_id)

    @classmethod
    def update_content(cls, post_id, content):
        """just update content"""
        return Post.update_content(post_id, content)

    @classmethod
    def update_permission(cls, post_id, update_info):
        """available_to_other
           anonymous_to_other
           comment_permission
        """
        return Post.update_permission(post_id, **update_info)

    @classmethod
    def delete_post(cls, post_id):
        return Post.delete_post(post_id)