#! /usr/bin/env python
# coding: utf-8

from tornado.web import Application

from lib.web.view import route as base_route
from lib.serve.config import app_config

def application(
    route_list,
    Application,
    xsrf_cookies=False,
):
    app = Application(
        xsrf_cookies=xsrf_cookies,
        debug=app_config.DEBUG,
        gzip=True
    )

    for route in route_list:
        # print route.host, route.handlers
        app.add_handlers(route.host, route.handlers)

    return app

def create_app():

    # collect route
    return application([base_route], Application)
