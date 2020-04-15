from collections import namedtuple
from unittest import mock

import pytest
import simplejson

from magic_admin.error import DIDTokenError
from magic_admin.resources.token import Token


class TestToken:

    did_token = 'magic_token'
    public_address = 'magic_address'
    issuer = 'did:ethr:{}'.format(public_address)

    @staticmethod
    def _generate_claim(fields=None):
        return {field: mock.ANY for field in fields or Token.required_fields}

    def test_required_fields(self):
        assert Token.required_fields.difference(
            {'nbf', 'sub', 'iss', 'ext', 'aud', 'tid', 'iat'},
        ) == frozenset()

    def test_check_required_fields_raises_error(self):
        with pytest.raises(DIDTokenError) as e:
            Token._check_required_fields(
                self._generate_claim(fields=['nbf', 'sub', 'aud', 'tid', 'iat']),
            )

        assert str(e.value) == 'DID token is missing required field(s): ' \
            '[\'ext\', \'iss\']'

    def test_check_required_fields_passes(self):
        Token._check_required_fields(self._generate_claim())

    def test_get_issuer_passes(self):
        mocked_claim = {'iss': self.issuer}

        with mock.patch.object(
            Token,
            'decode',
            return_value=(mock.ANY, mocked_claim),
        ) as mock_decode:
            assert Token.get_issuer(self.did_token) == self.issuer

        mock_decode.assert_called_once_with(self.did_token)

    def test_get_public_address_passes(self):
        with mock.patch(
            'magic_admin.resources.token.parse_public_address_from_issuer',
            return_value=self.public_address,
        ) as mock_parse_public_address, mock.patch.object(
            Token,
            'get_issuer',
        ) as mock_get_issuer:
            assert Token.get_public_address(self.did_token) == self.public_address

        mock_get_issuer.assert_called_once_with(self.did_token)
        mock_parse_public_address.assert_called_once_with(mock_get_issuer.return_value)


class TestTokenDecode:

    did_token = 'magic_token'
    public_address = 'magic_address'

    mock_funcs = namedtuple('mock_funcs', 'urlsafe_b64decode, json_loads')

    @pytest.fixture
    def setup_mocks(self):
        with mock.patch(
            'magic_admin.resources.token.base64.urlsafe_b64decode',
        ) as mock_urlsafe_b64decode, mock.patch(
            'magic_admin.resources.token.simplejson.loads',
        ) as mock_json_loads:
            yield self.mock_funcs(mock_urlsafe_b64decode, mock_json_loads)

    def test_decode_raises_error_if_did_token_is_malformed(self, setup_mocks):
        setup_mocks.urlsafe_b64decode.side_effect = Exception()

        with pytest.raises(DIDTokenError) as e:
            Token.decode(self.did_token)

        setup_mocks.urlsafe_b64decode.assert_called_once_with(self.did_token)
        assert str(e.value) == 'DID token is malformed. It has to be a based64 ' \
            'encoded JSON serialized string. Exception (<empty message>).'

    def test_decode_raises_error_if_did_token_has_missing_parts(self, setup_mocks):
        setup_mocks.json_loads.return_value = ('miss one part')

        with pytest.raises(DIDTokenError) as e:
            Token.decode(self.did_token)

        setup_mocks.urlsafe_b64decode.assert_called_once_with(self.did_token)
        setup_mocks.json_loads.assert_called_once_with(
            setup_mocks.urlsafe_b64decode.return_value.decode.return_value,
        )
        assert str(e.value) == 'DID token is malformed. It has to have two parts ' \
            '[proof, claim].'

    def test_decode_raises_error_if_claim_is_not_json_serializable(self, setup_mocks):
        with pytest.raises(DIDTokenError) as e:
            setup_mocks.json_loads.side_effect = [
                ('proof_in_str', 'claim_in_str'),  # Succeeds the first time.
                Exception(),  # Fails the second time.
            ]

            Token.decode(self.did_token)

        setup_mocks.urlsafe_b64decode.assert_called_once_with(self.did_token)
        assert setup_mocks.json_loads.call_args_list == [
            mock.call(setup_mocks.urlsafe_b64decode.return_value.decode.return_value),
            mock.call('claim_in_str'),
        ]
        assert str(e.value) == 'DID token is malformed. Given claim should be ' \
            'a JSON serialized string. Exception (<empty message>).'

    def test_decode_passes(self, setup_mocks):
        setup_mocks.json_loads.side_effect = [
            ('proof_in_str', 'claim_in_str'),
            'claim',
        ]

        with mock.patch.object(
            Token,
            '_check_required_fields',
        ) as mock_check_required_fields:
            assert Token.decode(self.did_token) == ('proof_in_str', 'claim')

        setup_mocks.urlsafe_b64decode.assert_called_once_with(self.did_token)
        mock_check_required_fields.assert_called_once_with('claim')
        assert setup_mocks.json_loads.call_args_list == [
            mock.call(setup_mocks.urlsafe_b64decode.return_value.decode.return_value),
            mock.call('claim_in_str'),
        ]


