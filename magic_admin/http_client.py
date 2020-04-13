import platform

import simplejson
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import magic_admin
from magic_admin import version
from magic_admin.config import base_url
from magic_admin.error import APIConnectionError
from magic_admin.error import APIError
from magic_admin.error import AuthenticationError
from magic_admin.error import BadRequestError
from magic_admin.error import PermissiongError
from magic_admin.error import RateLimitingError
from magic_admin.response import MagicResponse


class RequestsClient:

    def __init__(self, retries, timeout, backoff_factor):
        self._retries = retries
        self._timeout = timeout
        self._backoff_factor = backoff_factor

        self._setup_request_session()

    @staticmethod
    def _get_platform_info():
        platform_info = {}

        for attr, func in [
            ['language_version', platform.python_version],
            ['platform', platform.platform],
            ['uname', lambda: ' '.join(platform.uname())],
        ]:
            try:
                val = func()
            except Exception as e:
                val = '<{}>'.fortmat(str(e))

            platform_info[attr] = val

        return platform_info

    def _setup_request_session(self):
        """Take advantage of the ``requets.Session``. If cleint is making several
        requests to the same host, the underlying TCP connection will be reused,
        which can result in a significant performance increase.
        """
        self.http = Session()
        self.http.mount(
            base_url,
            HTTPAdapter(
                max_retries=Retry(
                    total=self._retries,
                    backoff_factor=self._backoff_factor,
                ),
            ),
        )

    def _get_request_headers(self):
        user_agent = {
            'language': 'python',
            'sdk_version': version.VERSION,
            'publisher': 'magic',
            'http_lib': self.__class__.__name__,
            **self._get_platform_info(),
        }

        if magic_admin.api_secret_key is None:
            raise AuthenticationError(
                message='API secret key is missing. Please specific an API secret '
                'key when you instantiate the `Magic(api_secrete_key=<KEY>)` object '
                'or use the environment variable, `MAGIC_API_SECRET_KEY`. You can '
                'get your API secret key from https://dashboard.magic.link. You if '
                'you having trouble, please don\'t hesitate to reach out to us at '
                'support@magic.link',
            )

        return {
            'X-Magic-Secret-Key': magic_admin.api_secret_key,
            'User-Agent': simplejson.dumps(user_agent),
        }

    def request(self, method, url, params=None, data=None):
        try:
            api_resp = self.http.request(
                method,
                url,
                params=params,
                # Requests auto-converts this to JSON and add content-type
                # `application/json`.
                json=data,
                headers=self._get_request_headers(),
                timeout=self._timeout,
            )
        except Exception as e:
            return self._handle_request_error(e)

        return self._parse_and_convert_to_api_response(
            api_resp,
            params,
            data,
        )

    def _parse_and_convert_to_api_response(self, resp, params, request_data):
        status_code = resp.status_code

        if 200 <= status_code < 300:
            return MagicResponse(resp.content, resp.json(), status_code)

        if status_code == 429:
            error_class = RateLimitingError
        elif status_code == 400:
            error_class = BadRequestError
        elif status_code == 401:
            error_class = AuthenticationError
        elif status_code == 403:
            error_class = PermissiongError
        else:
            error_class = APIError

        resp_data = resp.json()
        return error_class(
            http_status=resp_data.get('status'),
            http_code=status_code,
            http_resp_data=resp_data,
            http_message=resp_data.get('message'),
            http_error_code=resp_data.get('error_code'),
            http_request_params=params,
            http_request_data=request_data,
        )

    def _handle_request_error(self, e):
        message = 'Unexpected error thrown while communicating to Magic. ' \
            'Please reach out to support@magic.link if the problem continue. ' \
            'Error message: A {error_class} was raised - {error_message}'.format(
                error_class=e.__class__.__name__,
                error_message=str(e) or 'no error message.',
            )

        raise APIConnectionError(message)
