# coding:utf-8
try:
    from cookielib import MozillaCookieJar
except:
    from http.cookiejar import MozillaCookieJar

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from tornado.options import options
from tornado.httpclient import AsyncHTTPClient
from tornado.web import Application, RequestHandler

AsyncHTTPClient.configure("tornado_cookiejar.SimpleCookieJarClient")


class IndexHandler(RequestHandler):

    @coroutine
    def get(self):
        cli = AsyncHTTPClient()
        cookiejar = MozillaCookieJar("cookie.txt")
        response = yield cli.fetch("http://www.baidu.com/", cookie=cookiejar)
        print(cookiejar)
        self.write(response.body)

    def post(self):
        self.write(self.get_argument('name'))


def run():
    app = Application(
        [
            (r'/', IndexHandler),
        ],
        debug=True
    )
    options.parse_command_line()
    http_server = HTTPServer(app)
    http_server.listen(8881)

    IOLoop.instance().start()


if __name__ == '__main__':
    run()
