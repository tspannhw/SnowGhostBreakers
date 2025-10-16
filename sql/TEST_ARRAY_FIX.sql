-- ============================================
-- TEST: Verify ARRAY_CONSTRUCT Fix Works
-- ============================================
-- This test file verifies the fix for ARRAY_CONSTRUCT in VALUES clause
-- Run this BEFORE running the full sql/08_business_vocabulary.sql

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- TEST 1: Create temporary test table
-- ============================================

CREATE OR REPLACE TEMPORARY TABLE TEST_ARRAY_INSERT (
    id VARCHAR(50),
    name VARCHAR(200),
    tags ARRAY
);

-- ============================================
-- TEST 2: Try the FIXED pattern
-- ============================================

-- This should WORK
INSERT INTO TEST_ARRAY_INSERT (id, name, tags)
SELECT * FROM VALUES
('TEST_001', 'Test Item 1', ARRAY_CONSTRUCT('tag1', 'tag2', 'tag3')),
('TEST_002', 'Test Item 2', ARRAY_CONSTRUCT('alpha', 'beta', 'gamma'))
AS t(id, name, tags);

-- Verify it worked
SELECT * FROM TEST_ARRAY_INSERT;
-- Should show 2 rows with arrays

-- ============================================
-- TEST 3: Verify array contents
-- ============================================

SELECT 
    id,
    name,
    tags,
    ARRAY_SIZE(tags) AS tag_count,
    tags[0] AS first_tag
FROM TEST_ARRAY_INSERT;

-- ============================================
-- TEST 4: Test with NULL values (like TAXONOMY_ATTRIBUTES)
-- ============================================

CREATE OR REPLACE TEMPORARY TABLE TEST_TAXONOMY_ATTRIBUTES (
    attr_id VARCHAR(50),
    attr_name VARCHAR(200),
    valid_values ARRAY,
    measurement_unit VARCHAR(50),
    mandatory BOOLEAN
);

-- This matches the TAXONOMY_ATTRIBUTES structure
INSERT INTO TEST_TAXONOMY_ATTRIBUTES (attr_id, attr_name, valid_values, measurement_unit, mandatory)
SELECT * FROM VALUES
('ATTR_001', 'Opacity Level', 
 ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid'), 
 NULL, FALSE),
('ATTR_002', 'Manifestation Frequency',
 ARRAY_CONSTRUCT('Rare', 'Occasional', 'Frequent', 'Constant'), 
 NULL, TRUE),
('ATTR_003', 'Temperature',
 NULL, 
 'Celsius', FALSE)
AS t(attr_id, attr_name, valid_values, measurement_unit, mandatory);

-- Verify
SELECT * FROM TEST_TAXONOMY_ATTRIBUTES;
-- Should show 3 rows, 2 with arrays, 1 with NULL array

-- ============================================
-- TEST 5: Show array data
-- ============================================

SELECT 
    attr_name,
    valid_values,
    CASE 
        WHEN valid_values IS NULL THEN 'No values'
        ELSE 'Has ' || ARRAY_SIZE(valid_values) || ' values'
    END AS value_status
FROM TEST_TAXONOMY_ATTRIBUTES;

-- ============================================
-- TEST RESULTS
-- ============================================

SELECT 
    'Test Results' AS status,
    CASE 
        WHEN (SELECT COUNT(*) FROM TEST_ARRAY_INSERT) = 2 
         AND (SELECT COUNT(*) FROM TEST_TAXONOMY_ATTRIBUTES) = 3
        THEN '✓ ALL TESTS PASSED'
        ELSE '✗ TESTS FAILED'
    END AS result;

-- ============================================
-- If this test passes, the syntax is correct!
-- ============================================

-- Clean up
DROP TABLE IF EXISTS TEST_ARRAY_INSERT;
DROP TABLE IF EXISTS TEST_TAXONOMY_ATTRIBUTES;

SELECT '✓ Test complete. If you see this, the ARRAY_CONSTRUCT fix works!' AS message;

