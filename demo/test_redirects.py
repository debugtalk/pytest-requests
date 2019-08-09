from pytest_requests import TestCase
from demo.api.redirects import *


class TestRedirects(TestCase):

    def test_redirect_allow_redirects(self):
        ApiHttpBinGetRedirect302()\
            .config_allow_redirects(False)\
            .set_querystring({"status_code": 302})\
            .run()\
            .assert_status_code(302)
