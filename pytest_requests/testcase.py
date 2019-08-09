import requests


class TestCase(object):

    def create_session(self):
        """ create new HTTP session
        """
        return requests.sessions.Session()

    def run_test(self):
        """ run_test should be overrided.
        """
        raise NotImplementedError
