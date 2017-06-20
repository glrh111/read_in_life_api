#! /usr/bin/env python
# coding: utf-8


"""
登录系统:
登录方式: 手机号phone, 用户名, 第三方登录: username. 这三者都不许重复
如果是第三方登录: 存储openid到另一个表, 然后生成这里的相关信息.

register: 注册. 得区分下从哪里注册. 小程序 or 网页
log_in: 登录
log_out: 退出登录 清理session

"""

from lib.web.route import Route
from tornado.web import RequestHandler
from lib.web.view.jsonview import JsonQueryView, JsonPostView
from lib.web.view.userview import LoginView, UserView

from lib.web.model.redis_db import redis
from lib.web.model.sql_db import SQL_Session
from model.user import User
from lib.web.view.error import BadArgument

account_route = Route(prefix='/account')

@account_route('/ping')
class Ping(JsonQueryView):
    def get(self):

        print 'ping.ping', User.find_one()

        self.render({
            'wocao': '挺成功' + redis.get('wocao')
        })

@account_route('/register')
class Register(JsonPostView):
    def post(self):
        """nickname, password"""

        self.finish({

        })


@account_route('/log_in')
class LogIn(UserView, JsonPostView):
    def post(self):
        user_id = self.json.user_id
        if not user_id:
            raise BadArgument('user_id is essential.')

        if isinstance(user_id, str):
            if not(user_id.isdigit()):
                raise BadArgument('user_id should be digit.')

        user = User.find_one({'user_id': int(user_id)})
        if user:
            self.login(user)
            self.render({
                'user': user.base_info()
            })
        else:
            self.render({})


@account_route('/log_out')
class LogOut(LoginView, JsonPostView):
    def post(self):
        if self.current_user_id:
            self._session_rm()
        self.render({})