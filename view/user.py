#! /usr/bin/env python
# coding: utf-8

"""
/user/<user_id number>/post
用户的文章列表

"""

from lib.web.route import Route
from lib.web.view.jsonview import JsonQueryView
from lib.web.view.userview import UserView

from model.post import Post

user_route = Route(prefix='/user')


@user_route('/(?P<user_id>\d+)/post')
class AllPostByUser(JsonQueryView, UserView):
    """just for test"""
    def get(self, user_id):
        offset = int(self.query.offset or 0)
        limit = int(self.query.limit or 20)
        self.render({
            'post_list': Post.get_all_post_by_user_id(
                user_id=int(user_id),
                offset=offset,
                limit=limit
            )
        })