from django.core.exceptions import (
    ValidationError,
)


class DepartmentHierarchyService:

    # =====================================================
    # BEFORE SAVE
    # =====================================================

    @classmethod
    def before_save(
        cls,
        ctx,
    ):

        instance = ctx.instance

        parent = ctx.data.get(
            "parent",
        )

        company = ctx.data.get(
            "company",
        )

        cls.validate_company(
            parent,
            company,
        )

        cls.validate_cycle(
            instance,
            parent,
        )

        return ctx

    # =====================================================
    # COMPANY
    # =====================================================

    @staticmethod
    def validate_company(
        parent,
        company,
    ):

        if (
            not parent
            or not company
        ):
            return

        if (
            parent.company_id
            != company.id
        ):

            raise ValidationError({
                "parent": [
                    (
                        "Родительский отдел "
                        "должен принадлежать "
                        "той же компании"
                    ),
                ],
            })

    # =====================================================
    # CYCLE
    # =====================================================

    @staticmethod
    def validate_cycle(
        instance,
        parent,
    ):

        if (
            not instance
            or not parent
        ):
            return

        current = parent

        while current:

            if current.pk == instance.pk:

                raise ValidationError({
                    "parent": [
                        "Нельзя создать циклическую иерархию",
                    ],
                })

            current = current.parent

    # =====================================================
    # TREE META
    # =====================================================

    @classmethod
    def serialize_meta(
        cls,
        obj,
    ):

        return {
            "_depth": cls.get_depth(
                obj,
            ),
            "_parent": obj.parent_id,
            "_has_children": obj.has_children,
        }

    # =====================================================
    # DEPTH
    # =====================================================

    @staticmethod
    def get_depth(
        obj,
    ):

        depth = 0

        parent = obj.parent

        while parent:

            depth += 1

            parent = parent.parent

        return depth