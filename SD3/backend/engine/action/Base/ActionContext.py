class ActionContext:
    def __init__(self, *, action, request, payload=None, ctx=None):
        self.action = action
        self.request = request

        self.payload = payload or {}
        self.ctx = ctx or {}

        self.result = {}