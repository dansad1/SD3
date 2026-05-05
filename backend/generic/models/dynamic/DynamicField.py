from django.core.exceptions import ValidationError
from django.db import models



# =========================
# FIELD (описание поля)
# =========================

class DynamicField(models.Model):
    name = models.SlugField(max_length=100)
    label = models.CharField(max_length=255)

    field_type = models.CharField(max_length=50)

    required = models.BooleanField(default=False)
    unique = models.BooleanField(default=False)

    is_multiple = models.BooleanField(default=False)

    choices = models.TextField(blank=True, null=True)

    # 🔥 главное — без choices, полностью динамика
    entity = models.CharField(max_length=100)

    # порядок отображения (удобно)
    order = models.IntegerField(default=0)

    # дефолтные права (если нет override)
    default_can_view = models.BooleanField(default=True)
    default_can_edit = models.BooleanField(default=True)

    class Meta:
        unique_together = ("name", "entity")
        ordering = ["order", "id"]

    def clean(self):
        # защита от мусора
        if not entity_registry.get(self.entity):
            raise ValidationError({
                "entity": f"Unknown entity: {self.entity}"
            })

    def __str__(self):
        return f"{self.entity}.{self.name}"