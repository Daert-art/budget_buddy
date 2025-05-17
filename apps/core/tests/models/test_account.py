import os
import sys

import django
from django.test import TestCase

from apps.core.models import Account

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

class AccountModelTest(TestCase):
    def setUp(self):
        self.account_data = {
            "name": "Test Account",
            "balance": 1000.00,
            "currency": "USD",
        }
        self.account = Account.objects.create(**self.account_data)

    def test_create_account(self):
        """Test that an account can be created and saved to the database."""
        account = Account.objects.get(id=self.account.id)

        self.assertEqual(account.name, self.account_data["name"])
        self.assertEqual(account.balance, self.account_data["balance"])
        self.assertEqual(account.currency, self.account_data["currency"])

    def test_read_account(self):
        """Test that an account can be read from the database."""
        account = Account.objects.get(id=self.account.id)

        self.assertEqual(account.name, self.account_data["name"])
        self.assertEqual(account.balance, self.account_data["balance"])
        self.assertEqual(account.currency, self.account_data["currency"])

    def test_update_account(self):
        """Test that an account can be updated and changes are saved to the database."""
        account = Account.objects.get(id=self.account.id)

        account.name = "Updated Account"
        account.balance = 2000.00
        account.currency = "EUR"
        account.save()

        updated_account = Account.objects.get(id=self.account.id)

        self.assertEqual(updated_account.name, "Updated Account")
        self.assertEqual(updated_account.balance, 2000.00)
        self.assertEqual(updated_account.currency, "EUR")

    def test_delete_account(self):
        """Test that an account can be deleted."""
        account_id = self.account.id

        # Delete the account
        self.account.delete()

        # Check that the account no longer exists
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=account_id)