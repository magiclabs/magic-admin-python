from magic_admin.error import DIDTokenError
from magic_admin.error import MagicError


class MagicErrorBase:

    error_class = None

    message = 'Magic is amazing'

    def test_str(self):
        assert str(MagicError(self.message)) == self.message

    def test_str_with_empty_message(self):
        assert str(MagicError()) == '<empty message>'

    def test_repr(self):
        assert repr(MagicError(self.message)) == \
            'MagicError(message=\'Magic is amazing\')'


class TestMagicError(MagicErrorBase):

    error_class = MagicError


class TestDIDTokenError(MagicErrorBase):

    error_class = DIDTokenError
