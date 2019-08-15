from pytest_requests import HttpRequest


class ApiHttpBinGetJson(HttpRequest):

    method = HttpRequest.EnumHttpMethod.GET
    url = "https://httpbin.org/json"

