class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NameAlreadyRegisteredError(Error):
    def __init__(self, message, name, path):
        super(NameAlreadyRegisteredError, self).__init__(message, name, path)
