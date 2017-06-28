#! /usr/bin/env python
# coding: utf-8

"""
/user/<user_id number>/post
用户的文章列表

"""

from lib.web.route import Route
from lib.web.view.jsonview import JsonQueryView, JsonCommonView
from lib.web.view.userview import UserView, LoginView
from lib.web.view.error import BadArgument

from model.user import User
from model.post import Post
from controller.user import UserController


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


@user_route('/?')
class UserInfo(JsonCommonView, LoginView):
    """just for test"""
    SUPPORTED_METHODS = ('PUT')

    def put(self):
        """update
           update_type: 1 change: password: need verify password first
                        2 change other info:
        return: 1 success 2 failed
        """

        update_type = int(self.json.update_type or 0)
        if 1 == update_type:
            old_password = self.json.old_password
            new_password = self.json.new_password
            if not (old_password and new_password):
                raise BadArgument('old_password and new_password is essential.')
            result = UserController.update_password(
                user=self.current_user,
                old_password=old_password,
                new_password=new_password
            )
        elif 2 == update_type:
            result = UserController.update_user_info(
                user=self.current_user,
                json_info=self.json
            )
        else:
            raise BadArgument('update_type should be 1 or 2.')

        self.finish({
            'code': 1 if result else 2
        })


@user_route('/(?P<user_id>\d+)')
class UserInfo(JsonCommonView):
    """get one's user info"""
    SUPPORTED_METHODS = ('GET')

    def get(self, user_id):
        """get info"""
        user = User.get_user_by_id(int(user_id))
        self.render({
            'user': user.base_info if user else {}
        })

