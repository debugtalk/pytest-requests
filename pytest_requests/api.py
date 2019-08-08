
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

    def __init__(self):
        self.resp_obj = None

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
        self._config = {
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
        if not hasattr(self, "_params"):
            self._params = copy.deepcopy(self.__class__.params or {})

        self._params.update(params)
        return self

    def set_header(self, key, value):
        """ update request header
        """
        header = {key: value}
        return self.set_headers(**header)

    def set_headers(self, **headers):
        """ update request headers
        """
        if not hasattr(self, "_headers"):
            self._headers = copy.deepcopy(self.__class__.headers or {})

        self._headers.update(headers)
        return self

    def set_cookie(self, key, value):
        """ update request cookie
        """
        cookie = {key: value}
        return self.set_cookies(**cookie)

    def set_cookies(self, **kwargs):
        """ update request cookies
        """
        if not hasattr(self, "_cookies"):
            self._cookies = copy.deepcopy(self.__class__.cookies or {})

        self._cookies.update(kwargs)
        return self

    def set_body(self, body):
        """ set request body
        """
        self._body = body
        return self

    def update_body(self, **kwargs):
        """
        """
        self._body = parse_content(self.body, kwargs)
        return self

    def run(self, session = None):

        session = session or requests.sessions.Session()
        self._headers = getattr(self, "_headers", None) or self.headers

        kwargs = {
            "params": getattr(self, "_params", None) or self.params,
            "headers": self._headers,
            "cookies": getattr(self, "_cookies", None) or self.cookies
        }
        if hasattr(self, "_config"):
            kwargs.update(self._config)

        _body = self._body if hasattr(self, "_body") else self.body
        if isinstance(_body, dict):
            if self._headers and \
                self._headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
                kwargs["data"] = json.dumps(_body)
            else:
                kwargs["json"] = _body
        else:
            kwargs["data"] = _body

        _resp_obj = session.request(
            self.method,
            self.url,
            **kwargs
        )
        self.resp_obj = ResponseObject(_resp_obj)
        return self

    def extract_header(self, field):
        """ extract response header field.
        """
        return self.resp_obj.extract_header(field)

    def extract_body(self, field):
        """ extract response body field, field supports jmespath
        """
        return self.resp_obj.extract_body(field)

    def extract_(self, field):
        """ extract response field

        Args:
            field (str): response field
                e.g. status_code, headers.server, body.cookies.freeform

        """
        return self.resp_obj.extract(field)

    def get_response_object(self):
        """ get response object.
        """
        return self.resp_obj

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
            self.resp_obj.extract(field),
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
            self.resp_obj.extract_header(field),
            expected_value
        )

    def assert_body(self, field, expected_value):
        """ assert body filed equivalent to expected value, field supports jmespath

        Params:
            field (str): jmespath string
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.resp_obj.extract_body(field),
            expected_value
        )
