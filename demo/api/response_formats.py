from pytest_requests.api import HttpRequest, EnumMethod


class ApiHttpBinGetJson(HttpRequest):

    method = EnumMethod.GET
    url = "https://httpbin.org/json"

