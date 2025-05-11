from django.db import models
from apps.core.models.base_models import TimeStampedModel
from django.conf import settings



class Operation(TimeStampedModel):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    TYPE_CHOICES = [
        (INCOME, 'Дохід'),
        (EXPENSE, 'Витрата'),
    ]

    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='operations')
    account = models.ForeignKey("Account", on_delete=models.PROTECT, related_name='operations')
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name='operations')

    tags = models.ManyToManyField("Tag", blank=True, related_name='operations')


    def __str__(self):
        return f'{self.get_type_display()}: {self.amount} on {self.date.date()}'

    class Meta:
        ordering = ['-date']

