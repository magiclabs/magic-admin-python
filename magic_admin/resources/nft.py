"""Module for the Mint resource component. Mint ERC721 and ERC1155 tokens."""
from magic_admin.resources.base import ResourceComponent


class NFT(ResourceComponent):
    """Minting resource component."""

    v1_start_mint721 = '/v1/admin/nft/mint/721_mint'
    v1_start_mint1155 = '/v1/admin/nft/mint/1155_mint'

    def start_mint721(
        self,
        contract_id: str,
        quantity: int,
        destination_address: str,
    ):
        """Mint ERC721 tokens.

        Args:
            contract_id (str): The contract ID of the ERC721 token.
            quantity (int): The number of tokens to mint.
            destination_address (str): The address to mint the tokens to.

        Returns:
            {
                data: {
                    request_id: str,
                }, # noqa: RST203
                status: str,
                error_code: str,
                message: str,
            }

        """
        return self.request(
            'post',
            self.v1_start_mint721,
            data={
                'contract_id': contract_id,
                'quantity': quantity,
                'destination_address': destination_address,
            },
        )

    def start_mint1155(
        self,
        contract_id: str,
        quantity: int,
        token_id: int,
        destination_address: str,
    ):
        """Mint ERC1155 tokens.

        Args:
            contract_id (str): The contract ID of the ERC1155 token.
            quantity (int): The number of tokens to mint.
            token_id (int): The token ID of the ERC1155 token.
            destination_address (str): The address to mint the tokens to.

        Returns:
            {
                data: {
                    request_id: str,
                }, # noqa: RST203
                status: str,
                error_code: str,
                message: str,
            }

        """
        return self.request(
            'post',
            self.v1_start_mint1155,
            data={
                'contract_id': contract_id,
                'quantity': quantity,
                'token_id': token_id,
                'destination_address': destination_address,
            },
        )
