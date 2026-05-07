from django.db import models


FIELD_TYPES = [
    ("string", "String"),
    ("text", "Text"),
    ("richtext", "RichText"),
    ("number", "Number"),
    ("boolean", "Boolean"),
    ("date", "Date"),
    ("datetime", "DateTime"),
    ("json", "JSON"),
    ("relation", "Relation"),
]


class BaseField(models.Model):

    # =========================
    # IDENTITY
    # =========================

    name = models.SlugField(
        max_length=100,
    )

    label = models.CharField(
        max_length=255,
    )

    field_type = models.CharField(
        max_length=50,
        choices=FIELD_TYPES,
        default="string",
    )

    # =========================
    # RELATIONS
    # =========================

    relation_entity = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    is_multiple = models.BooleanField(
        default=False,
    )

    # =========================
    # UI
    # =========================

    placeholder = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    help_text = models.TextField(
        blank=True,
        null=True,
    )

    widget = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    width = models.IntegerField(
        default=12,
    )

    order = models.IntegerField(
        default=0,
    )

    # =========================
    # VALUES
    # =========================

    default_value = models.TextField(
        blank=True,
        null=True,
    )

    choices = models.TextField(
        blank=True,
        null=True,
    )

    # =========================
    # VALIDATION
    # =========================

    required = models.BooleanField(
        default=False,
    )

    readonly = models.BooleanField(
        default=False,
    )

    hidden = models.BooleanField(
        default=False,
    )

    unique = models.BooleanField(
        default=False,
    )

    regex = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    min_value = models.IntegerField(
        blank=True,
        null=True,
    )

    max_value = models.IntegerField(
        blank=True,
        null=True,
    )

    # =========================
    # SYSTEM
    # =========================

    is_system = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # =========================
    # META
    # =========================

    class Meta:
        abstract = True