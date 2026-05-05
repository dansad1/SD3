class ListContext:
    def __init__(self, *, list_obj, request):
        self.list = list_obj
        self.request = request

        self.entity = list_obj.get_entity()

        self.qs = None
        self.fields = []
        self.rows = []

        self.page = None
        self.paginator = None

        self.capabilities = {}