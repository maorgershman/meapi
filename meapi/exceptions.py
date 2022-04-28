class MeApiException(Exception):
    """
    Raise this exception if http status code is bigger than ``400``.

    :param http_status: status code of the http request. ``400=>``.
    :type http_status: int
    :param msg: ``api error msg``. for example: ``api_incorrect_activation_code``..
    :type msg: str
    :param reason: Human reason to the error.
    :type reason: str

    **Expected msg's:**

    - ``api_incorrect_pwd_token`` in :py:func:`~meapi.Me.generate_access_token`.
    - ``api_incorrect_activation_code`` in :py:func:`~meapi.Me.activate_account`.
    - ``api_search_passed_limit`` in :py:func:`~meapi.Me.phone_search`.
    - ``api_profile_view_passed_limit`` in :py:func:`~meapi.Me.get_profile_info`.
    """
    def __init__(self, http_status: int, msg: str, reason: str = None):
        self.http_status = http_status
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return f'http status: {self.http_status}, msg: {self.msg}, reason: {self.reason}'


class MeException(Exception):
    """
    Raise this exception when there is general error in the meapi library.

    :param msg: Reason of the exception.
    :type msg: str
    """
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
