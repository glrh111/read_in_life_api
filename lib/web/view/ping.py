#!/usr/bin/env python
# coding:utf-8

from . import route
from tornado.web import RequestHandler


@route('/_/ping')
class Ping(RequestHandler):
    def get(self):
        self.finish('pong')
