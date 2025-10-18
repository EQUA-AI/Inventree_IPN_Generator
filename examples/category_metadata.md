# Example Category Metadata Configurations# Example Category Metadata Configurations



This file provides example metadata configurations for various category structures.This file provides example metadata configurations for various EPCON categories.



## Simple Format## Standard Format



```json```json

{{

    "category_code": "CC",    "epcon_id": "CATEGORY-SUBCATEGORY",

    "subcategory_code": "SS"    "category_code": "CC",

}    "subcategory_code": "SS",

```    "range_start": NNNNNNNN,

    "range_end": NNNNNNNN

Where:}

- `CC` = Category code (typically 01-99)```

- `SS` = Subcategory code (typically 01-99)

## Combustion Equipment (COMB)

The plugin will generate IPNs like: `CC-SS-00001` (format depends on settings)

### Burners (COMB-01)

---```json

{

## Electronics Organization    "epcon_id": "COMB-01",

    "category_code": "01",

### Passive Components (01)    "subcategory_code": "01",

    "range_start": 10100001,

#### Resistors (01-01)    "range_end": 10199999

```json}

{```

    "category_code": "01",

    "subcategory_code": "01"### Gas Pressure Regulators / Governors (COMB-18)

}```json

```{

**Example IPNs:** `01-01-00001`, `01-01-00002`, `01-01-00003`    "epcon_id": "COMB-18",

    "category_code": "01",

#### Capacitors (01-02)    "subcategory_code": "18",

```json    "range_start": 10180001,

{    "range_end": 10189999

    "category_code": "01",}

    "subcategory_code": "02"```

}

```### Pilot Burners (COMB-23)

**Example IPNs:** `01-02-00001`, `01-02-00002`, `01-02-00003````json

{

#### Inductors (01-03)    "epcon_id": "COMB-23",

```json    "category_code": "01",

{    "subcategory_code": "23",

    "category_code": "01",    "range_start": 10230001,

    "subcategory_code": "03"    "range_end": 10239999

}}

``````

**Example IPNs:** `01-03-00001`, `01-03-00002`, `01-03-00003`

## Valves (VALVE)

### Active Components (02)

### Ball Valves (VALVE-01)

#### Integrated Circuits (02-01)```json

```json{

{    "epcon_id": "VALVE-01",

    "category_code": "02",    "category_code": "02",

    "subcategory_code": "01"    "subcategory_code": "01",

}    "range_start": 20100001,

```    "range_end": 20199999

**Example IPNs:** `02-01-00001`, `02-01-00002`, `02-01-00003`}

```

#### Transistors (02-02)

```json### Butterfly Valves (VALVE-02)

