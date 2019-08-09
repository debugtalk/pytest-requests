from pytest_requests.api import HttpRequest, EnumMethod


class ApiHttpBinGetRedirect302(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/redirect-to"
    params = {
        "url": "https://debugtalk.com",
        "status_code": 302
    }
