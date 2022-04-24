class MeApiException(Exception):
    """
    Raise this exception if http status code is bigger than ``400``.

    :param http_status: status code of the http request. ``400=>``.
    :type http_status: int
    :param msg: dict with data about the error. Usually under the ``detail`` key.
    :type msg: dict
    :param reason: The reason to the error.
    :type reason: str
    """
    def __init__(self, http_status: int, msg: dict, reason: str = None):
        self.http_status = http_status
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return f'http status: {self.http_status}, msg: {self.msg}, reason: {self.reason}'


class MeException(Exception):
    """
    Raise this exception when there is general error in the meapi library.

    :param msg: String of the exception.
    :type msg: str
    """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
