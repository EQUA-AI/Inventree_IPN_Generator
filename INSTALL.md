# Category IPN Generator Plugin - Installation Guide# EPCON IPN Generator Plugin - Installation Guide



## Prerequisites## Prerequisites



- InvenTree v0.18.0 or higher- InvenTree v0.18.0 or higher

- Python 3.9 or higher- Python 3.9 or higher

- PostgreSQL database (for InvenTree)- PostgreSQL database (for InvenTree)



## Installation Methods## Installation Methods



### Method 1: Using pip (Recommended)### Method 1: Using pip (Recommended)



```bash```bash

# Install the plugin# Install the plugin

pip install inventree-category-ipn-generatorpip install inventree-epcon-ipn-generator



# Restart InvenTree# Restart InvenTree

invoke server -ainvoke server -a

``````



### Method 2: From Source### Method 2: From Source



```bash```bash

# Clone or copy the plugin directory# Clone or copy the plugin directory

cd /path/to/inventree/plugins/cd /path/to/inventree/plugins/

git clone https://github.com/inventree/inventree-category-ipn.git category_ipn_generatorgit clone https://github.com/epcon/inventree-epcon-ipn.git epcon_ipn_generator



# Install in development mode# Install in development mode

cd category_ipn_generatorcd epcon_ipn_generator

pip install -e .pip install -e .



# Restart InvenTree# Restart InvenTree

invoke server -ainvoke server -a

``````



### Method 3: Manual Installation### Method 3: Manual Installation



```bash```bash

# Copy the plugin directory to InvenTree's plugins folder# Copy the plugin directory to InvenTree's plugins folder

cp -r category_ipn_generator /path/to/inventree/plugins/cp -r epcon_ipn_generator /path/to/inventree/plugins/



# Restart InvenTree# Restart InvenTree

invoke server -ainvoke server -a

``````



## Configuration## Configuration



### 1. Enable Event Integration### 1. Enable Event Integration



1. Navigate to **Settings → Plugins** in InvenTree1. Navigate to **Settings → Plugins** in InvenTree

2. Find **"Enable Event Integration"** setting2. Find **"Enable Event Integration"** setting

3. Set to **Active**3. Set to **Active**

4. Save changes4. Save changes



### 2. Activate the Plugin### 2. Activate the Plugin



1. In **Settings → Plugins**, find **"Category IPN Generator"**1. In **Settings → Plugins**, find **"EPCON IPN Generator"**

2. Click the **Activate** button2. Click the **Activate** button

3. Configure plugin settings as needed:3. Configure plugin settings as needed:

   - **Active**: Enable IPN generation (default: True)   - **Active**: Enable IPN generation (default: True)

   - **On Create**: Generate IPNs for new parts (default: True)   - **On Create**: Generate IPNs for new parts (default: True)

   - **On Change**: Generate IPNs when editing parts (default: False)   - **On Change**: Generate IPNs when editing parts (default: False)

   - **Skip if IPN Exists**: Don't overwrite existing IPNs (default: True)   - **Skip if IPN Exists**: Don't overwrite existing IPNs (default: True)

   - **Require Category**: Only generate for categorized parts (default: True)   - **Require Category**: Only generate for categorized parts (default: True)

   - **Digit Length**: Number of digits in sequential part (1-10, default: 5)

   - **Separator**: Character between codes (default: "-")### 3. Add Category Metadata



### 3. Add Category MetadataEach category needs EPCON metadata for IPN generation. See [Category Setup](#category-setup) below.



