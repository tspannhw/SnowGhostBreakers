# 📞 Stored Procedure Calling Guide

## ❌ The Error

```
Argument types of function 'PROCESS_GHOST_EVIDENCE' must be specified.
```

**Cause:** Snowflake requires explicit type specification when calling stored procedures in certain contexts.

---

## ✅ The Fix

### Issue Location
**File:** `sql/04_stored_procedures.sql`  
**Line:** 241 in `BATCH_PROCESS_EVIDENCE` procedure

### Before (BROKEN):
```sql
CALL PROCESS_GHOST_EVIDENCE(:current_evidence_id);
-- ❌ ERROR: Argument types must be specified
```

### After (FIXED):
```sql
CALL PROCESS_GHOST_EVIDENCE(:current_evidence_id::VARCHAR);
-- ✅ Works: Type explicitly cast to VARCHAR
```

---

## 📋 How to Call All Procedures

### 1. PROCESS_GHOST_EVIDENCE

**Signature:**
```sql
PROCEDURE PROCESS_GHOST_EVIDENCE(evidence_id_param VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call with string literal
CALL PROCESS_GHOST_EVIDENCE('EVID001');

-- With explicit type
CALL PROCESS_GHOST_EVIDENCE('EVID001'::VARCHAR);

-- From variable (requires type cast)
CALL PROCESS_GHOST_EVIDENCE(:evidence_id::VARCHAR);

-- Named parameter syntax
CALL PROCESS_GHOST_EVIDENCE(evidence_id_param => 'EVID001');
```

**Example:**
```sql
-- Process a specific evidence record
CALL PROCESS_GHOST_EVIDENCE('EVID001');
```

---

### 2. ANALYZE_SIGHTING_WITH_AI

**Signature:**
```sql
PROCEDURE ANALYZE_SIGHTING_WITH_AI(sighting_id_param VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call
CALL ANALYZE_SIGHTING_WITH_AI('SIGHT001');

-- With variable
CALL ANALYZE_SIGHTING_WITH_AI(:sighting_id::VARCHAR);

-- Named parameter
CALL ANALYZE_SIGHTING_WITH_AI(sighting_id_param => 'SIGHT001');
```

**Example:**
```sql
-- Analyze a sighting using Cortex AI
CALL ANALYZE_SIGHTING_WITH_AI('SIGHT003');
```

---

### 3. GENERATE_GHOST_REPORT

**Signature:**
```sql
PROCEDURE GENERATE_GHOST_REPORT(ghost_id_param VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call
CALL GENERATE_GHOST_REPORT('GH001');

-- With variable
CALL GENERATE_GHOST_REPORT(:ghost_id::VARCHAR);

-- Capture return value
LET report VARCHAR := (CALL GENERATE_GHOST_REPORT('GH001'));
```

**Example:**
```sql
-- Generate comprehensive ghost report
CALL GENERATE_GHOST_REPORT('GH002');
```

---

### 4. UPDATE_GHOST_THREAT_LEVEL

**Signature:**
```sql
PROCEDURE UPDATE_GHOST_THREAT_LEVEL(ghost_id_param VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call
CALL UPDATE_GHOST_THREAT_LEVEL('GH001');

-- With variable
CALL UPDATE_GHOST_THREAT_LEVEL(:ghost_id::VARCHAR);
```

**Example:**
```sql
-- Recalculate and update threat level based on recent activity
CALL UPDATE_GHOST_THREAT_LEVEL('GH004');
```

---

### 5. FIND_SIMILAR_SIGHTINGS

**Signature:**
```sql
PROCEDURE FIND_SIMILAR_SIGHTINGS(description_text VARCHAR, limit_count INT)
RETURNS TABLE (sighting_id VARCHAR, similarity_score FLOAT, description TEXT)
```

**Correct Calls:**
```sql
-- Direct call with literals
CALL FIND_SIMILAR_SIGHTINGS('shadow entity', 5);

-- With explicit types
CALL FIND_SIMILAR_SIGHTINGS('shadow entity'::VARCHAR, 5::INT);

-- With variables
CALL FIND_SIMILAR_SIGHTINGS(:search_text::VARCHAR, :limit::INT);

-- Named parameters
CALL FIND_SIMILAR_SIGHTINGS(
    description_text => 'floating objects',
    limit_count => 10
);
```

**Example:**
```sql
-- Find similar sightings
CALL FIND_SIMILAR_SIGHTINGS('cold temperature drop with EMF spike', 5);
```

---

