from backend.generic.models.BaseFieldSet import BaseFieldSet


class UserFieldSet(BaseFieldSet):

    class Meta:

        verbose_name = "Набор полей пользователя"
        verbose_name_plural = "Наборы полей пользователей"

    def __str__(self):
        return self.name
