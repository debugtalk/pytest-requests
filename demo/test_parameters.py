from pytest_requests import TestCase
from demo.api.http_methods import *
from demo.api.cookies import *


class TestParameters(TestCase):

    def test_share_parameters_between_steps(self):
        user_id = "adk129"
        ApiHttpbinGet()\
            .set_querystring({"user_id": user_id})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/get?abc=111&de=222&user_id={}".format(user_id))\
            .assert_body("headers.Accept", 'application/json')

        ApiHttpBinPost()\
            .set_body({"user_id": user_id})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/post")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body("json.user_id", "adk129")

    def test_extract_parameter(self):
        api_run = ApiHttpbinGet().run()
        status_code = api_run.get_("status_code")
        assert status_code == 200

        server = api_run.get_header("server")
        assert server == "nginx"

        accept_type = api_run.get_body("headers.Accept")
        assert accept_type == 'application/json'

    def test_parameters_association(self):
        # step 1: get value
        freeform = ApiHttpBinGetCookies()\
            .set_cookies({"freeform": "123"})\
            .run()\
            .get_body("cookies.freeform")
        assert freeform == "123"

        # step 2: use value as parameter
        ApiHttpBinPost()\
            .set_body({"freeform": freeform})\
            .run()\
            .assert_status_code(200)\
            .assert_header("server", "nginx")\
            .assert_body("url", "https://httpbin.org/post")\
            .assert_body("headers.Accept", 'application/json')\
            .assert_body("json.freeform", freeform)

