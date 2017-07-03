#! /usr/bin/env python
# coding: utf-8


"""
登录系统:
登录方式: 手机号phone, 用户名, 第三方登录: username. 这三者都不许重复
如果是第三方登录: 存储openid到另一个表, 然后生成这里的相关信息.

register: 注册. 得区分下从哪里注册. 小程序 or 网页
log_in:  登录
log_out: 退出登录 清理session

"""

from lib.web.route import Route
from lib.web.view.jsonview import JsonQueryView, JsonCommonView
from lib.web.view.userview import UserView

from model.post import Post, check_post_update_permission
from lib.web.view.error import BadArgument, LoginRequired
from controller.post import PostController

post_route = Route(prefix='/post')


@post_route('/?')
class AllPost(JsonQueryView, UserView):
    """all post desc by ctime
    POST: done
    GET: done
    """
    def get(self):
        offset = int(self.query.offset or 0)
        limit = int(self.query.limit or 20)

        self.render({
            'post_list': PostController.get_timeline_post(
                offset=offset,
                limit=limit,
                observer=self.current_user
            )
        })

    def post(self):
        """add new post"""
        if not self.current_user:
            raise LoginRequired

        new_post = PostController.new_post(self.current_user_id)

        self.render({
            'post': new_post.base_info
        })


@post_route('/(?P<post_id>\d+)')
class OnePost(JsonCommonView, UserView):
    """
    GET: done
    PUT: done
    DELETE: done
    """

    SUPPORTED_METHODS = ('GET', 'PUT', 'DELETE')

    def get(self, post_id):
        self.render({
            'post': PostController.get_post_by_id(int(post_id), observer=self.current_user)
        })

    @check_post_update_permission
    def put(self, post_id):
        """update
        update_type: 1 content
                     2 permission, title, abstract
        """

        if not self.current_user:
            raise LoginRequired
        post_id = int(post_id)
        update_type = int(self.json.update_type or 0)
        if 1 == update_type:
            content = self.json.content
            result = PostController.update_content(
                post_id=post_id,
                content=content
            )

        elif 2 == update_type:
            update_info = {}
            for update_field in [
                'available_to_other',
                'comment_permission',
                'title',
                'abstract'
            ]:
                value = getattr(self.json, update_field)
                if value not in ['', None]:
                    update_info.update({
                        update_field: value
                    })

            if not update_info:
                raise BadArgument(
                    'available_to_other or anonymous_to_other or comment_permission is essential.'
                )

            result = PostController.update_permission(
                post_id=post_id,
                update_info=update_info
            )
        else:
            raise BadArgument('update_type is essential.')

        self.render({
            'post': result.base_info
        })

    @check_post_update_permission
    def delete(self, post_id):
        """logically delete a post"""
        PostController.delete_post(int(post_id))
        self.render({})