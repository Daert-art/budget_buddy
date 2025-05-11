from django.db import models


class TimeStampedModel(models.Model):
    # Метадані
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.created_at} "
            f"{self.updated_at}"
        )

    class Meta:
        # Не створювати таблицю в БД
        abstract = True

