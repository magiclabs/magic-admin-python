import re

AUTHORIZATION_PATTERN = r'Bearer (?P<token>.+)'


def null_safe(value):
    if value is None or value in ['null', 'none', 'None', '']:
        return None

    return value


def parse_authorization_header_value(header_value):
    m = re.match(AUTHORIZATION_PATTERN, header_value)

    if m is None:
        return None

    return null_safe(m.group('token'))
