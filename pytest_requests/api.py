
import copy
import json
from typing import Any, Tuple

import requests

from pytest_requests.response import ResponseObject
from pytest_requests.utils import parse_content


class EnumMethod(object):
    ''' Enum HTTP method
    '''
    GET, HEAD, POST, PUT, OPTIONS, DELETE \
        = ("GET", "HEAD", "POST", "PUT", "OPTIONS", "DELETE")


class HttpRequest(object):

    method = "GET"
    url = None
    params = None
    headers = None
    cookies = None
    body = None

    def __init__(self, session=None):
        self.__session = session or requests.sessions.Session()
        self.__kwargs = {
            "params": copy.deepcopy(self.__class__.params or {}),
            "headers": copy.deepcopy(self.__class__.headers or {}),
            "cookies": copy.deepcopy(self.__class__.cookies or {})
        }

    def config_verify(self, is_verify: bool) -> "HttpRequest":
        """ config whether to verify the server’s TLS certificate
        """
        self.__kwargs["verify"] = is_verify
        return self

    def config_timeout(self, timeout: float) -> "HttpRequest":
        """ config how many seconds to wait for the server to send data before giving up
        """
        self.__kwargs["timeout"] = timeout
        return self

    def config_proxies(self, proxies: dict) -> "HttpRequest":
        """ config dictionary mapping protocol to the URL of the proxy.
        """
        self.__kwargs["proxies"] = proxies
        return self

    def config_allow_redirects(self, is_allow_redirects: bool) -> "HttpRequest":
        """ config whether to enable GET/OPTIONS/POST/PUT/PATCH/DELETE/HEAD redirection.
        """
        self.__kwargs["allow_redirects"] = is_allow_redirects
        return self

    def config_auth(self, auth: Tuple[str, str]) -> "HttpRequest":
        """ config Basic/Digest/Custom HTTP Auth, (username, password).
        """
        self.__kwargs["auth"] = auth
        return self

    def set_querystring(self, params: dict) -> "HttpRequest":
        """ update request query params
        """
        self.__kwargs["params"].update(params)
        return self

    def set_headers(self, headers: dict) -> "HttpRequest":
        """ update request headers
        """
        self.__kwargs["headers"].update(headers)
        return self

    def set_cookies(self, cookies: dict) -> "HttpRequest":
        """ update request cookies
        """
        self.__kwargs["cookies"].update(cookies)
        return self

    def set_body(self, body: Any) -> "HttpRequest":
        """ set request body
        """
        self.__body = body
        return self

    def update_body(self, **kwargs):
        """
        """
        self.__body = parse_content(self.body, kwargs)
        return self

    def run(self) -> "HttpResponse":
        """ make HTTP(S) request
        """
        try:
            resp_body = self.__body
        except AttributeError:
            resp_body = self.body

        if isinstance(resp_body, dict):
            if self.__kwargs["headers"] and \
                self.__kwargs["headers"].get("content-type", "")\
                    .startswith("application/x-www-form-urlencoded"):
                self.__kwargs["data"] = json.dumps(resp_body)
            else:
                self.__kwargs["json"] = resp_body
        else:
            self.__kwargs["data"] = resp_body

        _resp_obj = self.__session.request(
            self.method,
            self.url,
            **self.__kwargs
        )
        resp_obj = ResponseObject(_resp_obj)
        return HttpResponse(resp_obj)


class HttpResponse(object):

    def __init__(self, resp_obj: "requests.Response"):
        self.__resp_obj = resp_obj

    def get_header(self, field: str):
        """ extract response header field.
        """
        return self.__resp_obj.get_header(field)

    def get_body(self, field: str):
        """ extract response body field, field supports jmespath
        """
        return self.__resp_obj.get_body(field)

    def get_(self, field: str):
        """ extract response field

        Args:
            field (str): response field
                e.g. status_code, headers.server, body.cookies.freeform

        """
        return self.__resp_obj.extract(field)

    def get_response_object(self) -> "requests.Response":
        """ get response object.
        """
        return self.__resp_obj

    def __assert_with_expected(self, actual_value, expected_value):
        assert actual_value == expected_value
        return self

    def assert_(self, field: str, expected_value: Any) -> "HttpResponse":
        """ universal assertion with expected value

        Params:
            field (str): any field in response
                status_code
                headers.Content-Type
                body.details[0].name

        """
        return self.__assert_with_expected(
            self.__resp_obj.extract(field),
            expected_value
        )

    def assert_status_code(self, expected_value: int) -> "HttpResponse":
        return self.assert_("status_code", expected_value)

    def assert_header(self, field: str, expected_value: Any) -> "HttpResponse":
        """ assert header filed equivalent to expected value

        Params:
            field (str): case insensitive string, content-type or Content-Type are both okay.
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.__resp_obj.get_header(field),
            expected_value
        )

    def assert_body(self, field: str, expected_value: Any) -> "HttpResponse":
        """ assert body filed equivalent to expected value, field supports jmespath

        Params:
            field (str): jmespath string
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.__resp_obj.get_body(field),
            expected_value
        )
