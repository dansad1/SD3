class BaseStorage:

    def __init__(self):
        self.by_code = {}

    # =====================================================
    # ADD
    # =====================================================

    def add(self, code, instance):
        self.by_code[code] = instance

    # =====================================================
    # GET
    # =====================================================

    def get(self, code):
        return self.by_code.get(code)

    # =====================================================
    # ALL
    # =====================================================

    def all(self):
        return list(self.by_code.values())

    # =====================================================
    # ITEMS
    # =====================================================

    def items(self):
        return self.by_code.items()

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):
        self.by_code.clear()


class EntityStorage(BaseStorage):

    def __init__(self):
        super().__init__()
        self.by_model = {}

    # =====================================================
    # ADD
    # =====================================================

    def add(self, entity):

        super().add(
            entity.entity,
            entity,
        )

        self.by_model[entity.model] = entity

    # =====================================================
    # GET MODEL
    # =====================================================

    def get_by_model(self, model):
        return self.by_model.get(model)

    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        super().clear()

        self.by_model.clear()