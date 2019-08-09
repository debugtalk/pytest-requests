from pytest_requests.api import HttpRequest, EnumHttpMethod


class ApiHttpbinGet(HttpRequest):

    method = EnumHttpMethod.GET
    url = "http://httpbin.org/get"
    params = {
        "abc": "111",
        "de": "222"
    }
    headers = {"accept": "application/json"}


class ApiHttpBinPost(HttpRequest):

    method = EnumHttpMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    body = {"abc": 123}
