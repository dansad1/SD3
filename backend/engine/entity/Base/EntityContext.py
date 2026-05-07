class EntityContext:

    def __init__(
        self,
        *,
        entity,
        request,
        action=None,
        instance=None,
        queryset=None,
        payload=None,
    ):

        # =========================
        # CORE
        # =========================

        self.entity = entity

        self.model = entity.model

        self.request = request

        self.user = request.user

        # =========================
        # ACTION
        # =========================

        self.action = action

        # =========================
        # RUNTIME
        # =========================

        self.instance = instance

        self.queryset = queryset

        self.payload = payload or {}

        # =========================
        # SCHEMA
        # =========================

        self.fields = []

        self.schema = {}

        # =========================
        # QUERY
        # =========================

        self.filters = {}

        self.search = None

        self.ordering = []

        # =========================
        # RESULT
        # =========================

        self.result = None

        self.errors = {}

        # =========================
        # CACHE
        # =========================

        self.cache = {}