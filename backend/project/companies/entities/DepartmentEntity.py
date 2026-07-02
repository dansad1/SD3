from django.core.exceptions import (
    ValidationError,
)

from backend.engine.entity.Base.BaseEntity import (
    BaseEntity,
)

from backend.project.companies.models import (
    CompanyField,
    Department,
)


class DepartmentEntity(BaseEntity):

    # =====================================================
    # BASE
    # =====================================================

    model = Department

    entity = "department"

    # =====================================================
    # UI
    # =====================================================

    list_display = [
        "id",
        "name",
        "company",
        "parent",
        "created_at",
    ]

    search_fields = [
        "name",
    ]

    filter_fields = [
        "company",
        "parent",
        "archived",
    ]

    ordering = [
        "name",
    ]

    hierarchy = True

    hierarchy_parent_field = "parent"

    # =====================================================
    # ACCESS
    # =====================================================

    capabilities = {
        "list": "departments.view",
        "view": "departments.view",
        "create": "departments.create",
        "edit": "departments.edit",
        "delete": "departments.delete",
    }

    # =====================================================
    # QUERYSET
    # =====================================================

    def get_select_related(self):

        return [
            "company",
            "parent",
        ]

    def get_prefetch_related(self):

        return [
            "children",
            "users",
        ]

    # =====================================================
    # DYNAMIC FIELDS
    # =====================================================

    def get_dynamic_fields(
        self,
        request,
        obj=None,
    ):

        return (
            CompanyField.objects
            .filter(
                fieldset__is_active=True,
            )
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
            "label": obj.get_full_path(),
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

        if not payload.get(
            "name",
        ):
            errors["name"] = [
                "Название обязательно",
            ]

        parent = payload.get(
            "parent",
        )

        if (
            instance
            and parent
            and str(parent.pk) == str(instance.pk)
        ):
            errors["parent"] = [
                "Отдел не может быть родителем самому себе",
            ]

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

        instance = ctx.instance

        parent = ctx.data.get(
            "parent",
        )

        company = ctx.data.get(
            "company",
        )

        if (
            parent
            and company
            and parent.company_id != company.id
        ):
            raise ValidationError({
                "parent": [
                    "Родительский отдел должен принадлежать той же компании",
                ],
            })

        if instance and parent:

            current = parent

            while current:

                if current.pk == instance.pk:
                    raise ValidationError({
                        "parent": [
                            "Нельзя создать циклическую иерархию",
                        ],
                    })

                current = current.parent

        return ctx

    # =====================================================
    # TREE
    # =====================================================

    def serialize_hierarchy_meta(
        self,
        obj,
    ):

        return {
            "_depth": self.get_depth(obj),
            "_parent": obj.parent_id,
            "_has_children": obj.has_children,
        }

    def get_depth(
        self,
        obj,
    ):

        depth = 0

        parent = obj.parent

        while parent:
            depth += 1
            parent = parent.parent

        return depth

    # =====================================================
    # DELETE
    # =====================================================

    def before_delete(
        self,
        request,
        instance,
    ):

        instance.users.clear()

        return None