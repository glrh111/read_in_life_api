
from lib.web.model.sql_db import sql_session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String


class User(BaseModel):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    nickname = Column(String)

user = User(**{
    'nickname': 'wangli'
})

sql_session.add(user)
sql_session.commit()

user_list = sql_session.query(User).all()
for user_1 in user_list:
    print user_1.nickname, user_1.user_id



if __name__ == '__main__':
    sql_session.query(User).all()