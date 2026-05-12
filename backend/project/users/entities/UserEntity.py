from django.core.exceptions import (
    ValidationError
)

from django.contrib.auth.password_validation import (
    validate_password
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity
)

from backend.project.users.models import (
    User,
    UserField,
)


class UserEntity(BaseEntity):

    model = User

    entity = "users"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "login",
        "role",
        "is_active",
    ]

    search_fields = [
        "login",
    ]

    filter_fields = [
        "role",
        "is_active",
    ]

    ordering = [
        "login",
    ]

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "users.view",
        "view": "users.view",
        "create": "users.create",
        "edit": "users.edit",
        "delete": "users.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "role",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        fieldset = request.GET.get(
            "fieldset"
        )

        if not fieldset:
            return []

        return (
            UserField.objects
            .filter(
                fieldset_id=fieldset,
                fieldset__is_active=True,
            )
            .order_by(
                "order",
                "id",
            )
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    def represent_option(
        self,
        obj,
    ):

        return {
            "value": obj.pk,
            "label": obj.login,
        }

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        request,
        payload,
        instance=None,
    ):

        errors = {}

        password = payload.get(
            "password"
        )

        if (
            not instance
            and not password
        ):

            errors["password"] = [
                "Password required"
            ]

        if password:

            try:

                validate_password(
                    password
                )

            except ValidationError as e:

                errors["password"] = (
                    list(e.messages)
                )

        if errors:

            raise ValidationError(
                errors
            )

        return payload

    # =====================================================
    # SAVE
    # =====================================================

    def before_save(
        self,
        ctx,
    ):

        password = ctx.data.get(
            "password"
        )

        if password:

            ctx.instance.set_password(
                password
            )

            ctx.data.pop(
                "password",
                None,
            )

        return ctx

    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        if request.user.pk == instance.pk:

            raise ValidationError({
                "detail": [
                    "You cannot delete yourself"
                ]
            })

    # =====================================================
    # SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):

        if schema["name"] == "password":

            schema["writeonly"] = True

            schema["widget"] = "password"

        return schema