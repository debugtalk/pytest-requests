from pytest_requests.api import HttpRequest, EnumMethod


class ApiHttpbinGet(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/get"
    params = {
        "abc": "111",
        "de": "222"
    }
    headers = {"accept": "application/json"}


class ApiHttpBinPost(HttpRequest):

    method = EnumMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    body = {"abc": 123}
