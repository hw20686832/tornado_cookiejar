import time
try:
    from cookielib import Cookie
except:
    from http.cookiejar import Cookie

from tornado.httpclient import HTTPRequest


def cookiejar_from_simplecookie(cookie, cookiejar):
    for c in cookie.values():
        expires = c['expires']
        expires_time = None
        if expires:
            try:
                expires_time = time.strptime(expires,
                                             '%a, %d-%b-%y %H:%M:%S %Z')
                expires_time = time.mktime(expires_time)
            except:
                # For Python Cookies bug.
                pass

        ck = Cookie(
            c['version'] or None,
            c.key, c.value, None, None,
            c['domain'], None, None,
            c['path'], None, c['secure'] or None,
            expires_time, None, c['comment'] or None,
            None, {}
        )
        cookiejar.set_cookie(ck)

    return cookiejar


def parse_cookiejar(cookiejar):
    if cookiejar:
        return '; '.join("%s=%s" % (c.name, c.value) for c in cookiejar)


class CookieJarRequest(HTTPRequest):
    def __init__(self, url, cookie=None, **kwargs):
        self.cookie = cookie
        super(CookieJarRequest, self).__init__(url, **kwargs)
