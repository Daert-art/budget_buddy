import os
import sys
from datetime import date
from decimal import Decimal

import django
from django.test import TestCase

from apps.core.models import Recurring

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


# amount = models.DecimalField(max_digits=12, decimal_places=2)
# description = models.CharField(max_length=255, blank=True)
# type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.INCOME)
# frequency = models.CharField(max_length=10, choices=Frequency.choices, default=Frequency.MONTHLY)
# next_date = models.DateField()

class RecurringModelTest(TestCase):
    def setUp(self):
        """Create a test recurring before each test."""
        self.recurring_data = {
            "amount": Decimal("100.00"),
            "description": "Test Recurring",
            "type": "income",
            "frequency": "monthly",
            "next_date": date(2023, 10, 1),
        }
        # Create a Recurring object and save it to the database
        self.recurring = Recurring.objects.create(**self.recurring_data)

    def test_create_recurring(self):
        """Test that a recurring can be created and saved to the database."""
        recurring = Recurring.objects.get(id=self.recurring.id)

        # Check that the recurring fields match the expected values
        self.assertEqual(recurring.amount, self.recurring_data["amount"])
        self.assertEqual(recurring.description, self.recurring_data["description"])
        self.assertEqual(recurring.type, self.recurring_data["type"])
        self.assertEqual(recurring.frequency, self.recurring_data["frequency"])
        self.assertEqual(recurring.next_date, self.recurring_data["next_date"])

    def test_read_recurring(self):
        """Test that a recurring can be read from the database."""
        recurring = Recurring.objects.get(id=self.recurring.id)

        # Check that the recurring fields match the expected values
        self.assertEqual(recurring.amount, self.recurring_data["amount"])
        self.assertEqual(recurring.description, self.recurring_data["description"])
        self.assertEqual(recurring.type, self.recurring_data["type"])
        self.assertEqual(recurring.frequency, self.recurring_data["frequency"])
        self.assertEqual(recurring.next_date, self.recurring_data["next_date"])

    def test_update_recurring(self):
        """Test that a recurring can be updated and changes are saved to the database."""
        recurring = Recurring.objects.get(id=self.recurring.id)

        # Update the recurring fields
        recurring.amount = Decimal("200.00")
        recurring.description = "Updated Recurring"
        recurring.type = "expense"
        recurring.frequency = "weekly"
        recurring.next_date = date(2023, 10, 8)
        recurring.save()

        # Check that the updated recurring fields match the expected values
        updated_recurring = Recurring.objects.get(id=self.recurring.id)
        self.assertEqual(updated_recurring.amount, Decimal("200.00"))
        self.assertEqual(updated_recurring.description, "Updated Recurring")
        self.assertEqual(updated_recurring.type, "expense")
        self.assertEqual(updated_recurring.frequency, "weekly")
        self.assertEqual(updated_recurring.next_date, date(2023, 10, 8))

    def test_delete_recurring(self):
        """Test that a recurring can be deleted."""
        recurring_id = self.recurring.id

        # Delete the recurring
        self.recurring.delete()

        # Check that the recurring no longer exists
        with self.assertRaises(Recurring.DoesNotExist):
            Recurring.objects.get(id=recurring_id)