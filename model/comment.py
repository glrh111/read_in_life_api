
from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT

from lib.helpers import timestamp_by_13


class Comment(BaseModel):

    comment_id = Column(Integer, primary_key=True, autoincrement=True)

    content = Column(String)  # its markdown? no, take it as original string

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT, default=timestamp_by_13)


    def base_info(self):
        return {
            'post_id': self.post_id,
            'content': self.content
        }


if __name__ == '__main__':
    pass
    # sql_session.query(User).all()