
from uuid import uuid1

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
    # content = Column(String, default='')  # save mark down string
    head_version = Column(String) # version in PostHistory

    available_to_other = Column(Boolean, default=True) # if available to other
    anonymous_to_other = Column(Boolean, default=False) # if penname available to other
    comment_permission = Column(Integer, default=COMMENT_PERIMISSION.ANY_USER)

    deleted = Column(Boolean, default=False)   # if user delete it

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT, default=timestamp_by_13)

    @property
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

    @base_info.setter
    def base_info(self, value):
        raise AttributeError('base_info is a read only attribute.')

    @property
    def content(self):
        spec = {
            'post_id': self.post_id,
            'version': self.head_version
        }
        post_history = PostHistory.find_one(spec)
        if post_history:
            return post_history.content
        return ''

    @content.setter
    def content(self, value):
        raise AttributeError('content is a read only attribute.')

    @classmethod
    def get_all_post(cls, offset, limit):
        """order by utime"""
        spec = {
            'deleted': False,
            'available_to_other': True
        }
        sort = [('ctime', -1)]
        post_info_list = []
        for post in cls.find(spec, sort=sort, offset=offset, limit=limit):
            post_info_list.append(
                post.base_info
            )
        return post_info_list

    @classmethod
    def get_post_by_id(cls, post_id):
        """if is benren?"""
        spec = { 'post_id': int(post_id), 'deleted': False }
        post = cls.find_one(spec)
        return post if post else None

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
    def update_content(cls, post_id, content):
        """1. new a PostHistory and get its `version`
           2. update Post.head_version
        """
        # 1
        post_history = PostHistory.add_post_history(
            post_id, content
        )
        if not post_history:
            return None
        # 2
        new_post = cls.find_and_modify(
            spec={'post_id': post_id},
            update={
                'head_version': post_history.version,
                'utime': timestamp_by_13()
            }
        )
        if not new_post:
            print 'in Model.update_content', post_id, post_history, new_post
            return None
        print 'new_post', new_post
        return new_post

    @classmethod
    def update_post(cls, post_id, **kwargs):
        """update: content, and permission"""
        default_type_dict = {
            # 'content': str, # remove content here because ...much to say
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

        update_dict.update({
            'utime': timestamp_by_13()
        })

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


class PostHistory(BaseModel):
    """all modify history of post"""
    post_id = Column(Integer, primary_key=True)
    version = Column(String, primary_key=True)  # every time modify this post: uuid
    # parent_version = Column(Integer) # its father's parent_version. or None when its new

    content = Column(String, default='')  # save mark down string

    ctime = Column(BIGINT, default=timestamp_by_13)

    @classmethod
    def new_version(cls):
        return str(uuid1())

    @classmethod
    def add_post_history(cls, post_id, content):
        """1. new a version
           2. new a cls()
        """
        version = cls.new_version()
        record = cls(**{
            'post_id': post_id,
            'version': version,
            'content': content
        })
        re_record = None
        try:
            SQL_Session().add(record)
            SQL_Session().commit()
            re_record = cls.find_one({
                'post_id': post_id,
                'version': version
            })
        except Exception:
            SQL_Session().rollback()

        return re_record



# class PostLabel(BaseModel):
#     """post_id: label, deleted"""
#     label_id = Column(Integer, primary_key=True, autoincrement=True)
#     post_id = Column(Integer)
#
#     ctime = Column(BIGINT, default=timestamp_by_13)
#     utime = Column(BIGINT)


if __name__ == '__main__':
    pass
    # sql_session.query(User).all()