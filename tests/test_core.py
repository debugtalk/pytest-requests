from tests.api.httpbin import *

def test_version():
    from pytest_requests import __version__
    assert isinstance(__version__, str)


def test_httpbin_get():
    ApiHttpbinGet().run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get")\
        .validate("json().args", {})\
        .validate("json().headers.Accept", 'application/json')


def test_httpbin_get_with_prams():
    ApiHttpbinGet()\
        .set_params(abc=123, xyz=456)\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get?abc=123&xyz=456")\
        .validate("json().headers.Accept", 'application/json')


def test_httpbin_post_json():
    ApiHttpBinPost()\
        .set_json({"abc": 456})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')\
        .validate("json().headers.Content-Type", 'application/json')\
        .validate("json().json.abc", 456)


def test_httpbin_post_form_data():
    ApiHttpBinPost()\
        .set_header("content-type", "application/x-www-form-urlencoded; charset=utf-8")\
        .set_data("abc=123")\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')\
        .validate("json().headers.Content-Type", "application/x-www-form-urlencoded; charset=utf-8")\
        .validate("json().form.abc", "123")


def test_httpbin_post_data_in_json():
    ApiHttpBinPost()\
        .set_header("content-type", "application/json")\
        .set_data({"abc": "123"})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')\
        .validate("json().headers.Content-Type", "application/json")\
        .validate("json().json.abc", "123")


def test_httpbin_parameters_share():
    user_id = "adk129"
    ApiHttpbinGet()\
        .set_params(user_id=user_id)\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/get?user_id={}".format(user_id))\
        .validate("json().headers.Accept", 'application/json')

    ApiHttpBinPost()\
        .set_json({"user_id": user_id})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')\
        .validate("json().json.user_id", "adk129")


def test_httpbin_extract():
    api_run = ApiHttpbinGet().run()
    status_code = api_run.extract("status_code")
    assert status_code == 200

    server = api_run.extract("headers.server")
    assert server == "nginx"

    accept_type = api_run.extract("json().headers.Accept")
    assert accept_type == 'application/json'


def test_httpbin_setcookies():
    cookies = {
        "freeform1": "123",
        "freeform2": "456"
    }
    api_run = ApiHttpBinGetCookies().set_cookies(**cookies).run()
    freeform1 = api_run.extract("json().cookies.freeform1")
    freeform2 = api_run.extract("json().cookies.freeform2")
    assert freeform1 == "123"
    assert freeform2 == "456"

def test_httpbin_parameters_extract():
    # step 1: get value
    freeform = ApiHttpBinGetCookies()\
        .set_cookie("freeform", "123")\
        .run()\
        .extract("json().cookies.freeform")
    assert freeform == "123"

    # step 2: use value as parameter
    ApiHttpBinPost()\
        .set_json({"freeform": freeform})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", "nginx")\
        .validate("json().url", "https://httpbin.org/post")\
        .validate("json().headers.Accept", 'application/json')\
        .validate("json().json.freeform", freeform)


def test_httpbin_login_status():
    import requests
    session = requests.sessions.Session()

    # step1: login and get cookie
    ApiHttpBinGetSetCookies().set_params(freeform="567").run(session)

    # step2: request another api, check cookie
    resp = ApiHttpBinPost()\
        .set_json({"abc": 123})\
        .run(session).get_response()
    request_headers = resp.request.headers

    assert "freeform=567" in request_headers["Cookie"]
