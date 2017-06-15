#! /usr/bin/env python
# coding: utf-8


class Default:
    DEBUG = True

    PG_URL = 'pg:url:wocaon'


class Development(Default):
    pass


config = {
    'default': Default,
    'development': Development
}