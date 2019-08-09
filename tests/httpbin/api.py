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


class ApiHttpBinGetCookies(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies"
    headers = {"accept": "application/json"}


class ApiHttpBinGetSetCookies(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/cookies/set"
    headers = {"accept": "text/plain"}


class ApiHttpBinGetRedirect302(HttpRequest):

    method = EnumMethod.GET
    url = "http://httpbin.org/redirect-to"
    params = {
        "url": "https://debugtalk.com",
        "status_code": 302
    }


class ApiHttpBinGetJson(HttpRequest):

    method = EnumMethod.GET
    url = "https://httpbin.org/json"


class ApiHttpBinPostHtmlForm(HttpRequest):

    method = EnumMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = "custname={custname}&custtel={custtel}&custemail=m%40test.com&size=small&topping=cheese&topping=mushroom&delivery=14%3A30&comments=hello+world"


class ApiHttpBinPostJson(HttpRequest):

    method = EnumMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    body = {
		"comments": "hello world",
		"custemail": "m@test.com",
		"custname": "{custname}",
		"custtel": "{custtel}",
		"delivery": "14:30",
		"size": "small",
		"topping": [
			"cheese",
			"mushroom"
        ]
	}
