import requests


class TestCase(object):

    def create_session(self):
        """ create new HTTP session
        """
        return requests.sessions.Session()

    @staticmethod
    def parse_body(content, kwargs):

        if isinstance(content, dict):
            return {
                key: TestCase.parse_body(value, kwargs)
                for key, value in content.items()
            }

        elif isinstance(content, list):
            return [
                TestCase.parse_body(item, kwargs)
                for item in content
            ]

        elif isinstance(content, str):
            return content.format(**kwargs)

        else:
            return content


    def run_test(self):
        """ run_test should be overrided.
        """
        raise NotImplementedError
