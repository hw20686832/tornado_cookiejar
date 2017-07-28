# tornado_cookiejar
Cookiejar with AsyncHTTPClient support on tornado

# Usage
### Install
```
pip install tornado-cookiejar
```
### Code
```python
from http.cookiejar import CookieJar

AsyncHTTPClient.configure("tornado_cookiejar.SimpleCookieJarClient")

class IndexHandler(RequestHandler):

    @coroutine
    def get(self):
        cli = AsyncHTTPClient()
        cookiejar = CookieJar("cookie.txt")
        response = yield cli.fetch("http://www.baidu.com/", cookie=cookiejar)
        print(cookiejar)
        print(response.cookie)
        self.write(response.body)
```

or you can use request object
```python
from http.cookiejar import CookieJar

from tornado_cookiejar import CookieJarRequest

AsyncHTTPClient.configure("tornado_cookiejar.SimpleCookieJarClient")

class IndexHandler(RequestHandler):

    @coroutine
    def get(self):
        cli = AsyncHTTPClient()
        cookiejar = CookieJar("cookie.txt")
        req = CookieJarRequest("http://www.baidu.com/", cookie=cookiejar)
        response = yield cli.fetch(req)
        print(cookiejar)
        print(response.cookie)
        self.write(response.body)
```
