from django.core.exceptions import ValidationError


class BaseFieldType:

    code = "base"
    label = "Base"

    widget = None

    sortable = True
    searchable = False
    filterable = False

    # =====================================================
    # FIELD BUILDER FEATURES
    # =====================================================

    features = []

    default_value_widget = None

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        if (
            field.required
            and value in (
                None,
                "",
                [],
            )
        ):
            raise ValidationError(
                "Обязательное поле"
            )

        if (
            field.is_multiple
            and value is not None
            and not isinstance(
                value,
                list,
            )
        ):
            raise ValidationError(
                "Ожидался список"
            )

        return value

    # =====================================================
    # NORMALIZE
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):
        return value

    # =====================================================
    # SERIALIZE
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        return value

    # =====================================================
    # DESERIALIZE
    # =====================================================

    def deserialize(
        self,
        field,
        value,
    ):
        return value

    # =====================================================
    # VALUE ACCESS
    # =====================================================

    def get_value(
        self,
        field,
        obj,
    ):
        return getattr(
            obj,
            field.name,
            None,
        )

    def set_value(
        self,
        field,
        obj,
        value,
    ):
        setattr(
            obj,
            field.name,
            value,
        )

        return obj

    # =====================================================
    # UI
    # =====================================================

    def get_widget(
        self,
        field,
    ):
        return (
            self.widget
            or self.code
        )

    def get_features(
        self,
        field,
    ):
        return self.features

    def get_default_value_widget(
        self,
        field,
    ):
        return (
            self.default_value_widget
            or self.get_widget(field)
        )

    # =====================================================
    # UI SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        return {

            "type":
                self.code,

            "widget":
                self.get_widget(
                    field
                ),

            "sortable":
                self.sortable,

            "searchable":
                self.searchable,

            "filterable":
                self.filterable,

            # =====================================
            # FIELD BUILDER
            # =====================================

            "features":
                self.get_features(
                    field
                ),

            "default_value_widget":
                self.get_default_value_widget(
                    field
                ),
        }

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        if value in (
            None,
            "",
        ):
            return queryset

        return queryset.filter(
            **{
                field.name: value
            }
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def apply_search(
        self,
        queryset,
        field,
        value,
    ):

        if not value:
            return queryset

        if not self.searchable:
            return queryset

        return queryset.filter(
            **{
                f"{field.name}__icontains":
                    value
            }
        )

    # =====================================================
    # SORT
    # =====================================================

    def apply_sort(
        self,
        queryset,
        field,
        direction,
    ):

        if not self.sortable:
            return queryset

        key = field.name

        if direction == "desc":
            key = f"-{key}"

        return queryset.order_by(
            key
        )