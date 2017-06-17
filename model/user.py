
from lib.web.model.sql_db import sql_session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String


class User(BaseModel):

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)
    heihei = Column(String)
    wocaonidayue = Column(Integer)


    def base_info(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname
        }

    @classmethod
    def can_login(cls):
        return True


if __name__ == '__main__':
    sql_session.query(User).all()