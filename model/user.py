#! /usr/bin/env python
# coding: utf-8

import hashlib
import traceback

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT

from lib.serve.config import app_config
from lib.web.view.error import RegisterInfoNotSatisfy
from lib.helpers import timestamp_by_13

DEFAULT_PENNAME = '佚名'


class User(BaseModel):

    user_id = Column(Integer, primary_key=True)  # do not set this by hand

    # could login via those three field
    username = Column(String, default='')
    password_hash = Column(String)

    # user info
    email = Column(String, default='')
    penname = Column(String)
    avatar = Column(String)    # url from qiniu
    motto = Column(String)     # one sentence introduction
    brief_introduction = Column(String) # introduction
    country = Column(String)

    # register and login info
    ## time is 13 timestamp, the last bit is millisecond
    ctime = Column(BIGINT, default=timestamp_by_13)
    last_login_time = Column(BIGINT)

    @property
    def can_login(self):
        """if this user is disabled"""
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readble attribute.')

    @password.setter
    def password(self, value):
        """do not commit hear"""
        self.password_hash = User.encrypt_pwd(value)

    @property
    def base_info(self):
        return {
            'user_id': self.user_id,
            'penname': self.penname or DEFAULT_PENNAME,
        }

    @base_info.setter
    def base_info(self, value):
        raise ValueError('could not set value to base info')

    @classmethod
    def is_password_available(cls, password):
        if not isinstance(password, str):
            return False
        return bool(password)

    @classmethod
    def modify_password(cls, user, new_password):
        """False True"""
        if not cls.is_password_available(new_password):
            return False
        user.password = new_password
        user.save()

    @classmethod
    def encrypt_pwd(cls, password):
        m = hashlib.md5(app_config.PASSWORD_SECRET)
        m.update(password)
        password = m.hexdigest()
        return password

    @classmethod
    def verify_user(cls, user, password):
        return user.password_hash == cls.encrypt_pwd(password)

    @classmethod
    def if_register_field_available(cls, spec):
        """add new user. its a transaction
           spec is like this:
           {phone: wocao, country: nidaye}
        """
        return not bool(cls.find_one(spec))

    @classmethod
    def if_register_info_available_for_web(cls, json_info):
        """not userd now
        """

        # 1. look for register way
        value, field = [''] * 2
        for field in [
            'phone', 'username', 'email'
        ]:
            value = json_info.get(field)
            if value:
                break

        if not value:
            raise RegisterInfoNotSatisfy('phone or username or email is essential')

        register_info = {
            field: value
        }

        # 2. judge if register info (for phone) available
        if 'phone' == field:
            if json_info.get('country_code'):
                if not User.if_register_field_available({
                    'phone': value,
                    'country_code': json_info.get('country_code')
                }):
                    raise RegisterInfoNotSatisfy('this phone [{}:{}] already be registered'.format(
                        json_info.get('country_code'), value
                    ))
            else:
                raise RegisterInfoNotSatisfy('country_code is essential')

            register_info.update({
                'country_code': json_info.get('country_code')
            })

        if not User.if_register_field_available({
            field: value
        }):
            raise RegisterInfoNotSatisfy('this {} already be registered is essential')

        # 3. judge if password available
        password = str(json_info.get('password', ''))
        if not User.is_password_available(password):
            raise RegisterInfoNotSatisfy('password not available')

        return register_info, password   # register_info should be unique

    @classmethod
    def if_register_info_available_for_weapp(cls, json_info):
        """weapp, use openid?"""
        pass

    @classmethod
    def add_user(cls, username, password):
        """add new user
        should use transaction
        register_info should only contain the following field:
        email, username, (country_code, phone)
        """
        session = SQL_Session()
        return_user = None

        register_info = {
                'username': username,
                'password': password
            }
        try:
            user = User(**register_info)
            user.password = password
            session.add(user)
            # if have two records after committing, should also rollback.
            if cls.record_count({'username': username}) > 1:
                print '记录多于1条, rollback', {'username': username}
                session.rollback()
            else:
                session.commit()
                return_user = user
        except Exception:
            print 'in register_user (will rollback)', traceback.print_exc()
            session.rollback()

        return return_user

    @classmethod
    def update_last_login_time(cls, user):
        """update last login time"""
        re = False
        try:
            user.last_login_time = timestamp_by_13()
            SQL_Session().commit()
            re = True
        except Exception:
            SQL_Session().rollback()
        return re



if __name__ == '__main__':
    sql_session.query(User).all()