class TestTokenValidate:

    did_token = 'magic_token'
    public_address = 'magic_address'

    mock_funcs = namedtuple(
        'mock_funcs',
        [
            'proof',
            'claim',
            'decode',
            'recoverHash',
            'defunct_hash_message',
            'get_public_address',
            'epoch_time_now',
            'apply_did_token_nbf_grace_period',
        ],
    )

    @pytest.fixture
    def setup_mocks(self):
        proof = 'proof'
        claim = {
            'ext': 8084,
            'nbf': 6666,
        }

        with mock.patch.object(
            Token,
            'decode',
            return_value=(proof, claim),
        ) as decode, mock.patch(
            'magic_admin.resources.token.w3.eth.account.recoverHash',
            return_value=self.public_address,
        ) as recoverHash, mock.patch(
            'magic_admin.resources.token.defunct_hash_message',
        ) as defunct_hash_message, mock.patch.object(
            Token,
            'get_public_address',
            return_value=self.public_address,
        ) as get_public_address, mock.patch(
            'magic_admin.resources.token.epoch_time_now',
            return_value=claim['ext'] - 1,
        ) as epoch_time_now, mock.patch(
            'magic_admin.resources.token.apply_did_token_nbf_grace_period',
            return_value=claim['nbf'],
        ) as apply_did_token_nbf_grace_period:
            yield self.mock_funcs(
                proof,
                claim,
                decode,
                recoverHash,
                defunct_hash_message,
                get_public_address,
                epoch_time_now,
                apply_did_token_nbf_grace_period,
            )

    def _assert_validate_funcs_called(
        self,
        setup_mocks,
        is_time_func_called=False,
        is_grace_period_func_called=False,
    ):
        setup_mocks.decode.assert_called_once_with(self.did_token)
        setup_mocks.defunct_hash_message.assert_called_once_with(
            text=simplejson.dumps(setup_mocks.claim, separators=(',', ':')),
        )
        setup_mocks.recoverHash.assert_called_once_with(
            setup_mocks.defunct_hash_message.return_value,
            signature=setup_mocks.proof,
        )
        setup_mocks.get_public_address.assert_called_once_with(
            self.did_token,
        )

        if is_time_func_called:
            setup_mocks.epoch_time_now.assert_called_once_with()
        else:
            setup_mocks.epoch_time_now.assert_not_called()

        if is_grace_period_func_called:
            setup_mocks.apply_did_token_nbf_grace_period.assert_called_once_with(
                setup_mocks.claim['nbf'],
            )
        else:
            setup_mocks.apply_did_token_nbf_grace_period.assert_not_called()

    def test_validate_raises_error_if_signature_mismatch(self, setup_mocks):
        setup_mocks.get_public_address.return_value = 'random_public_address'

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(setup_mocks)
        assert str(e.value) == 'Signature mismatch between "proof" and "claim". ' \
            'Please generate a new token with an intended issuer.'

    def test_validate_raises_error_if_did_token_expires(self, setup_mocks):
        setup_mocks.epoch_time_now.return_value = \
            setup_mocks.claim['ext'] + 1

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            setup_mocks,
            is_time_func_called=True,
        )
        assert str(e.value) == 'Given DID token has expired. Please generate a ' \
            'new one.'

    def test_validate_raises_error_if_did_token_used_before_nbf(self, setup_mocks):
        setup_mocks.epoch_time_now.return_value = \
            setup_mocks.claim['nbf'] - 1

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            setup_mocks,
            is_time_func_called=True,
            is_grace_period_func_called=True,
        )
        assert str(e.value) == 'Given DID token cannot be used at this time. ' \
            'Please check the "nbf" field and regenerate a new token with a ' \
            'suitable value.'

    def test_validate_passes(self, setup_mocks):
        Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            setup_mocks,
            is_time_func_called=True,
            is_grace_period_func_called=True,
        )
