from unittest import mock

import pytest

import magic_admin
from magic_admin.error import AuthenticationError
from magic_admin.magic import Magic
from magic_admin.resources.base import ResourceComponent


class TestMagic:
    api_secret_key = "troll_goat"

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mocked_rc = mock.Mock(
            request=mock.Mock(
                return_value=mock.Mock(
                    data={
                        "client_id": "1234",
                    },
                ),
            ),
        )
        # self.mocked_rc.request=
        with mock.patch(
            "magic_admin.magic.RequestsClient", return_value=self.mocked_rc
        ):
            yield

    def test_init_with_secret_key(self):
        Magic(api_secret_key=self.api_secret_key)

        assert magic_admin.api_secret_key == self.api_secret_key

    @pytest.mark.parametrize(
        "resource_name",
        ResourceComponent._registry.keys(),
    )
    def test_init_with_request_client_set_on_resources(self, resource_name):
        magic = Magic(api_secret_key=self.api_secret_key)

        assert getattr(magic, resource_name)._request_client

    @pytest.mark.parametrize(
        "resource_name",
        ResourceComponent._registry.keys(),
    )
    def test_gets_resource(self, resource_name):
        magic = Magic(api_secret_key=self.api_secret_key)

        assert getattr(magic, resource_name)

    def test_raises_attr_error(self):
        with pytest.raises(AttributeError):
            Magic(api_secret_key=self.api_secret_key).troll_goat

    def test_raises_authentication_error_if_secret_key_missing(self):
        with pytest.raises(AuthenticationError):
            Magic()
