class FormContext:
    def __init__(self, *, form, request, mode, pk=None, payload=None):
        self.form = form
        self.request = request
        self.mode = mode
        self.pk = pk
        self.payload = payload or {}

        self.entity = form.get_entity()
        self.model = self.entity.model

        self.instance = None
        self.fields = []
        self.capabilities = {}

        self.data = {}
        self.clean = {}
        self.m2m = {}
        self.dynamic = {}

        self.result = None