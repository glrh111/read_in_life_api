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
from lib.web.view.jsonview import JsonQueryView, JsonPostView
from lib.web.view.userview import LoginView, UserView
from lib.web.view.error import RegisterInfoNotSatisfy

from lib.web.model.redis_db import redis
from lib.web.model.sql_db import SQL_Session
from model.user import User
from lib.web.view.error import BadArgument
from controller.account import AccountController, LoginType

account_route = Route(prefix='/account')

@gen.coroutine
def wocao(xiuxi):
    gen.sleep(xiuxi)

@account_route('/ping')
class Ping(JsonQueryView, LoginView):
    """just for test"""
    @gen.coroutine
    def get(self):

        xiuxi = self.query.xiuxi
        if xiuxi:
            yield wocao(int(xiuxi))

        print 'ping.ping', User.find_one()

        self.render({
            'wocao': '挺成功' + redis.get('wocao')
        })



@account_route('/register')
class Register(JsonPostView, UserView):
    """receive: 1. 任选一项 phone + country_code, username, email,
                2. 密码 password"""
    def post(self):
        """nickname, password"""
        print self.json, type(self.json), 'self.json'

        user = AccountController.register_user(self.json)

        self.login(user)

        self.finish({
            'user': user.base_info
        })


@account_route('/log_in')
class LogIn(JsonPostView, UserView):
    def post(self):

        login_type = self.json.login_type

        if not login_type:
            raise BadArgument('login_type is essential')

        login_type = int(login_type)

        f = AccountController.get_login_handler(login_type)

        user, merged_info = f(self.json)

        if user:
            self.login(user)

        self.render(merged_info)


@account_route('/associate')
class Associate(JsonPostView):

    def post(self):
        pass


@account_route('/log_out')
class LogOut(LoginView, JsonPostView):
    def post(self):
        if self.current_user_id:
            self._session_rm()
        self.render({})