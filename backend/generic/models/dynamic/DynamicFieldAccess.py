from SD3.backend.generic.models.dynamic.DynamicField import DynamicField
from django.db import models

class DynamicFieldAccess(models.Model):
    field = models.ForeignKey(
        DynamicField,
        on_delete=models.CASCADE,
        related_name="accesses"
    )

    role = models.ForeignKey(
        "UserRole",
        on_delete=models.CASCADE
    )

    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=True)

    class Meta:
        unique_together = ("field", "role")

    def __str__(self):
        return f"{self.role} → {self.field} (view={self.can_view}, edit={self.can_edit})"