from SD3.backend.engine.matrix.Base.BaseMatrix import BaseMatrix
from SD3.backend.engine.registry.BaseRegistry import BaseRegistry
from SD3.backend.engine.registry.autodiscover import all_subclasses
from SD3.backend.engine.registry.storage import BaseStorage


class MatrixRegistry(BaseRegistry):

    def __init__(self):
        super().__init__(storage=BaseStorage())

    def register(self, matrix_cls):
        instance = matrix_cls()
        return self.register_instance(instance.code, instance)

    def autodiscover(self, force=False):
        if self._autodiscovered and not force:
            return

        for cls in all_subclasses(BaseMatrix):
            meta = getattr(cls, "Meta", None)
            code = getattr(meta, "code", None) if meta else None

            if code:
                self.register(cls)

        self._autodiscovered = True


matrix_registry = MatrixRegistry()