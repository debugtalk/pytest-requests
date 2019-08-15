from pytest_requests import validators


def test_validator_equals():
    func = validators.equals(3)
    assert func(1+2)

    func = validators.eq("abc")
    assert func("abc ".strip())
