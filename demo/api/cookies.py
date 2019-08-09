from pytest_requests.api import HttpRequest, EnumHttpMethod


class ApiHttpBinGetCookies(HttpRequest):

    method = EnumHttpMethod.GET
    url = "http://httpbin.org/cookies"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(HttpRequest):

    method = EnumHttpMethod.GET
    url = "http://httpbin.org/cookies/set"
    headers = {"accept": "text/plain"}
