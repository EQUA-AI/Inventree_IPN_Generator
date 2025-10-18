"""Unit tests for Category IPN Generator Plugin"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from part.models import Part, PartCategory
from plugin import registry
import logging

logger = logging.getLogger("inventree")


class CategoryIPNGeneratorTests(TestCase):
    """Test suite for Category IPN Generator plugin"""

    def setUp(self):
        """Set up test environment"""
        self.plugin = registry.get_plugin('category-ipn-generator')
        
        if self.plugin:
            conf = self.plugin.plugin_config()
            conf.active = True
            conf.save()
            
            self.plugin.set_setting('ACTIVE', True)
            self.plugin.set_setting('ON_CREATE', True)
            self.plugin.set_setting('SKIP_IF_IPN_EXISTS', True)
            self.plugin.set_setting('REQUIRE_CATEGORY', True)
            self.plugin.set_setting('DIGIT_LENGTH', 5)
            self.plugin.set_setting('SEPARATOR', '-')
        
        self.category = PartCategory.objects.create(
            name='Test Valves',
            description='Test category for valves',
            metadata={
                'category_code': '02',
                'subcategory_code': '01'
            }
        )

    def tearDown(self):
        """Clean up test environment"""
        Part.objects.filter(category=self.category).delete()
        self.category.delete()

    def test_plugin_is_loaded(self):
        """Verify that the plugin is loaded and active"""
        self.assertIsNotNone(self.plugin, "Plugin should be loaded")
        self.assertTrue(self.plugin.get_setting('ACTIVE'), "Plugin should be active")

    def test_generate_first_ipn(self):
        """Test generating the first IPN in a category"""
        part = Part.objects.create(
            category=self.category,
            name='Test Valve 1',
            description='First test valve'
        )
        
        part.refresh_from_db()
        self.assertEqual(part.IPN, '02-01-00001', "First IPN should be 02-01-00001")

    def test_generate_sequential_ipns(self):
        """Test that IPNs increment sequentially"""
        part1 = Part.objects.create(category=self.category, name='Test Valve 1')
        part1.refresh_from_db()
        self.assertEqual(part1.IPN, '02-01-00001')
        
        part2 = Part.objects.create(category=self.category, name='Test Valve 2')
        part2.refresh_from_db()
        self.assertEqual(part2.IPN, '02-01-00002')
        
        part3 = Part.objects.create(category=self.category, name='Test Valve 3')
        part3.refresh_from_db()
        self.assertEqual(part3.IPN, '02-01-00003')

    def test_skip_if_ipn_exists(self):
        """Test that existing IPNs are not overwritten"""
        part = Part.objects.create(
            category=self.category,
            name='Test Valve Manual',
            IPN='99-99-99999'
        )
        
        part.refresh_from_db()
        self.assertEqual(part.IPN, '99-99-99999', "Existing IPN should not be overwritten")

    def test_part_without_category(self):
        """Test that parts without categories are skipped"""
        part = Part.objects.create(name='Test Part No Category')
        part.refresh_from_db()
        self.assertIsNone(part.IPN, "IPN should not be generated without category")

    def test_different_separator(self):
        """Test IPN generation with different separator"""
        self.plugin.set_setting('SEPARATOR', '/')
        part = Part.objects.create(category=self.category, name='Test Valve Slash')
        part.refresh_from_db()
        self.assertEqual(part.IPN, '02/01/00001', "IPN should use slash separator")
        self.plugin.set_setting('SEPARATOR', '-')

    def test_different_digit_length(self):
        """Test IPN generation with different digit lengths"""
        self.plugin.set_setting('DIGIT_LENGTH', 3)
        part = Part.objects.create(category=self.category, name='Test Valve 3 Digits')
        part.refresh_from_db()
        self.assertEqual(part.IPN, '02-01-001', "IPN should have 3 digits")
        self.plugin.set_setting('DIGIT_LENGTH', 5)

    def test_multiple_categories(self):
        """Test that IPNs are independent per category"""
        category2 = PartCategory.objects.create(
            name='Test Burners',
            metadata={'category_code': '01', 'subcategory_code': '01'}
        )
        
        part1 = Part.objects.create(category=self.category, name='Valve Part')
        part1.refresh_from_db()
        self.assertEqual(part1.IPN, '02-01-00001')
        
        part2 = Part.objects.create(category=category2, name='Burner Part')
        part2.refresh_from_db()
        self.assertEqual(part2.IPN, '01-01-00001')
        
        category2.delete()
