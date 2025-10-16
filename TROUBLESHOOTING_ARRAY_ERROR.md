# 🔧 Troubleshooting ARRAY_CONSTRUCT Error

## Issue: Still Getting ARRAY_CONSTRUCT Error

If you're still seeing:
```
Invalid expression [ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid')] in VALUES clause
```

After the fix was applied, try these steps:

---

## ✅ Step 1: Verify File is Updated

Check that your local file has been updated with the fix:

```bash
# Check if the fix is present (should show "SELECT * FROM VALUES")
grep -A 2 "INSERT INTO TAXONOMY_ATTRIBUTES" sql/08_business_vocabulary.sql
```

**Expected output:**
```sql
INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, ...)
SELECT * FROM VALUES              <-- This line is KEY
('ATTR_001', 'Opacity Level', ..., ARRAY_CONSTRUCT(...), ...),
```

**If you see:**
```sql
INSERT INTO TAXONOMY_ATTRIBUTES (...) VALUES   <-- WRONG! Old syntax
('ATTR_001', 'Opacity Level', ..., ARRAY_CONSTRUCT(...), ...),
```

Then your file wasn't updated. Refresh it or re-apply the changes.

---

## ✅ Step 2: Test the Fix Independently

Run the test file to verify the syntax works:

```sql
-- Run this first to test
!source sql/TEST_ARRAY_FIX.sql
```

Or copy the contents of `TEST_ARRAY_FIX.sql` into a worksheet and run it.

**If the test passes:** The syntax is correct, problem is elsewhere  
**If the test fails:** Something else is wrong with your Snowflake setup

---

## ✅ Step 3: Check File for Hidden Characters

Sometimes copy-paste can introduce hidden characters:

```bash
# Check for any weird characters
cat -A sql/08_business_vocabulary.sql | grep "TAXONOMY_ATTRIBUTES" -A 5
```

---

## ✅ Step 4: Manual Fix

If the automatic fix didn't work, manually edit the file:

### Find this section (around line 280):

**BEFORE:**
```sql
INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, attribute_category, data_type, valid_values, measurement_unit, description, mandatory) VALUES
('ATTR_001', 'Opacity Level', 'Physical', 'Enumeration', 
 ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid'), NULL,
 'Degree of visual solidity of the entity', FALSE),
...
('ATTR_010', 'Mobility Range', 'Physical', 'Enumeration',
 ARRAY_CONSTRUCT('Location-Bound', 'Limited-Range', 'Free-Roaming', 'Dimensional'), NULL,
 'Geographic restriction of entity movement', TRUE);
```

### Change to:

**AFTER:**
```sql
INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, attribute_category, data_type, valid_values, measurement_unit, description, mandatory)
SELECT * FROM VALUES
('ATTR_001', 'Opacity Level', 'Physical', 'Enumeration', 
 ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid'), NULL,
 'Degree of visual solidity of the entity', FALSE),
...
('ATTR_010', 'Mobility Range', 'Physical', 'Enumeration',
 ARRAY_CONSTRUCT('Location-Bound', 'Limited-Range', 'Free-Roaming', 'Dimensional'), NULL,
 'Geographic restriction of entity movement', TRUE)
AS t(attribute_id, attribute_name, attribute_category, data_type, valid_values, measurement_unit, description, mandatory);
```

**Key Changes:**
1. Remove `VALUES` from first line
2. Add `SELECT * FROM VALUES` on new line (line 281)
3. Add `AS t(column_names)` after last row (line 316)
4. Make sure last row has NO semicolon before `AS t`

---

## ✅ Step 5: Check for Multiple Errors

The error might be from a DIFFERENT section. Check all three sections:

```bash
# Check all INSERT statements with ARRAY_CONSTRUCT
grep -n "INSERT INTO.*SELECT \* FROM VALUES" sql/08_business_vocabulary.sql
```

Should show:
- Line 92: BUSINESS_VOCABULARY (Ghost Types)
- Line 136: BUSINESS_VOCABULARY (Threat Assessment)
- Line 160: BUSINESS_VOCABULARY (Equipment)
- Line 280: TAXONOMY_ATTRIBUTES

If any are missing the `SELECT * FROM VALUES`, that's your problem!

---

## ✅ Step 6: Run in Parts

Instead of running the whole file, run it in sections:

