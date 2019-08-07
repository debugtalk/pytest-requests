from pytest_requests.api import BaseApi


class ApiHttpbinGet(BaseApi):

    url = "http://httpbin.org/get"
    params = {
        "abc": "111",
        "de": "222"
    }
    method = "GET"
    headers = {"accept": "application/json"}


class ApiHttpBinPost(BaseApi):

    url = "http://httpbin.org/post"
    method = "POST"
    headers = {"accept": "application/json"}
    body = {"abc": 123}


class ApiHttpBinGetCookies(BaseApi):

    url = "http://httpbin.org/cookies"
    method = "GET"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(BaseApi):

    url = "http://httpbin.org/cookies/set"
    method = "GET"
    headers = {"accept": "text/plain"}
