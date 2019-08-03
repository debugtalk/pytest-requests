from hogwarts_apitest.api import BaseApi

def test_version():
    from hogwarts_apitest import __version__
    assert isinstance(__version__, str)

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
    data = "abc=123"
    json = {"abc": 123}


def test_httpbin_get():
    ApiHttpbinGet().run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get")\
        .validate("json().args", {})\
        .validate("json().headers.Accept", 'application/json')


def test_httpbin_get_with_prams():
    ApiHttpbinGet()\
        .set_params(abc=123, xyz=456)\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get?abc=123&xyz=456")\
        .validate("json().headers.Accept", 'application/json')


def test_httpbin_post():
    ApiHttpBinPost()\
        .set_json({"abc": 456})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')