{```json

    "category_code": "02",{

    "subcategory_code": "02"    "epcon_id": "VALVE-02",

}    "category_code": "02",

```    "subcategory_code": "02",

**Example IPNs:** `02-02-00001`, `02-02-00002`, `02-02-00003`    "range_start": 20200001,

    "range_end": 20299999

#### Diodes (02-03)}

```json```

{

    "category_code": "02",### Check Valves (VALVE-03)

    "subcategory_code": "03"```json

}{

```    "epcon_id": "VALVE-03",

**Example IPNs:** `02-03-00001`, `02-03-00002`, `02-03-00003`    "category_code": "02",

    "subcategory_code": "03",

### Connectors (03)    "range_start": 20300001,

    "range_end": 20399999

#### USB Connectors (03-01)}

```json```

{

    "category_code": "03",## Instrumentation (INST)

    "subcategory_code": "01"

}### Temperature Sensors (INST-01)

``````json

**Example IPNs:** `03-01-00001`, `03-01-00002`, `03-01-00003`{

    "epcon_id": "INST-01",

#### HDMI Connectors (03-02)    "category_code": "03",

```json    "subcategory_code": "01",

{    "range_start": 30100001,

    "category_code": "03",    "range_end": 30199999

    "subcategory_code": "02"}

}```

```

**Example IPNs:** `03-02-00001`, `03-02-00002`, `03-02-00003`### Pressure Sensors (INST-02)

```json

---{

    "epcon_id": "INST-02",

## Mechanical Parts Organization    "category_code": "03",

    "subcategory_code": "02",

### Fasteners (10)    "range_start": 30200001,

    "range_end": 30299999

#### Bolts (10-01)}

```json```

{

    "category_code": "10",### Flow Meters (INST-03)

    "subcategory_code": "01"```json

}{

```    "epcon_id": "INST-03",

**Example IPNs:** `10-01-00001`, `10-01-00002`, `10-01-00003`    "category_code": "03",

    "subcategory_code": "03",

#### Nuts (10-02)    "range_start": 30300001,

```json    "range_end": 30399999

{}

    "category_code": "10",```

    "subcategory_code": "02"

}## Electrical (ELEC)

```

**Example IPNs:** `10-02-00001`, `10-02-00002`, `10-02-00003`### Transformers (ELEC-01)

```json

#### Washers (10-03){

```json    "epcon_id": "ELEC-01",

{    "category_code": "04",

    "category_code": "10",    "subcategory_code": "01",

    "subcategory_code": "03"    "range_start": 40100001,

}    "range_end": 40199999

```}

**Example IPNs:** `10-03-00001`, `10-03-00002`, `10-03-00003````



### Brackets (11)### Control Panels (ELEC-02)

```json

#### L-Brackets (11-01){

```json    "epcon_id": "ELEC-02",

{    "category_code": "04",

    "category_code": "11",    "subcategory_code": "02",

    "subcategory_code": "01"    "range_start": 40200001,

}    "range_end": 40299999

```}

**Example IPNs:** `11-01-00001`, `11-01-00002`, `11-01-00003````



#### Flat Brackets (11-02)### Terminal Blocks (ELEC-03)

```json```json

{{

    "category_code": "11",    "epcon_id": "ELEC-03",

    "subcategory_code": "02"    "category_code": "04",

}    "subcategory_code": "03",

```    "range_start": 40300001,

**Example IPNs:** `11-02-00001`, `11-02-00002`, `11-02-00003`    "range_end": 40399999

}

### Enclosures (12)```



#### Plastic Cases (12-01)## Mechanical (MECH)

```json

{### Bearings (MECH-01)

    "category_code": "12",```json

    "subcategory_code": "01"{

}    "epcon_id": "MECH-01",

```    "category_code": "05",

**Example IPNs:** `12-01-00001`, `12-01-00002`, `12-01-00003`    "subcategory_code": "01",

    "range_start": 50100001,

#### Metal Enclosures (12-02)    "range_end": 50199999

```json}

