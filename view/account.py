#! /usr/bin/env python
# coding: utf-8


"""
register: 注册. 得区分下从哪里注册. 小程序 or 网页
log_in: 登录
log_out: 退出登录 清理session
"""

from lib.web.route import Route
from tornado.web import RequestHandler
from lib.web.view.jsonview import JsonQueryView

from lib.web.model.redis_db import redis
from lib.web.model.sql_db import sql_session
from model.user import User

account_route = Route(prefix='/account')

@account_route('/ping')
class Ping(JsonQueryView):
    def get(self):
        print 'week_index: ', self.query.week_index
        print 'set redis', redis.set('wocao', 'heihei')

        new_user = User(**{
            'nickname': 'wocaonidaye'
        })
        sql_session.add(new_user)
        sql_session.commit()

        for user in sql_session.query(User).all():
            print user.nickname, user.user_id

        self.finish({
            'wocao': '挺成功' + redis.get('wocao')
        })

@account_route('/register')
class Register(RequestHandler):
    def post(self):
        self.finish('pong from ping.ping')


@account_route('/log_in')
class LogIn(RequestHandler):
    def post(self):
        self.finish('pong from ping.ping')


@account_route('/log_out')
class LogOut(RequestHandler):
    def post(self):
        self.finish('pong from ping.ping')