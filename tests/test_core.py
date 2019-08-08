from tests.api.httpbin import *
from tests.testcases.httpbin import *


def test_version():
    from pytest_requests import __version__
    assert isinstance(__version__, str)


def test_httpbin_get():
    ApiHttpbinGet().run()\
        .assert_status_code(200)\
        .assert_header("server", "nginx")\
        .assert_body("url", "https://httpbin.org/get?abc=111&de=222")\
        .assert_body("args", {"abc": "111", "de": "222"})\
        .assert_body("headers.Accept", 'application/json')


def test_httpbin_get_with_set_params():
    ApiHttpbinGet()\
        .set_params(abc=123, xyz=456)\
        .run()\
        .assert_status_code(200)\
        .assert_header("server", "nginx")\
        .assert_body("url", "https://httpbin.org/get?abc=123&de=222&xyz=456")\
        .assert_body("headers.Accept", 'application/json')\
        .assert_body("args", {"abc": "123", "de": "222", "xyz": "456"})


def test_httpbin_get_with_multiple_set_params():
    ApiHttpbinGet()\
        .set_param("abc", 123)\
        .set_params(xyz=456)\
        .run()\
        .assert_status_code(200)\
        .assert_header("server", "nginx")\
        .assert_body("url", "https://httpbin.org/get?abc=123&de=222&xyz=456")\
        .assert_body("headers.Accept", 'application/json')\
        .assert_body("args", {"abc": "123", "de": "222", "xyz": "456"})


def test_with_raw_assert():
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


def test_httpbin_post_json():
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


def test_httpbin_post_form_data():
    ApiHttpBinPost()\
        .set_header("User-Agent", "pytest-requests")\
        .set_header("content-type", "application/x-www-form-urlencoded; charset=utf-8")\
        .set_body("abc=123")\
        .run()\
        .assert_status_code(200)\
        .assert_header("server", "nginx")\
        .assert_body("url", "https://httpbin.org/post")\
        .assert_body("headers.Accept", 'application/json')\
        .assert_body('headers."Content-Type"', "application/x-www-form-urlencoded; charset=utf-8")\
        .assert_body("form.abc", "123")\
        .assert_body('headers."User-Agent"', "pytest-requests")


def test_httpbin_post_data_in_json():
    headers = {
        "User-Agent": "pytest-requests",
        "content-type": "application/json"
    }
    ApiHttpBinPost()\
        .set_headers(**headers)\
        .set_body({"abc": "123"})\
        .run()\
        .assert_status_code(200)\
        .assert_header("server", "nginx")\
        .assert_body("url", "https://httpbin.org/post")\
        .assert_body("headers.Accept", 'application/json')\
        .assert_body('headers."Content-Type"', "application/json")\
        .assert_body("json.abc", "123")\
        .assert_body('headers."User-Agent"', "pytest-requests")


def test_httpbin_parameters_share():
    user_id = "adk129"
    ApiHttpbinGet()\
        .set_param("user_id", user_id)\
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


def test_httpbin_extract():
    api_run = ApiHttpbinGet().run()
    status_code = api_run.extract_("status_code")
    assert status_code == 200

    server = api_run.extract_header("server")
    assert server == "nginx"

    accept_type = api_run.extract_body("headers.Accept")
    assert accept_type == 'application/json'


def test_httpbin_setcookies():
    cookies = {
        "freeform1": "123",
        "freeform2": "456"
    }
    api_run = ApiHttpBinGetCookies().set_cookies(**cookies).run()
    freeform1 = api_run.extract_body("cookies.freeform1")
    freeform2 = api_run.extract_body("cookies.freeform2")
    assert freeform1 == "123"
    assert freeform2 == "456"

def test_httpbin_parameters_extract():
    # step 1: get value
    freeform = ApiHttpBinGetCookies()\
        .set_cookie("freeform", "123")\
        .run()\
        .extract_body("cookies.freeform")
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


def test_httpbin_login_status():
    import requests
    session = requests.sessions.Session()

    # step1: login and get cookie
    ApiHttpBinGetSetCookies(session).set_params(freeform="567").run()

    # step2: request another api, check cookie
    resp = ApiHttpBinPost(session)\
        .set_body({"abc": 123})\
        .run().get_response_object()

    request_headers = resp.request.headers
    assert "freeform=567" in request_headers["Cookie"]


def test_httpbin_redirect_allow_redirects():
    ApiHttpBinGetRedirect302()\
        .set_config(allow_redirects=False)\
        .set_param("status_code", 302)\
        .run()\
        .assert_status_code(302)


def test_httpbin_get_json():
    title = ApiHttpBinGetJson()\
        .set_config(verify=False)\
        .set_header("User-Agent", "pytest-requests")\
        .set_cookie("username", "debugtalk")\
        .run()\
        .assert_status_code(200)\
        .assert_header("content-Type", "application/json")\
        .assert_body("slideshow.slides[0].title", "Wake up to WonderWidgets!")\
        .extract_body("slideshow.slides[1].title")

    assert title == "Overview"


def test_httpbin_update_post_body():
    ApiHttpBinPostHtmlForm()\
        .set_header("User-Agent", "pytest-requests")\
        .update_body(custname="leo", custtel="18699999999")\
        .run()\
        .assert_status_code(200)\
        .assert_header("Content-Type", "application/json")\
        .assert_body("form.comments", "hello world")\
        .assert_body("form.topping[0]", "cheese")\
        .assert_body("form.custname", "leo")\
        .assert_body("form.custtel", "18699999999")

    ApiHttpBinPostJson()\
        .set_header("User-Agent", "pytest-requests")\
        .update_body(custname="leo", custtel="18699999999")\
        .run()\
        .assert_status_code(200)\
        .assert_header("Content-Type", "application/json")\
        .assert_body("json.comments", "hello world")\
        .assert_body("json.topping[0]", "cheese")\
        .assert_body("json.custname", "leo")\
        .assert_body("json.custtel", "18699999999")


def test_testcase_demo():
    TestUpdatePostBody().run_test()
    TestLoginStatus().run_test()
