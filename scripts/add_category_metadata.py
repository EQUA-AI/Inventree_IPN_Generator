"""Python script to add category metadata to InvenTree categories

This script helps add category codes to InvenTree categories for 
the Category IPN Generator plugin.
"""

import json

# Example category metadata mapping
# Customize this for your categories
CATEGORY_METADATA = {
    "Resistors": {
        "category_code": "01",
        "subcategory_code": "01"
    },
    "Capacitors": {
        "category_code": "01",
        "subcategory_code": "02"
    },
    "Integrated Circuits": {
        "category_code": "02",
        "subcategory_code": "01"
    },
    "Fasteners": {
        "category_code": "10",
        "subcategory_code": "01"
    },
    # Add more categories here...
}


def generate_sql():
    """Generate SQL statements to add metadata to categories"""
    
    print("-- SQL statements to add category metadata to InvenTree categories")
    print("-- Run these in PostgreSQL to update your categories\n")
    
    for category_name, metadata in CATEGORY_METADATA.items():
        metadata_json = json.dumps(metadata)
        
        sql = f"""
UPDATE part_partcategory 
SET metadata = '{metadata_json}'::jsonb
WHERE name = '{category_name}';
"""
        print(sql)


def generate_python():
    """Generate Python code to add metadata using Django ORM"""
    
    print("# Python code to add category metadata to InvenTree categories")
    print("# Run this in InvenTree's Django shell: python manage.py shell\n")
    print("from part.models import PartCategory\n")
    
    for category_name, metadata in CATEGORY_METADATA.items():
        print(f"# Update {category_name}")
        print(f"category = PartCategory.objects.get(name='{category_name}')")
        print(f"category.metadata = {metadata}")
        print(f"category.save()")
        print()


if __name__ == "__main__":
    print("="*80)
    print("Category IPN Generator - Metadata Setup Script")
    print("="*80)
    print()
    
    print("Choose an option:")
    print("1. Generate SQL statements")
    print("2. Generate Python code")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    print()
    print("-"*80)
    print()
    
    if choice == "1":
        generate_sql()
    elif choice == "2":
        generate_python()
    else:
        print("Invalid choice. Please run the script again and enter 1 or 2.")
