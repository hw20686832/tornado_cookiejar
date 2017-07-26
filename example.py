# coding:utf-8
try:
    from cookielib import CookieJar
except:
    from http.cookiejar import CookieJar

from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from tornado.httpclient import AsyncHTTPClient

AsyncHTTPClient.configure("tornado_cookiejar.SimpleCookieJarClient")


@coroutine
def run():
    cookiejar = CookieJar()
    cli = AsyncHTTPClient()
    response = yield cli.fetch("http://www.baidu.com", cookie=cookiejar)
    print(response.code)
    print(cookiejar)

IOLoop.current().run_sync(run)
