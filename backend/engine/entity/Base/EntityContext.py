class EntityContext:
    def __init__(self, *, entity, request):
        self.entity = entity
        self.model = entity.model
        self.request = request
        self.user = request.user