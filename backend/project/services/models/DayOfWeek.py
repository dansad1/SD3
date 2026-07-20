from django.db import models


DAYS_OF_WEEK = [
    (0, "Понедельник"),
    (1, "Вторник"),
    (2, "Среда"),
    (3, "Четверг"),
    (4, "Пятница"),
    (5, "Суббота"),
    (6, "Воскресенье"),
]


class DayOfWeek(models.Model):

    code = models.IntegerField(
        "День недели",
        choices=DAYS_OF_WEEK,
        unique=True,
    )

    class Meta:

        ordering = [
            "code",
        ]

        verbose_name = "День недели"
        verbose_name_plural = "Дни недели"

    def __str__(self):

        return dict(
            DAYS_OF_WEEK
        ).get(
            self.code,
            f"День {self.code}",
        )
