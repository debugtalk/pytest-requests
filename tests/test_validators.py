import pytest
from pytest_requests import validators


def test_validator_equals():
    func = validators.equals(3)
    assert func(1+2)

    func = validators.eq("abc")
    assert func("abc ".strip())


def test_validator_greater_than():
    func = validators.gt(400)
    assert func(401)

    with pytest.raises(AssertionError):
        assert func(400)


def test_validator_less_than():
    func = validators.lt(400)
    assert func(301)

    with pytest.raises(AssertionError):
        assert func(400)
