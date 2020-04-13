import pytest

from magic_admin.magic import Magic
from magic_admin.resources.base import ResourceComponent


class TestMagic:

    @pytest.mark.parametrize(
        'resource_name',
        ResourceComponent._registry.keys(),
    )
    def test_magic_gets_resource(self, resource_name):
        magic = Magic()

        assert getattr(magic, resource_name)

    def test_magic_raises_attr_error(self):
        with pytest.raises(AttributeError):
            Magic().troll_goat
