class ValidationContext:

    def __init__(
        self,
        *,
        field,
        value,
        payload=None,
        request=None,
        entity=None,
        instance=None,
    ):

        self.field = field

        self.value = value

        self.payload = payload or {}

        self.request = request

        self.entity = entity

        self.instance = instance

        self.errors = []