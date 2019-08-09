
import copy
import json

import requests

from pytest_requests.response import ResponseObject
from pytest_requests.utils import parse_content


class EnumMethod(object):
    ''' Enum HTTP method
    '''
    GET, HEAD, POST, PUT, OPTIONS, DELETE \
        = ("GET", "HEAD", "POST", "PUT", "OPTIONS", "DELETE")


class BaseApi(object):

    method = "GET"
    url = ""
    params = None
    headers = None
    cookies = None
    body = None

    def __init__(self, session=None):
        self.__session = session or requests.sessions.Session()

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
        self.__config = {
            "verify": verify,
            "auth": auth,
            "timeout": timeout,
            "proxies": proxies,
            "allow_redirects": allow_redirects,
            "hooks": hooks,
            "stream": stream,
            "cert": cert
        }
        return self

    def set_param(self, key, value):
        """ update request param
        """
        param = {key: value}
        return self.set_params(**param)

    def set_params(self, **params):
        """ update request params
        """
        try:
            self.__params.update(params)
        except AttributeError:
            self.__params = copy.deepcopy(self.__class__.params or {})
            self.__params.update(params)

        return self

    def set_headers(self, headers_dict):
        """ update request headers
        """
        try:
            self.__headers.update(headers_dict)
        except AttributeError:
            self.__headers = copy.deepcopy(self.__class__.headers or {})
            self.__headers.update(headers_dict)

        return self

    def set_cookie(self, key, value):
        """ update request cookie
        """
        cookie = {key: value}
        return self.set_cookies(**cookie)

    def set_cookies(self, **kwargs):
        """ update request cookies
        """
        try:
            self.__cookies.update(kwargs)
        except AttributeError:
            self.__cookies = copy.deepcopy(self.__class__.cookies or {})
            self.__cookies.update(kwargs)

        return self

    def set_body(self, body):
        """ set request body
        """
        self.__body = body
        return self

    def update_body(self, **kwargs):
        """
        """
        self.__body = parse_content(self.body, kwargs)
        return self

    def __get_private_attribute(self, attr_name):
        """ get private attribute value

        Args:
            attr_name (enum str): headers, params, cookies, body

        """
        try:
            return getattr(self, "_BaseApi__{}".format(attr_name))
        except AttributeError:
            return getattr(self, attr_name)

    def run(self):
        """ make HTTP(S) request
        """
        self.__headers = self.__get_private_attribute("headers")

        kwargs = {
            "params": self.__get_private_attribute("params"),
            "headers": self.__headers,
            "cookies": self.__get_private_attribute("cookies")
        }

        try:
            kwargs.update(self.__config)
        except AttributeError:
            pass

        try:
            resp_body = self.__body
        except AttributeError:
            resp_body = self.body

        if isinstance(resp_body, dict):
            if self.__headers and \
                self.__headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
                kwargs["data"] = json.dumps(resp_body)
            else:
                kwargs["json"] = resp_body
        else:
            kwargs["data"] = resp_body

        _resp_obj = self.__session.request(
            self.method,
            self.url,
            **kwargs
        )
        resp_obj = ResponseObject(_resp_obj)
        return ApiResponse(resp_obj)


class ApiResponse(object):

    def __init__(self, resp_obj):
        self.__resp_obj = resp_obj

    def extract_header(self, field):
        """ extract response header field.
        """
        return self.__resp_obj.extract_header(field)

    def extract_body(self, field):
        """ extract response body field, field supports jmespath
        """
        return self.__resp_obj.extract_body(field)

    def extract_(self, field):
        """ extract response field

        Args:
            field (str): response field
                e.g. status_code, headers.server, body.cookies.freeform

        """
        return self.__resp_obj.extract(field)

    def get_response_object(self):
        """ get response object.
        """
        return self.__resp_obj

    def __assert_with_expected(self, actual_value, expected_value):
        assert actual_value == expected_value
        return self

    def assert_(self, field, expected_value):
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

    def assert_status_code(self, expected_value):
        return self.assert_("status_code", expected_value)

    def assert_header(self, field, expected_value):
        """ assert header filed equivalent to expected value

        Params:
            field (str): case insensitive string, content-type or Content-Type are both okay.
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.__resp_obj.extract_header(field),
            expected_value
        )

    def assert_body(self, field, expected_value):
        """ assert body filed equivalent to expected value, field supports jmespath

        Params:
            field (str): jmespath string
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.__resp_obj.extract_body(field),
            expected_value
        )
