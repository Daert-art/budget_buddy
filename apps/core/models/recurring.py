from django.db import models
from apps.core.models.base_models import TimeStampedModel
from apps.core.models.operation import Operation
from django.conf import settings


class Recurring(TimeStampedModel):
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    FREQUENCY_CHOICES = [
        (DAILY, 'Щодня'),
        (WEEKLY, 'Щотижня'),
        (MONTHLY, 'Щомісяця'),
    ]

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=Operation.TYPE_CHOICES)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default=MONTHLY)
    next_date = models.DateField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recurrings')
    account = models.ForeignKey("Account", on_delete=models.PROTECT, related_name='recurrings')
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='recurrings')

    def __str__(self):
        return (
            f'{self.get_frequency_display()} {self.get_type_display()} '
            f'{self.amount} on {self.next_date}'
        )