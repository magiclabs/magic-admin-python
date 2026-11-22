from enum import Enum

from magic_admin.config import base_url
from magic_admin.http_client import RequestsClient


class ResourceMeta(type):
    def __init__(cls, name, bases, cls_dict):
        if not hasattr(cls, "_registry"):
            cls._registry = {}
        else:
            cls._registry[name] = cls()

        super().__init__(name, bases, cls_dict)


class ResourceComponent(metaclass=ResourceMeta):
    _base_url = base_url

    def __getattr__(self, resource_name):
        if resource_name in self._registry:
            return self._registry[resource_name]
        else:
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute '{resource_name}'",
            )

    def setup_request_client(self, retries, timeout, backoff_factor):
        _request_client = RequestsClient(retries, timeout, backoff_factor)

        for resource in self._registry.values():
            resource._request_client = _request_client

    def _construct_url(self, url_path):
        return f"{self._base_url}{url_path}"

    def _sanitize_request_data(self, data):
        if isinstance(data, dict):
            return {k: self._sanitize_request_data(v) for k, v in data.items()}

        elif isinstance(data, (list, tuple)):
            return [self._sanitize_request_data(item) for item in data]

        elif isinstance(data, Enum):
            return data.value

        return data

    def request(self, method, url_path, params=None, data=None):
        return self._request_client.request(
            method.lower(),
            self._construct_url(url_path),
            params=self._sanitize_request_data(params),
            data=self._sanitize_request_data(data),
        )