### 6. BATCH_PROCESS_EVIDENCE

**Signature:**
```sql
PROCEDURE BATCH_PROCESS_EVIDENCE()
```

**Correct Calls:**
```sql
-- No parameters needed
CALL BATCH_PROCESS_EVIDENCE();
```

**Example:**
```sql
-- Process all pending evidence
CALL BATCH_PROCESS_EVIDENCE();
```

---

### 7. GENERATE_INVESTIGATION_SUMMARY

**Signature:**
```sql
PROCEDURE GENERATE_INVESTIGATION_SUMMARY(investigation_id_param VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call
CALL GENERATE_INVESTIGATION_SUMMARY('CASE001');

-- With variable
CALL GENERATE_INVESTIGATION_SUMMARY(:case_id::VARCHAR);
```

**Example:**
```sql
-- Generate executive summary for an investigation
CALL GENERATE_INVESTIGATION_SUMMARY('CASE003');
```

---

### 8. CLASSIFY_GHOST_TYPE

**Signature:**
```sql
PROCEDURE CLASSIFY_GHOST_TYPE(description_text VARCHAR)
```

**Correct Calls:**
```sql
-- Direct call
CALL CLASSIFY_GHOST_TYPE('Translucent figure in Victorian clothing');

-- With variable
CALL CLASSIFY_GHOST_TYPE(:description::VARCHAR);

-- Capture result
LET ghost_type VARCHAR := (CALL CLASSIFY_GHOST_TYPE('Shadow in corner'));
```

**Example:**
```sql
-- Classify ghost type from description
CALL CLASSIFY_GHOST_TYPE('Green glowing entity consuming food');
```

---

## 🎯 Key Rules

### Rule 1: Direct Literals Usually Work
```sql
-- These usually work without explicit types
CALL PROCEDURE_NAME('string_value');
CALL PROCEDURE_NAME('string', 123);
```

### Rule 2: Variables Need Type Casts
```sql
-- Always cast variables
DECLARE my_var VARCHAR;
my_var := 'value';
CALL PROCEDURE_NAME(:my_var::VARCHAR);  -- ✅ Correct
CALL PROCEDURE_NAME(:my_var);           -- ❌ May fail
```

### Rule 3: Inside Other Procedures, Always Cast
```sql
-- When calling from another procedure
CREATE PROCEDURE caller()
AS
$$
DECLARE
    id VARCHAR := 'ID001';
BEGIN
    -- Always use type cast
    CALL other_procedure(:id::VARCHAR);  -- ✅ Correct
    CALL other_procedure(:id);           -- ❌ May fail
END;
$$;
```

### Rule 4: Use Named Parameters for Clarity
```sql
-- Named parameters are explicit and clear
CALL PROCEDURE_NAME(
    param1 => 'value1',
    param2 => 123
);
```

---

## 🔍 Debugging Procedure Calls

### Check Procedure Signature
```sql
-- See all procedures
SHOW PROCEDURES LIKE 'PROCESS%';

-- Describe specific procedure
DESCRIBE PROCEDURE PROCESS_GHOST_EVIDENCE(VARCHAR);
```

### Test with Different Call Methods

#### Method 1: Direct Literal
```sql
CALL PROCESS_GHOST_EVIDENCE('EVID001');
```

#### Method 2: Explicit Type Cast
```sql
CALL PROCESS_GHOST_EVIDENCE('EVID001'::VARCHAR);
```

#### Method 3: Named Parameter
```sql
CALL PROCESS_GHOST_EVIDENCE(evidence_id_param => 'EVID001');
```

#### Method 4: With Variable
```sql
SET my_id = 'EVID001';
CALL PROCESS_GHOST_EVIDENCE($my_id::VARCHAR);
```

---

## 📊 Common Patterns

### Pattern 1: Loop Through Records
```sql
DECLARE
    my_cursor CURSOR FOR SELECT id FROM my_table;
    current_id VARCHAR;
BEGIN
    FOR record IN my_cursor DO
        current_id := record.id;
        -- Always cast when calling from loop
        CALL my_procedure(:current_id::VARCHAR);
    END FOR;
END;
```

### Pattern 2: Conditional Calls
```sql
IF (condition) THEN
    CALL procedure1(:param::VARCHAR);
ELSE
    CALL procedure2(:param::VARCHAR);
END IF;
```

### Pattern 3: Capturing Return Values
```sql
DECLARE
    result VARCHAR;
BEGIN
    -- For procedures that return values
    result := (CALL my_procedure('param'::VARCHAR));
    RETURN result;
END;
```

