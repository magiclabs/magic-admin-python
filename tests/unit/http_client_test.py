import json
from collections import namedtuple
from unittest import mock

import pytest

import magic_admin
from magic_admin import version
from magic_admin.config import base_url
from magic_admin.error import APIConnectionError
from magic_admin.error import APIError
from magic_admin.error import AuthenticationError
from magic_admin.error import BadRequestError
from magic_admin.error import ForbiddenError
from magic_admin.error import RateLimitingError
from magic_admin.http_client import RequestsClient
from magic_admin.response import MagicResponse


class TestRequestsClient:
    retries = 1
    timeout = 2
    backoff_factor = 3

    def test_init(self):
        with mock.patch(
            "magic_admin.http_client.RequestsClient._setup_request_session",
        ) as mock_setup_request_session:
            rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)

        assert rc._retries == self.retries
        assert rc._timeout == self.timeout
        assert rc._backoff_factor == self.backoff_factor

        mock_setup_request_session.assert_called_once_with()

    def test_get_platform_info(self):
        platform_name = "troll_goat"
        py_version = "9.0.0.0"
        error_msg = "error_msg"

        platform = mock.Mock(
            platform=mock.Mock(return_value=platform_name),
            python_version=mock.Mock(return_value=py_version),
            uname=mock.Mock(side_effect=Exception(error_msg)),
        )

        with mock.patch(
            "magic_admin.http_client.platform",
            platform,
        ):
            assert RequestsClient._get_platform_info() == {
                "platform": platform_name,
                "language_version": py_version,
                "uname": "<{}>".format(error_msg),
            }

        platform.platform.assert_called_once_with()
        platform.python_version.assert_called_once_with()
        platform.uname.assert_called_once_with()

    def test_setup_request_session(self):
        with (
            mock.patch(
                "magic_admin.http_client.Session",
            ) as mock_session,
            mock.patch(
                "magic_admin.http_client.HTTPAdapter",
            ) as mock_http_adapter,
            mock.patch(
                "magic_admin.http_client.Retry",
            ) as mock_retry,
        ):
            RequestsClient(self.retries, self.timeout, self.backoff_factor)

        mock_retry.assert_called_once_with(
            total=self.retries,
            backoff_factor=self.backoff_factor,
        )
        mock_http_adapter.assert_called_once_with(
            max_retries=mock_retry.return_value,
        )
        mock_session.return_value.mount.assert_called_once_with(
            base_url,
            mock_http_adapter.return_value,
        )
        mock_session.assert_called_once_with()

    def test_get_request_headers(self):
        rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)
        platform_info = {"troll": "goat"}
        magic_admin.api_secret_key = "magic_secret_key"

        with mock.patch.object(
            rc,
            "_get_platform_info",
            return_value=platform_info,
        ) as mock_get_platform_info:
            assert rc._get_request_headers() == {
                "X-Magic-Secret-Key": magic_admin.api_secret_key,
                "User-Agent": json.dumps(
                    {
                        "language": "python",
                        "sdk_version": version.VERSION,
                        "publisher": "magic",
                        "http_lib": rc.__class__.__name__,
                        **platform_info,
                    }
                ),
            }

        mock_get_platform_info.assert_called_once_with()

    def test_get_request_headers_raises_error(self):
        rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)
        magic_admin.api_secret_key = None

        with pytest.raises(AuthenticationError):
            rc._get_request_headers()

    def test_handle_request_error(self):
        rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)
        exception = Exception("troll_goat")

        with pytest.raises(APIConnectionError) as e:
            rc._handle_request_error(exception)

        assert str(e.value) == (
            "Unexpected error thrown while communicating to Magic. "
            "Please reach out to support@magic.link if the problem continues. "
            "Error message: {error_class} was raised - {error_message}".format(
                error_class=exception.__class__.__name__,
                error_message=str(exception) or "no error message.",
            )
        )


