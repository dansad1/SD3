class ResourceListContext:
    def __init__(self, *, list_obj, request):
        self.list = list_obj
        self.request = request

        self.resource = list_obj.get_resource()

        self.params = request.GET.dict()
        self.result = None

        self.rows = []
        self.fields = []
        self.meta = {}