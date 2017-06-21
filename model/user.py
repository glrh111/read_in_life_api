
import hashlib

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String

from lib.serve.config import app_config

class User(BaseModel):

    user_id = Column(Integer, primary_key=True)  # do not set this by hand

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

    @property
    def can_login(self):
        """if this user is desabled"""
        return True

    def base_info(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'password': self.password
        }

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
        user.save()

    @classmethod
    def encrypt_pwd(cls, password):
        m = hashlib.md5(app_config.PASSWORD_SECRET)
        m.update(password)
        password = m.hexdigest()
        return password

    @classmethod
    def verify_user(cls, user, password):
        return user.password == cls.encrypt_pwd(password)

    @classmethod
    def if_register_field_available(cls, spec):
        """add new user. its a transaction
           spec is like this:
           {phone: wocao, country: nidaye}
        """
        return not bool(cls.find_one(spec))

    @classmethod
    def register_user(cls, spec):
        pass
        pass


# modify a password
print 'in user.model'
user = User.find_one({'user_id': 1})

print user.base_info()

User.modify_password(user, 'wocaonidaye')
user2 = User.find_one({'user_id': 1})
print user2.base_info()

print User.verify_user(user2, 'niday2e')

User(**{
    'nickname': 'hahah'
}).save()

print User.find_one({'nickname': 'hahah'}).base_info()



if __name__ == '__main__':
    sql_session.query(User).all()