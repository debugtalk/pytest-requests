import requests

from pytest_requests.utils import parse_content


class TestCase(object):

    def create_session(self):
        """ create new HTTP session
        """
        return requests.sessions.Session()

    @staticmethod
    def parse_body(content, kwargs):
        return parse_content(content, kwargs)

    def run_test(self):
        """ run_test should be overrided.
        """
        raise NotImplementedError
