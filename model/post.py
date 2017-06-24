
from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT, \
    Boolean

from lib.helpers import timestamp_by_13


class Post(BaseModel):

    post_id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer) # relate to User.user_id
    content = Column(String)  # save mark down string

    available = Column(Boolean, default=True) # if available by other
    deleted = Column(Boolean, default=False)   # if user delete it

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT, default=timestamp_by_13)


    def base_info(self):
        return {
            'post_id': self.post_id,
            'content': self.content
        }

    @classmethod
    def add_post(cls):
        pass


class PostLabel(BaseModel):
    """post_id: label, deleted"""
    label_id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer)

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT)
    pass


if __name__ == '__main__':
    pass
    # sql_session.query(User).all()