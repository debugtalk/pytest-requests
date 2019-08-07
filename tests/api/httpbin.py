from pytest_requests.api import BaseApi, EnumMethod


class ApiHttpbinGet(BaseApi):

    method = EnumMethod.GET
    url = "http://httpbin.org/get"
    params = {
        "abc": "111",
        "de": "222"
    }
    headers = {"accept": "application/json"}


class ApiHttpBinPost(BaseApi):

    method = EnumMethod.POST
    url = "http://httpbin.org/post"
    headers = {"accept": "application/json"}
    body = {"abc": 123}


class ApiHttpBinGetCookies(BaseApi):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(BaseApi):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies/set"
    headers = {"accept": "text/plain"}


class ApiHttpBinGetRedirect302(BaseApi):

    method = EnumMethod.GET
    url = "http://httpbin.org/redirect-to"
    params = {
        "url": "https://debugtalk.com",
        "status_code": 302
    }


class ApiHttpBinGetJson(BaseApi):

    method = EnumMethod.GET
    url = "https://httpbin.org/json"
