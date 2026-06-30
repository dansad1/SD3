from django.db import models
from django.db.models.fields.reverse_related import (
    ManyToManyRel,
    ManyToOneRel,
)


class RelationAccessor:

    # =====================================================
    # GET
    # =====================================================

    def get(
        self,
        instance,
        field,
    ):

        source = field.source

        # =================================================
        # FK
        # =================================================

        if isinstance(
            source,
            models.ForeignKey,
        ):
            return getattr(
                instance,
                source.name,
            )

        # =================================================
        # M2M
        # =================================================

        if isinstance(
            source,
            models.ManyToManyField,
        ):
            return getattr(
                instance,
                source.name,
            ).all()

        # =================================================
        # REVERSE FK
        # =================================================

        if isinstance(
            source,
            ManyToOneRel,
        ):
            return getattr(
                instance,
                source.get_accessor_name(),
            ).all()

        # =================================================
        # REVERSE M2M
        # =================================================

        if isinstance(
            source,
            ManyToManyRel,
        ):
            return getattr(
                instance,
                source.get_accessor_name(),
            ).all()

        raise RuntimeError(
            f"Unsupported relation: {type(source)}"
        )

    # =====================================================
    # SET
    # =====================================================

    def set(
        self,
        instance,
        field,
        value,
    ):

        source = field.source

        # =================================================
        # FK
        # =================================================

        if isinstance(
            source,
            models.ForeignKey,
        ):

            setattr(
                instance,
                source.name,
                value,
            )

            return

        # =================================================
        # M2M
        # =================================================

        if isinstance(
            source,
            models.ManyToManyField,
        ):

            manager = getattr(
                instance,
                source.name,
            )

            manager.set(
                value or [],
            )

            return

        # =================================================
        # REVERSE FK
        # =================================================

        if isinstance(
            source,
            ManyToOneRel,
        ):

            manager = getattr(
                instance,
                source.get_accessor_name(),
            )

            current = {
                obj.pk
                for obj in manager.all()
            }

            new = {
                obj.pk
                for obj in (
                    value
                    or []
                )
            }

            fk_name = (
                source.field.name
            )

            #
            # REMOVE
            #

            for obj in manager.exclude(
                pk__in=new,
            ):

                setattr(
                    obj,
                    fk_name,
                    None,
                )

                obj.save()

            #
            # ADD
            #

            queryset = (
                source.related_model.objects.filter(
                    pk__in=new - current,
                )
            )

            for obj in queryset:

                setattr(
                    obj,
                    fk_name,
                    instance,
                )

                obj.save()

            return

        # =================================================
        # REVERSE M2M
        # =================================================

        if isinstance(
            source,
            ManyToManyRel,
        ):

            manager = getattr(
                instance,
                source.get_accessor_name(),
            )

            manager.set(
                value or [],
            )

            return

        raise RuntimeError(
            f"Unsupported relation: {type(source)}"
        )