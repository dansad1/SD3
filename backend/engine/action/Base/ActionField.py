class ActionField:

    def __init__(self, data):

        self.data = data

        self.name = data.get("name")
        self.label = data.get("label")

        self.field_type = data.get(
            "field_type",
            data.get("type", "string")
        )

        self.required = data.get("required", False)
        self.readonly = data.get("readonly", False)

    def __getattr__(self, item):
        return self.data.get(item)