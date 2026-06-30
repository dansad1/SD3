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
        return value

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):
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