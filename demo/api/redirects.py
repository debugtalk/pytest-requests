from pytest_requests.api import HttpRequest, EnumHttpMethod


class ApiHttpBinGetRedirect302(HttpRequest):

    method = EnumHttpMethod.GET
    url = "http://httpbin.org/redirect-to"
    params = {
        "url": "https://debugtalk.com",
        "status_code": 302
    }
