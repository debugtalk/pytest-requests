import json

JSONDecodeError = json.JSONDecodeError

""" failure type exceptions
    these exceptions will mark test as failure
"""

class MyBaseFailure(Exception):
    pass

class ExtractFailure(MyBaseFailure):
    pass


""" error type exceptions
    these exceptions will mark test as error
"""

class MyBaseError(Exception):
    pass

class ParamsError(MyBaseError):
    pass
