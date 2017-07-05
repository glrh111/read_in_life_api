#! /usr/bin/env python
# coding: utf-8

import inspect
from uuid import uuid1
import functools

from lib.web.model.sql_db import SQL_Session, BaseModel
from sqlalchemy import Column, Integer, ForeignKey, String, BIGINT, \
    Boolean

from model.user import User
from lib.web.view.error import OperationNotPermit

from lib.helpers import timestamp_by_13
from lib.jsob import JsOb


COMMENT_PERIMISSION = JsOb({
    'ANY_USER': 1,
    'ONLY_FOLLOWER': 2,
    'ONLY_FOLLOWING': 3,
    'NO_ONE': 4,    # forbidden
})


def check_post_update_permission(f):
    """only its user_id has update permission"""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        func_args = inspect.getcallargs(f, *args, **kwargs)
        # get post_id and current_user_id from self
        post_id = int(func_args.get('post_id') or 0)
        self = func_args.get('self')
        current_user_id = getattr(self, 'current_user_id')
        # check permission
        post = Post.find_one({'post_id': post_id})
        if post and current_user_id and post.user_id == current_user_id:
            return f(*args, **kwargs)
        raise OperationNotPermit
    return wrapper


class Post(BaseModel):

    post_id = Column(Integer, primary_key=True, autoincrement=True)  # dont set it by hand

    user_id = Column(Integer) # relate to User.user_id
    # content = Column(String, default='')  # save mark down string
    head_version = Column(String) # version in PostHistory

    title = Column(String)     # could edit
    abstract = Column(String)  # displayed on post list

    available_to_other = Column(Boolean, default=False) # if available to other
    # anonymous_to_other = Column(Boolean, default=False) # if penname available to other; delete by glrh11 in 20170703
    comment_permission = Column(Integer, default=COMMENT_PERIMISSION.ANY_USER)

    deleted = Column(Boolean, default=False)   # if user delete it

    ctime = Column(BIGINT, default=timestamp_by_13)
    utime = Column(BIGINT, default=timestamp_by_13)

    @property
    def base_info(self):
        """author_info
        """
        # not available
        if self.deleted:
            return {}

        return {
            'post_id': self.post_id,
            'content': self.content,
            'title': self.title,
            'abstract': self.abstract,
            'utime': self.utime,
            'is_available_to_other': self.available_to_other
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
    def attach_user_info(cls, post):
        """1"""
        user_info = {}
        user = User.find_one({'user_id': post.user_id})
        if user:
            user_info = user.base_info
        return user_info

    @classmethod
    def _get_a_post(cls, post_id, observer=None):
        spec = {'post_id': int(post_id), 'deleted': False}
        post = cls.find_one(spec)
        if post:
            post_info = post.base_info
            user_info = cls.attach_user_info(post)
            post_info.update({
                'user_info': user_info,
                'is_self': True if observer and (observer.user_id == post.user_id) else False
            })
            return post_info
        else:
            return None

    @classmethod
    def _get_post_list(cls, spec, offset, limit, observer=None):
        """observer 是查看文章列表的人。如果是作者本人，用一个字段is_self标识出来。
           方便前端做出某些判断。
        """
        sort = [('ctime', -1)]
        post_info_list = []
        for post in cls.find(spec, sort=sort, offset=offset, limit=limit):
            post_info = post.base_info
            user_info = cls.attach_user_info(post)
            post_info.update({
                'user_info': user_info,
                'is_self': True if observer and (observer.user_id == post.user_id) else False
            })

            post_info_list.append(
                post_info
            )
        return post_info_list

    # 个人主页看到的文章列表. 区别对待别人看自己，和自己看自己
    # get_user_post_by_self
    # get_user_post_by_other

    @classmethod
    def get_user_post_by_self(cls, user, offset, limit):
        """用户本人看到的自己的文章列表"""
        spec_published = {
            'user_id': user.user_id,
            'available_to_other': True,
            'deleted': False
        }
        spec_not_published = {
            'user_id': user.user_id,
            'available_to_other': False,
            'deleted': False
        }

        return {
            'published': cls._get_post_list(spec_published, offset=offset, limit=limit, observer=user),
            'not_published': cls._get_post_list(spec_not_published, offset=offset, limit=limit, observer=user)
        }

    @classmethod
    def get_user_post_by_other(cls, user, offset, limit, observer=None):
        """别人(observer)看到的自己(user)的文章列表
           别人与自己看到的，有区别。
        """
        # 判断是否是本人
        if observer and observer.user_id == user.user_id:
            return cls.get_user_post_by_self(user=user, offset=offset, limit=limit)
        spec_published = {
            'user_id': user.user_id,
            'available_to_other': True,
            'deleted': False
        }

        return {
            'published': cls._get_post_list(spec_published, offset=offset, limit=limit, observer=observer),
        }

    @classmethod
    def get_timeline_post(cls, offset, limit, observer=None):
        """用户时间线上，看到的文章列表。所有用户的文章倒序排列。"""
        spec = {
            'deleted': False,
            'available_to_other': True
        }
        return cls._get_post_list(spec, offset, limit, observer=observer)

    @classmethod
    def get_post_by_id(cls, post_id, observer=None):
        """需要判断是否是本人"""
        return cls._get_a_post(post_id=post_id, observer=observer)

    @classmethod
    def add_post(
            cls,
            user_id,
            available_to_other=False,
            comment_permission=COMMENT_PERIMISSION.ANY_USER
    ):
        post = cls(**{
            'user_id': user_id,
            'available_to_other': bool(available_to_other),
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
    def update_content_info(cls, post_id, content_info):
        """1. new a PostHistory and get its `version`
           2. update Post.head_version

           update in 2017-07-05 could update <title, abstract>
        """

        content = content_info.get('content')
        re_post = None
        if content:
            # 1
            post_history = PostHistory.add_post_history(
                post_id, content
            )
            if post_history:
                # 2
                new_post = cls.find_and_modify(
                    spec={'post_id': post_id},
                    update={
                        'head_version': post_history.version,
                        'utime': timestamp_by_13()
                    }
                )
                if new_post:
                    re_post = new_post

        update_info = {}
        for field in ['title', 'abstract']:
            value = content_info.get(field)
            if value:
                update_info.update({
                    field: value
                })
        if update_info:
            update_info.update({
                'utime': timestamp_by_13()
            })
            new_post = cls.find_and_modify(
                spec={'post_id': post_id},
                update=update_info
            )
            if new_post:
                re_post = new_post

        return re_post

    @classmethod
    def update_other_info(cls, post_id, **kwargs):
        """update: permission and title, abstract"""
        default_type_dict = {
            # 'content': str, # remove content here because ...much to say
            'available_to_other': bool,
            # 'anonymous_to_other': bool,
            'comment_permission': int,

            'title': None,
            'abstract': None
        }

        update_dict = {

        }
        for key, type_handler in default_type_dict.items():
            try:
                value = kwargs.get(key)
                if value not in [None, '']:

                    if 'comment_permission' == key:
                        if value not in COMMENT_PERIMISSION.values():
                            continue
                    value = type_handler(value) if type_handler else value
                    update_dict.update({
                        key: value
                    })
            except Exception:
                pass

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
            update={ 'deleted': True, 'utime': timestamp_by_13() }
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