from django.db import models
from apps.core.models.base_models import TimeStampedModel


class Category(TimeStampedModel):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    TYPE_CHOICES = [
        (INCOME, 'Дохід'),
        (EXPENSE, 'Витрата'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'