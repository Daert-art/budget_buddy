from django.db import models
from apps.core.models.base_models import TimeStampedModel
from apps.core.models.enums import TransactionType


class Category(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.INCOME)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'
