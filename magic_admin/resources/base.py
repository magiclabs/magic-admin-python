class ResourceMeta(type):

    def __init__(cls, name, bases, cls_dict):
        if not hasattr(cls, '_registry'):
            cls._registry = {}
        else:
            cls._registry[name] = cls()

        super().__init__(name, bases, cls_dict)


class ResourceComponent(metaclass=ResourceMeta):

    def __getattr__(self, resource_name):
        if resource_name in self._registry:
            return self._registry[resource_name]
        else:
            raise AttributeError(
                '{object_name} has no attribute \'{resource_name}\''.format(
                    object_name=self.__class__.__name__,
                    resource_name=resource_name,
                ),
            )
