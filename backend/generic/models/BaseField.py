from django.db import models


FIELD_TYPES = [

    # ==========================================
    # TEXT
    # ==========================================

    ("string", "String"),
    ("text", "Text"),
    ("richtext", "RichText"),

    # ==========================================
    # NUMBERS
    # ==========================================

    ("number", "Number"),

    # ==========================================
    # BOOLEAN
    # ==========================================

    ("boolean", "Boolean"),

    # ==========================================
    # DATE
    # ==========================================

    ("date", "Date"),
    ("datetime", "DateTime"),

    # ==========================================
    # DATA
    # ==========================================

    ("json", "JSON"),

    # ==========================================
    # GENERIC RELATION
    # ==========================================

    ("relation", "Relation"),

    # ==========================================
    # SPECIAL
    # ==========================================

    ("email", "Email"),
    ("phone", "Phone"),
    ("password", "Password"),

    # ==========================================
    # DOMAIN
    # ==========================================

    ("user", "User"),
    ("role", "Role"),
    ("company", "Company"),
    ("ticket", "Ticket"),

    ("status", "Status"),
    ("priority", "Priority"),
]
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


from django.db import models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True


class BaseField(TimeStampedModel):

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
        db_index=True,
    )

    required = models.BooleanField(
        default=False,
    )

    is_multiple = models.BooleanField(
        default=False,
    )

    placeholder = models.CharField(
        max_length=255,
        blank=True,
        default="",
    )

    help_text = models.CharField(
        max_length=1000,
        blank=True,
        default="",
    )

    choices = models.JSONField(
        default=list,
        blank=True,
    )

    options = models.JSONField(
        default=dict,
        blank=True,
    )

    section = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
    )

    is_system = models.BooleanField(
        default=False,
    )

    unique = models.BooleanField(
        default=False,
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["field_type"]),
            models.Index(fields=["section"]),
        ]