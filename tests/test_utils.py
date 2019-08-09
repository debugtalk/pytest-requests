from pytest_requests import utils


def test_version():
    from pytest_requests import __version__
    assert isinstance(__version__, str)


def test_parse_content():
    kwargs = {"a": 1, "b": "xyz"}

    assert utils.parse_content("http://httpbin.org/", kwargs) == "http://httpbin.org/"
    assert utils.parse_content("POST", kwargs) == "POST"
    assert utils.parse_content(123, kwargs) == 123

    headers = {
        "a": "{a}",
        "User-Agent": "chrome"
    }
    assert utils.parse_content(headers, kwargs), {'a': '1', 'User-Agent': 'chrome'}

    data = "key=123&value={b}"
    assert utils.parse_content(data, kwargs) == "key=123&value=xyz"
