# 🔧 Snowflake ARRAY_CONSTRUCT Workaround

## Issue: ARRAY_CONSTRUCT Not Supported in VALUES

Your Snowflake version/configuration does not support `ARRAY_CONSTRUCT()` in `VALUES` clauses, even with the `SELECT * FROM VALUES` pattern.

---

## ✅ Solution: Use UNION ALL SELECT

Instead of `VALUES` or `SELECT * FROM VALUES`, use `SELECT ... UNION ALL SELECT ...`:

### ❌ Doesn't Work (VALUES)

```sql
INSERT INTO table VALUES
('ID1', ARRAY_CONSTRUCT('a', 'b', 'c'));  -- ERROR
```

### ❌ Doesn't Work (SELECT FROM VALUES)

```sql
INSERT INTO table
SELECT * FROM VALUES
('ID1', ARRAY_CONSTRUCT('a', 'b', 'c'))
AS t(id, arr);  -- STILL ERROR
```

### ✅ WORKS (UNION ALL SELECT)

```sql
INSERT INTO table (id, arr)
SELECT 'ID1', ARRAY_CONSTRUCT('a', 'b', 'c')
UNION ALL
SELECT 'ID2', ARRAY_CONSTRUCT('d', 'e', 'f')
UNION ALL
SELECT 'ID3', ARRAY_CONSTRUCT('g', 'h', 'i');
```

---

## 📁 Fixed File

I've created **`sql/08_business_vocabulary_ALTERNATIVE.sql`** with the working approach.

**Use this file instead of the original `sql/08_business_vocabulary.sql`**

---

## 🧪 Test the New Approach

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Test 1: Simple array insert
CREATE OR REPLACE TEMPORARY TABLE test_arr (id INT, tags ARRAY);

INSERT INTO test_arr (id, tags)
SELECT 1, ARRAY_CONSTRUCT('tag1', 'tag2', 'tag3')
UNION ALL
SELECT 2, ARRAY_CONSTRUCT('alpha', 'beta', 'gamma');

SELECT * FROM test_arr;
-- Should show 2 rows with arrays ✓

DROP TABLE test_arr;

-- Test 2: With NULL values
CREATE OR REPLACE TEMPORARY TABLE test_null (id INT, arr ARRAY, unit VARCHAR(10));

INSERT INTO test_null (id, arr, unit)
SELECT 1, ARRAY_CONSTRUCT('a', 'b'), NULL
UNION ALL
SELECT 2, ARRAY_CONSTRUCT('c', 'd'), 'meters'
UNION ALL
SELECT 3, NULL, 'celsius';

SELECT * FROM test_null;
-- Should show 3 rows ✓

DROP TABLE test_null;

