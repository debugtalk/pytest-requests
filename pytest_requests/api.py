
import copy
import json
from typing import Any

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

    def set_config(self, verify=None, auth=None, timeout=None, proxies=None,
            allow_redirects=True, hooks=None, stream=None, cert=None):
        """ set request configuration

        Args:
            verify
            auth
            timeout
            proxies
            allow_redirects
            hooks
            stream
            cert

        """
        config_kwargs = {
            "verify": verify,
            "auth": auth,
            "timeout": timeout,
            "proxies": proxies,
            "allow_redirects": allow_redirects,
            "hooks": hooks,
            "stream": stream,
            "cert": cert
        }
        self.__kwargs.update(config_kwargs)
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
