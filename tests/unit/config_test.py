from magic_admin.config import base_url


def test_base_url():
    assert base_url == "https://api.toaster.magic.link"
