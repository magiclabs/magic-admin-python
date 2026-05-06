from magic_admin.resources.base import ResourceComponent
from magic_admin.resources.wallet import WalletType
from magic_admin.utils.did_token import construct_issuer_with_public_address


class User(ResourceComponent):
    v1_user_info = "/v1/admin/user"
    v1_users_info = "/v1/admin/users"
    v1_user_logout = "/v1/admin/user/logout"
    v2_user_info = "/v2/admin/user"

    def get_metadata_by_email(self, email, provider=None):
        params = {"type": "email", "value": email}
        if provider:
            params["provider"] = provider
        return self.request("get", self.v2_user_info, params=params)

    def get_metadata_by_issuer_and_wallet(self, issuer, wallet_type):
        return self.request(
            "get",
            self.v1_user_info,
            params={"issuer": issuer, "wallet_type": wallet_type},
        )

    def get_metadata_by_public_address_and_wallet(self, public_address, wallet_type):
        return self.get_metadata_by_issuer_and_wallet(
            construct_issuer_with_public_address(public_address),
            wallet_type,
        )

    def get_metadata_by_token_and_wallet(self, did_token, wallet_type):
        return self.get_metadata_by_issuer_and_wallet(
            self.Token.get_issuer(did_token), wallet_type
        )

    def get_metadata_by_issuer(self, issuer):
        return self.get_metadata_by_issuer_and_wallet(issuer, WalletType.NONE)

    def get_metadata_by_public_address(self, public_address):
        return self.get_metadata_by_issuer(
            construct_issuer_with_public_address(public_address),
        )

    def get_metadata_by_public_addresses(self, public_addresses):
        return self.request(
            "post",
            self.v1_users_info,
            data={
                "issuers": [
                    construct_issuer_with_public_address(addr)
                    for addr in public_addresses
                ],
            },
        )

    def get_metadata_by_token(self, did_token):
        return self.get_metadata_by_issuer(self.Token.get_issuer(did_token))

    def logout_by_issuer(self, issuer):
        return self.request("post", self.v1_user_logout, data={"issuer": issuer})

    def logout_by_public_address(self, public_address):
        return self.logout_by_issuer(
            construct_issuer_with_public_address(public_address),
        )

    def logout_by_token(self, did_token):
        return self.logout_by_issuer(self.Token.get_issuer(did_token))
