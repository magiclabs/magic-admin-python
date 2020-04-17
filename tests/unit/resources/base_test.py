from unittest import mock

import pytest

from magic_admin.resources.base import ResourceComponent


class TestResourceComponent:

    retries = 1
    timeout = 2
    backoff_factor = 3

    method = 'get'
    url_path = '/troll/goat'
    params = 'params'
    data = 'data'

    @pytest.fixture(autouse=True)
    def setup(self):
        self.rc = ResourceComponent()

    def test_setup_request_client(self):
        with mock.patch(
            'magic_admin.resources.base.RequestsClient',
        ) as mock_request_client:
            self.rc.setup_request_client(
                self.retries,
                self.timeout,
                self.backoff_factor,
            )

        mock_request_client.assert_called_once_with(
            self.retries,
            self.timeout,
            self.backoff_factor,
        )
        for resource in self.rc._registry.values():
            assert getattr(resource, '_request_client') == \
                mock_request_client.return_value

    def test_construct_url(self):
        assert self.rc._construct_url(self.url_path) == '{}{}'.format(
            self.rc._base_url,
            self.url_path,
        )

    def test_request(self):
        self.rc._request_client = mock.Mock()

        with mock.patch.object(
            self.rc,
            '_construct_url',
        ) as mock_construct_url:
            assert self.rc.request(
                self.method,
                self.url_path,
                params=self.params,
                data=self.data,
            ) == self.rc._request_client.request.return_value

        mock_construct_url.assert_called_once_with(self.url_path)
