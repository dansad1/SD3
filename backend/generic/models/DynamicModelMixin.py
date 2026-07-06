from backend.generic.models.DynamicValueService import DynamicValueService


class DynamicModelMixin:

    def get_dynamic_map(
        self,
    ):
        return DynamicValueService.get_map(
            self,
        )

    def get_value(
        self,
        field_name,
        default=None,
    ):
        return DynamicValueService.get(
            self,
            field_name,
            default,
        )