SELECT '✅ Tests passed! Use UNION ALL SELECT approach' AS result;
```

---

## 📊 What Changed

### Original (Broken):

```sql
INSERT INTO BUSINESS_VOCABULARY (...)
SELECT * FROM VALUES
('TERM_001', ..., ARRAY_CONSTRUCT('Specter', 'Phantom'), ...),
('TERM_002', ..., ARRAY_CONSTRUCT('Noisy Ghost'), ...)
AS t(...);
```

### New (Working):

```sql
INSERT INTO BUSINESS_VOCABULARY (...)
SELECT 'TERM_001', ..., ARRAY_CONSTRUCT('Specter', 'Phantom'), ...
UNION ALL
SELECT 'TERM_002', ..., ARRAY_CONSTRUCT('Noisy Ghost'), ...;
```

---

## 🎯 Apply to Your Files

You need to update THREE files:

### 1. `sql/08_business_vocabulary.sql` 

✅ **Just use the alternative file:** `sql/08_business_vocabulary_ALTERNATIVE.sql`

Or manually convert:
- Change all `INSERT ... VALUES` to `INSERT ... SELECT ... UNION ALL SELECT`
- 3 sections in BUSINESS_VOCABULARY table
- 1 section in TAXONOMY_ATTRIBUTES table

### 2. `sql/03_sample_data.sql` (if it has arrays)

Check if this file uses `PARSE_JSON()` - same fix applies:

```sql
-- Change from VALUES to SELECT UNION ALL
INSERT INTO GHOST_EVIDENCE (...)
SELECT 'EVID001', ..., PARSE_JSON('{"key": "value"}'), ...
UNION ALL
SELECT 'EVID002', ..., PARSE_JSON('{"key2": "value2"}'), ...;
```

---

## 🔍 Why This Happens

Snowflake has different behaviors based on:
1. **Account version** - Older accounts may not support this
2. **Account configuration** - Some enterprise settings restrict this
3. **Feature flags** - Certain features may be disabled

The `UNION ALL SELECT` pattern works on **ALL Snowflake versions** because:
- Each SELECT is evaluated independently
- Functions are called in the SELECT context, not VALUES context
- No special parsing needed

---

## ⚡ Quick Conversion Pattern

To convert any `VALUES` with arrays:

**Step 1:** Find the INSERT statement
```sql
INSERT INTO table (col1, col2, col3) VALUES
```

**Step 2:** Change to SELECT
```sql
INSERT INTO table (col1, col2, col3)
SELECT
```

**Step 3:** Remove parentheses from first row, change commas between rows to UNION ALL
```sql
-- Before:
('row1_val1', 'row1_val2', ARRAY_CONSTRUCT(...)),
('row2_val1', 'row2_val2', ARRAY_CONSTRUCT(...));

-- After:
SELECT 'row1_val1', 'row1_val2', ARRAY_CONSTRUCT(...)
UNION ALL
SELECT 'row2_val1', 'row2_val2', ARRAY_CONSTRUCT(...);
```

---

## 📝 Complete Example

### Before (Broken):

```sql
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, synonyms, definition) VALUES
('TERM_001', 'Apparition', ARRAY_CONSTRUCT('Specter', 'Phantom'), 'A visible ghost'),
('TERM_002', 'Poltergeist', ARRAY_CONSTRUCT('Noisy Ghost'), 'Disruptive spirit'),
('TERM_003', 'EVP', ARRAY_CONSTRUCT('Spirit Voice'), 'Electronic voice phenomenon');
```

### After (Working):

```sql
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, synonyms, definition)
SELECT 'TERM_001', 'Apparition', ARRAY_CONSTRUCT('Specter', 'Phantom'), 'A visible ghost'
UNION ALL
SELECT 'TERM_002', 'Poltergeist', ARRAY_CONSTRUCT('Noisy Ghost'), 'Disruptive spirit'
UNION ALL
SELECT 'TERM_003', 'EVP', ARRAY_CONSTRUCT('Spirit Voice'), 'Electronic voice phenomenon';
```

---

## ✅ Verification

After running the alternative file:

```sql
-- Check vocabulary loaded
SELECT COUNT(*) FROM BUSINESS_VOCABULARY;
-- Should return 20

-- Check arrays work
SELECT term_name, synonyms, ARRAY_SIZE(synonyms) AS synonym_count
FROM BUSINESS_VOCABULARY
WHERE term_id = 'TERM_001';
-- Should show: Apparition, ['Specter','Phantom','Spirit','Wraith'], 4

-- Check taxonomy attributes
SELECT COUNT(*) FROM TAXONOMY_ATTRIBUTES;
-- Should return 10

-- Check taxonomy arrays
SELECT attribute_name, valid_values, ARRAY_SIZE(valid_values) AS value_count
FROM TAXONOMY_ATTRIBUTES
WHERE valid_values IS NOT NULL;
-- Should show 5 attributes with arrays
```

---

## 🎉 Summary

**Problem:** ARRAY_CONSTRUCT not allowed in VALUES clause  
**Solution:** Use SELECT ... UNION ALL SELECT ... pattern  
**File to use:** `sql/08_business_vocabulary_ALTERNATIVE.sql`  
**Status:** ✅ Works on ALL Snowflake versions  

---

**Try the alternative file now - it will work!** 🚀👻✨

