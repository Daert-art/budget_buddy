from django.db import models
from django.conf import settings
from apps.core.models.base_models import TimeStampedModel
from apps.core.models.operation import Operation


class Budget(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
    period_start = models.DateField()
    period_end = models.DateField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='budgets'
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='budgets'
    )

    def __str__(self):
        return (
            f'Бюджет «{self.category.name}»: '
            f'{self.limit_amount} '
            f'з {self.period_start} по {self.period_end}'
        )

    def spent_amount(self):
        """Повертає суму витрат за вказаною категорією і періодом."""
        return Operation.objects.filter(
            user=self.user,
            category=self.category,
            type='EXPENSE',
            date__range=(self.period_start, self.period_end)
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0

    def remaining(self):
        """Скільки ще залишилось витратити з бюджету."""
        return self.limit_amount - self.spent_amount()

    def is_exceeded(self):
        """Перевіряє, чи витрати перевищили бюджет."""
        return self.spent_amount() > self.limit_amount
