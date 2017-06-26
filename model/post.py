
from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT, \
    Boolean

from model.user import User

from lib.helpers import timestamp_by_13
from lib.jsob import JsOb


COMMENT_PERIMISSION = JsOb({
    'ANY_USER': 1,
    'ONLY_FOLLOWER': 2,
    'ONLY_FOLLOWING': 3,
    'NO_ONE': 4,    # forbidden
})

class Post(BaseModel):

    post_id = Column(Integer, primary_key=True, autoincrement=True)  # dont set it by hand

    user_id = Column(Integer) # relate to User.user_id
    content = Column(String, default='')  # save mark down string

    available_to_other = Column(Boolean, default=True) # if available to other
    anonymous_to_other = Column(Boolean, default=False) # if penname available to other
    comment_permission = Column(Integer, default=COMMENT_PERIMISSION.ANY_USER)

    deleted = Column(Boolean, default=False)   # if user delete it

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT, default=timestamp_by_13)

    def base_info(self):
        """author_info

        :return:
        """
        # not available
        if not self.available_to_other:
            return {}

        user_info = {}
        if self.anonymous_to_other:
            user_info = User.get_anonymous_user_base_info()
        else:
            user = User.find_one({ 'user_id': self.user_id })
            if user:
                user_info = user.base_info

        return {
            'post_id': self.post_id,
            'content': self.content,
            'user_info': user_info
        }

    @classmethod
    def add_post(
            cls,
            user_id,
            available_to_other=True,
            anonymous_to_other=False,
            comment_permission=COMMENT_PERIMISSION.ANY_USER
    ):
        post = cls(**{
            'user_id': user_id,
            'available_to_other': bool(available_to_other),
            'anonymous_to_other': bool(anonymous_to_other),
            'comment_permission': int(comment_permission),
        })
        session = SQL_Session()
        return_post = None
        try:
            session.add(post)
            session.commit()
            return_post = post
        except Exception:
            session.rollback()

        return return_post

    @classmethod
    def update_post(cls, post_id, **kwargs):
        """update: content, and permission"""
        default_type_dict = {
            'content': str,
            'available_to_other': bool,
            'anonymous_to_other': bool,
            'comment_permission': int
        }

        update_dict = {

        }
        for key, type_handler in default_type_dict.items():
            value = kwargs.get(key)
            if value:

                if 'comment_permission' == key:
                    if value not in COMMENT_PERIMISSION.values():
                        return None

                update_dict.update({
                    key: type_handler(value)
                })

        # do update
        if not update_dict:
            return None

        return cls.find_and_modify(
            spec={'post_id': post_id},
            update=update_dict
        )

    @classmethod
    def delete_post(cls, post_id):
        """delete a post"""
        return cls.find_and_modify(
            spec={'post_id': post_id},
            update={ 'deleted': True }
        )


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