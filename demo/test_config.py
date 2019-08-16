from pytest_requests import TestCase

from demo.api.response_formats import ApiHttpBinGetJson


class TestConfigRequest(TestCase):

    def test_config_verify(self):
        title = ApiHttpBinGetJson()\
            .config_verify(False)\
            .set_headers({"User-Agent": "pytest-requests"})\
            .set_cookies({"username": "debugtalk"})\
            .run()\
            .assert_status_code(200)\
            .assert_header("content-Type").equals("application/json")\
            .assert_body("slideshow.slides[0].title").equals("Wake up to WonderWidgets!")\
            .get_body("slideshow.slides[1].title")

        assert title == "Overview"
