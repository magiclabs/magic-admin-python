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


class DIDTokenError(MagicError):
    pass
