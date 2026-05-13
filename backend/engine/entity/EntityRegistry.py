from backend.engine.entity.Base.BaseEntity import BaseEntity
from backend.engine.registry.BaseRegistry import BaseRegistry
from backend.engine.registry.autodiscover import all_subclasses
from backend.engine.registry.hooks import RegistryHooks
from backend.engine.registry.storage import EntityStorage
from backend.engine.registry.validator import validate_duplicate, is_valid_entity_class


class EntityRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(
            storage=EntityStorage(),
            hooks=RegistryHooks(),
        )

    # =========================
    # REGISTER
    # =========================

    def register(self, entity_cls):
        instance = entity_cls()

        # 🔥 проверка дубликатов по model
        validate_duplicate(
            self.storage.get_by_model(instance.model),
            instance,
            "Model"
        )

        return self.register_instance(
            instance.entity,
            instance
        )

    # =========================
    # SAVE (🔥 ВАЖНО)
    # =========================

    def _save(self, code, instance):
        # EntityStorage сам знает как сохранять
        self.storage.add(instance)

    # =========================
    # AUTODISCOVER
    # =========================

    def autodiscover(self, force=False):

        if self._autodiscovered and not force:
            return

        seen = set()

        for cls in reversed(all_subclasses(BaseEntity)):

            if not is_valid_entity_class(cls):
                continue

            entity = getattr(cls, "entity", None)

            if not entity:
                continue

            # ====================================
            # берем newest class
            # ====================================

            if entity in seen:
                continue

            seen.add(entity)

            self.register(cls)

        self._autodiscovered = True
    # =========================
    # EXTRA API
    # =========================

    def get_by_model(self, model):
        entity = self.storage.get_by_model(model)

        if not entity:
            raise KeyError(
                f"Unknown model: {model.__name__}"
            )

        return entity

    def for_model(self, model):
        return self.storage.get_by_model(model)


# 🔥 singleton (правильно — вне класса)
entity_registry = EntityRegistry()