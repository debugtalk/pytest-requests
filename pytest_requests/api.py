
import json

import requests

from pytest_requests.response import ResponseObject


class BaseApi(object):

    method = "GET"
    url = ""
    params = None
    data = None
    headers = None
    cookies = None
    files = None
    auth = None
    timeout = None
    allow_redirects = True
    proxies = None
    hooks = None
    stream = None
    verify = None
    cert = None
    json = None

    def __init__(self):
        self.resp_obj = None

    def set_params(self, **params):
        self.params = params
        return self

    def set_header(self, key, value):
        self.headers = self.headers or {}
        self.headers.update({key: value})
        return self

    def set_cookie(self, key, value):
        self.cookies = self.cookies or {}
        self.cookies.update({key: value})
        return self

    def set_cookies(self, **kwargs):
        self.cookies = self.cookies or {}
        self.cookies.update(kwargs)
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_json(self, json_data):
        self.json = json_data
        return self

    def run(self, session = None):
        if isinstance(self.data, dict) and self.headers and\
            self.headers.get("content-type") == "application/json":
            self.data = json.dumps(self.data)

        session = session or requests.sessions.Session()
        _resp_obj = session.request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            headers=self.headers,
            cookies=self.cookies,
            files=self.files,
            auth=self.auth,
            timeout=self.timeout,
            allow_redirects=self.allow_redirects,
            proxies=self.proxies,
            hooks=self.hooks,
            stream=self.stream,
            verify=self.verify,
            cert=self.cert,
            json=self.json
        )
        self.resp_obj = ResponseObject(_resp_obj)
        return self

    def extract_response(self, field):
        return self.resp_obj.extract(field)

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
        """ assert body filed equivalent to expected value

        Params:
            field (str): jmespath string
            expected_value: expected value in any type

        """
        return self.__assert_with_expected(
            self.resp_obj.extract_body(field),
            expected_value
        )

    def get_response(self):
        return self.resp_obj
