from pytest_requests import HttpRequest


class ApiHttpBinGetCookies(HttpRequest):

    method = HttpRequest.EnumHttpMethod.GET
    url = "http://httpbin.org/cookies"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(HttpRequest):

    method = HttpRequest.EnumHttpMethod.GET
    url = "http://httpbin.org/cookies/set"
    headers = {"accept": "text/plain"}
