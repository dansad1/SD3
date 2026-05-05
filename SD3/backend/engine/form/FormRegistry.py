from SD3.backend.engine.form.BaseForm import BaseForm
from SD3.backend.engine.registry.BaseRegistry import BaseRegistry
from SD3.backend.engine.registry.autodiscover import all_subclasses
from SD3.backend.engine.registry.storage import BaseStorage


class FormRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(storage=BaseStorage())

    def register(self, form_cls):
        instance = form_cls()
        return self.register_instance(instance.code, instance)

    def _find_override(self, code):
        for cls in all_subclasses(BaseForm):
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

        entity_name = code.replace(".form", "")
        entity = entity_registry.get(entity_name)

        return self.register_instance(
            code,
            AutoEntityForm(entity)
        )


form_registry = FormRegistry()