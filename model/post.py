
from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String


class Post(BaseModel):

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)


    def base_info(self):
        return {
            'post_id': self.post_id,
            'content': self.content
        }


if __name__ == '__main__':
    pass
    # sql_session.query(User).all()