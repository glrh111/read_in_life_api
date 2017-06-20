
import hashlib

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String

from lib.serve.config import app_config

class User(BaseModel):

    user_id = Column(Integer, primary_key=True)

    # could login via those three field
    country_code = Column(String, default='')
    phone = Column(String, default='')
    username = Column(String, default='')
    email = Column(String, default='')

    password = Column(String)

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

    @classmethod
    def _is_password_available(cls, password):
        if not isinstance(password, str):
            return False
        return bool(password)

    @classmethod
    def modify_password(cls, user, new_password):
        """False True"""
        if not cls._is_password_available(new_password):
            return False

        user.password = cls.encrypt_pwd(new_password)
        SQL_Session().commit()

    @classmethod
    def encrypt_pwd(cls, password):
        m = hashlib.md5(app_config.PASSWORD_SECRET)
        m.update(password)
        password = m.hexdigest()
        return password

    @classmethod
    def verify_user(cls, user, password):
        return user.password == cls.encrypt_pwd(password)

    def base_info(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname
        }

    @property
    def can_login(self):
        """if this user is desabled"""
        return True

    @classmethod
    def if_register_field_available(cls, register_info):
        """register_info: dict"""
        pass

    @classmethod
    def register_user(cls):
        """add new user. its a transaction"""
        pass




if __name__ == '__main__':
    sql_session.query(User).all()