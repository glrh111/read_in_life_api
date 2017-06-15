#! /usr/bin/env python

import os

from spec.config import config

config_name = os.getenv('READ_IN_LIFE_API_ENV', 'default')

app_config = config[config_name]