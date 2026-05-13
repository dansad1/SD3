from backend.engine.registry.hooks import RegistryHooks
from backend.engine.registry.validator import validate_duplicate


class BaseRegistry:

    def __init__(self, storage, hooks=None):
        self.storage = storage
        self.hooks = hooks or RegistryHooks()
        self._autodiscovered = False

    # =====================================================
    # REGISTER
    # =====================================================

    def register_instance(self, code, instance):

        if not code:
            raise RuntimeError("code is required")

        existing = self.storage.get(code)

        # ====================================
        # validate duplicate
        # ====================================

        validate_duplicate(
            existing,
            instance,
            label=code,
        )

        # ====================================
        # hooks before
        # ====================================

        self.hooks.run_before(instance)

        # ====================================
        # save
        # ====================================

        self._save(code, instance)


        # ====================================
        # hooks after
        # ====================================

        self.hooks.run_after(instance)

        return instance

    # =====================================================
    # SAVE
    # =====================================================

    def _save(self, code, instance):
        self.storage.add(code, instance)

    # =====================================================
    # GET
    # =====================================================

    def get(self, code):

        obj = self.storage.get(code)

        if not obj:
            raise KeyError(f"Unknown: {code}")

        return obj

    # =====================================================
    # ALL
    # =====================================================

    def all(self):
        return self.storage.all()

    # =====================================================
    # ITEMS
    # =====================================================

    def items(self):
        return self.storage.items()

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        if hasattr(self.storage, "clear"):
            self.storage.clear()

        self._autodiscovered = False