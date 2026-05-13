from backend.engine.action.Base.BaseAction import BaseAction
from backend.engine.registry.BaseRegistry import BaseRegistry
from backend.engine.registry.autodiscover import all_subclasses
from backend.engine.registry.storage import BaseStorage


class ActionRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(
            storage=BaseStorage()
        )

    # =====================================================
    # REGISTER
    # =====================================================

    def register(self, action_cls):

        instance = action_cls()

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

        for cls in reversed(all_subclasses(BaseAction)):

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
# SINGLETON
# =====================================================

actions = ActionRegistry()