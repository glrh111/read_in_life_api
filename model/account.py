#! /usr/bin/env python
# coding: utf-8

"""
第三方登录的账户关联信息
"""

import hashlib
import traceback

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT
from lib.jsob import JsOb
from lib.helpers import timestamp_by_13

from lib.serve.config import app_config
from lib.web.view.error import RegisterInfoNotSatisfy

# to find if its equal with WECHAT.openid and WEAPP.openid
PLATFORM = JsOb({
    'WECHAT': 1,
    'WEAPP' : 2
})


class SNSAccount(BaseModel):

    user_id = Column(Integer, primary_key=True)

    openid = Column(String, primary_key=True)
    platform = Column(Integer, primary_key=True)

    # TODO: add session_key

    ctime = Column(BIGINT, default=timestamp_by_13)

    @classmethod
    def add_sns_account(cls, user_id, open_id, platform):
        """这三个参数确定的信息必须唯一.
        而且需要保证 openid 和 platform确定的record唯一。因为只能对应同一个账号。
        """
        info = {
            'user_id': int(user_id),
            'openid': str(open_id),
            'platform': int(platform)
        }
        info_unique = {
            'openid': str(open_id),
            'platform': int(platform)
        }
        session = SQL_Session()

        return_acc = None
        try:
            acc = SNSAccount(**info)
            session.add(acc)
            # if have two records after committing, should also rollback.
            if cls.record_count(info_unique) > 1:
                print '记录多于1条, rollback', info
                session.rollback()
            else:
                session.commit()
                return_acc = acc
        except Exception:
            print 'in register_user (will rollback)', traceback.print_exc()
            session.rollback()

        return return_acc