### Section 1: Tables Only
```sql
-- Lines 1-83: Create tables
```

### Section 2: Business Vocabulary - Ghost Types
```sql
-- Lines 90-133: First vocabulary INSERT
```

### Section 3: Business Vocabulary - Threat Assessment
```sql
-- Lines 135-157: Second vocabulary INSERT
```

### Section 4: Business Vocabulary - Equipment
```sql
-- Lines 159-181: Third vocabulary INSERT
```

### Section 5: Taxonomy Attributes
```sql
-- Lines 280-316: Taxonomy INSERT
```

This will tell you EXACTLY which section has the error.

---

## ✅ Step 7: Alternative - Use Simple Arrays

If all else fails, use literal array syntax:

**Change from:**
```sql
ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid')
```

**To:**
```sql
['Transparent', 'Translucent', 'Semi-Solid', 'Solid']::ARRAY
```

**Full example:**
```sql
INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, valid_values)
SELECT * FROM VALUES
('ATTR_001', 'Opacity Level', ['Transparent', 'Translucent', 'Semi-Solid', 'Solid']::ARRAY)
AS t(attribute_id, attribute_name, valid_values);
```

---

## 🔍 Debug: Exact Line Number

If you know the exact line number of the error:

```bash
# Show context around the error line
sed -n '280,320p' sql/08_business_vocabulary.sql | cat -n
```

Then manually inspect that section.

---

## 📞 Still Not Working?

### Check Snowflake Version

```sql
SELECT CURRENT_VERSION();
```

The `SELECT * FROM VALUES` pattern should work in all recent Snowflake versions, but if you're on a very old version, you might need to use a workaround.

### Alternative Pattern (for older Snowflake)

```sql
-- Create temp table first
CREATE OR REPLACE TEMPORARY TABLE temp_taxonomy AS
SELECT 
    'ATTR_001' AS attribute_id,
    'Opacity Level' AS attribute_name,
    ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid') AS valid_values,
    'Physical' AS attribute_category,
    'Enumeration' AS data_type,
    NULL AS measurement_unit,
    'Degree of visual solidity' AS description,
    FALSE AS mandatory
UNION ALL
SELECT 'ATTR_002', 'Manifestation Frequency', 
    ARRAY_CONSTRUCT('Rare', 'Occasional', 'Frequent', 'Constant'),
    'Temporal', 'Enumeration', NULL, 'How often entity manifests', TRUE
-- ... continue for all rows

-- Then insert from temp table
INSERT INTO TAXONOMY_ATTRIBUTES 
SELECT * FROM temp_taxonomy;
```

---

## ✅ Verification Query

After successful insert, verify with:

```sql
-- Check data loaded
SELECT COUNT(*) FROM TAXONOMY_ATTRIBUTES;
-- Should return 10

-- Check arrays
SELECT 
    attribute_name,
    valid_values,
    ARRAY_SIZE(valid_values) AS value_count
FROM TAXONOMY_ATTRIBUTES
WHERE valid_values IS NOT NULL;
-- Should show arrays for ATTR_001, 002, 003, 009, 010

-- Show first attribute details
SELECT 
    attribute_name,
    valid_values,
    valid_values[0] AS first_value,
    valid_values[1] AS second_value
FROM TAXONOMY_ATTRIBUTES
WHERE attribute_id = 'ATTR_001';
-- Should show: 'Opacity Level', ['Transparent', 'Translucent', ...], 'Transparent', 'Translucent'
```

---

## 📝 Summary Checklist

- [ ] File contains `SELECT * FROM VALUES` (not just `VALUES`)
- [ ] File contains `AS t(column_names)` at the end
- [ ] No semicolon before `AS t(...)`
- [ ] All parentheses are balanced
- [ ] All commas are correct
- [ ] Test file (`TEST_ARRAY_FIX.sql`) passes
- [ ] Snowflake version is recent
- [ ] No hidden characters in file

---

**If all checklist items pass and it still doesn't work, there may be a Snowflake configuration or permissions issue.**

Contact your Snowflake administrator or check query history for the exact error:

```sql
SELECT 
    query_text,
    error_message,
    error_code
FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
WHERE error_message LIKE '%ARRAY_CONSTRUCT%'
ORDER BY start_time DESC
LIMIT 1;
```

