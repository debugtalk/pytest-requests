import jmespath
import requests

from pytest_requests import exceptions


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

    def extract_header(self, field):
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

    def extract_body(self, field):
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
            return self.extract_header(sub_query)

        # response body
        elif top_query in ["body", "json()"]:
            return self.extract_body(sub_query)
