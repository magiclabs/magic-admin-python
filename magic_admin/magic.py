from magic_admin.resources.base import ResourceComponent


class Magic:

    resource = ResourceComponent()

    def __getattr__(self, attribute_name):
        try:
            return getattr(self.resource, attribute_name)
        except AttributeError:
            pass

        return super().__getattribute__(attribute_name)