Each category needs metadata with category codes for IPN generation. See [Category Setup](#category-setup) below.## Category Setup



## Category Setup### Option A: Using Django Shell



### Metadata Structure```bash

# Enter Django shell

Categories need two simple metadata fields:python manage.py shell

- `category_code`: Main category identifier (e.g., "01", "02")```

- `subcategory_code`: Sub-category identifier (e.g., "01", "18")

```python

**Example IPN Format:** `01-18-00001`from part.models import PartCategory

- `01` = category_code

- `18` = subcategory_code# Get or create a category

- `00001` = sequential number (5 digits by default)category = PartCategory.objects.get(name="Burners")



### Option A: Using Django Shell# Add EPCON metadata

category.metadata = {

```bash    "epcon_id": "COMB-01",

# Enter Django shell    "category_code": "01",

python manage.py shell    "subcategory_code": "01",

```    "range_start": 10100001,

    "range_end": 10199999

```python}

from part.models import PartCategory

category.save()

# Get or create a category```

category = PartCategory.objects.get(name="Electronic Components")

### Option B: Using SQL

# Add category metadata

category.metadata = {```sql

    "category_code": "01",-- PostgreSQL example

    "subcategory_code": "18"UPDATE part_partcategory 

}SET metadata = '{

    "epcon_id": "COMB-01",

category.save()    "category_code": "01",

    "subcategory_code": "01",

# Another example - Mechanical Parts    "range_start": 10100001,

mechanical = PartCategory.objects.get(name="Mechanical Parts")    "range_end": 10199999

mechanical.metadata = {}'::jsonb

    "category_code": "02",WHERE name = 'Burners';

    "subcategory_code": "01"```

}

mechanical.save()### Option C: Using Helper Script

```

```bash

### Option B: Using SQL# Run the metadata generator script

python scripts/add_category_metadata.py

```sql```

-- PostgreSQL example

UPDATE part_partcategory This will generate SQL or Python code based on your `CATEGORY_METADATA` configuration.

SET metadata = '{

    "category_code": "01",## Verification

    "subcategory_code": "18"

}'::jsonb### Test the Plugin

WHERE name = 'Electronic Components';

1. Create a new part in a category with EPCON metadata

-- Add metadata to multiple categories2. Leave the IPN field blank

UPDATE part_partcategory 3. Save the part

SET metadata = '{4. The IPN should be automatically assigned

    "category_code": "02",

    "subcategory_code": "01"### Verify Category Metadata

}'::jsonb

WHERE name = 'Mechanical Parts';```bash

```# Run verification script

python manage.py shell < scripts/verify_category_metadata.py

### Option C: Using Helper Script```



```bashThis will check all categories and report any issues.

# Run the metadata generator script

python scripts/add_category_metadata.py### Check Logs

```

```bash

This will prompt you for category codes and generate the metadata.# View InvenTree logs

tail -f /path/to/inventree/logs/inventree.log | grep "EPCON IPN"

### Choosing Category Codes```



Some suggestions for organizing your codes:Look for messages like:

```

**By Department:**INFO: EPCON IPN Generator: Assigned IPN '10100001' to part 'Eclipse Burner' (ID: 123)

- 01 = Electronics```

- 02 = Mechanical  

- 03 = Hardware## Troubleshooting

- 04 = Software

### Plugin Not Appearing

**By Product Line:**

- 10 = Product A**Problem:** Plugin doesn't show up in Settings → Plugins

- 20 = Product B

- 30 = Product C**Solution:**

1. Ensure InvenTree is restarted after installation

**By Function:**2. Check that the plugin directory is in the correct location

- 01 = Fasteners3. Verify that `__init__.py` and `core.py` exist in the plugin folder

- 02 = Connectors

- 03 = Sensors### IPNs Not Being Generated



Use subcategory codes for further subdivision (01-99).**Problem:** Parts are created but IPNs remain blank



## Customizing IPN Format**Solutions:**

1. Check that "Event Integration" is enabled

### Change Separator2. Verify the plugin is activated

3. Ensure "Active" setting is enabled in plugin settings

```python4. Check that category has valid metadata:

# In InvenTree plugin settings, change "Separator" to:   ```python

# Slash: "/" → produces 01/18/00001   from part.models import PartCategory

# Underscore: "_" → produces 01_18_00001   cat = PartCategory.objects.get(name="Your Category")

# None: "" → produces 011800001   print(cat.metadata)

# Period: "." → produces 01.18.00001   ```

```5. Review logs for error messages



### Change Digit Length### ValidationError on IPN



```python**Problem:** `ValidationError: IPN 'XXXXX' is outside the valid range`

# In InvenTree plugin settings, change "Digit Length" to:

# 3 digits → produces 01-18-001 (max 999 parts)**Solution:**

# 5 digits → produces 01-18-00001 (max 99,999 parts)- The IPN you're trying to use is outside the category's range

# 8 digits → produces 01-18-00000001 (max 99,999,999 parts)- Check category metadata: `range_start` and `range_end`

```- Either use an IPN within the range, or adjust the category's range



## Verification### Range Exhausted



### Test the Plugin**Problem:** `No available IPNs in range X-Y for category 'Z'`



1. Create a new part in a category with metadata**Solution:**

2. Leave the IPN field blank- The category's number range is full

3. Save the part- Increase the `range_end` value in category metadata:

4. The IPN should be automatically assigned (e.g., "01-18-00001")  ```python

  category.metadata['range_end'] = 10299999  # Increase range

