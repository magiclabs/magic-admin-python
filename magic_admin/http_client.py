import platform

import simplejson
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import magic_admin
from magic_admin import version
from magic_admin.config import base_url


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

            return self._parse_and_convert_api_response(api_resp)
        except Exception as e:
            return self._handle_request_error(e)

    def _parse_and_convert_api_response(self, resp):
        pass

    def _handle_request_error(self, error):
        pass
