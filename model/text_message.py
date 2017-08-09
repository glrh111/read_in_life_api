
"""
 * message_id
 *
 * from_id
 * to_id
 * content
 *
 * if_read
 *
 * ctime
 * read_time
"""
from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT, Boolean

from lib.helpers import timestamp_by_13


class TextMessage(BaseModel):

    message_id = Column(BIGINT, primary_key=True, autoincrement=True)
    message_type = Column(BIGINT) # 1 group message; 2 c to c message

    from_id = Column(BIGINT)  # sender
    to_id = Column(BIGINT)
    content = Column(String)

    if_read = Column(Boolean, default=False)

    ctime = Column(BIGINT, default=timestamp_by_13)
    read_time = Column(BIGINT, default=None)

    @classmethod
    def fake_message(cls):
        for i in range (10):
            message = TextMessage()
            message.from_id = i
            message.to_id = 20
            message.content = "i love you" + str(i)
            message.save()


if __name__ == '__main__':
    pass
    # sql_session.query(User).all()