from pytest_requests.testcase import BaseTestcase
from tests.httpbin.api import *


class TestUpdatePostBody(BaseTestcase):

    def run_test(self):
        ApiHttpBinPostHtmlForm(self.session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .update_body(custname="leo", custtel="18699999999")\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type", "application/json")\
            .assert_body("form.comments", "hello world")\
            .assert_body("form.topping[0]", "cheese")\
            .assert_body("form.custname", "leo")\
            .assert_body("form.custtel", "18699999999")

        ApiHttpBinPostJson(self.session)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .update_body(custname="leo", custtel="18699999999")\
            .run()\
            .assert_status_code(200)\
            .assert_header("Content-Type", "application/json")\
            .assert_body("json.comments", "hello world")\
            .assert_body("json.topping[0]", "cheese")\
            .assert_body("json.custname", "leo")\
            .assert_body("json.custtel", "18699999999")


class TestLoginStatus(BaseTestcase):

    def run_test(self):
        # step1: login and get cookie
        ApiHttpBinGetSetCookies(self.session)\
            .set_params(freeform="567")\
            .run()

        # step2: request another api, check cookie
        resp = ApiHttpBinPost(self.session)\
            .set_body({"abc": 123})\
            .run()\
            .get_response_object()

        request_headers = resp.request.headers
        assert "freeform=567" in request_headers["Cookie"]
