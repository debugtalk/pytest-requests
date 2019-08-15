import types
from typing import Any

import jmespath
import requests

from pytest_requests import exceptions


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

    def __assert_with_expected(self, actual_value, expected):
        """ Make assertion with expected value.
            By default, assert actual_value equal to expected value.

            You can also assert with custom validator.
            e.g. assert_("status_code", gt(400))

        """
        if isinstance(expected, types.FunctionType):
            assert expected(actual_value)
        else:
            # assert equal by default
            assert actual_value == expected

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


class ResponseObject(object):

    def __init__(self, resp_obj):
        """ initialize with a requests.Response object

        Args:
            resp_obj (instance): requests.Response instance

        """
        self.resp_obj = resp_obj

    def __getattr__(self, key):
        try:
            if key in ["json", "json()"]:
                value = self.resp_obj.json()
            elif key == "cookies":
                value =  self.resp_obj.cookies.get_dict()
            else:
                value =  getattr(self.resp_obj, key)

            self.__dict__[key] = value
            return value
        except AttributeError:
            err_msg = "ResponseObject does not have attribute: {}".format(key)
            # logger.log_error(err_msg)
            raise exceptions.ParamsError(err_msg)

    def get_header(self, field):
        """ extract header field.
        """
        headers = self.headers
        if not field:
            # extract headers
            return headers

        try:
            return headers[field]
        except KeyError:
            err_msg = u"Failed to extract header! => headers.{}\n".format(field)
            err_msg += u"response headers: {}\n".format(headers)
            # logger.log_error(err_msg)
            raise exceptions.ExtractFailure(err_msg)

    def get_body(self, field):
        """ extract body field with jmespath.
        """
        try:
            body = self.json
        except exceptions.JSONDecodeError:
            err_msg = u"Failed to extract body! => body.{}\n".format(field)
            err_msg += u"response body: {}\n".format(self.content)
            # logger.log_error(err_msg)
            raise exceptions.ExtractFailure(err_msg)

        if not field:
            # extract response body
            return body

        return jmespath.search(field, body)


    def extract(self, field):
        """ extract field from response object

        Args:
            field (str): string joined by delimiter.
            e.g.
                "status_code"
                "headers"
                "cookies"
                "content"
                "headers.content-type"
                "content.person.name.first_name"

        """
        # string.split(sep=None, maxsplit=1) -> list of strings
        # e.g. "content.person.name" => ["content", "person.name"]
        try:
            top_query, sub_query = field.split('.', 1)
        except ValueError:
            top_query = field
            sub_query = None

        # status_code
        if top_query in ["status_code", "encoding", "ok", "reason", "url"]:
            if sub_query:
                # status_code.XX, ok.xyz
                err_msg = u"Failed to extract: {}\n".format(field)
                raise exceptions.ParamsError(err_msg)

            return getattr(self, top_query)

        # cookies
        elif top_query == "cookies":
            cookies = self.cookies
            if not sub_query:
                # extract cookies
                return cookies

            try:
                return cookies[sub_query]
            except KeyError:
                err_msg = u"Failed to extract cookie! => {}\n".format(field)
                err_msg += u"response cookies: {}\n".format(cookies)
                # logger.log_error(err_msg)
                raise exceptions.ExtractFailure(err_msg)

        # headers
        elif top_query == "headers":
            return self.get_header(sub_query)

        # response body
        elif top_query in ["body", "json()"]:
            return self.get_body(sub_query)
