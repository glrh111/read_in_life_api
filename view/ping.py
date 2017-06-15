from lib.web.route import Route
from tornado.web import RequestHandler

ping_route = Route(prefix='/ping')

@ping_route('/ping')
class PingTest(RequestHandler):
    def get(self):
        self.finish('pong from ping.ping')