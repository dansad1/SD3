from SD3.backend.engine.Resource.ResourceList.ResourceList import ResourceList
from SD3.backend.engine.Resource.ResourceRegistry import resource_registry
from SD3.backend.engine.entity.EntityRegistry import entity_registry
from SD3.backend.engine.list.AutoEntityList import AutoEntityList
from SD3.backend.engine.list.BaseList import BaseList
from SD3.backend.engine.registry.BaseRegistry import BaseRegistry
from SD3.backend.engine.registry.autodiscover import all_subclasses
from SD3.backend.engine.registry.storage import BaseStorage


class ListRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(storage=BaseStorage())

    def register(self, list_cls):
        instance = list_cls()
        return self.register_instance(instance.code, instance)

    def _find_override(self, code):
        for cls in all_subclasses(BaseList):
            if getattr(cls, "code", None) == code:
                return cls()
        return None

    def get(self, code):

        instance = self.storage.get(code)
        if instance:
            return instance

        override = self._find_override(code)
        if override:
            return self.register_instance(code, override)

        if not code.endswith(".list"):
            raise ValueError(f"Invalid list code: {code}")

        name = code[:-5]

        # resource fallback
        try:
            resource = resource_registry.get(name)
            return self.register_instance(
                code,
                ResourceList(resource=resource, code=code)
            )
        except KeyError:
            pass

        # entity fallback
        entity = entity_registry.get(name)

        return self.register_instance(
            code,
            AutoEntityList(entity)
        )


list_registry = ListRegistry()