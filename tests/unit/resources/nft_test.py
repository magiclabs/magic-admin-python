"""Test Mint resource component."""
from unittest import mock

from magic_admin.resources.nft import Mint


class TestNFT:  # noqa: WPS306
    """Test Mint resource component."""

    quantity = 2
    destination_address = '0x3c15B0e0e00A9edD2Be824064f9C9C29fc136C4E'
    token_id = 1
    mint = Mint()
    contract_id = 'bsdjfkn-sjknfskn-kjsnf'

    def test_start_mint721(self):
        """Test mint 721."""
        self.mint.request = mock.Mock()
        self.mint.start_mint721(
            self.contract_id,
            self.quantity,
            self.destination_address,
        )

        self.mint.request.assert_called_once_with(
            'post',
            self.mint.v1_start_mint721,
            params={
                'contract_id': self.contract_id,
                'quantity': self.quantity,
                'destination_address': self.destination_address,
            },
        )

    def test_start_mint1155(self):
        """Test mint 1155."""
        self.mint.request = mock.Mock()
        self.mint.start_mint1155(
            self.contract_id,
            self.quantity,
            self.token_id,
            self.destination_address,
        )

        self.mint.request.assert_called_once_with(
            'post',
            self.mint.v1_start_mint1155,
            params={
                'contract_id': self.contract_id,
                'quantity': self.quantity,
                'token_id': self.token_id,
                'destination_address': self.destination_address,
            },
        )