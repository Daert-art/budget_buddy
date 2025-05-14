import os
import sys
from decimal import Decimal

import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date

from django.test import TestCase

from apps.core.models import Operation
from apps.core.models.enums import TransactionType


# id = models.AutoField(primary_key=True)
# amount = models.DecimalField(max_digits=12, decimal_places=2)
# date = models.DateTimeField(auto_now_add=True)
# description = models.CharField(max_length=255, blank=True)
# type = models.CharField(max_length=10, choices=TYPE_CHOICES)

class OperationModelTest(TestCase):
    def setUp(self):
        """Створення тестової операції перед кожним тестом."""
        self.operation_data = {
            "amount" : 100.00,
            "date" : date(2023, 10, 1),
            "description" : "Test operation",
            "type" : TransactionType.INCOME,
        }
        # Створити об'єкт Operation, збереження його в базі даних
        self.operation = Operation.objects.create(**self.operation_data)
    def test_create_operation(self):
        """Перевірка що операція створюється правильно в базі даних"""
        operation = Operation.objects.get(id=self.operation.id)
        # Перевірка ідентичності через збіг полів
        #1
        self.assertEqual(operation.amount, self.operation_data["amount"])
        self.assertEqual(operation.date, self.operation_data["date"])
        self.assertEqual(operation.description, self.operation_data["description"])
        self.assertEqual(operation.type, self.operation_data["type"])

        #2 коли реалізовано метод __eq__ __hash__ в моделі Operation
        #self.assertEqual(operation, self.operation)

    def test_read_operation(self):
        """Перевірка що операцію можна прочитати з бази даних."""
        # отримуємо чинну операцію
        operation = Operation.objects.get(id=self.operation.id)

        # перевіряємо, що значення полів відповідають очікуваним
        self.assertEqual(operation.amount, self.operation_data["amount"])
        self.assertEqual(operation.date, self.operation_data["date"])
        self.assertEqual(operation.description, self.operation_data["description"])
        self.assertEqual(operation.type, self.operation_data["type"])

    def test_update_operation(self):
        """Перевірка що операцію можна відредагувати та зміни зберігаються в БД."""
        # отримуємо чинну операцію
        operation = Operation.objects.get(id=self.operation.id)

        # змінюємо значення полів
        operation.amount = Decimal('200.00')
        operation.date = date(2023, 11, 1)
        operation.description = "Updated operation"
        operation.type = TransactionType.EXPENSE
        operation.save()

        # заново дістанемо цю ж операцію з БД
        updated = Operation.objects.get(id=self.operation.id)
        self.assertEqual(updated.amount, Decimal('200.00'))
        self.assertEqual(updated.date, date(2023, 11, 1))
        self.assertEqual(updated.description, "Updated operation")
        self.assertEqual(updated.type, TransactionType.EXPENSE)

    def test_delete_operation(self):
        """Перевірка що операцію можна видалити."""
        op_id = self.operation.id

        # видаляємо запис
        self.operation.delete()

        # переконуємося, що його більше немає
        self.assertFalse(Operation.objects.filter(id=op_id).exists())
        with self.assertRaises(Operation.DoesNotExist):
            Operation.objects.get(id=op_id)

