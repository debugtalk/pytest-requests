from pytest_requests.api import HttpRequest, EnumMethod


class ApiHttpBinGetCookies(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies/set"
    headers = {"accept": "text/plain"}
