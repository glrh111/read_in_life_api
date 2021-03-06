"""
JsonView
    JsonPostView
        JsonSignatureView
    JsonQueryView
    JsonCommonView
"""

import ujson
from tornado.web import HTTPError, gen
import traceback
import sys

from error import DictError
from baseview import BaseView
from lib.serve.config import app_config
from lib.jsob import JsOb, StripJsOb
from lib.signature import make_signature, signature_verify
from lib.serve.config import app_config


def write_error(self, status_code, **kwargs):
    traceback.print_exc()
    self.set_header('Content-Type', 'application/json; charset=UTF-8')
    self.finish(
        {
            'code': 2,
            'message': ''.join(
                traceback.format_exception(
                    *sys.exc_info())) if app_config.DEBUG else self._reason
        }
    )


class JsonView(BaseView):

    SUPPORTED_METHODS = ('POST', 'GET')

    write_error = write_error

    def prepare(self):
        self.content_type = self.request.headers.get('content-type')
        super(JsonView, self).prepare()

    def get_all_method(self):
        old = self.SUPPORTED_METHODS
        if 0 == len(old):
            old = []
        else:
            if not isinstance(old, tuple):
                old = [old]
            else:
                old = list(old)
        return old + ['OPTIONS']

    @gen.coroutine
    def _execute(self, transforms, *args, **kwargs):
        self._transforms = transforms
        try:
            if self.request.method not in self.get_all_method():
                raise HTTPError(405)
            try:
                result = self.prepare()
                if result is not None:
                    result = yield result
            except DictError as e:
                self.finish(e.dump())

            if self._prepared_future is not None:
                self._prepared_future.set_result(None)
            if self._finished:
                return

            args = [self.decode_argument(arg) for arg in args]
            kwargs = dict((k, self.decode_argument(v, name=k))
                          for (k, v) in kwargs.iteritems())
            if hasattr(self, 'init'):
                getattr(self, 'init')(*args, **kwargs)
            try:
                method = getattr(self, self.request.method.lower())
                result = method(*args, **kwargs)
                if result is not None:
                    yield result
            except DictError as e:
                # self._handle_request_exception(e)
                self.finish(e.dump())

            if self._auto_finish and not self._finished:
                self.finish()
        except Exception, e:
            self._handle_request_exception(e)

    def render(self, chunk):
        default_response = {
            'code': 1,
            'message': 'OK'
        }
        if not chunk:
            chunk = default_response
        chunk.update(default_response)
        self.finish(chunk)

    def finish(self, chunk=None):
        chunk = chunk or ''
        # callback = self.get_argument('callback', None)
        # if callback:  # this is done for jsonp, but I don't care
        #     if type(chunk) is dict:
        #         chunk = ujson.dumps(chunk, ensure_ascii=False)
        #     chunk = '%s(%s)' % (callback, chunk)
        self.set_header('Content-Type', 'application/json; charset=UTF-8')

        # write origin
        self.set_header('Access-Control-Allow-Origin', app_config.CORS_STRING)
        self.set_header('Access-Control-Request-Method', 'GET,POST,PUT,DELETE')
        self.set_header('Access-Control-Allow-Methods', ','.join(self.get_all_method()) )
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Access-Control-Allow-Headers', 'X-PINGOTHER, Content-Type')

        if isinstance(chunk, dict):
            super(JsonView, self).finish(ujson.dumps(chunk, ensure_ascii=False))
        else:
            super(JsonView, self).finish(chunk)

    def options(self, *args, **kwargs):
        self.set_header('Allow', ','.join(self.get_all_method()) )
        self.finish()


class JsonPostView(JsonView):

    SUPPORTED_METHODS = ('POST')

    @property
    def json(self):
        if not self.request.body:
            return JsOb()
        try:
            return StripJsOb(
                **ujson.loads(self.request.body.decode('utf-8', 'ignore')))
        except ValueError as e:
            raise HTTPError(400, reason="%s, may be bad json" % str(e))


class JsonQueryView(JsonView):

    def prepare(self):
        query_ = self.request.query_arguments
        self.query = JsOb(**{k: query_[k][0] for k in query_.iterkeys()})
        super(JsonQueryView, self).prepare()


class JsonCommonView(JsonView):
    @property
    def json(self):
        if not self.request.body:
            return JsOb()
        try:
            return StripJsOb(
                **ujson.loads(self.request.body.decode('utf-8', 'ignore')))
        except ValueError as e:
            raise HTTPError(400, reason="%s, may be bad json" % str(e))

    @property
    def query(self):
        query_ = self.request.query_arguments
        return JsOb(**{k: query_[k][0] for k in query_.iterkeys()})


class JsonSignatureView(JsonPostView):
    '''json view with signature
    '''
    def prepare(self):
        super(JsonPostView, self).prepare()
        data = ujson.loads(self.request.body.decode('utf-8', 'ignore'))
        signature = data.pop('signature', None)
        if not app_config.DEBUG and not signature_verify(
                data,
                signature,
                app_config.SIGNATURE_SECRET
        ):
            raise HTTPError(403)