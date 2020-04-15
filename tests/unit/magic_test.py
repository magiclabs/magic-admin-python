from unittest import mock

from magic_admin.magic import BACKOFF_FACTOR
from magic_admin.magic import Magic
from magic_admin.magic import RETRIES
from magic_admin.magic import TIMEOUT


class TestMagic:

    api_secret_key = 'troll_goat'

    def test_init(self):
        mocked_rc = mock.Mock()

        with mock.patch(
            'magic_admin.magic.ResourceComponent',
            return_value=mocked_rc,
        ) as mock_resource_component, mock.patch(
            'magic_admin.magic.Magic._set_api_secret_key',
        ) as mock_set_api_secret_key:
            Magic(api_secret_key=self.api_secret_key)

        mock_resource_component.assert_called_once_with()
        mocked_rc.setup_request_client.setup_request_client(
            RETRIES,
            TIMEOUT,
            BACKOFF_FACTOR,
        )
        mock_set_api_secret_key.assert_called_once_with(self.api_secret_key)

    def test_retrieves_secret_key_from_env_variable(self):
        pass
