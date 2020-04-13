from magic_admin.resources.base import ResourceComponent
from magic_admin.utils.did_token import construct_issuer_with_public_address


class User(ResourceComponent):

    v1_user_info = '/v1/admin/auth/user/get'
    v2_user_logout = '/v2/admin/auth/user/logout'

    def get_metadata_by_issuer(self, issuer):
        return self.request('get', self.v1_user_info, params={'issuer': issuer})

    def get_metadata_by_public_address(self, public_address):
        return self.get_metadata_by_issuer(
            construct_issuer_with_public_address(public_address),
        )

    def get_metadata_by_token(self, did_token):
        return self.get_metadata_by_issuer(self.Token.get_issuer(did_token))

    def logout_by_issuer(self, issuer):
        return self.request('post', self.v2_user_logout, data={'issuer': issuer})

    def logout_by_public_address(self, public_address):
        return self.logout_by_issuer(
            construct_issuer_with_public_address(public_address),
        )

    def logout_by_token(self, did_token):
        return self.logout_by_issuer(self.Token.get_issuer(did_token))
