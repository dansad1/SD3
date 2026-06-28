
from django.core.exceptions import ValidationError
from django.db.models import Q


class BaseFieldType:

    code = "base"
    label = "Base"

    widget = None

    sortable = True
    searchable = False
    filterable = False

    features = []

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):
        return []

    # =====================================================
    # VALIDATION
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
    # NORMALIZATION
    # =====================================================

    def normalize(
        self,
        field,
        value,
    ):
        return value

    def should_save(
        self,
        field,
        value,
    ):
        return True
    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(
        self,
        field,
        value,
    ):
        return value

    def deserialize(
        self,
        field,
        value,
    ):
        return value

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

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        field,
        request=None,
        instance=None,
    ):

        schema = {

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

            "features":
                self.get_features(
                    field
                ),
        }

        options = self.get_options(
            field,
            request=request,
            instance=instance,
        )

        if options:
            schema["options"] = options

        return schema

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(

            self,

            queryset,

            field,

            value,

    ):

        print(

            "APPLY",

            field.name,

            value,

        )

        qs = queryset.filter(

            **{

                field.name:

                    value,

            }

        )

        print(

            "COUNT",

            qs.count(),

        )

        return qs
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
                    value,
            }
        )

    def build_search_q(
            self,
            field,
            value,
    ):

        if not value:
            return Q()

        if not self.searchable:
            return Q()

        return Q(
            **{
                f"{field.name}__icontains":
                    value,
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
        print("SORT", field.name, direction)

        if not self.sortable:
            return queryset

        key = field.name

        if direction == "desc":
            key = f"-{key}"

        print("ORDER BY", key)

        return queryset.order_by(key)