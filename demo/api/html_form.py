from pytest_requests import HttpRequest


class ApiHttpBinPostHtmlForm(HttpRequest):

    method = HttpRequest.EnumHttpMethod.POST
    url = "http://httpbin.org/post"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = "custname={custname}&custtel={custtel}&custemail=m%40test.com&size=small&topping=cheese&topping=mushroom&delivery=14%3A30&comments=hello+world"


class ApiHttpBinPostJson(HttpRequest):

    method = HttpRequest.EnumHttpMethod.POST
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
