from django.db import models

from backend.engine.fields.base import (
    BaseField,
)


from django.db import models

from backend.engine.fields.base import (
    BaseField,
)
from backend.engine.fields.django_accessor import DjangoFieldAccessor


class DjangoField(BaseField):

    # =====================================================
    # ACCESSOR
    # =====================================================

    @property
    def accessor(self):

        return DjangoFieldAccessor()

    # =====================================================
    # VALUE API
    # =====================================================

    def get_value(
        self,
        obj,
    ):

        return self.accessor.get(
            obj,
            self,
        )

    def set_value(
        self,
        obj,
        value,
    ):

        return self.accessor.set(
            obj,
            self,
            value,
        )

    # =====================================================
    # CORE
    # =====================================================

    @property
    def name(self):

        return self.source.name

    @property
    def type(self):

        field = self.source

        # =================================================
        # RELATION
        # =================================================

        if isinstance(
            field,
            (
                models.ForeignKey,
                models.ManyToManyField,
            ),
        ):
            return "relation"

        # =================================================
        # TEXT
        # =================================================

        if isinstance(
            field,
            models.TextField,
        ):
            return "text"

        if isinstance(
            field,
            (
                models.CharField,
                models.EmailField,
                models.SlugField,
            ),
        ):
            return "string"

        # =================================================
        # NUMBERS
        # =================================================

        if isinstance(
            field,
            (
                models.IntegerField,
                models.FloatField,
                models.DecimalField,
            ),
        ):
            return "number"

        # =================================================
        # BOOL
        # =================================================

        if isinstance(
            field,
            models.BooleanField,
        ):
            return "boolean"

        # =================================================
        # DATE
        # =================================================

        if isinstance(
            field,
            models.DateTimeField,
        ):
            return "datetime"

        if isinstance(
            field,
            models.DateField,
        ):
            return "date"

        # =================================================
        # JSON
        # =================================================

        if isinstance(
            field,
            models.JSONField,
        ):
            return "json"

        return "string"

    # =====================================================
    # UI
    # =====================================================

    @property
    def label(self):

        return (
            self.source.verbose_name
            or self.name
        )

    @property
    def placeholder(self):

        return None

    @property
    def help_text(self):

        return (
            self.source.help_text
            or ""
        )

    @property
    def widget(self):

        return None

    @property
    def width(self):

        return 12

    @property
    def order(self):

        return 0

    # =====================================================
    # VALIDATION
    # =====================================================

    @property
    def required(self):

        return not (
            self.source.blank
            or self.source.null
        )

    @property
    def readonly(self):

        return not getattr(
            self.source,
            "editable",
            True,
        )

    @property
    def hidden(self):

        return False

    @property
    def unique(self):

        return getattr(
            self.source,
            "unique",
            False,
        )

    @property
    def regex(self):

        return None

    @property
    def min_value(self):

        return None

    @property
    def max_value(self):

        return None

    # =====================================================
    # RELATIONS
    # =====================================================

    @property
    def is_multiple(self):

        return getattr(
            self.source,
            "many_to_many",
            False,
        )

    @property
    def relation_entity(self):

        remote = getattr(
            self.source,
            "remote_field",
            None,
        )

        if not remote:
            return None

        model = remote.model

        # 🔥 lazy import
        from backend.engine.entity.EntityRegistry import (
            entity_registry,
        )

        entity = (
            entity_registry
            .for_model(model)
        )

        if not entity:
            return None

        return entity.entity

    # =====================================================
    # CHOICES
    # =====================================================

    @property
    def choices(self):

        choices = getattr(
            self.source,
            "choices",
            None,
        )

        if not choices:
            return []

        return [

            {
                "value": value,
                "label": label,
            }

            for value, label in choices
        ]