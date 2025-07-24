from unittest import mock
from unittest.mock import sentinel

import pytest
from pretend import stub

from magic_admin.resources.user import User
from magic_admin.resources.wallet import WalletType
from testing.data.did_token import future_did_token
from testing.data.did_token import public_address


class TestUser:
    metadata_with_wallets = stub(
        data=stub(
            email=sentinel.email,
            issuer=sentinel.issuer,
            public_address=sentinel.public_address,
            wallets=[
                stub(
                    network=sentinel.network,
                    wallet_type=WalletType.ETH.value,
                    public_address=sentinel.public_address_1,
                ),
                stub(
                    network=sentinel.network,
                    wallet_type=WalletType.ETH.value,
                    public_address=sentinel.public_address_2,
                ),
                stub(
                    network=sentinel.network,
                    wallet_type=WalletType.ETH.value,
                    public_address=sentinel.public_address_3,
                ),
            ],
        ),
        error_code=sentinel.error_code,
        message=sentinel.message,
        status=sentinel.status,
    )

    metadata_no_wallets = stub(
        data=stub(
            email=sentinel.email,
            issuer=sentinel.issuer,
            public_address=sentinel.public_address,
        ),
        error_code=sentinel.error_code,
        message=sentinel.message,
        status=sentinel.ok,
    )

    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User()
        self.user.Token = mock.Mock()

    @pytest.fixture
    def mock_construct_issuer_with_public_address(self, mocker):
        return mocker.patch(
            "magic_admin.resources.user.construct_issuer_with_public_address",
            return_value=sentinel.public_address,
        )

    def test_get_metadata_by_issuer(self):
        self.user.get_metadata_by_issuer_and_wallet = mock.Mock(
            return_value=self.metadata_no_wallets,
        )

        assert (
            self.user.get_metadata_by_issuer(
                sentinel.issuer,
            )
            == self.metadata_no_wallets
        )

        self.user.get_metadata_by_issuer_and_wallet.assert_called_once_with(
            sentinel.issuer,
            WalletType.NONE,
        )

    def test_get_metadata_by_issuer_and_any_wallet(self):
        self.user.request = mock.Mock(return_value=self.metadata_with_wallets)

        assert (
            self.user.get_metadata_by_issuer_and_wallet(
                sentinel.issuer,
                WalletType.ANY,
            )
            == self.metadata_with_wallets
        )

        self.user.request.assert_called_once_with(
            "get",
            self.user.v1_user_info,
            params={
                "issuer": sentinel.issuer,
                "wallet_type": WalletType.ANY,
            },
        )

    def test_get_metadata_by_token(self):
        self.user.get_metadata_by_issuer = mock.Mock(
            return_value=self.metadata_no_wallets
        )

        assert (
            self.user.get_metadata_by_token(
                future_did_token,
            )
            == self.user.get_metadata_by_issuer.return_value
        )

        self.user.Token.get_issuer.assert_called_once_with(future_did_token)
        self.user.get_metadata_by_issuer.assert_called_once_with(
            self.user.Token.get_issuer.return_value,
        )

    def test_get_metadata_by_token_and_any_wallet(self):
        self.user.get_metadata_by_issuer_and_wallet = mock.Mock(
            return_value=self.metadata_with_wallets,
        )

        assert (
            self.user.get_metadata_by_token_and_wallet(
                future_did_token,
                WalletType.ANY,
            )
            == self.user.get_metadata_by_issuer_and_wallet.return_value
        )

        self.user.Token.get_issuer.assert_called_once_with(future_did_token)
        self.user.get_metadata_by_issuer_and_wallet.assert_called_once_with(
            self.user.Token.get_issuer.return_value,
            WalletType.ANY,
        )

    def test_get_metadata_by_public_address(
        self,
        mock_construct_issuer_with_public_address,
    ):
        self.user.get_metadata_by_issuer = mock.Mock(
            return_value=self.metadata_no_wallets
        )

        assert (
            self.user.get_metadata_by_public_address(
                sentinel.public_address,
            )
            == self.user.get_metadata_by_issuer.return_value
        )

        mock_construct_issuer_with_public_address.assert_called_once_with(
            sentinel.public_address,
        )
        self.user.get_metadata_by_issuer.assert_called_once_with(
            mock_construct_issuer_with_public_address.return_value,
        )

    def test_get_metadata_by_public_address_and_any_wallet(
        self,
        mock_construct_issuer_with_public_address,
    ):
        self.user.get_metadata_by_issuer_and_wallet = mock.Mock(
            return_value=self.metadata_with_wallets,
        )

        assert (
            self.user.get_metadata_by_public_address_and_wallet(
                sentinel.public_address,
                WalletType.ANY,
            )
            == self.user.get_metadata_by_issuer_and_wallet.return_value
        )

        mock_construct_issuer_with_public_address.assert_called_once_with(
            sentinel.public_address,
        )
        self.user.get_metadata_by_issuer_and_wallet.assert_called_once_with(
            mock_construct_issuer_with_public_address.return_value,
            WalletType.ANY,
        )

    def test_logout_by_issuer(self):
        self.user.request = mock.Mock()

        assert self.user.logout_by_issuer(
            sentinel.issuer,
        )

        self.user.request.assert_called_once_with(
            "post",
            self.user.v1_user_logout,
            data={
                "issuer": sentinel.issuer,
            },
        )

    def test_logout_by_public_address(
        self,
        mock_construct_issuer_with_public_address,
    ):
        self.user.logout_by_issuer = mock.Mock()

        assert (
            self.user.logout_by_public_address(
                public_address,
            )
            == self.user.logout_by_issuer.return_value
        )

        mock_construct_issuer_with_public_address.assert_called_once_with(
            public_address,
        )
        self.user.logout_by_issuer.assert_called_once_with(
            mock_construct_issuer_with_public_address.return_value,
        )

    def test_logout_by_token(self):
        self.user.logout_by_issuer = mock.Mock()

        assert (
            self.user.logout_by_token(
                future_did_token,
            )
            == self.user.logout_by_issuer.return_value
        )

        self.user.Token.get_issuer.assert_called_once_with(future_did_token)
        self.user.logout_by_issuer.assert_called_once_with(
            self.user.Token.get_issuer.return_value,
        )
