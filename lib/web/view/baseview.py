"""
this BaseView do nothing. But add a layer to tornado and actually used.
"""

import sys
import traceback
import httplib
from tornado.web import RequestHandler
from tornado import escape
from tornado.httpclient import HTTPError

from lib.serve.config import app_config

def json_encode(value):
    """JSON-encodes the given Python object."""
    # JSON permits but does not require forward slashes to be escaped.
    # This is useful when json data is emitted in a <script> tag
    # in HTML, as it prevents </script> tags from prematurely terminating
    # the javscript.  Some json libraries do this escaping by default,
    # although python's standard library does not, so we do it here.
    # http://stackoverflow.com/questions/1580647/json-why-are-forward-slashes-escaped
    try:
        s = yajl.dumps(value)
    except:
        s = json.dumps(value, ensure_ascii=False)
    return s.replace("</", "<\\/")

escape.json_encode = json_encode

def write_json_error(self, status_code, **kwargs):
    self.set_header('Content-Type', 'application/json; charset=UTF-8')
    self.write(
        {
            'code': status_code,
            'message': ''.join(
                traceback.format_exception(
                    *sys.exc_info())) if app_config.DEBUG else self._reason
        }
    )

def write_html_error(self, status_code, **kwargs):
    # from solo.web.render import render as _render
    # if status_code == 404:
    #     path = join(APP, 'base/error/404.html')
    #     html = _render(path)
    #     return self.write(html)
    # if status_code == 500:
    #     path = join(APP, 'base/error/500.html')
    #     html = _render(path)
    #     return self.write(html)
    # if self.settings.get('debug') and \
    #         ('exc_info' in kwargs or 'exception' in kwargs):
    #     # in debug mode, try to send a traceback
    #     self.set_header('Content-Type', 'text/plain')
    #     for line in traceback.format_exception(*sys.exc_info()):
    #         self.write(line)
    # else:
    message = kwargs.get('message', httplib.responses[status_code])
    html = '<html><title>%(code)s : %(message)s</title><body>%(code)s : %(message)s</body></html>' % {
        'code': status_code,
        'message': message,
    }
    self.write(html)

def write_error(self, status_code, **kwargs):
    if self.request.headers.get('accept').startswith('application/json'):
        write_json_error(self, status_code, **kwargs)
    else:
        write_html_error(self, status_code, **kwargs)


class BaseView(RequestHandler):

    pass