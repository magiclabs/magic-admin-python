def parse_public_address_from_issuer(issuer):
    """
    Args:
        issuer (str): Issuer (the signer, the "user"). This field is represented
            as a Decentralized Identifier populated with the user's Ethereum
            public key.

    Returns:
        public_address (str): An Ethereum public key.
    """
    return issuer.split(':')[-1]


def construct_issuer_with_public_address(public_address):
    return 'did:ethr:{}'.format(public_address)
