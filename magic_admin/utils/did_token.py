from magic_admin.error import DIDTokenError


def parse_public_address_from_issuer(issuer):
    """
    Args:
        issuer (str): Issuer (the signer, the "user"). This field is represented
            as a Decentralized Identifier populated with the user's Ethereum
            public key.

    Returns:
        public_address (str): An Ethereum public key.
    """
    try:
        return issuer.split(':')[2]
    except IndexError:
        raise DIDTokenError(
            'Given issuer ({}) is malformed. Please make sure it follows the '
            '`did:method-name:method-specific-id` format.'.format(issuer),
        )


def construct_issuer_with_public_address(public_address):
    return 'did:ethr:{}'.format(public_address)
