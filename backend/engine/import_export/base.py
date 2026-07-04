from django.utils.encoding import force_str


class BaseImportExportService:

    MAX_ROWS = 5000

    IMPORT_DENY_FIELDS = {
        "id",
        "groups",
        "user_permissions",
        "is_superuser",
        "is_staff",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    EXPORT_DENY_FIELDS = {
        "password",
        "groups",
        "user_permissions",
    }

    TEMPLATE_DENY_FIELDS = {
        "id",
        "groups",
        "user_permissions",
        "is_superuser",
        "is_staff",
        "created_at",
        "updated_at",
        "deleted_at",
    }

    def __init__(
        self,
        entity,
        request,
    ):
        self.entity = entity
        self.request = request

    @property
    def lookup_field(
        self,
    ):
        return getattr(
            self.entity,
            "import_lookup_field",
            "id",
        )

    def safe_value(
        self,
        value,
    ):
        if value is None:
            return ""

        if isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
            ),
        ):
            return value

        return force_str(
            value,
        )

    def get_template_fields(
        self,
    ):
        return self.get_fields_for_policy(
            deny_fields=self.TEMPLATE_DENY_FIELDS,
            skip_hidden=True,
            skip_readonly=True,
            skip_writeonly=False,
        )

    def get_import_fields(
        self,
    ):
        return self.get_fields_for_policy(
            deny_fields=self.IMPORT_DENY_FIELDS,
            skip_hidden=True,
            skip_readonly=True,
            skip_writeonly=False,
        )

    def get_export_fields(
        self,
    ):
        return self.get_fields_for_policy(
            deny_fields=self.EXPORT_DENY_FIELDS,
            skip_hidden=False,
            skip_readonly=False,
            skip_writeonly=True,
        )

    def get_fields_for_policy(
        self,
        deny_fields,
        skip_hidden,
        skip_readonly,
        skip_writeonly,
    ):
        result = []

        for field in self.entity.get_fields(
            self.request,
        ):
            if field.name in deny_fields:
                continue

            schema = field.get_schema()

            if (
                skip_hidden
                and schema.get("hidden")
            ):
                continue

            if (
                skip_readonly
                and schema.get("readonly")
            ):
                continue

            if (
                skip_writeonly
                and schema.get("writeonly")
            ):
                continue

            result.append(
                field,
            )

        return result

    def get_field_map(
        self,
        fields,
    ):
        return {
            field.name: field
            for field in fields
        }