# Category-Based IPN Auto-Generator Plugin

InvenTree plugin for automatically generating Internal Part Numbers (IPNs) based on category codes and sequential numbering.

## 🎯 Overview

This plugin automatically assigns IPNs to parts based on their category's metadata. Each category contains simple category codes that are combined with a sequential number to create unique, structured part numbers.

### IPN Format

**Pattern**: `[category_code][separator][subcategory_code][separator][sequential_number]`

**Example**: `01-18-00001`
- `01` = Category code
- `18` = Subcategory code  
- `00001` = Sequential number (5 digits by default)

### How It Works

When a part is created without an IPN:
1. Plugin reads the category metadata (`category_code`, `subcategory_code`)
2. Builds prefix: e.g., `01-18-`
3. Finds highest existing sequential number with this prefix
4. Assigns next number: `01-18-00001`, `01-18-00002`, etc.

## 📋 Features

- ✅ Auto-generates IPNs based on category codes
- ✅ Sequential numbering per category (1, 2, 3...)
- ✅ Configurable separator character (-, /, _, or none)
- ✅ Configurable digit length (1-10 digits)
- ✅ Independent sequences per category prefix
- ✅ Validates IPNs match expected format
- ✅ Prevents duplicate IPNs
- ✅ Skips parts that already have IPNs
- ✅ Works on part creation and optionally on edit
- ✅ Comprehensive error handling and logging

## 🚀 Installation

### From pip (Recommended)

```bash
pip install inventree-category-ipn-generator
invoke server -a
```

### From Source

```bash
cd /path/to/inventree/plugins/
git clone https://github.com/inventree/inventree-category-ipn.git
cd inventree-category-ipn
pip install -e .
invoke server -a
```

## ⚙️ Configuration

### 1. Enable Event Integration

1. Go to **Settings → Plugins** in InvenTree
2. Enable **"Enable Event Integration"**
3. Save

### 2. Activate Plugin

1. In **Settings → Plugins**, find **"Category IPN Generator"**
2. Click **Activate**
3. Configure settings:

| Setting | Description | Default |
|---------|-------------|---------|
| **Active** | Enable IPN generation | `True` |
| **On Create** | Generate IPNs for new parts | `True` |
| **On Change** | Reassign IPNs when editing parts (⚠️ use caution) | `False` |
| **Skip if IPN Exists** | Don't overwrite existing IPNs | `True` |
| **Require Category** | Only generate for categorized parts | `True` |
| **Digit Length** | Number of digits in sequential part (1-10) | `5` |
| **Separator** | Character between codes (e.g., -, /, _) | `-` |

### 3. Add Category Metadata

Each category needs metadata with two codes:

```json
{
    "category_code": "01",
    "subcategory_code": "18"
}
```

**Using Django Shell:**

```python
from part.models import PartCategory

category = PartCategory.objects.get(name="Electronic Components")
category.metadata = {
    "category_code": "01",
    "subcategory_code": "18"
}
category.save()
```

**Using SQL (PostgreSQL):**

```sql
UPDATE part_partcategory 
SET metadata = '{"category_code": "01", "subcategory_code": "18"}'::jsonb
WHERE name = 'Electronic Components';
```

## 📖 Usage Examples

### Example 1: Default Configuration

**Plugin Settings:**
- Separator: `-`
- Digit Length: `5`

**Category Metadata:**
```json
{"category_code": "02", "subcategory_code": "01"}
```

**Generated IPNs:**
- First part: `02-01-00001`
- Second part: `02-01-00002`
- Third part: `02-01-00003`

### Example 2: Custom Separator

**Plugin Settings:**
- Separator: `/`
- Digit Length: `5`

**Generated IPNs:**
- `02/01/00001`
- `02/01/00002`
- `02/01/00003`

### Example 3: Shorter Digit Length

**Plugin Settings:**
- Separator: `-`
- Digit Length: `3`

**Generated IPNs:**
- `02-01-001`
- `02-01-002`
- `02-01-999` (max for 3 digits)

### Example 4: No Separator

**Plugin Settings:**
- Separator: `` (empty)
- Digit Length: `5`

**Generated IPNs:**
- `020100001`
- `020100002`
- `020100003`

## 🧪 Testing

### Run All Tests

```bash
python manage.py test epcon_ipn_generator.tests
```

### Run Specific Test

```bash
python manage.py test epcon_ipn_generator.tests.CategoryIPNGeneratorTests.test_generate_first_ipn
```

### With Coverage

```bash
coverage run --source='epcon_ipn_generator' manage.py test
coverage report
```

## 🐛 Troubleshooting

### Plugin Not Generating IPNs

**Check:**
1. Event Integration enabled in InvenTree settings
2. Plugin activated
3. "Active" setting enabled in plugin
4. Category has valid metadata
5. Check logs for errors

```bash
tail -f /path/to/inventree/logs/inventree.log | grep "Category IPN"
```

### Wrong IPN Format

**Issue:** IPNs don't match expected format

**Solution:** Check plugin settings for separator and digit length match your expectations.

### Missing Category Metadata

**Issue:** `Category 'XYZ' does not have category_code metadata`

**Solution:** Add metadata to the category (see Configuration section).

## 📚 Documentation

- [Installation Guide](INSTALL.md) - Detailed installation steps
- [Project Summary](PROJECT_SUMMARY.md) - Technical overview
- [Example Metadata](examples/category_metadata.md) - Sample configurations

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - Free for commercial and personal use.

Copyright (c) 2025 InvenTree Community Contributors

## 🔗 Links

- **GitHub**: https://github.com/inventree/inventree-category-ipn
- **InvenTree**: https://inventree.org
- **Forum**: https://forum.inventree.org
