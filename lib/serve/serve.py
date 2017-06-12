#! /usr/bin/env python
# coding:utf-8

import sys
import os
import argparse
import tornado.web
import tornado.ioloop

def _application(
    route_list,
    Application,
    xsrf_cookies=False,
):
    app = Application(
        xsrf_cookies=xsrf_cookies,
        debug=DEBUG,     ## TODO: FROM CONFIG
        gzip=True
    )

    for route in route_list:
        # print route.host, route.handlers
        app.add_handlers(route.host, route.handlers)

    return app

def main(route, port):
    print '执行到了这里...2'
    if len(sys.argv) != 1 and sys.argv[1][:6] == '--port':
        port = sys.argv[1].rsplit('=')[1]

    print 'SERVE ON PORT %s' % port, '*' * 20
    # for i in route:
    #     print i.handlers
    # print 'route_list', route, type(route)
    application = _application(route, tornado.web.Application)
    application.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    # ioloop.set_blocking_log_threshold(0.2)
    ioloop.start()


def serve():
    # read
    # from solo.config import APP, HOST, PORT_BEGIN
    from importlib import import_module
    from app.web.view._route import ROUTE_LIST as WEB_ROUTE_LIST
    # 首先导入_url
    # 再次导入_route
    __import__('app.%s.view._url' % APP)
    __import__('app.web.view._url')
    ROUTE_LIST = import_module('app.%s.view._route' % APP).ROUTE_LIST
    ROUTE_LIST += WEB_ROUTE_LIST
    main(reversed(ROUTE_LIST), PORT_BEGIN)




SERVE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
ROOT_PATH = os.path.join(
    os.path.join(SERVE_PATH, os.path.pardir), os.path.pardir
)


if __name__ == '__main__':
    print SERVE_PATH, ROOT_PATH
    # serve()