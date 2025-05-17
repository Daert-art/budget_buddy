import os
import sys

import django
from django.test import TestCase

from apps.core.models import Category

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# name = models.CharField(max_length=100)
# type = models.CharField(max_length=10, choices=TransactionType.choices, default=TransactionType.INCOME)

class CategoryModelTest(TestCase):
    def setUp(self):
        """Create a test category before each test."""
        self.category_data = {
            "name": "Test Category",
            "type": "income",
        }
        # Create a Category object and save it to the database
        self.category = Category.objects.create(**self.category_data)

    def test_create_category(self):
        """Test that a category can be created and saved to the database."""
        category = Category.objects.get(id=self.category.id)
        # Check that the category fields match the expected values
        self.assertEqual(category.name, self.category_data["name"])
        self.assertEqual(category.type, self.category_data["type"])

    def test_read_category(self):
        """Test that a category can be read from the database."""
        category = Category.objects.get(id=self.category.id)
        # Check that the category fields match the expected values
        self.assertEqual(category.name, self.category_data["name"])
        self.assertEqual(category.type, self.category_data["type"])

    def test_update_category(self):
        """Test that a category can be updated and changes are saved to the database."""
        category = Category.objects.get(id=self.category.id)
        # Update the category fields
        category.name = "Updated Category"
        category.type = "expense"
        category.save()

        # Check that the updated category fields match the expected values
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, "Updated Category")
        self.assertEqual(updated_category.type, "expense")

    def test_delete_category(self):
        """Test that a category can be deleted."""
        category_id = self.category.id

        # Delete the category
        self.category.delete()

        # Check that the category no longer exists
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)