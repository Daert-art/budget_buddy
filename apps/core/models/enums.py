from django.db import models
from django.db.models import TextChoices


class TransactionType(models.TextChoices):
    INCOME = 'INCOME', 'Дохід'
    EXPENSE = 'EXPENSE', 'Витрата'


class Frequency(TextChoices):
    DAILY = 'DAILY', 'Щодня'
    WEEKLY = 'WEEKLY', 'Щотижня'
    MONTHLY = 'MONTHLY', 'Щомісяця'
    YEARLY = 'YEARLY', 'Щороку'

class Currency(models.TextChoices):
    UAH = 'UAH', '₴ Гривня'
    USD = 'USD', '$ Долар'
    EUR = 'EUR', '€ Євро'

