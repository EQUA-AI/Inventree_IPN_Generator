"""Verify category metadata in InvenTree

This script checks that all categories have the required metadata
for IPN generation.
"""

from part.models import PartCategory
import sys


def verify_category_metadata():
    """Check all categories for required metadata"""
    
    print("="*80)
    print("Category IPN Generator - Metadata Verification")
    print("="*80)
    print()
    
    # Get all categories
    categories = PartCategory.objects.all()
    
    total = categories.count()
    valid = 0
    invalid = []
    
    print(f"Found {total} categories\n")
    
    for category in categories:
        metadata = category.metadata or {}
        
        # Check for required fields
        has_category_code = 'category_code' in metadata
        has_subcategory_code = 'subcategory_code' in metadata
        
        if has_category_code and has_subcategory_code:
            valid += 1
            status = "✅ VALID"
            
            # Validate code values
            try:
                category_code = str(metadata['category_code'])
                subcategory_code = str(metadata['subcategory_code'])
                
                # Check if codes are reasonable (not empty, not too long)
                if not category_code or len(category_code) > 10:
                    status = "⚠️  INVALID CATEGORY CODE"
                    invalid.append({
                        'category': category.name,
                        'issue': f"category_code is invalid: '{category_code}'"
                    })
                elif not subcategory_code or len(subcategory_code) > 10:
                    status = "⚠️  INVALID SUBCATEGORY CODE"
                    invalid.append({
                        'category': category.name,
                        'issue': f"subcategory_code is invalid: '{subcategory_code}'"
                    })
            except (ValueError, TypeError):
                status = "⚠️  INVALID VALUES"
                invalid.append({
                    'category': category.name,
                    'issue': "code values cannot be converted to strings"
                })
        else:
            status = "❌ MISSING METADATA"
            missing_fields = []
            if not has_category_code:
                missing_fields.append('category_code')
            if not has_subcategory_code:
                missing_fields.append('subcategory_code')
            
            invalid.append({
                'category': category.name,
                'issue': f"Missing fields: {', '.join(missing_fields)}"
            })
        
        code_info = ""
        if has_category_code and has_subcategory_code:
            code_info = f"{metadata['category_code']}-{metadata['subcategory_code']}"
        
        print(f"{status} | {category.name:40} | Codes: {code_info:10}")
    
    print()
    print("-"*80)
    print(f"Summary: {valid}/{total} categories have valid metadata")
    print("-"*80)
    
    if invalid:
        print()
        print("Issues found:")
        print()
        for item in invalid:
            print(f"❌ {item['category']}")
            print(f"   {item['issue']}")
            print()
        
        return False
    else:
        print()
        print("✅ All categories have valid metadata!")
        print()
        return True


if __name__ == "__main__":
    # This script should be run within InvenTree's Django environment
    # python manage.py shell < scripts/verify_category_metadata.py
    
    try:
        success = verify_category_metadata()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
