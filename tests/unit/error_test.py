from magic_admin.error import DIDTokenError
from magic_admin.error import MagicError


class MagicErrorBase:

    error_class = None

    message = 'Magic is amazing'

    def test_str(self):
        assert str(self.error_class(self.message)) == self.message

    def test_str_with_empty_message(self):
        assert str(self.error_class()) == '<empty message>'

    def test_repr(self):
        assert repr(self.error_class(self.message)) == \
            '{}(message=\'Magic is amazing\')'.format(self.error_class.__name__)


class TestMagicError(MagicErrorBase):

    error_class = MagicError


class TestDIDTokenError(MagicErrorBase):

    error_class = DIDTokenError
