class MagicError(Exception):

    def __init__(self, message=None):
        super().__init__(message)
        self._message = message

    def __str__(self):
        return self._message or '<empty message>'

    def __repr__(self):
        return '{error_class}(message={message!r})'.format(
            error_class=self.__class__.__name__,
            message=self._message,
        )

    def to_dict(self):
        return {'message': str(self)}


class DIDTokenError(MagicError):
    pass


class APIConnectionError(MagicError):
    pass


class RequestError(MagicError):

    def __init__(
        self,
        message=None,
        http_status=None,
        http_code=None,
        http_resp_data=None,
        http_message=None,
        http_error_code=None,
        http_request_params=None,
        http_request_data=None,
        http_method=None,
    ):
        super().__init__(message)
        self.http_status = http_status
        self.http_code = http_code
        self.http_resp_data = http_resp_data
        self.http_message = http_message
        self.http_error_code = http_error_code
        self.http_request_params = http_request_params
        self.http_request_data = http_request_data
        self.http_method = http_method

    def __repr__(self):
        return '{error_class}(message={message!r}, ' \
            'http_error_code={http_error_code}, ' \
            'http_code={http_code}).'.format(
                error_class=self.__class__.__name__,
                message=self._message or None,
                http_error_code=self.http_error_code or None,
                http_code=self.http_code or None,
            )

    def to_dict(self):
        _dict = super().to_dict()
        for attr in self.__dict__:
            if attr.startswith('http_'):
                _dict[attr] = self.__dict__[attr]

        return _dict


class RateLimitingError(RequestError):
    pass


class BadRequestError(RequestError):
    pass


class AuthenticationError(RequestError):
    pass


class ForbiddenError(RequestError):
    pass


class APIError(RequestError):
    pass
