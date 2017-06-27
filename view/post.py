#! /usr/bin/env python
# coding: utf-8


"""
登录系统:
登录方式: 手机号phone, 用户名, 第三方登录: username. 这三者都不许重复
如果是第三方登录: 存储openid到另一个表, 然后生成这里的相关信息.

register: 注册. 得区分下从哪里注册. 小程序 or 网页
log_in:  登录
log_out: 退出登录 清理session

"""
import time

from tornado.web import gen

from lib.web.route import Route
from tornado.web import RequestHandler
from lib.web.view.jsonview import JsonQueryView, JsonPostView, JsonCommonView
from lib.web.view.userview import LoginView, UserView
from lib.web.view.error import RegisterInfoNotSatisfy

from lib.web.model.sql_db import SQL_Session
from model.user import User
from model.post import Post
from lib.web.view.error import BadArgument, LoginRequired
from controller.post import PostController

post_route = Route(prefix='/post')


@post_route('/?')
class AllPost(JsonQueryView, UserView):
    """just for test"""
    def get(self):
        offset = int(self.query.offset or 0)
        limit = int(self.query.limit or 20)

        self.render({
            'post_list': Post.get_all_post(
                offset=offset,
                limit=limit
            )
        })

    def post(self):
        """add new post"""
        if not self.current_user:
            raise LoginRequired

        new_post = PostController.new_post(self.current_user_id)

        self.render({
            'post': new_post.base_info
        })


@post_route('/(?P<post_id>\d+)')
class OnePost(JsonCommonView, UserView):
    """just for test"""

    SUPPORTED_METHODS = ('GET', 'PUT', 'DELETE')

    def get(self, post_id):
        start = int(self.query.start or 0)
        size = int(self.query.size or 0)

        print start, size, post_id

        self.render({
            'wocao': '挺成功'
        })

    def put(self, post_id):
        """update
        update_type: 1 content
                     2 permission
        """
        print self.json

        if not self.current_user:
            raise LoginRequired
        post_id = int(post_id)
        update_type = int(self.json.update_type or 0)
        if 1 == update_type:
            content = self.json.content
            result = PostController.update_content(
                post_id=post_id,
                content=content,
                current_user_id=self.current_user_id
            )
            self.render({
                'post': result.base_info
            })
        elif 2 == update_type:
            pass
        else:
            raise BadArgument('update_type is essential.')


    def delete(self, post_id):
        """logically delete a post"""
        pass