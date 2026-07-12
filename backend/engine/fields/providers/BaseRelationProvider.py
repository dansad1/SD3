class BaseRelationProvider:

    code = None

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):
        return None

    # =====================================================
    # INITIAL
    # =====================================================

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):
        return None

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):
        return value

    # =====================================================
    # NORMALIZATION
    # =====================================================

    def normalize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):
        return value

    # =====================================================
    # SERIALIZATION
    # =====================================================

    def serialize(
        self,
        field,
        value,
        request=None,
        instance=None,
    ):

        if value is None:
            return [] if field.is_multiple else None

        if field.is_multiple:

            return [
                {
                    "value": item.pk,
                    "label": str(item),
                }
                for item in value
            ]

        return {
            "value": value.pk,
            "label": str(value),
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

        if field.is_multiple:

            return queryset.filter(
                **{
                    f"{field.name}__in": value,
                }
            )

        return queryset.filter(
            **{
                field.name: value,
            }
        )

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        instance,
        field,
        value,
    ):

        field.accessor.set(
            instance,
            field,
            value,
        )

    # =====================================================
    # HOOKS
    # =====================================================

    def before_save(
        self,
        instance,
        field,
        value,
    ):
        pass

    def after_save(
        self,
        instance,
        field,
        value,
    ):
        pass