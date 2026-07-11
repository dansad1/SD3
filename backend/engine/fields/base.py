import inspect

from django.db.models import Q

from backend.project.audit.utils.logging import make_json_safe


class BaseField:

    META_FIELDS = {
        "created_at",
        "updated_at",
        "deleted_at",
        "created_by",
        "updated_by",
    }

    def __init__(
        self,
        source,
    ):
        self.source = source

    # =====================================================
    # REQUIRED
    # =====================================================

    @property
    def name(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def accessor(self):
        raise NotImplementedError

    # =====================================================
    # PRESENTATION
    # =====================================================

    @property
    def presentation(self):

        if self.name in self.META_FIELDS:
            return "meta"

        return None

    # =====================================================
    # COMMON
    # =====================================================

    @property
    def label(self):
        return getattr(
            self.source,
            "label",
            self.name,
        )

    @property
    def required(self):
        return getattr(
            self.source,
            "required",
            False,
        )

    @property
    def unique(self):
        return getattr(
            self.source,
            "unique",
            False,
        )

    @property
    def is_multiple(self):
        return getattr(
            self.source,
            "is_multiple",
            False,
        )

    # =====================================================
    # UI
    # =====================================================

    @property
    def placeholder(self):
        return getattr(
            self.source,
            "placeholder",
            "",
        )

    @property
    def help_text(self):
        return getattr(
            self.source,
            "help_text",
            "",
        )

    @property
    def section(self):
        return getattr(
            self.source,
            "section",
            None,
        )

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):
        return (
            getattr(
                self.source,
                "choices",
                [],
            )
            or []
        )

    # =====================================================
    # OPTIONS
    # =====================================================

    @property
    def options(self):
        return (
            getattr(
                self.source,
                "options",
                None,
            )
            or {}
        )

    # =====================================================
    # TYPE
    # =====================================================

    @property
    def field_type(self):

        if hasattr(
            self,
            "_field_type",
        ):
            return self._field_type

        from backend.engine.fields.types.registry import (
            get_field_type,
        )

        self._field_type = get_field_type(
            self.type,
        )

        return self._field_type

    # =====================================================
    # SAVE
    # =====================================================

    @property
    def requires_post_save(self):

        method = getattr(
            self.field_type,
            "requires_post_save",
            None,
        )

        if callable(
            method,
        ):
            return method(
                self,
            )

        return False

    # =====================================================
    # VALUE
    # =====================================================

    def get_value(
        self,
        instance,
    ):
        return self.accessor.get(
            instance,
            self,
        )

    def set_value(
        self,
        instance,
        value,
    ):
        return self.accessor.set(
            instance,
            self,
            value,
        )

    # =====================================================
    # BEHAVIOR
    # =====================================================

    def validate(
        self,
        value,
    ):
        return self.field_type.validate(
            self,
            value,
        )

    def normalize(
        self,
        value,
    ):
        return self.field_type.normalize(
            self,
            value,
        )

    def should_save(
        self,
        value,
    ):
        return self.field_type.should_save(
            self,
            value,
        )

    def serialize(
        self,
        value,
    ):
        return self.field_type.serialize(
            self,
            value,
        )

    def deserialize(
        self,
        value,
    ):
        return self.field_type.deserialize(
            self,
            value,
        )

    # =====================================================
    # SCHEMA
    # =====================================================

    def get_schema(
        self,
        request=None,
        instance=None,
    ):

        method = self.field_type.get_schema

        parameters = inspect.signature(
            method,
        ).parameters

        if "request" in parameters:

            schema = method(
                self,
                request=request,
                instance=instance,
            )

        else:

            #
            # Backward compatibility
            #

            schema = method(
                self,
            )

        schema.update({

            "name":
                self.name,

            "label":
                self.label,

            "required":
                self.required,

            "placeholder":
                self.placeholder,

            "help_text":
                self.help_text,

            "multiple":
                self.is_multiple,

            "unique":
                self.unique,

        })

        if self.presentation:

            schema[
                "presentation"
            ] = self.presentation

        if self.section:

            schema.setdefault(
                "ui",
                {},
            )

            schema["ui"][
                "section"
            ] = self.section

        if (
            "options"
            not in schema
            and self.choices
        ):
            schema[
                "options"
            ] = self.choices

        return schema

    # =====================================================
    # FILTER
    # =====================================================

    def apply_filter(
            self,
            queryset,
            value,
    ):
        raise NotImplementedError

    # =====================================================
    # SEARCH
    # =====================================================

    def build_search_q(
        self,
        value,
    ):

        if (
            not value
            or not self.field_type.searchable
        ):
            return Q()

        return Q(
            **{
                f"{self.name}__icontains":
                    value,
            }
        )

    def get_audit_value(
            self,
            instance,
    ):
        value = self.get_value(
            instance,
        )

        value = self.serialize(
            value,
        )

        return make_json_safe(
            value,
        )