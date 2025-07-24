from unittest import mock

from magic_admin import did_token_nbf_grace_period_s
from magic_admin.utils.time import apply_did_token_nbf_grace_period
from magic_admin.utils.time import epoch_time_now


class TestTimeUtils:
    def test_epoch_time_now(self):
        with mock.patch("magic_admin.utils.time.time") as mock_time:
            mock_time.time.return_value = 8084

            assert epoch_time_now() == 8084

        mock_time.time.assert_called_once_with()

    def test_apply_did_token_nbf_grace_period(self):
        timestamp = 8084
        assert (
            apply_did_token_nbf_grace_period(
                timestamp,
            )
            == timestamp - did_token_nbf_grace_period_s
        )
