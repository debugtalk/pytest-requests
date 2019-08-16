import copy
import json
from typing import Any, Tuple

import requests

from pytest_requests.exceptions import ParamsError

from .response import HttpResponse, ResponseObject


class HttpRequest(object):

    class EnumHttpMethod(object):
        """ Enum HTTP method
        """
        GET, HEAD, POST, PUT, OPTIONS, DELETE \
            = ("GET", "HEAD", "POST", "PUT", "OPTIONS", "DELETE")

    def __init__(self, session=None):
        self.__session = session or requests.sessions.Session()
        self.__kwargs = {
            "params": copy.deepcopy(getattr(self, "params", {})),
            "headers": copy.deepcopy(getattr(self, "headers", {})),
            "cookies": copy.deepcopy(getattr(self, "cookies", {}))
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

    def run(self) -> "HttpResponse":
        """ make HTTP(S) request
        """
        try:
            resp_body = self.__body
        except AttributeError:
            resp_body = getattr(self, "body", None)

        if isinstance(resp_body, dict):
            if self.__kwargs["headers"] and \
                self.__kwargs["headers"].get("content-type", "")\
                    .startswith("application/x-www-form-urlencoded"):
                self.__kwargs["data"] = json.dumps(resp_body)
            else:
                self.__kwargs["json"] = resp_body
        else:
            self.__kwargs["data"] = resp_body

        method = getattr(self, "method", "GET")
        try:
            url = getattr(self, "url")
        except AttributeError:
            raise ParamsError("url missing!")

        _resp_obj = self.__session.request(
            method,
            url,
            **self.__kwargs
        )
        resp_obj = ResponseObject(_resp_obj)
        return HttpResponse(resp_obj)
