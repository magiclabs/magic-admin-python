from magic_admin.resources.base import ResourceComponent


class User(ResourceComponent):

    v1_user_info = '/v1/admin/auth/user/get'
    v2_user_logout = '/v2/admin/auth/user/logout'

    def get_metadata_by_issuer(self, issuer):
        self.request('get', self.v1_user_info, params={'issuer': issuer})

    def get_metadata_by_public_address(self, public_address):
        pass

    def get_metadata_by_token(self, did_token):
        pass

    def logout_by_issuer(self, issuer):
        pass

    def logout_by_public_address(self, public_address):
        pass

    def logout_by_token(self, did_token):
        pass
