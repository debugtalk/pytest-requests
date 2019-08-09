from pytest_requests import HttpRequest, EnumHttpMethod


class ApiHttpBinGetJson(HttpRequest):

    method = EnumHttpMethod.GET
    url = "https://httpbin.org/json"

