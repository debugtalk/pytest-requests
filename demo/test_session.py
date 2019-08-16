from pytest_requests import TestCase
from demo.api.html_form import *
from demo.api.cookies import *
from demo.api.http_methods import *


class TestUpdatePostBody(TestCase):

    def run_test(self):
        session = self.create_session()

        kwargs = {
            "custname": "leo",
            "custtel": "18699999999"
        }
        form_data_body = self.parse_body(ApiHttpBinPostHtmlForm.body, kwargs)
        ApiHttpBinPostHtmlForm(session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .set_body(form_data_body)\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type").equals("application/json")\
            .assert_body("form.comments").equals("hello world")\
            .assert_body("form.topping[0]").equals("cheese")\
            .assert_body("form.custname").equals("leo")\
            .assert_body("form.custtel").equals("18699999999")

        json_body = self.parse_body(ApiHttpBinPostJson.body, kwargs)
        ApiHttpBinPostJson(session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .set_body(json_body)\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type").equals("application/json")\
            .assert_body("json.comments").equals("hello world")\
            .assert_body("json.topping[0]").equals("cheese")\
            .assert_body("json.custname").equals("leo")\
            .assert_body("json.custtel").equals("18699999999")


class TestLoginStatus(TestCase):

    def run_test(self):
        session = self.create_session()

        # step1: login and get cookie
        ApiHttpBinGetSetCookies(session)\
            .set_querystring({"freeform": "567"})\
            .run()

        # step2: request another api, check cookie
        resp = ApiHttpBinPost(session)\
            .set_body({"abc": 123})\
            .run()\
            .get_response_object()

        request_headers = resp.request.headers
        assert "freeform=567" in request_headers["Cookie"]


class TestCookies(TestCase):

    def test_httpbin_setcookies(self):
        cookies = {
            "freeform1": "123",
            "freeform2": "456"
        }
        api_run = ApiHttpBinGetCookies().set_cookies(cookies).run()
        freeform1 = api_run.get_body("cookies.freeform1")
        freeform2 = api_run.get_body("cookies.freeform2")
        assert freeform1 == "123"
        assert freeform2 == "456"
