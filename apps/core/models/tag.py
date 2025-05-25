from django.db import models
from apps.core.models.base_models import TimeStampedModel
from django.conf import settings


class Tag(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='tags')
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='tags',
        null=True,
        blank=True,
        help_text="Категорія, до якої належить цей тег"
    )

    def __str__(self):
        return f'{self.name} (категорія: {self.category.name if self.category else "—"})'