{```

    "category_code": "12",

    "subcategory_code": "02"### Couplings (MECH-02)

}```json

```{

**Example IPNs:** `12-02-00001`, `12-02-00002`, `12-02-00003`    "epcon_id": "MECH-02",

    "category_code": "05",

---    "subcategory_code": "02",

    "range_start": 50200001,

## Product Line Organization    "range_end": 50299999

}

### Product A (20)```



#### Hardware Components (20-01)### Gears (MECH-03)

```json```json

{{

    "category_code": "20",    "epcon_id": "MECH-03",

    "subcategory_code": "01"    "category_code": "05",

}    "subcategory_code": "03",

```    "range_start": 50300001,

**Example IPNs:** `20-01-00001`, `20-01-00002`, `20-01-00003`    "range_end": 50399999

}

#### Software Components (20-02)```

```json

{## How to Apply These Examples

    "category_code": "20",

    "subcategory_code": "02"### Using Python (Django Shell)

}

``````python

**Example IPNs:** `20-02-00001`, `20-02-00002`, `20-02-00003`from part.models import PartCategory



#### Documentation (20-03)# Example: Update Burners category

```jsoncategory = PartCategory.objects.get(name="Burners")

{category.metadata = {

    "category_code": "20",    "epcon_id": "COMB-01",

    "subcategory_code": "03"    "category_code": "01",

}    "subcategory_code": "01",

```    "range_start": 10100001,

**Example IPNs:** `20-03-00001`, `20-03-00002`, `20-03-00003`    "range_end": 10199999

}

### Product B (21)category.save()

```

#### Hardware Components (21-01)

```json### Using SQL (PostgreSQL)

{

    "category_code": "21",```sql

    "subcategory_code": "01"-- Example: Update Gas Pressure Regulators category

}UPDATE part_partcategory 

```SET metadata = '{

**Example IPNs:** `21-01-00001`, `21-01-00002`, `21-01-00003`    "epcon_id": "COMB-18",

    "category_code": "01",

#### Software Components (21-02)    "subcategory_code": "18",

```json    "range_start": 10180001,

{    "range_end": 10189999

    "category_code": "21",}'::jsonb

    "subcategory_code": "02"WHERE name = 'Gas Pressure Regulators / Governors';

}```

```

**Example IPNs:** `21-02-00001`, `21-02-00002`, `21-02-00003`## Bulk Update Script



---```python

from part.models import PartCategory

## Department-Based Organization

# Dictionary of category name -> metadata

### Engineering (30)CATEGORIES = {

    "Burners": {

#### Design Files (30-01)        "epcon_id": "COMB-01",

```json        "category_code": "01",

{        "subcategory_code": "01",

    "category_code": "30",        "range_start": 10100001,

    "subcategory_code": "01"        "range_end": 10199999

}    },

```    "Gas Pressure Regulators / Governors": {

**Example IPNs:** `30-01-00001`, `30-01-00002`, `30-01-00003`        "epcon_id": "COMB-18",

        "category_code": "01",

#### Prototypes (30-02)        "subcategory_code": "18",

```json        "range_start": 10180001,

{        "range_end": 10189999

    "category_code": "30",    },

    "subcategory_code": "02"    # Add more categories...

}}

```

**Example IPNs:** `30-02-00001`, `30-02-00002`, `30-02-00003`# Update all categories

for category_name, metadata in CATEGORIES.items():

#### Test Equipment (30-03)    try:

```json        category = PartCategory.objects.get(name=category_name)

{        category.metadata = metadata

    "category_code": "30",        category.save()

    "subcategory_code": "03"        print(f"✅ Updated: {category_name}")

}    except PartCategory.DoesNotExist:

```        print(f"❌ Not found: {category_name}")

**Example IPNs:** `30-03-00001`, `30-03-00002`, `30-03-00003`    except Exception as e:

        print(f"❌ Error updating {category_name}: {str(e)}")

### Production (31)```



#### Assembly Parts (31-01)## Notes

```json

{1. **Range Sizing**: Each subcategory gets 10,000 numbers (e.g., 10100001-10109999)

    "category_code": "31",2. **Expandability**: Ranges can be adjusted as needed (e.g., 10100001-10199999 for 100,000 numbers)

    "subcategory_code": "01"3. **Consistency**: Keep the numbering scheme consistent across categories

}4. **Documentation**: Document your numbering scheme for future reference

```

**Example IPNs:** `31-01-00001`, `31-01-00002`, `31-01-00003`## Customization



#### QA Test Parts (31-02)Modify these examples to match your EPCON numbering system:

```json

{1. Adjust `range_start` and `range_end` values

    "category_code": "31",2. Update `epcon_id` to match your category codes

    "subcategory_code": "02"3. Ensure `category_code` and `subcategory_code` align with your system

}
```
**Example IPNs:** `31-02-00001`, `31-02-00002`, `31-02-00003`

