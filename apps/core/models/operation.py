# apps/core/models/operation.py

from django.db import models
from datetime import date as _date
from django.conf import settings
from apps.core.models.base_models import TimeStampedModel
from apps.core.models.enums import TransactionType

class Operation(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=_date.today)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.EXPENSE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='operations'
    )
    account = models.ForeignKey(
        "Account",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='operations'
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='operations'
    )

    # Замінили ManyToManyField на ForeignKey для зв’язку 1→N
    tag = models.ForeignKey(
        "Tag",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='operations'
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        tag_part = f' [{self.tag.name}]' if self.tag else ''
        return f'{self.get_type_display()}: {self.amount}{tag_part} on {self.date}'
