import os

import magic_admin
from magic_admin.resources.base import ResourceComponent


class Magic:

    def __getattr__(self, attribute_name):
        try:
            return getattr(self._resource, attribute_name)
        except AttributeError:
            pass

        return super().__getattribute__(attribute_name)

    def __init__(self, api_secret_key=None, retries=3, timeout=10, backoff_factor=0.02):
        self._set_api_secret_key(api_secret_key)
        self._resource = ResourceComponent()
        self._resource._init_request_client(retries, timeout, backoff_factor)

    def _set_api_secret_key(self, api_secret_key):
        magic_admin.api_secret_key = api_secret_key or os.environ.get(
            'MAGIC_API_SECRET_KEY',
        )

        if magic_admin.api_secret_key is None:
            raise ValueError(
                'API secret key is missing. Please specific an API secret key when '
                'you instantiate the `Magic(api_secrete_key=<KEY>)` object or use '
                'the environment variable, `MAGIC_API_SECRET_KEY`. You can get your '
                'API secret key from https://dashboard.magic.link. You if you having '
                'trouble, please don\'t hesitate to reach out to us at support@magic.link',
            )
