

class MeApiException(Exception):

    def __init__(self, http_status: int, msg: dict, reason=None):
        self.http_status = http_status
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return f'http status: {self.http_status}, msg: {self.msg}, reason: {self.reason}'


class MeException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg
