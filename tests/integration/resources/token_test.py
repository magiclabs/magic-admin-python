from unittest import mock

from pretend import stub

from magic_admin.resources.token import Token
from testing.data.did_token import claim
from testing.data.did_token import future_did_token
from testing.data.did_token import issuer
from testing.data.did_token import proof
from testing.data.did_token import public_address


class TestToken:
    def test_check_required_fields(self):
        Token._check_required_fields(claim)

    def test_decode(self):
        assert Token.decode(future_did_token) == (proof, claim)

    def test_get_issuer(self):
        assert Token.get_issuer(future_did_token) == issuer

    def test_get_public_address(self):
        assert Token.get_public_address(future_did_token) == public_address

    def test_validate(self):
        with mock.patch(
            "magic_admin.resources.token.magic_admin",
            new=stub(client_id="did:magic:731848cc-084e-41ff-bbdf-7f103817ea6b"),
        ):
            Token.validate(future_did_token)
