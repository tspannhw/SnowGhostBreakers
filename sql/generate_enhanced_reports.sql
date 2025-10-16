-- ============================================================================
-- Generate Enhanced Ghost Reports with Cortex AI
-- ============================================================================
-- Creates detailed investigation reports for active ghosts using Cortex Complete
-- and stores them in a dedicated table

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================================================
-- Step 1: Create table to store enhanced reports
-- ============================================================================
CREATE TABLE IF NOT EXISTS GHOST_ENHANCED_REPORTS (
    report_id VARCHAR(50) PRIMARY KEY DEFAULT UUID_STRING(),
    ghost_id VARCHAR(50),
    ghost_name VARCHAR(200),
    ghost_type VARCHAR(100),
    enhanced_description TEXT,
    generated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    model_used VARCHAR(50) DEFAULT 'mistral-large2',
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);

COMMENT ON TABLE GHOST_ENHANCED_REPORTS IS 'AI-generated detailed investigation reports for ghosts';

-- ============================================================================
-- Step 2: Insert enhanced reports for active ghosts
-- ============================================================================
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Write a detailed paranormal investigation report for: ',
            ghost_name, ' (', ghost_type, '). ',
            'Description: ', description, '. ',
            'Make it scientific and professional.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE status = 'Active'
LIMIT 5;

-- ============================================================================
-- Step 3: View the generated reports
-- ============================================================================
SELECT 
    report_id,
    ghost_name,
    ghost_type,
    LEFT(enhanced_description, 200) as report_preview,
    generated_at
FROM GHOST_ENHANCED_REPORTS
ORDER BY generated_at DESC;

-- ============================================================================
-- Step 4: Get full report for a specific ghost
-- ============================================================================
SELECT 
    ghost_name,
    ghost_type,
    enhanced_description as full_report,
    generated_at
FROM GHOST_ENHANCED_REPORTS
WHERE ghost_id = 'GH001'  -- Change to specific ghost_id
ORDER BY generated_at DESC
LIMIT 1;

-- ============================================================================
-- Optional: Generate reports for ALL active ghosts (not just 5)
-- ============================================================================
/*
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Write a detailed paranormal investigation report for: ',
            ghost_name, ' (', ghost_type, '). ',
            'Description: ', description, '. ',
            'Threat Level: ', threat_level, '. ',
            'Make it scientific and professional.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE status = 'Active'
AND ghost_id NOT IN (SELECT ghost_id FROM GHOST_ENHANCED_REPORTS);  -- Avoid duplicates
*/

-- ============================================================================
-- Optional: Regenerate report for a specific ghost
-- ============================================================================
/*
-- Delete old report
DELETE FROM GHOST_ENHANCED_REPORTS WHERE ghost_id = 'GH001';

-- Generate new report
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Write a detailed paranormal investigation report for: ',
            ghost_name, ' (', ghost_type, '). ',
            'Description: ', description, '. ',
            'Origin: ', origin_story, '. ',
            'Threat Level: ', threat_level, '. ',
            'Make it scientific and professional with recommendations.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE ghost_id = 'GH001';
*/

SELECT '✅ Enhanced reports generated successfully!' as status;

