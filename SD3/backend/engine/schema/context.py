class FieldContext:
    def __init__(self, *, model, field, entity, request, action):
        self.model = model
        self.field = field
        self.entity = entity
        self.request = request
        self.action = action

        self.name = field.name
        self.type = None
        self.schema = {}