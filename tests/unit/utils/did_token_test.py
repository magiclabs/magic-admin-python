import pytest

from magic_admin.error import DIDTokenError
from magic_admin.utils.did_token import construct_issuer_with_public_address
from magic_admin.utils.did_token import parse_public_address_from_issuer
from testing.data.did_token import issuer
from testing.data.did_token import public_address


class TestDIDToken:

    malformed_issuer = 'troll_goat'

    def test_parse_public_address_from_issuer(self):
        assert parse_public_address_from_issuer(issuer) == public_address

    def test_parse_public_address_from_issuer_raises_error(self):
        with pytest.raises(DIDTokenError) as e:
            parse_public_address_from_issuer(self.malformed_issuer)

        assert str(e.value) == \
            'Given issuer ({}) is malformed. Please make sure it follows the ' \
            '`did:method-name:method-specific-id` format.'.format(self.malformed_issuer)

    def test_construct_issuer_with_public_address(self):
        assert issuer == construct_issuer_with_public_address(public_address)
