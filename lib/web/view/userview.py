
from error import UserDisabled, LoginRequired
from baseview import BaseView
from lib.web.model.session import Session
from lib.web.model.redis_db import redis

from lib.serve.config import app_config


class UserView(BaseView):
    '''view with session
    '''

    def _session_new(self, user_id):
        session = Session.new(user_id, app_config.SESSION_EXPIRE)
        self.set_cookie('session', session, domain="." + app_config.HOST,
                        expires_days=app_config.SESSION_EXPIRE)

    def _session_rm(self):
        self.clear_cookie('session', domain="." + app_config.HOST)
        Session.rm(self.current_user_id)

    def get_current_user(self):
        if self.current_user_id:
            user = User.find_one(dict(user_id=self.current_user_id))
            if user is not None:
                return user
            else:
                self.clear_cookie('session', domain="." + app_config.HOST)
                self.current_user_id = 0
                return None

    def login(self, user):
        if user.can_login:
            self._session_new(user.user_id)
        else:
            raise UserDisabled()

    @property
    def current_user_id(self):
        if not hasattr(self, '_current_user_id'):
            s = self.get_cookie('session')
            self._current_user_id = _current_user_id = Session.id_by_b64(s)
            if s and not _current_user_id:
                self.clear_cookie('session', domain="." + app_config.HOST)
        return self._current_user_id or 0

    @current_user_id.setter
    def current_user_id(self, value):
        self._current_user_id = value


class LoginView(UserView):
    '''need login
    '''

    def prepare(self):
        if not self.get_current_user():
            raise LoginRequired()
            # self.redirect('/login')
        super(LoginView, self).prepare()