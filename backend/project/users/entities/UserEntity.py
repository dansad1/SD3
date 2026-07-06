from django.core.exceptions import (
    ValidationError,
)

from django.contrib.auth.password_validation import (
    validate_password,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.generic.models import (
    DynamicField,
    DjangoField,
)
from backend.project.users.entities.sync import sync_user

from backend.project.users.models import (
    User,
    UserField,
)


class UserEntity(BaseEntity):

    model = User

    entity = "user"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "login",
        "role",
        "is_active",
        "telegram",
        "department",
        "company"
    ]

    search_fields = [
        "login",
        "telegram",
        "company"
    ]

    filter_fields = [
        "role",
        "is_active",
    ]

    ordering = [
        "login",
    ]

    # =====================================================
    # FIELD POLICY
    # =====================================================

    exclude_fields = {
        "groups",
        "user_permissions",
        "last_login",
        "created_at",
        "updated_at",
        "fieldset"
    }

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
            "fieldset",
        ]

    def get_prefetch_related(self):

        return [
            "dynamic_values",
            "dynamic_values__field",
        ]

    # =====================================================
    # FIELDS
    # =====================================================

    def get_fields(
        self,
        request,
        obj=None,
    ):

        fields = []

        for field in self.model._meta.get_fields():

            name = getattr(
                field,
                "name",
                None,
            )

            if not name:
                continue

            if not self.include_model_field(
                field
            ):
                continue

            fields.append(
                DjangoField(field)
            )

        existing_names = {
            field.name
            for field in fields
        }

        for field in self.get_dynamic_fields(
            request,
            obj=obj,
        ):

            if (
                field.name
                in existing_names
            ):
                continue

            fields.append(
                DynamicField(field)
            )

        return fields

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        return (
            UserField.objects
            .all()
            .order_by(
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
            "label": (
                obj.get_value(
                    "full_name"
                )
                or obj.login
            ),
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
            "password",
        )

        if (
                instance is None
                and not password
        ):
            errors["password"] = [
                "Password required",
            ]

        if password not in (
                None,
                "",
                "********",
        ):
            try:
                validate_password(
                    password,
                    user=instance,
                )

            except ValidationError as e:
                errors["password"] = list(
                    e.messages,
                )

        if errors:
            raise ValidationError(
                errors,
            )

        return payload
    # =====================================================
    # BEFORE SAVE
    # =====================================================

    def before_save(
            self,
            ctx,
    ):
        ctx = super().before_save(
            ctx,
        )

        password = ctx.data.pop(
            "password",
            None,
        )

        if password not in (
                None,
                "",
                "********",
        ):
            ctx.instance.set_password(
                password,
            )

        return ctx

    # =====================================================
    # AFTER SAVE
    # =====================================================

    def after_save(
            self,
            ctx,
    ):
        ctx = super().after_save(
            ctx,
        )

        sync_user(
            ctx.instance,

        )

        return ctx
    # =====================================================
    # BEFORE DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        if (
            request.user.pk
            == instance.pk
        ):

            raise ValidationError({
                "detail": [
                    "You cannot delete yourself"
                ]
            })

        super().before_delete(
            request,
            instance,
        )

    # =====================================================
    # FIELD SCHEMA
    # =====================================================

    def customize_field_schema(
        self,
        request,
        schema,
        field=None,
    ):

        name = schema.get(
            "name"
        )

        if name == "password":

            schema.update({

                "writeonly": True,

                "widget": "password",
            })

        if (
            not request.user.is_superuser
        ):

            if name in {
                "is_superuser",
                "is_staff",
            }:

                schema["hidden"] = True

        if name in {
            "created_at",
            "updated_at",
            "last_login",
        }:

            schema["readonly"] = True

        return schema