from pytest_requests import HttpRequest


class ApiHttpBinGetRedirect302(HttpRequest):

    method = HttpRequest.EnumHttpMethod.GET
    url = "http://httpbin.org/redirect-to"
    params = {
        "url": "https://debugtalk.com",
        "status_code": 302
    }
