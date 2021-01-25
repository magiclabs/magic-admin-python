MAGIC_IDENTITY_KEY = '_magic_identity_token'
MAGIC_AUTH_BACKEND = 'magic_admin.django.auth.backends.MagicAuthBackend'


class MagicAuthBackendMode:

    DJANGO_DEFAULT_AUTH = 0
    MAGIC = 1

    ALLOWED_MODES = frozenset([DJANGO_DEFAULT_AUTH, MAGIC])