class TestRequestClientRequest:
    retries = 1
    timeout = 2
    backoff_factor = 3

    mock_tuple = namedtuple(
        "mock_tuple",
        [
            "get_request_headers",
            "handle_request_error",
            "parse_and_convert_to_api_response",
        ],
    )

    @pytest.fixture(autouse=True)
    def setup(self):
        self.some_headers = {"troll": "goat"}
        self.method = "post"
        self.url = "/path"
        self.params = "params"
        self.data = "data"

        self.rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)
        self.rc.http = mock.Mock()

    @pytest.fixture
    def mock_funcs(self):
        with (
            mock.patch.object(
                self.rc,
                "_get_request_headers",
                return_value=self.some_headers,
            ) as mock_get_request_headers,
            mock.patch.object(
                self.rc,
                "_handle_request_error",
            ) as mock_handle_request_error,
            mock.patch.object(
                self.rc,
                "_parse_and_convert_to_api_response",
            ) as mock_parse_and_convert_to_api_response,
        ):
            yield self.mock_tuple(
                mock_get_request_headers,
                mock_handle_request_error,
                mock_parse_and_convert_to_api_response,
            )

    def test_request_no_exception_and_returns_api_response(self, mock_funcs):
        assert (
            self.rc.request(
                self.method,
                self.url,
                params=self.params,
                data=self.data,
            )
            == mock_funcs.parse_and_convert_to_api_response.return_value
        )

        mock_funcs.get_request_headers.assert_called_once_with()
        self.rc.http.request.assert_called_once_with(
            self.method,
            self.url,
            params=self.params,
            json=self.data,
            headers=self.some_headers,
            timeout=self.timeout,
        )
        mock_funcs.handle_request_error.assert_not_called()
        mock_funcs.parse_and_convert_to_api_response.assert_called_once_with(
            self.rc.http.request.return_value,
            self.params,
            self.data,
        )

    def test_request_exceptions_and_handles_error(self, mock_funcs):
        exception = Exception()
        self.rc.http.request = mock.Mock(side_effect=exception)

        assert (
            self.rc.request(
                self.method,
                self.url,
                params=self.params,
                data=self.data,
            )
            == mock_funcs.handle_request_error.return_value
        )

        mock_funcs.get_request_headers.assert_called_once_with()
        self.rc.http.request.assert_called_once_with(
            self.method,
            self.url,
            params=self.params,
            json=self.data,
            headers=self.some_headers,
            timeout=self.timeout,
        )
        mock_funcs.handle_request_error.assert_called_once_with(exception)
        mock_funcs.parse_and_convert_to_api_response.assert_not_called()


class TestParseAndConvertToAPIResponse:
    retries = 1
    timeout = 2
    backoff_factor = 3

    @pytest.fixture(autouse=True)
    def setup(self):
        self.params = "params"
        self.request_data = "request_data"
        self.data = {
            "data": "troll_goat",
            "status": "failed",
            "message": "troll_goat_is_cute",
            "error_code": "some_error",
        }

        self.rc = RequestsClient(self.retries, self.timeout, self.backoff_factor)
        self.resp = mock.Mock(json=mock.Mock(return_value=self.data))

    def test_ok_response(self):
        self.resp.status_code = 200

        parsed_resp = self.rc._parse_and_convert_to_api_response(
            self.resp,
            self.params,
            self.request_data,
        )

        assert isinstance(parsed_resp, MagicResponse)
        assert parsed_resp.content == self.resp.content
        assert parsed_resp.status_code == self.resp.status_code
        assert parsed_resp.data == self.data

    @pytest.mark.parametrize(
        "status_code,error_class",
        [
            (400, BadRequestError),
            (401, AuthenticationError),
            (403, ForbiddenError),
            (429, RateLimitingError),
            # Generic API Error if we did not specify handling it.
            (499, APIError),
        ],
    )
    def test_client_error_response(self, status_code, error_class):
        self.resp.status_code = status_code

        with pytest.raises(error_class) as e:
            self.rc._parse_and_convert_to_api_response(
                self.resp,
                self.params,
                self.request_data,
            )

        assert e.value.to_dict() == {
            "http_status": self.data["status"],
            "http_code": self.resp.status_code,
            "http_resp_data": self.data["data"],
            "http_message": self.data["message"],
            "http_error_code": self.data["error_code"],
            "http_request_params": self.params,
            "http_request_data": self.request_data,
            "http_method": self.resp.request.method,
            "message": mock.ANY,
        }
