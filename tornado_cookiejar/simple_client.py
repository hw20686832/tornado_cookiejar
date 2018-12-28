# coding:utf-8
import time
try:
    from Cookie import SimpleCookie
except:
    from http.cookies import SimpleCookie

from tornado.concurrent import Future
from tornado import httputil, stack_context
from tornado.simple_httpclient import SimpleAsyncHTTPClient
from tornado.httpclient import (HTTPRequest, HTTPResponse,
                                HTTPError, _RequestProxy)

from .cookie import (CookieJarRequest, parse_cookiejar,
                     cookiejar_from_simplecookie)


class SimpleCookieJarClient(SimpleAsyncHTTPClient):
    def fetch(self, request, callback=None, raise_error=True, **kwargs):
        if self._closed:
            raise RuntimeError("fetch() called on closed AsyncHTTPClient")
        if not isinstance(request, HTTPRequest):
            request = CookieJarRequest(
                url=request,
                cookie=kwargs.pop('cookie', None),
                **kwargs
            )
        else:
            if kwargs:
                raise ValueError("kwargs can't be used if request is an HTTPRequest object")
        # We may modify this (to add Host, Accept-Encoding, etc),
        # so make sure we don't modify the caller's object.  This is also
        # where normal dicts get converted to HTTPHeaders objects.
        _headers = httputil.HTTPHeaders(request.headers)
        cookiejar = request.cookie
        cookie_str = parse_cookiejar(cookiejar)
        if cookie_str:
            _headers['Cookie'] = cookie_str
        request.headers = _headers
        request = _RequestProxy(request, self.defaults)
        future = Future()
        if callback is not None:
            callback = stack_context.wrap(callback)

            def handle_future(future):
                exc = future.exception()
                if isinstance(exc, HTTPError) and exc.response is not None:
                    response = exc.response
                elif exc is not None:
                    response = HTTPResponse(
                        request, 599, error=exc,
                        request_time=time.time() - request.start_time)
                else:
                    response = future.result()
                self.io_loop.add_callback(callback, response)
            future.add_done_callback(handle_future)

        def handle_response(response):
            if raise_error and response.error:
                future.set_exception(response.error)
            else:
                if cookiejar is not None:
                    cookies = response.headers.get_list("Set-Cookie")
                    sc = SimpleCookie()
                    for c in cookies:
                        sc.load(c)
                    cookiejar.clear()
                    _cookiejar = cookiejar_from_simplecookie(sc, cookiejar)
                    response.cookie = _cookiejar
                future.set_result(response)
        self.fetch_impl(request, handle_response)
        return future
