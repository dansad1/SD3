class BaseStorage:

    def __init__(self):
        self.by_code = {}

    def add(self, code, instance):
        self.by_code[code] = instance

    def get(self, code):
        return self.by_code.get(code)

    def all(self):
        return list(self.by_code.values())
class EntityStorage(BaseStorage):

    def __init__(self):
        super().__init__()
        self.by_model = {}

    def add(self, entity):
        super().add(entity.entity, entity)
        self.by_model[entity.model] = entity

    def get_by_model(self, model):
        return self.by_model.get(model)