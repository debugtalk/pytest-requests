import requests


class BaseTestcase(object):

    def __init__(self):
        self.session = requests.sessions.Session()

    def run_test(self):
        """ run_test should be overrided.
        """
        raise NotImplementedError
