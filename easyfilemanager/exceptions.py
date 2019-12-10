class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NameAlreadyRegisteredError(Error):
    def __init__(self, message, name, path):
        super(NameAlreadyRegisteredError, self).__init__(message, name, path)


class InvalidDataFormatError(Error):
    def __init__(self, message, name, path, error) -> None:
        super().__init__(message, name, path, error)


class EmptyFileError(Error):
    def __init__(self, message, name, path) -> None:
        super().__init__(message, name, path)
