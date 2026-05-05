from SD3.backend.engine.action.Base.BaseAction import BaseAction
from SD3.backend.engine.registry.BaseRegistry import BaseRegistry
from SD3.backend.engine.registry.autodiscover import all_subclasses
from SD3.backend.engine.registry.storage import BaseStorage

f

class ActionRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(storage=BaseStorage())

    def register(self, action_cls):
        instance = action_cls()
        return self.register_instance(instance.code, instance)

    def autodiscover(self, force=False):
        if self._autodiscovered and not force:
            return

        for cls in all_subclasses(BaseAction):
            if getattr(cls, "code", None):
                self.register(cls)

        self._autodiscovered = True


actions = ActionRegistry()