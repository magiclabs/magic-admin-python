class MagicDjangoException(Exception):
    pass


class UnsupportedAuthMode(MagicDjangoException):
    pass


class PublicAddressDoesNotExist(MagicDjangoException):
    pass


class UserEmailMissmatch(MagicDjangoException):
    pass


class MissingUserEmailInput(MagicDjangoException):
    pass


class MissingAuthorizationHeader(MagicDjangoException):
    pass


class UnableToLoadUserFromIdentityToken(MagicDjangoException):
    pass
