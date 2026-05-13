from backend.engine.entity.EntityRegistry import entity_registry
from backend.engine.form.AutoEntityForm import AutoEntityForm
from backend.engine.form.BaseForm import BaseForm
from backend.engine.registry.BaseRegistry import BaseRegistry
from backend.engine.registry.autodiscover import all_subclasses
from backend.engine.registry.storage import BaseStorage


class FormRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(
            storage=BaseStorage(),
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, form_cls):

        instance = form_cls()

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

        for cls in reversed(all_subclasses(BaseForm)):

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

        for cls in reversed(all_subclasses(BaseForm)):

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
        # auto entity form
        # ====================================

        if not code.endswith(".form"):
            raise ValueError(
                f"Invalid form code: {code}"
            )

        entity_name = code[:-5]

        entity = entity_registry.get(entity_name)

        return self.register_instance(
            code,
            AutoEntityForm(entity),
        )


# =====================================================
# SINGLETON
# =====================================================

form_registry = FormRegistry()