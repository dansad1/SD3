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
    ("email", "Email"),
    ("phone", "Phone")
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



    # =========================
    # VALUES
    # =========================

    default_value = models.TextField(
        blank=True,
        null=True,
    )



    # =========================
    # VALIDATION
    # =========================

    required = models.BooleanField(
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
