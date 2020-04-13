from unittest import mock

import pytest
import simplejson

from magic_admin.error import DIDTokenError
from magic_admin.resources.token import Token


class TestToken:

    did_token = 'magic_token'
    public_address = 'magic_address'
    issuer = 'did:ethr:{}'.format(public_address)

    def test_required_fields(self):
        assert Token.required_fields.difference(
            {'nbf', 'sub', 'iss', 'ext', 'aud', 'tid', 'iat'},
        ) == frozenset()

    def test_parse_public_address(self):
        assert Token._parse_public_address(self.issuer) == self.public_address

    def test_check_required_fields_raises_error(self):
        claim = {
            'nbf': mock.ANY,
            'sub': mock.ANY,
            'aud': mock.ANY,
            'tid': mock.ANY,
            'iat': mock.ANY,
        }

        with pytest.raises(DIDTokenError) as e:
            Token._check_required_fields(claim)

        assert str(e.value) == 'DID token is missing required field(s): ' \
            '[\'ext\', \'iss\']'

    def test_check_required_fields_passes(self):
        claim = {
            'nbf': mock.ANY,
            'sub': mock.ANY,
            'aud': mock.ANY,
            'tid': mock.ANY,
            'iat': mock.ANY,
            'iss': mock.ANY,
            'ext': mock.ANY,
        }

        Token._check_required_fields(claim)

    def test_decode_raises_error_if_did_token_is_malformed(self):
        exception = Exception()

        with mock.patch(
            'magic_admin.resources.token.base64.urlsafe_b64decode',
            side_effect=exception,
        ) as mock_urlsafe_b64decode, pytest.raises(
            DIDTokenError,
        ) as e:
            Token.decode(self.did_token)

        mock_urlsafe_b64decode.assert_called_once_with(self.did_token)
        assert str(e.value) == 'DID token is malformed. It has to be a based64 ' \
            'encoded JSON serialized string. Exception (<empty message>).'

    def test_decode_raises_error_if_did_token_has_missing_parts(self):
        malformed_decoded_did_token = ('miss one part')

        with mock.patch(
            'magic_admin.resources.token.simplejson.loads',
            return_value=malformed_decoded_did_token,
        ) as mock_json_loads, mock.patch(
            'magic_admin.resources.token.base64.urlsafe_b64decode',
        ) as mock_urlsafe_b64decode, pytest.raises(
            DIDTokenError,
        ) as e:
            Token.decode(self.did_token)

        mock_urlsafe_b64decode.assert_called_once_with(self.did_token)
        mock_json_loads.assert_called_once_with(
            mock_urlsafe_b64decode.return_value.decode.return_value,
        )
        assert str(e.value) == 'DID token is malformed. It has to have two parts ' \
            '[proof, claim].'

    def test_decode_raises_error_if_claim_is_not_json_serializable(self):
        exception = Exception()

        with mock.patch(
            'magic_admin.resources.token.simplejson.loads',
        ) as mock_json_loads, mock.patch(
            'magic_admin.resources.token.base64.urlsafe_b64decode',
        ) as mock_urlsafe_b64decode, pytest.raises(
            DIDTokenError,
        ) as e:
            mock_json_loads.side_effect = [
                ('proof_in_str', 'claim_in_str'),  # Succeeds the first time.
                exception,  # Fails the second time.
            ]

            Token.decode(self.did_token)

        mock_urlsafe_b64decode.assert_called_once_with(self.did_token)
        assert mock_json_loads.call_args_list == [
            mock.call(mock_urlsafe_b64decode.return_value.decode.return_value),
            mock.call('claim_in_str'),
        ]
        assert str(e.value) == 'DID token is malformed. Given claim should be ' \
            'a JSON serialized string. Exception (<empty message>).'

    def test_decode_passes(self):
        with mock.patch(
            'magic_admin.resources.token.simplejson.loads',
            side_effect=[('proof_in_str', 'claim_in_str'), 'claim'],
        ) as mock_json_loads, mock.patch(
            'magic_admin.resources.token.base64.urlsafe_b64decode',
        ) as mock_urlsafe_b64decode, mock.patch.object(
            Token,
            '_check_required_fields',
        ) as mock_check_required_fields:
            assert Token.decode(self.did_token) == ('proof_in_str', 'claim')

        mock_urlsafe_b64decode.assert_called_once_with(self.did_token)
        mock_check_required_fields.assert_called_once_with('claim')
        assert mock_json_loads.call_args_list == [
            mock.call(mock_urlsafe_b64decode.return_value.decode.return_value),
            mock.call('claim_in_str'),
        ]

    def test_get_issuer_passes(self):
        mocked_claim = {'iss': self.issuer}

        with mock.patch.object(
            Token,
            'decode',
            return_value=(mock.ANY, mocked_claim),
        ) as mock_decode:
            assert Token.get_issuer(self.did_token) == self.issuer

        mock_decode.assert_called_once_with(self.did_token)

    def test_get_public_address_pass(self):
        with mock.patch.object(
            Token,
            '_parse_public_address',
            return_value=self.public_address,
        ) as mock_parse_public_address, mock.patch.object(
            Token,
            'get_issuer',
        ) as mock_get_issuer:
            assert Token.get_public_address(self.did_token) == self.public_address

        mock_get_issuer.assert_called_once_with(self.did_token)
        mock_parse_public_address.assert_called_once_with(mock_get_issuer.return_value)

    def test_validate_raises_error_if_signature_mismatch(self, mock_validate):
        mock_validate['mock_get_public_address'].return_value = 'random_public_address'

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(mock_validate)
        assert str(e.value) == 'Signature mismatch between "proof" and "claim". ' \
            'Please generate a new token with an intended issuer.'

    @pytest.fixture
    def mock_validate(self):
        proof = 'proof'
        claim = {
            'ext': 8084,
            'nbf': 6666,
        }

        with mock.patch.object(
            Token,
            'decode',
            return_value=(proof, claim),
        ) as mock_decode, mock.patch(
            'magic_admin.resources.token.w3.eth.account.recoverHash',
            return_value=self.public_address,
        ) as mock_recoverHash, mock.patch(
            'magic_admin.resources.token.defunct_hash_message',
        ) as mock_defunct_hash_message, mock.patch.object(
            Token,
            'get_public_address',
            return_value=self.public_address,
        ) as mock_get_public_address, mock.patch(
            'magic_admin.resources.token.epoch_time_now',
            return_value=claim['ext'] - 1,
        ) as mock_epoch_time_now, mock.patch(
            'magic_admin.resources.token.apply_did_token_nbf_grace_period',
            return_value=claim['nbf'],
        ) as mock_apply_did_token_nbf_grace_period:
            yield {
                'proof': proof,
                'claim': claim,
                'mock_decode': mock_decode,
                'mock_recoverHash': mock_recoverHash,
                'mock_defunct_hash_message': mock_defunct_hash_message,
                'mock_get_public_address': mock_get_public_address,
                'mock_epoch_time_now': mock_epoch_time_now,
                'mock_apply_did_token_nbf_grace_period': mock_apply_did_token_nbf_grace_period,
            }

    def _assert_validate_funcs_called(
        self,
        mock_validate,
        should_time_func_called=False,
        should_grace_period_func_called=False,
    ):
        mock_validate['mock_decode'].assert_called_once_with(self.did_token)
        mock_validate['mock_defunct_hash_message'].assert_called_once_with(
            text=simplejson.dumps(mock_validate['claim'], separators=(',', ':')),
        )
        mock_validate['mock_recoverHash'].assert_called_once_with(
            mock_validate['mock_defunct_hash_message'].return_value,
            signature=mock_validate['proof'],
        )
        mock_validate['mock_get_public_address'].assert_called_once_with(
            self.did_token,
        )

        if should_time_func_called:
            mock_validate['mock_epoch_time_now'].assert_called_once_with()
        else:
            mock_validate['mock_epoch_time_now'].assert_not_called()

        if should_grace_period_func_called:
            mock_validate['mock_apply_did_token_nbf_grace_period'].assert_called_once_with(
                mock_validate['claim']['nbf'],
            )
        else:
            mock_validate['mock_apply_did_token_nbf_grace_period'].assert_not_called()

    def test_validate_raises_error_if_did_token_expires(self, mock_validate):
        mock_validate['mock_epoch_time_now'].return_value = \
            mock_validate['claim']['ext'] + 1

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            mock_validate,
            should_time_func_called=True,
        )
        assert str(e.value) == 'Given DiD token has expired. Please generate a ' \
            'new one.'

    def test_validate_raises_error_if_did_token_used_before_nbf(self, mock_validate):
        mock_validate['mock_epoch_time_now'].return_value = \
            mock_validate['claim']['nbf'] - 1

        with pytest.raises(DIDTokenError) as e:
            Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            mock_validate,
            should_time_func_called=True,
            should_grace_period_func_called=True,
        )
        assert str(e.value) == 'Given DID token cannot be used at this time. ' \
            'Please check the "nbf" field and regenerate a new token with a ' \
            'suitable value.'

    def test_validate_passes(self, mock_validate):
        Token.validate(self.did_token)

        self._assert_validate_funcs_called(
            mock_validate,
            should_time_func_called=True,
            should_grace_period_func_called=True,
        )
