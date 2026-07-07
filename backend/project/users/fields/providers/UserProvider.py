from backend.engine.fields.providers.BaseRelationProvider import (
    BaseRelationProvider,
)

from backend.engine.fields.providers.registry import (
    register_relation_provider,
)

from backend.project.users.models import (
    User,
)


@register_relation_provider
class UserProvider(
    BaseRelationProvider,
):

    code = "user"

    # =====================================================
    # OPTIONS
    # =====================================================

    def get_options(
        self,
        field,
        request=None,
        instance=None,
    ):

        queryset = (
            User.objects
            .all()
        )

        options = [

            {
                "value": obj.pk,
                "label": str(obj),
            }

            for obj in queryset

        ]

        options.sort(

            key=lambda item: (
                item["label"]
                or ""
            ).casefold()

        )

        return options

    # =====================================================
    # INITIAL
    # =====================================================

    def get_initial(
        self,
        field,
        request=None,
        instance=None,
    ):

        if not request:
            return None


        if not request.user.is_authenticated:
            return None


        # только заявитель
        if field.name != "requester":
            return None


        return request.user

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

        return super().validate(
            field,
            value,
            request=request,
            instance=instance,
        )

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

        return super().normalize(
            field,
            value,
            request=request,
            instance=instance,
        )

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

        return super().serialize(
            field,
            value,
            request=request,
            instance=instance,
        )

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
        self,
        queryset,
        field,
        value,
    ):

        return super().apply_filter(
            queryset,
            field,
            value,
        )

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
        self,
        instance,
        field,
        value,
    ):

        pass

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
        self,
        instance,
        field,
        value,
    ):

        pass