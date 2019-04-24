"""Traffic Info's exceptions."""


class TrafficInfoError(Exception):
    """Base class for exceptions in this module."""


class WebdriverNotFoundError(TrafficInfoError):
    """
    Exception raised when the webdriver is not found.

    Attributes:
        path: The webdriver's path.

    """

    def __init__(self, path):
        """Class init."""
        super(WebdriverNotFoundError, self).__init__()
        msg = "Webdriver not found"
        if path is not None:
            msg += f" ({path})"
        self.msg = f"{msg}."


class NotExecutableError(TrafficInfoError):
    """
    Raised when the webdriver file is not executable.

    Attributes:
        path: The webdriver's path.

    """

    def __init__(self, path):
        """Class init."""
        super(NotExecutableError, self).__init__()
        self.msg = f"The file {path} is not executable."
