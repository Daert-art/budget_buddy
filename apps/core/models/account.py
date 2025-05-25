from django.conf import settings
from django.db import models

from apps.core.models.base_models import TimeStampedModel
from apps.core.models.enums import Currency


class Account(TimeStampedModel):
    # Основні поля
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='account_images/', null=True, blank=True)
    name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH,
    )

    # Зовнішні ключі
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='accounts')

    def __str__(self):
        return (
            f'{self.name}: {self.balance} '
            f'{self.currency}'
            f'{super().__str__()}'
        )
