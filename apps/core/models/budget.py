from django.db import models
from apps.core.models.base_models import TimeStampedModel
from django.conf import settings


class Budget(TimeStampedModel):
    id = models.AutoField(primary_key=True)

    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name='budgets')

    def __str__(self):
        return (
            f'Budget «{self.category.name}»: '
            f'{self.limit_amount} '
            f'from {self.period_start} to {self.period_end}'
        )
