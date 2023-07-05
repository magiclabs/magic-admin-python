from unittest import mock

import pytest

import magic_admin
from magic_admin.error import AuthenticationError
from magic_admin.magic import BACKOFF_FACTOR
from magic_admin.magic import Magic
from magic_admin.magic import RETRIES
from magic_admin.magic import TIMEOUT


class TestMagic:

    api_secret_key = 'troll_goat'

    @pytest.fixture(autouse=True)
    def setup(self):
        self.mocked_resource_component = mock.Mock()
        self.mocked_request_client = mock.Mock(
            request=mock.Mock(
                return_value=mock.Mock(
                    data={
                        'client_id': '1234',
                    },
                ),
            ),
        )
        with mock.patch(
            'magic_admin.magic.ResourceComponent',
            return_value=self.mocked_resource_component,
        ), mock.patch(
            'magic_admin.magic.RequestsClient',
            return_value=self.mocked_request_client,
        ):
            yield

    @pytest.fixture(autouse=True)
    def teardown(self):
        yield
        magic_admin.api_secret_key = None

    def test_init(self):
        with mock.patch(
            'magic_admin.magic.Magic._set_api_secret_key',
        ) as mock_set_api_secret_key:
            Magic(api_secret_key=self.api_secret_key)

        self.mocked_resource_component.setup_request_client.assert_called_once_with(
            RETRIES,
            TIMEOUT,
            BACKOFF_FACTOR,
        )
        mock_set_api_secret_key.assert_called_once_with(self.api_secret_key)

    def test_retrieves_secret_key_from_env_variable(self):
        assert magic_admin.api_secret_key is None

        with mock.patch(
            'os.environ.get',
            return_value=self.api_secret_key,
        ) as mock_env_get:
            Magic()

        assert magic_admin.api_secret_key == self.api_secret_key
        mock_env_get.assert_called_once_with('MAGIC_API_SECRET_KEY')

    def test_retrieves_secret_key_from_the_passed_in_value(self):
        assert magic_admin.api_secret_key is None

        Magic(api_secret_key=self.api_secret_key)

        assert magic_admin.api_secret_key == self.api_secret_key

    def test_raises_authentication_error_if_secret_key_is_missing(self):
        with pytest.raises(AuthenticationError):
            Magic()
