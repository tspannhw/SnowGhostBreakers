# ✅ SQL Fixes Applied - Sample Data

## 🔧 Issues Fixed

### 1. ❌ PARSE_JSON in VALUES Clause Error

**Error Message:**
```
Invalid expression [PARSE_JSON('{"camera": "Full Spectrum", ...}')] in VALUES clause
```

**Problem:**  
`PARSE_JSON()` function cannot be used directly in a `VALUES` clause in Snowflake.

**Solution:**  
Changed from `INSERT INTO ... VALUES` to `INSERT INTO ... SELECT * FROM VALUES ... AS t()`

---

## 📝 What Was Changed

### Before (BROKEN):
```sql
-- This doesn't work!
INSERT INTO GHOST_EVIDENCE (evidence_id, sighting_id, ghost_id, evidence_type, 
                            file_path, capture_datetime, metadata, processing_status)
VALUES
    ('EVID001', 'SIGHT001', 'GH001', 'Image', '@GHOST_IMAGES_STAGE/library_ghost_001.jpg',
     '2024-10-01 18:45:30', PARSE_JSON('{"camera": "Full Spectrum", "exposure": "1/60s"}'), 'Analyzed');
     --                     ^^^^^^^^^ ERROR: Can't use functions in VALUES
```

### After (FIXED):
```sql
-- This works!
INSERT INTO GHOST_EVIDENCE (evidence_id, sighting_id, ghost_id, evidence_type, 
                            file_path, capture_datetime, metadata, processing_status)
SELECT * FROM VALUES
    ('EVID001', 'SIGHT001', 'GH001', 'Image', '@GHOST_IMAGES_STAGE/library_ghost_001.jpg',
     '2024-10-01 18:45:30'::TIMESTAMP_NTZ, PARSE_JSON('{"camera": "Full Spectrum", "exposure": "1/60s"}'), 'Analyzed')
AS t(evidence_id, sighting_id, ghost_id, evidence_type, file_path, capture_datetime, metadata, processing_status);
--   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Column aliases match table columns
```

---

## 📊 Fixed Sections

### 1. GHOST_EVIDENCE Table Inserts
**Lines 73-91** - Fixed 5 evidence records with JSON metadata

### 2. SENSOR_READINGS Table Inserts
**Lines 123-135** - Fixed 3 sensor readings with JSON raw_data

---

## 🎯 Key Pattern to Remember

### ❌ Don't Use:
```sql
-- Functions in VALUES don't work
INSERT INTO table VALUES (PARSE_JSON('{}'), CURRENT_TIMESTAMP());
INSERT INTO table VALUES (ARRAY_CONSTRUCT('a', 'b'));
INSERT INTO table VALUES (OBJECT_CONSTRUCT('key', 'value'));
```

### ✅ Use This Instead:
```sql
-- SELECT FROM VALUES works with functions
INSERT INTO table
SELECT * FROM VALUES
    (PARSE_JSON('{}'), CURRENT_TIMESTAMP()),
    (PARSE_JSON('{}'), CURRENT_TIMESTAMP())
AS t(json_col, timestamp_col);
```

### ✅ Or Even Simpler:
```sql
-- For VARIANT columns, just use strings (auto-parsed)
INSERT INTO table (id, metadata) VALUES
    (1, '{"key": "value"}'),  -- Snowflake auto-converts to VARIANT
    (2, '{"key": "value2"}');
```

---

## 🔍 Other Common Snowflake Patterns

### Working with JSON/VARIANT

#### Option 1: Use SELECT FROM VALUES (Most Flexible)
```sql
INSERT INTO my_table (id, json_data)
SELECT * FROM VALUES
    (1, PARSE_JSON('{"name": "Ghost", "type": "Apparition"}')),
    (2, PARSE_JSON('{"name": "Slimer", "type": "Ectoplasm"}'))
AS t(id, json_data);
```

#### Option 2: Let Snowflake Auto-Parse (Simplest)
```sql
INSERT INTO my_table (id, json_data) VALUES
    (1, '{"name": "Ghost", "type": "Apparition"}'),
    (2, '{"name": "Slimer", "type": "Ectoplasm"}');
-- Snowflake automatically converts strings to VARIANT
```

#### Option 3: Use OBJECT_CONSTRUCT (Best for Dynamic)
```sql
INSERT INTO my_table (id, json_data)
SELECT 
    id,
    OBJECT_CONSTRUCT(
        'name', ghost_name,
        'type', ghost_type,
        'threat', threat_level
    ) as json_data
FROM source_table;
```

### Working with Arrays

#### ❌ Don't Use in VALUES:
```sql
INSERT INTO table VALUES (ARRAY_CONSTRUCT('a', 'b', 'c'));  -- ERROR
```

#### ✅ Use SELECT FROM VALUES:
```sql
INSERT INTO my_table (id, tags)
SELECT * FROM VALUES
    (1, ARRAY_CONSTRUCT('ghost', 'apparition', 'friendly')),
    (2, ARRAY_CONSTRUCT('ghost', 'poltergeist', 'dangerous'))
AS t(id, tags);
```

#### ✅ Or Parse from String:
```sql
INSERT INTO my_table (id, tags) VALUES
    (1, PARSE_JSON('["ghost", "apparition", "friendly"]')),
    (2, PARSE_JSON('["ghost", "poltergeist", "dangerous"]'));
```

### Working with Timestamps

#### Best Practice: Explicit Casting
```sql
INSERT INTO my_table
SELECT * FROM VALUES
    (1, '2024-10-01 18:45:30'::TIMESTAMP_NTZ),
    (2, '2024-10-02 19:30:00'::TIMESTAMP_NTZ)
AS t(id, timestamp_col);
```

#### Or Use TO_TIMESTAMP:
```sql
INSERT INTO my_table
SELECT * FROM VALUES
    (1, TO_TIMESTAMP('2024-10-01 18:45:30')),
    (2, TO_TIMESTAMP('2024-10-02 19:30:00'))
AS t(id, timestamp_col);
```

---

## ✅ Verification

### Test the Fixed Script

```sql
-- Run the sample data script
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Execute sql/03_sample_data.sql
-- Should now complete without errors!

-- Verify the data loaded
SELECT COUNT(*) FROM GHOST_EVIDENCE;  -- Should be 5
SELECT COUNT(*) FROM SENSOR_READINGS; -- Should be 3

-- Check JSON metadata loaded correctly
SELECT 
    evidence_id,
    metadata:camera::STRING as camera,
    metadata:iso::INT as iso
FROM GHOST_EVIDENCE
WHERE evidence_id = 'EVID001';

-- Expected output:
-- EVID001 | Full Spectrum | 3200
```

---

## 📚 References

- [Snowflake INSERT Documentation](https://docs.snowflake.com/en/sql-reference/sql/insert)
- [PARSE_JSON Function](https://docs.snowflake.com/en/sql-reference/functions/parse_json)
- [VARIANT Data Type](https://docs.snowflake.com/en/sql-reference/data-types-semistructured)
- [Working with Semi-Structured Data](https://docs.snowflake.com/en/user-guide/semistructured-concepts)

---

## 🎉 Summary

✅ **Fixed:** All `PARSE_JSON()` calls in sample data  
✅ **Pattern:** Use `SELECT * FROM VALUES ... AS t()` for functions  
✅ **Benefit:** Cleaner code with proper function evaluation  
✅ **Status:** Ready to run without errors!

**File Fixed:** `sql/03_sample_data.sql`  
**Lines Modified:** 73-91 (evidence), 123-135 (sensors)  
**Date:** October 16, 2025

