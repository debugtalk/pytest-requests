from pytest_requests import TestCase
from demo.api.http_methods import *


class TestHttpMethods(TestCase):

    def test_get(self):
        ApiHttpbinGet().run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/get?abc=111&de=222")\
            .assert_body("args", {"abc": "111", "de": "222"})\
            .assert_body("headers.Accept", 'application/json')

    def test_get_with_querystring(self):
        ApiHttpbinGet()\
            .set_querystring({"abc": 123, "xyz": 456})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/get?abc=123&de=222&xyz=456")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body("args", {"abc": "123", "de": "222", "xyz": "456"})

    def test_post_json(self):
        ApiHttpBinPost()\
            .set_body({"abc": 456})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_header("content-Type", "application/json")\
            .assert_body("url", "https://httpbin.org/post")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body('headers."Content-Type"', 'application/json')\
            .assert_body("json.abc", 456)

        headers = {
            "User-Agent": "pytest-requests",
            "content-type": "application/json"
        }
        ApiHttpBinPost()\
            .set_headers(headers)\
            .set_body({"abc": "123"})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/post")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body('headers."Content-Type"', "application/json")\
            .assert_body("json.abc", "123")\
            .assert_body('headers."User-Agent"', "pytest-requests")

    def test_post_form_data(self):
        headers = {
            "User-Agent": "pytest-requests",
            "content-type": "application/x-www-form-urlencoded; charset=utf-8"
        }
        ApiHttpBinPost()\
            .set_headers(headers)\
            .set_body("abc=123")\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/post")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body('headers."Content-Type"', "application/x-www-form-urlencoded; charset=utf-8")\
            .assert_body("form.abc", "123")\
            .assert_body('headers."User-Agent"', "pytest-requests")

    def test_uniform_assert_method(self):
        ApiHttpBinPost()\
            .set_body({"abc": 456})\
            .run()\
            .assert_("status_code", 200)\
            .assert_("headers.server", "nginx")\
            .assert_("headers.content-Type", "application/json")\
            .assert_("body.url", "https://httpbin.org/post")\
            .assert_("body.headers.Accept", 'application/json')\
            .assert_('body.headers."Content-Type"', 'application/json')\
            .assert_("body.json.abc", 456)
