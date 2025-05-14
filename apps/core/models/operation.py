from django.db import models
from apps.core.models.base_models import TimeStampedModel
from django.conf import settings
from datetime import date as _date
from apps.core.models.enums import TransactionType


class Operation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=_date.today)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.INCOME)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='operations')
    account = models.ForeignKey("Account", on_delete=models.PROTECT, null=True, blank=True, related_name='operations')
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True, related_name='operations')

    tags = models.ManyToManyField("Tag", blank=True, related_name='operations')

    def __str__(self):
        return f'{self.get_type_display()}: {self.amount} on {self.date}'

    class Meta:
        ordering = ['-date']
