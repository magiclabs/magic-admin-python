from magic_admin.resources.base import ResourceComponent
from magic_admin.error import DIDTokenMalformed, DIDTokenExpired
from magic_admin.error import ExpectedBearerStringError
from web3 import Web3
import json


class Utils(ResourceComponent):
    """
    Utility methods for Magic Admin SDK.
    """

    def parse_authorization_header(self, header: str) -> str:
        """
        Parse a raw DID Token from the given Authorization header.

        Args:
            header (str): The Authorization header string

        Raises:
            ExpectedBearerStringError: If header is not in 'Bearer {token}' format

        Returns:
            str: The DID token extracted from the header
        """
        if not header.lower().startswith("bearer "):
            raise ExpectedBearerStringError(
                message="Expected argument to be a string in the `Bearer {token}` format."
            )

        return header[7:]  # Remove 'Bearer ' prefix

    def validate_token_ownership(
        self,
        did_token: str,
        contract_address: str,
        contract_type: str,
        rpc_url: str,
        token_id: str = None,
    ) -> dict:
        """
        Token Gating function validates user ownership of wallet + NFT.

        Args:
            did_token (str): The DID token to validate
            contract_address (str): The smart contract address
            contract_type (str): Either 'ERC721' or 'ERC1155'
            rpc_url (str): The RPC endpoint URL
            token_id (str, optional): Required for ERC1155 contracts

        Raises:
            ValueError: If ERC1155 is specified without token_id
            Exception: If DID token validation fails

        Returns:
            dict: Response with validation result
                {
                    'valid': bool,
                    'error_code': str,
                    'message': str
                }
        """
        # Make sure if ERC1155 has a tokenId
        if contract_type == "ERC1155" and not token_id:
            raise ValueError("ERC1155 requires a tokenId")

        # Validate DID token
        try:
            self.Token.validate(did_token)
            wallet_address = self.Token.get_public_address(did_token)
        except DIDTokenMalformed:
            return {
                "valid": False,
                "error_code": "UNAUTHORIZED",
                "message": "Invalid DID token: ERROR_MALFORMED_TOKEN",
            }
        except DIDTokenExpired:
            return {
                "valid": False,
                "error_code": "UNAUTHORIZED",
                "message": "Invalid DID token: ERROR_DIDT_EXPIRED",
            }
        except Exception as e:
            raise Exception(str(e))

        # Check on-chain if user owns NFT by calling contract with web3
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        if contract_type == "ERC721":
            # ERC721 ABI for balanceOf function
            abi = json.loads(
                '[{"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'
            )
            contract = w3.eth.contract(address=contract_address, abi=abi)
            balance = contract.functions.balanceOf(wallet_address).call()
        else:  # ERC1155
            # ERC1155 ABI for balanceOf function
            abi = json.loads(
                '[{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"id","type":"uint256"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"}]'
            )
            contract = w3.eth.contract(address=contract_address, abi=abi)
            balance = contract.functions.balanceOf(wallet_address, int(token_id)).call()

        if balance > 0:
            return {"valid": True, "error_code": "", "message": ""}

        return {
            "valid": False,
            "error_code": "NO_OWNERSHIP",
            "message": "User does not own this token.",
        }
