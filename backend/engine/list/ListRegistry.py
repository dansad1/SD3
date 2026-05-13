from backend.engine.Resource.ResourceList.ResourceList import ResourceList
from backend.engine.Resource.ResourceRegistry import resource_registry
from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.list.AutoEntityList import AutoEntityList
from backend.engine.list.BaseList import BaseList
from backend.engine.registry.BaseRegistry import BaseRegistry
from backend.engine.registry.autodiscover import all_subclasses
from backend.engine.registry.storage import BaseStorage


class ListRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(
            storage=BaseStorage(),
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, list_cls):

        instance = list_cls()

        return self.register_instance(
            instance.code,
            instance,
        )

    # =====================================================
    # AUTODISCOVER
    # =====================================================

    def autodiscover(self, force=False):

        if self._autodiscovered and not force:
            return

        seen = set()

        for cls in reversed(all_subclasses(BaseList)):

            code = getattr(cls, "code", None)

            if not code:
                continue

            # ====================================
            # newest class wins
            # ====================================

            if code in seen:
                continue

            seen.add(code)

            self.register(cls)

        self._autodiscovered = True

    # =====================================================
    # OVERRIDES
    # =====================================================

    def _find_override(self, code):

        for cls in reversed(all_subclasses(BaseList)):

            cls_code = getattr(cls, "code", None)

            if cls_code == code:
                return cls()

        return None

    # =====================================================
    # GET
    # =====================================================

    def get(self, code):

        # ====================================
        # cache
        # ====================================

        instance = self.storage.get(code)

        if instance:
            return instance

        # ====================================
        # explicit override
        # ====================================

        override = self._find_override(code)

        if override:
            return self.register_instance(
                code,
                override,
            )

        # ====================================
        # validate
        # ====================================

        if not code.endswith(".list"):
            raise ValueError(
                f"Invalid list code: {code}"
            )

        name = code[:-5]

        # ====================================
        # resource fallback
        # ====================================

        try:

            resource = resource_registry.get(name)

            return self.register_instance(
                code,
                ResourceList(
                    resource=resource,
                    code=code,
                ),
            )

        except KeyError:
            pass

        # ====================================
        # entity fallback
        # ====================================

        entity = entity_registry.get(name)

        return self.register_instance(
            code,
            AutoEntityList(entity),
        )


# =====================================================
# SINGLETON
# =====================================================

list_registry = ListRegistry()