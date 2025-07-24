import pytest

from magic_admin.utils.http import null_safe
from magic_admin.utils.http import parse_authorization_header_value


class TestNullSafe:
    @pytest.mark.parametrize("value", [None, "null", "none", "None", ""])
    def test_returns_none(self, value):
        assert null_safe(value) is None

    def test_returns_value(self):
        value = "troll_goat"

        assert null_safe(value) == value


class TestParseAuthHeaderValue:
    malformed = "wrong_format"
    expected = "Bearer troll_goat"

    def test_returns_none_if_not_in_bearer_format(self):
        assert parse_authorization_header_value(self.malformed) is None

    def test_returns_value(self):
        assert parse_authorization_header_value(self.expected) == "troll_goat"
