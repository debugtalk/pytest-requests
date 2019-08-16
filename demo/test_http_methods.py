from demo.api.http_methods import *
from pytest_requests import TestCase


class TestHttpMethods(TestCase):

    def test_get(self):
        ApiHttpbinGet().run()\
            .assert_status_code(200)\
            .assert_("status_code").less_than(300)\
            .assert_header("server").equals("nginx")\
            .assert_body("url").equals("https://httpbin.org/get?abc=111&de=222")\
            .assert_body("args").equals({"abc": "111", "de": "222"})\
            .assert_body("headers.Accept").equals('application/json')

    def test_get_with_querystring(self):
        ApiHttpbinGet()\
            .set_querystring({"abc": 123, "xyz": 456})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server").equals("nginx")\
            .assert_body("url").equals("https://httpbin.org/get?abc=123&de=222&xyz=456")\
            .assert_body("headers.Accept").equals('application/json')\
            .assert_body("args").equals({"abc": "123", "de": "222", "xyz": "456"})

    def test_post_json(self):
        ApiHttpBinPost() \
            .set_body({"abc": 456})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server").equals("nginx")\
            .assert_header("content-Type").equals("application/json")\
            .assert_body("url").equals("https://httpbin.org/post")\
            .assert_body("headers.Accept").equals('application/json')\
            .assert_body('headers."Content-Type"').equals('application/json')\
            .assert_body("json.abc").equals(456)

        headers = {
            "User-Agent": "pytest-requests",
            "content-type": "application/json"
        }
        ApiHttpBinPost()\
            .set_headers(headers)\
            .set_body({"abc": "123"})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server").equals("nginx") \
            .assert_body("url").equals("https://httpbin.org/post")\
            .assert_body("headers.Accept").equals('application/json')\
            .assert_body('headers."Content-Type"').equals("application/json")\
            .assert_body("json.abc").equals("123")\
            .assert_body('headers."User-Agent"').equals("pytest-requests")

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
            .assert_header("server").equals("nginx")\
            .assert_body("url").equals("https://httpbin.org/post")\
            .assert_body("headers.Accept").equals('application/json')\
            .assert_body('headers."Content-Type"').equals("application/x-www-form-urlencoded; charset=utf-8")\
            .assert_body("form.abc").equals("123")\
            .assert_body('headers."User-Agent"').equals("pytest-requests")

    def test_uniform_assert_method(self):
        ApiHttpBinPost()\
            .set_body({"abc": 456})\
            .run()\
            .assert_("status_code").equals(200)\
            .assert_("headers.server").equals("nginx")\
            .assert_("headers.content-Type").equals("application/json")\
            .assert_("body.url").equals("https://httpbin.org/post")\
            .assert_("body.headers.Accept").equals('application/json')\
            .assert_('body.headers."Content-Type"').equals('application/json')\
            .assert_("body.json.abc").equals(456)
