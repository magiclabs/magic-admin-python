import os

import magic_admin
from magic_admin.config import api_secret_api_key_missing_message
from magic_admin.error import AuthenticationError
from magic_admin.resources.base import ResourceComponent


RETRIES = 3
TIMEOUT = 10
BACKOFF_FACTOR = 0.02


class Magic:

    def __getattr__(self, attribute_name):
        try:
            return getattr(self._resource, attribute_name)
        except AttributeError:
            pass

        return super().__getattribute__(attribute_name)

    def __init__(
        self,
        api_secret_key=None,
        retries=RETRIES,
        timeout=TIMEOUT,
        backoff_factor=BACKOFF_FACTOR,
    ):
        self._resource = ResourceComponent()

        self._resource.setup_request_client(retries, timeout, backoff_factor)
        self._set_api_secret_key(api_secret_key)

    def _set_api_secret_key(self, api_secret_key):
        magic_admin.api_secret_key = api_secret_key or os.environ.get(
            'MAGIC_API_SECRET_KEY',
        )

        if magic_admin.api_secret_key is None:
            raise AuthenticationError(api_secret_api_key_missing_message)
