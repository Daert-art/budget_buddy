from django.db import models
from apps.core.models.base_models import TimeStampedModel
from apps.core.models.enums import TransactionType, Frequency
from django.conf import settings


class Recurring(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.INCOME)
    frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTHLY)
    next_date = models.DateField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='recurrings')
    account = models.ForeignKey("Account", on_delete=models.PROTECT, null=True, blank=True,
                                related_name='recurrings')
    category = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='recurrings')

    def __str__(self):
        return (
            f'{self.get_frequency_display()} {self.get_type_display()} '
            f'{self.amount} on {self.next_date}'
        )
