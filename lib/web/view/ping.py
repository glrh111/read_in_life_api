#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from _route import route
from app.web.view.baseview import View


@route('/_/ping')
class Ping(View):
    def get(self):
        self.finish('pong')
