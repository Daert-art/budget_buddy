from django.db import models

class CategoryType(models.TextChoices):
    INCOME  = 'INCOME',  'Дохід'
    EXPENSE = 'EXPENSE', 'Витрата'

class OperationType(models.TextChoices):
    INCOME  = 'INCOME',  'Дохід'
    EXPENSE = 'EXPENSE', 'Витрата'

class Frequency(models.TextChoices):
    DAILY   = 'DAILY',   'Щодня'
    WEEKLY  = 'WEEKLY',  'Щотижня'
    MONTHLY = 'MONTHLY', 'Щомісяця'