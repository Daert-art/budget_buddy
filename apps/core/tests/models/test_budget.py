import os
import sys
from datetime import date, timedelta
from decimal import Decimal

import django
from django.test import TestCase

from apps.core.models import Budget

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# limit_amount = models.DecimalField(max_digits=12, decimal_places=2)
# period_start = models.DateField()
# period_end = models.DateField()

class BudgetModelTest(TestCase):
    def setUp(self):
        """Create a test budget before each test."""
        self.budget_data = {
            "limit_amount": Decimal("1000.00"),
            "period_start": date.today(),
            "period_end": date.today()+timedelta(days=30),
        }
        # Create a Budget object and save it to the database
        self.budget = Budget.objects.create(**self.budget_data)

    def test_create_budget(self):
        """Test that a budget can be created and saved to the database."""
        budget = Budget.objects.get(id=self.budget.id)

        # Check that the budget fields match the expected values
        self.assertEqual(budget.limit_amount, self.budget_data["limit_amount"])
        self.assertEqual(budget.period_start, self.budget_data["period_start"])
        self.assertEqual(budget.period_end, self.budget_data["period_end"])

    def test_read_budget(self):
        """Test that a budget can be read from the database."""
        budget = Budget.objects.get(id=self.budget.id)

        # Check that the budget fields match the expected values
        self.assertEqual(budget.limit_amount, self.budget_data["limit_amount"])
        self.assertEqual(budget.period_start, self.budget_data["period_start"])
        self.assertEqual(budget.period_end, self.budget_data["period_end"])

    def test_update_budget(self):
        """Test that a budget can be updated and changes are saved to the database."""
        budget = Budget.objects.get(id=self.budget.id)

        # Update the budget fields
        budget.limit_amount = Decimal("2000.00")
        budget.period_start = date.today() + timedelta(days=1)
        budget.period_end = date.today() + timedelta(days=31)
        budget.save()

        # Check that the updated budget fields match the expected values
        updated_budget = Budget.objects.get(id=self.budget.id)
        self.assertEqual(updated_budget.limit_amount, Decimal("2000.00"))
        self.assertEqual(updated_budget.period_start, date.today() + timedelta(days=1))
        self.assertEqual(updated_budget.period_end, date.today() + timedelta(days=31))

    def test_delete_budget(self):
        """Test that a budget can be deleted."""
        budget_id = self.budget.id

        # Delete the budget
        self.budget.delete()

        # Check that the budget no longer exists
        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(id=budget_id)
