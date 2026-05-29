# =========================================================
# USER ENTITY
# =========================================================

from django.core.exceptions import (
    ValidationError,
)

from django.contrib.auth.password_validation import (
    validate_password,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.users.models import (
    User,
    UserField,
)


class UserEntity(BaseEntity):

    # =====================================================
    # CORE
    # =====================================================

    model = User

    entity = "user"

    # =====================================================
    # UI
    # =====================================================

    list_display = [

        "login",

        "role",

        "is_active",

        # dynamic examples
        "telegram",
        "department",
    ]

    search_fields = [

        "login",

        "telegram",
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

        # django auth internals
        "groups",
        "user_permissions",

        # system
        "last_login",
        "created_at",
        "updated_at",
    }

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {

        "list":
            "users.view",

        "view":
            "users.view",

        "create":
            "users.create",

        "edit":
            "users.edit",

        "delete":
            "users.delete",
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

        # =============================================
        # DEFAULT
        # =============================================

        if (
            not fieldset
            or fieldset == "default"
        ):

            return []

        # =============================================
        # VALIDATE
        # =============================================

        try:

            fieldset_id = int(
                fieldset
            )

        except (
            TypeError,
            ValueError,
        ):

            return []

        # =============================================
        # RESULT
        # =============================================

        return (

            UserField.objects

            .filter(

                fieldset_id=fieldset_id,

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
            "password"
        )

        if (
                instance is None
                and not password
        ):
            errors["password"] = [
                "Password required"
            ]

        if password:

            try:

                validate_password(
                    password,
                    user=instance,
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
    def before_save(
        self,
        ctx,
    ):

        password = ctx.data.get(
            "password"
        )

        # =============================================
        # PASSWORD
        # =============================================

        if password:

            ctx.instance.set_password(
                password
            )

            # не сохраняем raw password
            ctx.data.pop(
                "password",
                None,
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

        # =============================================
        # SELF DELETE PROTECTION
        # =============================================

        if request.user.pk == instance.pk:

            raise ValidationError({

                "detail": [

                    "You cannot delete yourself"
                ]
            })

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

        # =============================================
        # PASSWORD
        # =============================================

        if name == "password":

            schema.update({

                "writeonly": True,

                "widget": "password",
            })

        # =============================================
        # SECURITY
        # =============================================

        if (
            not request.user.is_superuser
        ):

            if name in {

                "is_superuser",
                "is_staff",
            }:

                schema["hidden"] = True

        # =============================================
        # SYSTEM READONLY
        # =============================================

        if name in {

            "created_at",

            "updated_at",

            "last_login",
        }:

            schema["readonly"] = True

        return schema