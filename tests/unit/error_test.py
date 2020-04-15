from magic_admin.error import APIConnectionError
from magic_admin.error import APIError
from magic_admin.error import AuthenticationError
from magic_admin.error import BadRequestError
from magic_admin.error import DIDTokenError
from magic_admin.error import MagicError
from magic_admin.error import PermissiongError
from magic_admin.error import RateLimitingError
from magic_admin.error import RequestError


class MagicErrorBase:

    error_class = None

    message = 'Magic is amazing'

    def test_str(self):
        assert str(self.error_class(self.message)) == self.message

    def test_str_with_empty_message(self):
        assert str(self.error_class()) == '<empty message>'

    def test_repr(self):
        assert repr(self.error_class(self.message)) == '{}(message=\'Magic is '
        'amazing\')'.format(
            self.error_class.__name__,
        )

    def test_to_dict(self):
        assert self.error_class(self.message).to_dict() == {'message': str(self.message)}


class TestMagicError(MagicErrorBase):

    error_class = MagicError


class TestDIDTokenError(MagicErrorBase):

    error_class = DIDTokenError


class TestAPIConnectionError(MagicErrorBase):

    error_class = APIConnectionError


class RequestErrorBase:

    error_class = None

    message = 'Magic is amazing'
    http_status = 'success'
    http_code = 200
    http_resp_data = {'magic': 'link'}
    http_message = 'Troll goat is cute'
    http_error_code = 'TROLL_GOAT_IS_CUTE'
    http_request_params = 'a=b&b=c'
    http_request_data = {'magic': 'link'}
    http_method = 'post'

    def test_str(self):
        assert str(self.error_class(self.message)) == self.message

    def test_str_with_empty_message(self):
        assert str(self.error_class()) == '<empty message>'

    def test_repr(self):
        assert repr(
            self.error_class(
                self.message,
                http_error_code=self.http_error_code,
                http_code=self.http_code,
            ),
        ) == '{}(message=\'Magic is amazing\', http_error_code={}, http_code={}).'.format(
            self.error_class.__name__,
            self.http_error_code,
            self.http_code,
        )

    def test_to_dict(self):
        assert self.error_class(
            self.message,
            http_error_code=self.http_error_code,
            http_code=self.http_code,
            http_status=self.http_status,
            http_resp_data=self.http_resp_data,
            http_message=self.http_message,
            http_request_params=self.http_request_params,
            http_request_data=self.http_request_data,
            http_method=self.http_method,
        ).to_dict() == {
            'message': self.message,
            'http_error_code': self.http_error_code,
            'http_code': self.http_code,
            'http_status': self.http_status,
            'http_resp_data': self.http_resp_data,
            'http_message': self.http_message,
            'http_request_params': self.http_request_params,
            'http_request_data': self.http_request_data,
            'http_method': self.http_method,
        }


class TestRequestError(RequestErrorBase):

    error_class = RequestError


class TestRateLimitingError(RequestErrorBase):

    error_class = RateLimitingError


class TestBadRequestError(RequestErrorBase):

    error_class = BadRequestError


class TestAuthenticationError(RequestErrorBase):

    error_class = AuthenticationError


class TestPermissiongError(RequestErrorBase):

    error_class = PermissiongError


class TestAPIError(RequestErrorBase):

    error_class = APIError
