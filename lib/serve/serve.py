#! /usr/bin/env python
# coding:utf-8

import sys
import os
import argparse
import tornado.web
import tornado.ioloop

# prepare: add sys.path
import prepare

# config: read config
from config import app_config

# create_app: collect route
from create_app import create_app

# run


def run_server():
    # print '执行到了这里...2'
    # if len(sys.argv) != 1 and sys.argv[1][:6] == '--port':
    #     port = sys.argv[1].rsplit('=')[1]

    print 'SERVE ON PORT %s' % 8000
    application = create_app()
    application.listen(8000)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == '__main__':
    print 'in serve: ', app_config.DEBUG
    run_server()