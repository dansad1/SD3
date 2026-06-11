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


class BaseField(models.Model):

    # =====================================================
    # IDENTITY
    # =====================================================

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

    # =====================================================
    # DEFAULT VALUE
    # =====================================================

    default_value = models.TextField(
        blank=True,
        null=True,
    )

    # =====================================================
    # VALIDATION
    # =====================================================

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

    min_value = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    max_value = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    # =====================================================
    # MULTI VALUE
    # =====================================================

    is_multiple = models.BooleanField(
        default=False,
    )

    # =====================================================
    # UX HINTS
    # =====================================================

    placeholder = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    help_text = models.TextField(
        blank=True,
        null=True,
    )

    # =====================================================
    # ENUM VALUES
    # =====================================================

    choices = models.JSONField(
        default=list,
        blank=True,
    )

    # =====================================================
    # TYPE CONFIG
    # =====================================================

    options = models.JSONField(
        default=dict,
        blank=True,
    )

    # =====================================================
    # GROUPING
    # =====================================================

    section = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
    )

    # =====================================================
    # SYSTEM
    # =====================================================

    is_system = models.BooleanField(
        default=False,
    )

    # =====================================================
    # AUDIT
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True