#### Packaging Materials (31-03)
```json
{
    "category_code": "31",
    "subcategory_code": "03"
}
```
**Example IPNs:** `31-03-00001`, `31-03-00002`, `31-03-00003`

---

## Custom Separator Examples

### Using Slash Separator (/)

**Plugin Setting:** `SEPARATOR = "/"`

Same metadata as above, but IPNs will look like:
- `01/01/00001` (Resistors)
- `02/01/00001` (Integrated Circuits)
- `10/01/00001` (Bolts)

### Using Underscore Separator (_)

**Plugin Setting:** `SEPARATOR = "_"`

IPNs will look like:
- `01_01_00001` (Resistors)
- `02_01_00001` (Integrated Circuits)
- `10_01_00001` (Bolts)

### Using No Separator

**Plugin Setting:** `SEPARATOR = ""`

IPNs will look like:
- `010100001` (Resistors)
- `020100001` (Integrated Circuits)
- `100100001` (Bolts)

---

## Custom Digit Length Examples

### Short Format (3 digits)

**Plugin Setting:** `DIGIT_LENGTH = 3`

IPNs will look like:
- `01-01-001` (max 999 parts per category)
- `01-01-002`
- `01-01-999`

### Long Format (8 digits)

**Plugin Setting:** `DIGIT_LENGTH = 8`

IPNs will look like:
- `01-01-00000001` (max 99,999,999 parts per category)
- `01-01-00000002`
- `01-01-99999999`

---

## How to Apply Metadata

### Using Django Shell

```python
from part.models import PartCategory

# Single category
category = PartCategory.objects.get(name="Resistors")
category.metadata = {
    "category_code": "01",
    "subcategory_code": "01"
}
category.save()

# Multiple categories
categories_config = [
    ("Resistors", "01", "01"),
    ("Capacitors", "01", "02"),
    ("Inductors", "01", "03"),
]

for name, cat_code, subcat_code in categories_config:
    cat = PartCategory.objects.get(name=name)
    cat.metadata = {
        "category_code": cat_code,
        "subcategory_code": subcat_code
    }
    cat.save()
    print(f"✓ Updated {name}")
```

### Using SQL (PostgreSQL)

```sql
-- Single category
UPDATE part_partcategory 
SET metadata = '{"category_code": "01", "subcategory_code": "01"}'::jsonb
WHERE name = 'Resistors';

-- Multiple categories
UPDATE part_partcategory SET metadata = '{"category_code": "01", "subcategory_code": "01"}'::jsonb WHERE name = 'Resistors';
UPDATE part_partcategory SET metadata = '{"category_code": "01", "subcategory_code": "02"}'::jsonb WHERE name = 'Capacitors';
UPDATE part_partcategory SET metadata = '{"category_code": "01", "subcategory_code": "03"}'::jsonb WHERE name = 'Inductors';
UPDATE part_partcategory SET metadata = '{"category_code": "02", "subcategory_code": "01"}'::jsonb WHERE name = 'Integrated Circuits';
```

---

## Tips for Choosing Codes

### Keep it Simple
- Use 2-digit codes for both category and subcategory
- Leave gaps for future expansion (01, 02, 05, 10 instead of 01, 02, 03, 04)

### Be Consistent
- Same category code across similar items
- Sequential subcategory codes within each category

### Plan Ahead
- Reserve code ranges for different purposes
- 01-09: Electronics
- 10-19: Mechanical
- 20-29: Product lines
- 30-39: Departments

### Document Your System
- Keep a master list of all codes
- Include descriptions of what each code represents
- Share with your team

---

## Verification

After setting up metadata, verify it works:

```python
from part.models import Part, PartCategory

# Get your category
category = PartCategory.objects.get(name="Resistors")

# Create a test part
part = Part.objects.create(
    category=category,
    name="Test Resistor",
    description="10K Ohm"
)

# Check the generated IPN
print(f"Generated IPN: {part.IPN}")  # Should be 01-01-00001 (or similar)
```
