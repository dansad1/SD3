class MatrixContext:
    def __init__(self, *, matrix, request, payload=None):
        self.matrix = matrix
        self.request = request
        self.payload = payload or {}

        self.schema = None
        self.data = {}
        self.changes = []
        self.result = None
        self.capabilities = {}