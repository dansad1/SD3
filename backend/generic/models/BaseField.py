from django.db import models

FIELD_TYPES = [

    # ==========================================
    # TEXT
    # ==========================================

    ("string", "String"),
    ("text", "Text"),
    ("richtext", "RichText"),
    ("comments", "Comments"),

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
    ("file", "File"),

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


from django.db import models


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(
        "Создано",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        "Обновлено",
        auto_now=True,
        editable=False,
    )

    class Meta:

        abstract = True


class BaseField(TimeStampedModel):

    name = models.SlugField(
        "Код",
        max_length=100,
    )

    label = models.CharField(
        "Название",
        max_length=255,
    )

    field_type = models.CharField(
        "Тип поля",
        max_length=50,
        choices=FIELD_TYPES,
        default="string",
        db_index=True,
    )

    required = models.BooleanField(
        "Обязательное",
        default=False,
    )

    is_multiple = models.BooleanField(
        "Множественное",
        default=False,
    )

    placeholder = models.CharField(
        "Подсказка в поле",
        max_length=255,
        blank=True,
        default="",
    )

    help_text = models.CharField(
        "Текст помощи",
        max_length=1000,
        blank=True,
        default="",
    )

    choices = models.JSONField(
        "Варианты выбора",
        default=list,
        blank=True,
    )

    options = models.JSONField(
        "Настройки",
        default=dict,
        blank=True,
    )

    section = models.CharField(
        "Раздел",
        max_length=100,
        blank=True,
        default="",
        db_index=True,
    )

    is_system = models.BooleanField(
        "Системное поле",
        default=False,
    )

    unique = models.BooleanField(
        "Уникальное значение",
        default=False,
    )

    class Meta:

        abstract = True

        indexes = [
            models.Index(
                fields=[
                    "field_type",
                ],
            ),
            models.Index(
                fields=[
                    "section",
                ],
            ),
        ]

