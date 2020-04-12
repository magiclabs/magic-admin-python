import base64

import simplejson
from eth_account.messages import defunct_hash_message
from web3.auto import w3

from magic_admin.error import DIDTokenError
from magic_admin.resources.base import ResourceComponent
from magic_admin.utils.time import apply_did_token_nbf_grace_period
from magic_admin.utils.time import epoch_time_now


EXPECTED_DID_TOKEN_CONTENT_LENGTH = 2


class Token(ResourceComponent):

    required_fields = frozenset([
        'iat',
        'ext',
        'nbf',
        'iss',
        'sub',
        'aud',
        'tid',
    ])

    @staticmethod
    def _parse_public_address(issuer):
        """
        Args:
            issuer (str): Issuer (the signer, the "user"). This field is represented
                as a Decentralized Identifier populated with the user's Ethereum
                public key.

        Returns:
            public_address (str): An Ethereum public key.
        """
        return issuer.split(':')[-1]

    @classmethod
    def _check_required_fields(cls, claim):
        """
        Args:
            claim (dict): A dict that represents the claim portion of the DID
                token.

        Returns:
            None.
        """
        for field in cls.required_fields:
            if field not in claim:
                raise DIDTokenError(
                    message='DID token is missing a required field: {}'.format(
                        field,
                    ),
                )

    @classmethod
    def decode(cls, did_token):
        """
        Args:
            did_token (base64.str): Base64 encoded string.

        Raises:
            DIDTokenError: If token format is invalid.

        Returns:
            proof (str): A signed message.
            claim (dict): A dict of unsigned message.
        """
        try:
            decoded_did_token = simplejson.loads(
                base64.urlsafe_b64decode(did_token).decode('utf-8'),
            )
        except Exception:
            raise DIDTokenError(
                message='DID token is malformed. It has to be a based64 encoded '
                'JSON serialized string.',
            )

        if len(decoded_did_token) != EXPECTED_DID_TOKEN_CONTENT_LENGTH:
            raise DIDTokenError(
                message='DID token is malformed. It has to have two parts '
                '[proof, claim].',
            )

        proof = decoded_did_token[0]

        try:
            claim = simplejson.loads(decoded_did_token[1])
        except Exception:
            raise DIDTokenError(
                message='DID token is malformed. Given claim should be a JSON '
                'serialized string.',
            )

        cls._check_required_fields(claim)

        return proof, claim

    @classmethod
    def get_issuer(cls, did_token):
        """
        Args:
            did_token (base64.str): Base64 encoded string.

        Returns:
            issuer (str): Issuer (the signer, the "user"). This field is represented
                as a Decentralized Identifier populated with the user's Ethereum
                public key.
        """
        _, claim = cls.decode(did_token)

        return claim['iss']

    @classmethod
    def get_public_address(cls, did_token):
        """
        Args:
            did_token (base64.str): Base64 encoded string.

        Returns:
            public_address (str): An Ethereum public key.
        """
        return cls._parse_public_address(cls.get_issuer(did_token))

    @classmethod
    def validate(cls, did_token):
        """
        Args:
            did_token (base64.str): Base64 encoded string.

        Raises:
            DIDTokenError: If DID token fails the validation.

        Returns:
            None.
        """
        proof, claim = cls.decode(did_token)
        recovered_address = w3.eth.account.recoverHash(
            defunct_hash_message(
                text=simplejson.dumps(claim, separators=(',', ':')),
            ),
            signature=proof,
        )

        if recovered_address != cls.get_public_address(did_token):
            raise DIDTokenError(
                message='Signature mismatch between "proof" and "claim". Please '
                'generate a new token with an intended issuer.',
            )

        current_time_in_s = epoch_time_now()

        if current_time_in_s > claim['ext']:
            raise DIDTokenError(
                message='Given DiD token has expired. Please generate a new one.',
            )

        if current_time_in_s < apply_did_token_nbf_grace_period(claim['nbf']):
            raise DIDTokenError(
                message='Given DID token cannot be used at this time. Please '
                'check the "nbf" field and regenerate a new token with a suitable '
                'value.',
            )