Example test:  category.save()

```python  ```

from part.models import Part, PartCategory

## Uninstallation

# Get category

category = PartCategory.objects.get(name="Electronic Components")```bash

# Deactivate the plugin in InvenTree UI first

# Create part without IPN

part = Part.objects.create(# Then uninstall via pip

    category=category,pip uninstall inventree-epcon-ipn-generator

    name="Test Resistor",

    description="10K Ohm resistor"# Or remove the directory

)rm -rf /path/to/inventree/plugins/epcon_ipn_generator



# Check generated IPN# Restart InvenTree

print(f"Generated IPN: {part.IPN}")  # Should be something like "01-18-00001"invoke server -a

``````



### Verify Category Metadata## Next Steps



```bash- Read the [README.md](README.md) for detailed documentation

# Run verification script- Review example category metadata structures

python manage.py shell < scripts/verify_category_metadata.py- Set up all EPCON categories with appropriate ranges

```- Test IPN generation with sample parts



This will check all categories and report any issues.## Support



### Check LogsFor issues or questions:

- GitHub Issues: https://github.com/epcon/inventree-epcon-ipn/issues

```bash- Email: support@epcon.com

# View InvenTree logs
tail -f /path/to/inventree/logs/inventree.log | grep "Category IPN"
```

Look for messages like:
```
INFO: Category IPN Generator: Assigned IPN '01-18-00001' to part 'Test Resistor' (ID: 123)
```

## Troubleshooting

### Plugin Not Appearing

**Problem:** Plugin doesn't show up in Settings → Plugins

**Solution:**
1. Ensure InvenTree is restarted after installation
2. Check that the plugin directory is in the correct location
3. Verify that `__init__.py` and `core.py` exist in the plugin folder
4. Check InvenTree logs for plugin loading errors

### IPNs Not Being Generated

**Problem:** Parts are created but IPNs remain blank

**Solutions:**
1. Check that "Event Integration" is enabled in InvenTree settings
2. Verify the plugin is activated
3. Ensure "Active" setting is enabled in plugin settings
4. Check that category has valid metadata:
   ```python
   from part.models import PartCategory
   cat = PartCategory.objects.get(name="Your Category")
   print(cat.metadata)
   # Should show: {'category_code': 'XX', 'subcategory_code': 'YY'}
   ```
5. Review logs for error messages:
   ```bash
   tail -f /path/to/inventree/logs/inventree.log
   ```

### ValidationError on IPN

**Problem:** `ValidationError: IPN 'XX-YY-ZZZZZ' does not match expected format`

**Solution:**
- The IPN format doesn't match your category's codes
- Check the category metadata for correct codes
- Ensure separator and digit length settings match your IPNs
- Example: If you have "01-18-001" but digit length is set to 5, change it to 3

### Missing Category Metadata

**Problem:** `Category 'XYZ' does not have category_code metadata`

**Solution:**
- Add metadata to the category:
  ```python
  from part.models import PartCategory
  cat = PartCategory.objects.get(name="XYZ")
  cat.metadata = {
      "category_code": "03",
      "subcategory_code": "05"
  }
  cat.save()
  ```

### Maximum Sequential Number Reached

**Problem:** New parts aren't getting IPNs in a category

**Solution:**
- You may have reached the maximum for your digit length
- Example: With 5 digits, max is 99999
- Either:
  1. Increase digit length in plugin settings
  2. Use a different subcategory code
  3. Archive old parts and reset numbering (advanced)

### Duplicate IPN Error

**Problem:** `IntegrityError: duplicate key value violates unique constraint`

**Solution:**
- Another part already has this IPN
- The plugin should handle this automatically
- If it persists, check for:
  1. Manual IPN assignments conflicting with auto-generated ones
  2. Multiple instances of InvenTree writing to same database
  3. Plugin conflicts (disable other IPN plugins)

## Uninstallation

```bash
# Deactivate the plugin in InvenTree UI first

# Then uninstall via pip
pip uninstall inventree-category-ipn-generator

# Or remove the directory
rm -rf /path/to/inventree/plugins/category_ipn_generator

# Restart InvenTree
invoke server -a
```

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Review example category metadata structures in `examples/`
- Set up all your categories with appropriate codes
- Test IPN generation with sample parts
- Configure separator and digit length to match your needs

## Support

For issues or questions:
- GitHub Issues: https://github.com/inventree/inventree-category-ipn/issues
- InvenTree Forum: https://forum.inventree.org
- Email: plugins@inventree.org
