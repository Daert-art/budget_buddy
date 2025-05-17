import os
import sys

import django
from django.test import TestCase

from apps.core.models import Tag

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

class TagModelTest(TestCase):
    def setUp(self):
        """Create a test tag before each test."""
        self.tag_data = {
            "name": "Test Tag",
        }
        # Create a Tag object and save it to the database
        self.tag = Tag.objects.create(**self.tag_data)

    def test_create_tag(self):
        """Test that a tag can be created and saved to the database."""
        tag = Tag.objects.get(id=self.tag.id)
        # Check that the tag fields match the expected values
        self.assertEqual(tag.name, self.tag_data["name"])

    def test_read_tag(self):
        """Test that a tag can be read from the database."""
        tag = Tag.objects.get(id=self.tag.id)
        # Check that the tag fields match the expected values
        self.assertEqual(tag.name, self.tag_data["name"])

    def test_update_tag(self):
        """Test that a tag can be updated and changes are saved to the database."""
        tag = Tag.objects.get(id=self.tag.id)
        # Update the tag fields
        tag.name = "Updated Tag"
        tag.save()

        # Check that the updated tag fields match the expected values
        updated_tag = Tag.objects.get(id=self.tag.id)
        self.assertEqual(updated_tag.name, "Updated Tag")

    def test_delete_tag(self):
        """Test that a tag can be deleted."""
        tag_id = self.tag.id

        # Delete the tag
        self.tag.delete()

        # Check that the tag no longer exists
        with self.assertRaises(Tag.DoesNotExist):
            Tag.objects.get(id=tag_id)