#! /usr/bin/env python
# coding: utf-8

import hashlib
import traceback

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String

from lib.serve.config import app_config
from lib.web.view.error import RegisterInfoNotSatisfy



class User(BaseModel):

    user_id = Column(Integer, primary_key=True)  # do not set this by hand

    # could login via those three field
    country_code = Column(String, default='')
    phone = Column(String, default='')
    username = Column(String, default='')
    email = Column(String, default='')

    password_hash = Column(String)

    # user info
    nickname = Column(String)
    avatar = Column(String)    # url from qiniu
    motto = Column(String)     # one sentence introduction
    brief_introduction = Column(String) # introduction
    country = Column(String)

    # register and login info
    ## time is 13 timestamp, the last bit is millisecond
    ctime = Column(Integer)
    last_login_time = Column(Integer)

    @property
    def can_login(self):
        """if this user is desabled"""
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readble attribute.')

    @password.setter
    def password(self, value):
        self.password_hash = User.encrypt_pwd(value)

    @property
    def base_info(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'password': self.password_hash
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
        """rely on `if_register_field_available`
           and add a level on it.

           :return dict: register info
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
    def register_user(cls, register_info, password):
        """add new user
        should use transaction
        register_info should only contain the following field:
        email, username, (country_code, phone)
        """
        filtered_register_info = {}
        for field in [
            'phone', 'username', 'email', 'country_code'
        ]:
            value = register_info.get(field)
            if value:
                filtered_register_info.update({
                    field: value
                })

        session = SQL_Session()
        return_user = None
        try:
            user = User(**filtered_register_info)
            user.password = password
            session.add(user)
            # if have two records after committing, should also rollback.
            if cls.record_count(filtered_register_info) > 1:
                print '记录多于1条, rollback', filtered_register_info
                session.rollback()
            else:
                session.commit()
                return_user = user
        except Exception:
            print 'in register_user (will rollback)', traceback.print_exc()
            session.rollback()

        return return_user



if __name__ == '__main__':
    sql_session.query(User).all()