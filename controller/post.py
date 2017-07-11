#! /usr/bin/env python
# coding: utf-8

from model.post import Post
from model.user import User


class PostController(object):

    @classmethod
    def get_timeline_post(cls, offset, limit, observer=None):
        """all post DESC by"""
        return Post.get_timeline_post(
            offset=offset,
            limit=limit,
            observer=observer
        )

    @classmethod
    def get_user_post_by_self(cls, user, offset, limit):
        """自己看自己的文章列表"""
        return Post.get_user_post_by_self(user, offset, limit)

    @classmethod
    def get_user_post_by_other(cls, user_id, offset, limit, observer=None):
        """observer看user_id的文章列表
           observer=None 匿名查看
        """
        user = User.find_one({ 'user_id': user_id })
        if user:
            return Post.get_user_post_by_other(user, offset, limit, observer=observer)
        else:
            return []

    @classmethod
    def get_post_by_id(cls, post_id, observer=None):
        """observer代表看到这一篇文章的人。
        """
        return Post.get_post_by_id(post_id, observer=observer)

    @classmethod
    def new_post(cls, current_user_id):
        if not current_user_id:
            return None
        return Post.add_post(current_user_id)

    @classmethod
    def update_content_info(cls, post_id, content_info):
        """just update content"""
        return Post.update_content_info(post_id, content_info)

    @classmethod
    def update_permission(cls, post_id, update_info):
        """available_to_other
           #anonymous_to_other
           comment_permission
           title
           abstract
        """
        return Post.update_other_info(post_id, **update_info)

    @classmethod
    def delete_post(cls, post_id):
        return Post.delete_post(post_id)