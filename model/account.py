#! /usr/bin/env python
# coding: utf-8

"""
第三方登录的账户关联信息
"""

import hashlib
import traceback

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String

from lib.serve.config import app_config
from lib.web.view.error import RegisterInfoNotSatisfy

# to find if its equal with WECHAT.openid and WEAPP.openid
class PLATFORM:
    WECHAT = 1
    WEAPP = 2


class SNSAccount(BaseModel):

    user_id = Column(Integer)

    openid = Column(Integer)
    platform = Column(Integer)

    ctime = Column(Integer)