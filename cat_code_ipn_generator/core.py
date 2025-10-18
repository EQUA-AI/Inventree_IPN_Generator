"""Category-Based IPN Generator Plugin - Core Implementation

Automatically generates Internal Part Numbers (IPNs) for parts based on
their category codes and sequential numbering.
"""

from plugin import InvenTreePlugin
from plugin.mixins import EventMixin, ValidationMixin, SettingsMixin

from part.models import Part
from django.core.exceptions import ValidationError

import logging
import re

from . import PLUGIN_VERSION

logger = logging.getLogger("inventree")


def validate_digit_length(value):
    """Validate that digit length is between 1 and 10"""
    try:
        val = int(value)
        if val < 1 or val > 10:
            raise ValidationError("Digit length must be between 1 and 10")
        return val
    except (ValueError, TypeError):
        raise ValidationError("Digit length must be a valid integer")


class CategoryIPNGeneratorPlugin(EventMixin, ValidationMixin, SettingsMixin, InvenTreePlugin):
    """Plugin to auto-generate IPNs based on category codes.
    
    This plugin reads category metadata containing:
    - category_code: Primary category code (e.g., "01")
    - subcategory_code: Subcategory code (e.g., "18")
    
    IPN Format: [category_code][subcategory_code][sequential_number]
    Example: 01-18-00001
    
    When a part is created without an IPN, the plugin:
    1. Reads the category metadata
    2. Finds the next sequential number for that category
    3. Assigns it automatically
    """

    # Plugin metadata
    TITLE = "Category IPN Generator"
    NAME = "CategoryIPNGenerator"
    SLUG = "category-ipn-generator"
    DESCRIPTION = "Automatically generate IPNs based on category codes and sequential numbering"
    VERSION = PLUGIN_VERSION

    # Additional project information
    AUTHOR = "InvenTree Community"
    WEBSITE = "https://github.com/inventree/inventree-category-ipn"
    LICENSE = "MIT"

    # Supported InvenTree versions
    MIN_VERSION = '0.18.0'

    # Plugin settings
    SETTINGS = {
        'ACTIVE': {
            'name': 'Active',
            'description': 'Enable/disable IPN generator without uninstalling the plugin',
            'validator': bool,
            'default': True,
        },
        'ON_CREATE': {
            'name': 'On Create',
            'description': 'Generate IPNs when creating new parts',
            'validator': bool,
            'default': True,
        },
        'ON_CHANGE': {
            'name': 'On Change',
            'description': 'Regenerate IPNs when editing parts (⚠️ use with caution - may overwrite existing IPNs)',
            'validator': bool,
            'default': False,
        },
        'SKIP_IF_IPN_EXISTS': {
            'name': 'Skip if IPN Exists',
            'description': 'Do not overwrite existing IPNs when enabled',
            'validator': bool,
            'default': True,
        },
        'REQUIRE_CATEGORY': {
            'name': 'Require Category',
            'description': 'Only generate IPNs for parts that have a category assigned',
            'validator': bool,
            'default': True,
        },
        'DIGIT_LENGTH': {
            'name': 'Sequential Number Digits',
            'description': 'Number of digits for the sequential part (1-10). Example: 5 digits = 00001, 00002, etc.',
            'validator': validate_digit_length,
            'default': 5,
        },
        'SEPARATOR': {
            'name': 'Separator Character',
            'description': 'Character to separate category codes and number (e.g., "-" gives "01-18-00001")',
            'default': '-',
        },
    }

    def wants_process_event(self, event: str) -> bool:
        """Determine if the plugin should process a given event.
        
        Args:
            event: The InvenTree event name (e.g., 'part_part.created')
            
        Returns:
            True if the plugin should process this event, False otherwise
        """
        # Only process events when plugin is active
        if not self.get_setting('ACTIVE'):
            logger.debug("Category IPN Generator: Plugin is not active, skipping event")
            return False
        
        # Process part creation events if ON_CREATE is enabled
        if event == 'part_part.created':
            return self.get_setting('ON_CREATE')
        
        # Process part save events if ON_CHANGE is enabled
        if event == 'part_part.saved':
            return self.get_setting('ON_CHANGE')
        
        return False

    def process_event(self, event: str, *args, **kwargs) -> None:
        """Main event handler - generates IPN for parts.
        
        Args:
            event: The InvenTree event name
            **kwargs: Event data including 'id' (part ID) and 'model' (model name)
        """
        # Extract event data
        part_id = kwargs.get('id', None)
        model = kwargs.get('model', None)

        # Only process Part model events
        if model != 'Part':
            logger.debug(f"Category IPN Generator: Event model is '{model}', not 'Part'. Skipping.")
            return

        if not part_id:
            logger.warning("Category IPN Generator: No part ID provided in event. Skipping.")
            return

        try:
            part = Part.objects.get(id=part_id)
        except Part.DoesNotExist:
            logger.error(f"Category IPN Generator: Part with ID {part_id} does not exist. Skipping.")
            return

        # Skip if part already has an IPN and SKIP_IF_IPN_EXISTS is enabled
        if part.IPN and self.get_setting('SKIP_IF_IPN_EXISTS'):
            logger.debug(f"Category IPN Generator: Part {part.name} (ID: {part_id}) already has IPN '{part.IPN}'. Skipping.")
            return

        # Require category if setting is enabled
        if not part.category and self.get_setting('REQUIRE_CATEGORY'):
            logger.info(f"Category IPN Generator: Part {part.name} (ID: {part_id}) has no category and REQUIRE_CATEGORY is enabled. Skipping.")
            return

        # Generate and assign IPN
        try:
            new_ipn = self.generate_ipn_for_part(part)
            
            if new_ipn:
                part.IPN = new_ipn
                part.save()
                logger.info(f"Category IPN Generator: Assigned IPN '{new_ipn}' to part '{part.name}' (ID: {part_id})")
            else:
                logger.warning(f"Category IPN Generator: Could not generate IPN for part '{part.name}' (ID: {part_id})")
                
        except Exception as e:
            logger.error(f"Category IPN Generator: Error generating IPN for part '{part.name}' (ID: {part_id}): {str(e)}")

    def generate_ipn_for_part(self, part: Part) -> str:
        """Generate an IPN for a part based on its category metadata.
        
        Args:
            part: The Part instance to generate an IPN for
            
        Returns:
            The generated IPN as a string, or None if generation fails
        """
        # If part has no category, we can't generate an IPN
        if not part.category:
            logger.warning(f"Category IPN Generator: Part '{part.name}' has no category. Cannot generate IPN.")
            return None

        category = part.category
        
        # Read category metadata
        metadata = category.metadata or {}
        
        # Extract category codes
        category_code = metadata.get('category_code', None)
        subcategory_code = metadata.get('subcategory_code', None)
        
        # Validate metadata
        if not category_code or not subcategory_code:
            logger.error(
                f"Category IPN Generator: Category '{category.name}' "
                f"missing 'category_code' or 'subcategory_code' in metadata. Cannot generate IPN."
            )
            return None

        # Get plugin settings
        digit_length = int(self.get_setting('DIGIT_LENGTH'))
        separator = self.get_setting('SEPARATOR')
        
        # Build the prefix (category_code + separator + subcategory_code)
        prefix = f"{category_code}{separator}{subcategory_code}{separator}"
        
        # Find the next sequential number for this category
        next_number = self.get_next_number_for_category(category, prefix, digit_length)
        
        if next_number is None:
            logger.error(
                f"Category IPN Generator: Could not generate sequential number "
                f"for category '{category.name}'"
            )
            return None

        # Format the number with leading zeros
        formatted_number = str(next_number).zfill(digit_length)
        
        # Build the complete IPN
        ipn = f"{prefix}{formatted_number}"
        
        logger.debug(f"Category IPN Generator: Generated IPN '{ipn}' for category '{category.name}'")
        
        return ipn

    def get_next_number_for_category(self, category, prefix: str, digit_length: int) -> int:
        """Find the next sequential number for a category.
        
        Args:
            category: The PartCategory instance
            prefix: The IPN prefix (e.g., "01-18-")
            digit_length: Number of digits for the sequential part
            
        Returns:
            The next sequential number (e.g., 1, 2, 3...), or None if error
        """
        # Query all parts in this category with IPNs matching the prefix
        existing_parts = Part.objects.filter(
            category=category,
            IPN__isnull=False,
            IPN__startswith=prefix
        ).exclude(
            IPN=''
        ).order_by('-IPN')

        # Find the highest sequential number
        highest_number = 0
        
        # Regular expression to extract the sequential number from the IPN
        # Example: "01-18-00042" -> extract "00042" -> 42
        pattern = re.compile(rf'^{re.escape(prefix)}(\d+)$')
        
        for part in existing_parts:
            match = pattern.match(part.IPN)
            if match:
                try:
                    number = int(match.group(1))
                    if number > highest_number:
                        highest_number = number
                except (ValueError, TypeError):
                    # Skip invalid numbers
                    continue

        # Next number is highest + 1 (or 1 if no existing parts)
        next_number = highest_number + 1
        
        # Check if the number exceeds the maximum possible for the digit length
        max_number = 10 ** digit_length - 1
        if next_number > max_number:
            logger.error(
                f"Category IPN Generator: Sequential number {next_number} exceeds maximum "
                f"for {digit_length} digits (max: {max_number}) in category '{category.name}'"
            )
            return None

        return next_number

    def validate_part_ipn(self, ipn: str, part: Part, **kwargs) -> None:
        """Validate that a part's IPN matches the expected format for its category.
        
        This is called by InvenTree's ValidationMixin when a part is being saved.
        
        Args:
            ipn: The IPN being validated
            part: The Part instance
            **kwargs: Additional validation context
            
        Raises:
            ValidationError: If the IPN is invalid for the part's category
        """
        # Skip validation if no IPN
        if not ipn:
            return

        # Skip validation if no category
        if not part.category:
            return

        category = part.category
        metadata = category.metadata or {}
        
        # Extract category codes from metadata
        category_code = metadata.get('category_code', None)
        subcategory_code = metadata.get('subcategory_code', None)

        # If no category codes in metadata, skip validation
        if not category_code or not subcategory_code:
            return

        # Get plugin settings
        separator = self.get_setting('SEPARATOR')
        digit_length = int(self.get_setting('DIGIT_LENGTH'))
        
        # Build the expected prefix
        expected_prefix = f"{category_code}{separator}{subcategory_code}{separator}"
        
        # Validate IPN format
        if not ipn.startswith(expected_prefix):
            raise ValidationError(
                f"IPN '{ipn}' does not match the expected format for category '{category.name}'. "
                f"Expected format: {expected_prefix}[{digit_length} digits]. "
                f"Example: {expected_prefix}{'0' * digit_length}"
            )
        
        # Validate the sequential number part
        sequential_part = ipn[len(expected_prefix):]
        
        if not sequential_part.isdigit():
            raise ValidationError(
                f"IPN '{ipn}' has invalid sequential number. Must be numeric digits."
            )
        
        if len(sequential_part) != digit_length:
            raise ValidationError(
                f"IPN '{ipn}' sequential number has {len(sequential_part)} digits, "
                f"but plugin is configured for {digit_length} digits."
            )
