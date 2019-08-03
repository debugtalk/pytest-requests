from hogwarts_apitest.api import BaseApi


class ApiHttpbinGet(BaseApi):

    url = "http://httpbin.org/get"
    params = {}
    method = "GET"
    headers = {"accept": "application/json"}


class ApiHttpBinPost(BaseApi):

    url = "http://httpbin.org/post"
    method = "POST"
    params = {}
    headers = {"accept": "application/json"}
    json = {"abc": 123}


class ApiHttpBinGetCookies(BaseApi):

    url = "http://httpbin.org/cookies"
    method = "GET"
    params = {}
    headers = {"accept": "application/json"}