---

## ⚠️ Common Mistakes

### ❌ Mistake 1: No Type Cast with Variables
```sql
DECLARE id VARCHAR := 'ID001';
CALL procedure(:id);  -- ERROR
```

**Fix:**
```sql
CALL procedure(:id::VARCHAR);  -- ✅
```

### ❌ Mistake 2: Wrong Type
```sql
CALL procedure(123);  -- If procedure expects VARCHAR
```

**Fix:**
```sql
CALL procedure('123');  -- ✅
-- or
CALL procedure(123::VARCHAR);  -- ✅
```

### ❌ Mistake 3: Missing Parameters
```sql
CALL procedure_with_two_params('value1');  -- ERROR: Missing param
```

**Fix:**
```sql
CALL procedure_with_two_params('value1', 'value2');  -- ✅
```

### ❌ Mistake 4: Wrong Parameter Order
```sql
-- If signature is: procedure(id VARCHAR, name VARCHAR)
CALL procedure('John', 'ID001');  -- Wrong order!
```

**Fix:**
```sql
CALL procedure('ID001', 'John');  -- ✅ Correct order
-- or use named parameters
CALL procedure(name => 'John', id => 'ID001');  -- ✅ Order doesn't matter
```

---

## 🧪 Complete Test Script

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Test 1: Process Evidence
CALL PROCESS_GHOST_EVIDENCE('EVID001');
SELECT 'Test 1 passed' as status;

-- Test 2: Analyze Sighting
CALL ANALYZE_SIGHTING_WITH_AI('SIGHT001');
SELECT 'Test 2 passed' as status;

-- Test 3: Generate Report
CALL GENERATE_GHOST_REPORT('GH001');
SELECT 'Test 3 passed' as status;

-- Test 4: Update Threat Level
CALL UPDATE_GHOST_THREAT_LEVEL('GH001');
SELECT 'Test 4 passed' as status;

-- Test 5: Find Similar Sightings
CALL FIND_SIMILAR_SIGHTINGS('shadow entity', 5);
SELECT 'Test 5 passed' as status;

-- Test 6: Batch Process
CALL BATCH_PROCESS_EVIDENCE();
SELECT 'Test 6 passed' as status;

-- Test 7: Investigation Summary
CALL GENERATE_INVESTIGATION_SUMMARY('CASE001');
SELECT 'Test 7 passed' as status;

-- Test 8: Classify Ghost Type
CALL CLASSIFY_GHOST_TYPE('Green entity consuming food');
SELECT 'Test 8 passed' as status;

SELECT '✅ All procedure calls successful!' as final_status;
```

---

## 📚 Reference: All Procedure Signatures

```sql
-- Evidence Processing
PROCEDURE PROCESS_GHOST_EVIDENCE(evidence_id_param VARCHAR)

-- AI Analysis
PROCEDURE ANALYZE_SIGHTING_WITH_AI(sighting_id_param VARCHAR)
PROCEDURE CLASSIFY_GHOST_TYPE(description_text VARCHAR)

-- Report Generation
PROCEDURE GENERATE_GHOST_REPORT(ghost_id_param VARCHAR)
PROCEDURE GENERATE_INVESTIGATION_SUMMARY(investigation_id_param VARCHAR)

-- Data Management
PROCEDURE UPDATE_GHOST_THREAT_LEVEL(ghost_id_param VARCHAR)
PROCEDURE BATCH_PROCESS_EVIDENCE()

-- Search & Similarity
PROCEDURE FIND_SIMILAR_SIGHTINGS(description_text VARCHAR, limit_count INT)
RETURNS TABLE (sighting_id VARCHAR, similarity_score FLOAT, description TEXT)
```

---

## ✅ Summary

### Key Takeaways:

1. ✅ **Always cast variables to type** when calling procedures
2. ✅ **Use `::VARCHAR` or `::INT`** for explicit type casting
3. ✅ **Named parameters** work great for clarity
4. ✅ **Test procedures** with different call methods
5. ✅ **Check signatures** with `DESCRIBE PROCEDURE`

### Fixed in This Update:
- ✅ `BATCH_PROCESS_EVIDENCE` now casts variable to VARCHAR
- ✅ All procedure calls properly typed
- ✅ Complete calling guide created

---

**File Fixed:** `sql/04_stored_procedures.sql`  
**Line Fixed:** 241  
**Status:** ✅ **Ready to Use**  
**Date:** October 16, 2025

