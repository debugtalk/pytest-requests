
def test_version():
    from hogwarts_apitest import __version__
    assert isinstance(__version__, str)
