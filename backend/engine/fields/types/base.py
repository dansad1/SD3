from django.core.exceptions import ValidationError


class BaseFieldType:

    # =====================================================
    # META
    # =====================================================

    code = "base"

    label = "Base"

    widget = None

    sortable = True

    searchable = False

    filterable = False

    # =====================================================
    # VALIDATE
    # =====================================================

    def validate(
        self,
        field,
        value,
    ):

        # =============================================
        # REQUIRED
        # =============================================

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

        # =============================================
        # MULTIPLE
        # =============================================

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
    # WIDGET
    # =====================================================

    def get_widget(
        self,
        field,
    ):

        return (
            self.widget
            or self.code
        )

    # =====================================================
    # UI SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
    ):

        return {

            # =========================================
            # TYPE
            # =========================================

            "type":
                self.code,

            # =========================================
            # WIDGET
            # =========================================

            "widget":
                self.get_widget(
                    field
                ),

            # =========================================
            # CAPABILITIES
            # =========================================

            "sortable":
                self.sortable,

            "searchable":
                self.searchable,

            "filterable":
                self.filterable,
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

        return queryset.filter(**{
            field.name: value
        })

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

        return queryset.filter(**{
            f"{field.name}__icontains": value
        })

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