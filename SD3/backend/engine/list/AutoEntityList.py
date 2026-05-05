# core/api/engine/list/AutoEntityList.py
from SD3.backend.engine.list.BaseList import BaseList
from SD3.backend.engine.schema.builder import EntitySchemaBuilder


class AutoEntityList(BaseList):

    def __init__(self, entity):
        self.entity = entity
        self.code = f"{entity.entity}.list"

    def get_fields(self, request):

        builder = EntitySchemaBuilder(self.get_entity())
        schema = builder.build(request)

        entity = self.get_entity()
        allowed = set(entity.list_display or [])

        return [
            {
                "key": f["name"],
                "label": f["label"],
                "sortable": True,
            }
            for f in schema["fields"]
            if not allowed or f["name"] in allowed
        ]

    # 🔥 ВОТ ЭТО ДОБАВЬ
    def get_default_visible_fields(self, request):
        fields = self.get_fields(request)
        return [f["key"] for f in fields]