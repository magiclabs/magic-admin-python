from unittest import mock

import pytest

from magic_admin.resources.user import User
from testing.data.did_token import future_did_token
from testing.data.did_token import issuer
from testing.data.did_token import public_address


class TestUser:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User()

    @pytest.fixture
    def mock_get_metadata_by_issuer(self):
        with mock.patch.object(
            self.user,
            'get_metadata_by_issuer',
        ) as mock_get_metadata_by_issuer:
            yield mock_get_metadata_by_issuer

    @pytest.fixture
    def mock_logout_by_issuer(self):
        with mock.patch.object(
            self.user,
            'logout_by_issuer',
        ) as mock_logout_by_issuer:
            yield mock_logout_by_issuer

    @pytest.fixture
    def mock_construct_issuer_with_public_address(self):
        with mock.patch(
            'magic_admin.resources.user.construct_issuer_with_public_address',
        ) as mock_construct_issuer_with_public_address:
            yield mock_construct_issuer_with_public_address

    def test_get_metadata_by_issuer(self):
        with mock.patch.object(
            self.user,
            'request',
        ) as mock_request:
            assert self.user.get_metadata_by_issuer(issuer) == mock_request.return_value

        mock_request.assert_called_once_with(
            'get',
            self.user.v1_user_info,
            params={'issuer': issuer},
        )

    def test_get_metadata_by_public_address(
        self,
        mock_get_metadata_by_issuer,
        mock_construct_issuer_with_public_address,
    ):
        assert self.user.get_metadata_by_public_address(
            public_address,
        ) == mock_get_metadata_by_issuer.return_value

        mock_construct_issuer_with_public_address.assert_called_once_with(
            public_address,
        )
        mock_get_metadata_by_issuer.assert_called_once_with(
            mock_construct_issuer_with_public_address.return_value,
        )

    def test_get_metadata_by_token(self, mock_get_metadata_by_issuer):
        self.user.Token = mock.Mock()

        assert self.user.get_metadata_by_token(
            future_did_token,
        ) == mock_get_metadata_by_issuer.return_value

        self.user.Token.get_issuer.assert_called_once_with(future_did_token)
        mock_get_metadata_by_issuer.assert_called_once_with(
            self.user.Token.get_issuer.return_value,
        )

    def test_logout_by_issuer(self):
        with mock.patch.object(
            self.user,
            'request',
        ) as mock_request:
            assert self.user.logout_by_issuer(issuer) == mock_request.return_value

        mock_request.assert_called_once_with(
            'post',
            self.user.v2_user_logout,
            data={'issuer': issuer},
        )

    def test_logout_by_public_address(
        self,
        mock_logout_by_issuer,
        mock_construct_issuer_with_public_address,
    ):
        assert self.user.logout_by_public_address(
            public_address,
        ) == mock_logout_by_issuer.return_value

        mock_construct_issuer_with_public_address.assert_called_once_with(
            public_address,
        )
        mock_logout_by_issuer.assert_called_once_with(
            mock_construct_issuer_with_public_address.return_value,
        )

    def test_logout_by_token(self, mock_logout_by_issuer):
        self.user.Token = mock.Mock()

        assert self.user.logout_by_token(
            future_did_token,
        ) == mock_logout_by_issuer.return_value

        self.user.Token.get_issuer.assert_called_once_with(future_did_token)
        mock_logout_by_issuer.assert_called_once_with(
            self.user.Token.get_issuer.return_value,
        )
