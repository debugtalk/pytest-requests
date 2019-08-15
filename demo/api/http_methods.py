from pytest_requests import HttpRequest


class ApiHttpbinGet(HttpRequest):

    method = HttpRequest.EnumHttpMethod.GET
    url = "http://httpbin.org/get"
    params = {
        "abc": "111",
        "de": "222"
    }
    headers = {"accept": "application/json"}


class ApiHttpBinPost(HttpRequest):

    method = HttpRequest.EnumHttpMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    body = {"abc": 123}
