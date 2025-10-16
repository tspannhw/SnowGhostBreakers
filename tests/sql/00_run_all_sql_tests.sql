-- ============================================================================
-- MASTER SQL TEST RUNNER
-- ============================================================================
-- Purpose: Run all SQL tests and generate comprehensive report
-- Author: Ghost Detection Test Suite
-- Version: 1.0
-- ============================================================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Display test banner
SELECT '
╔══════════════════════════════════════════════════════════════════════════╗
║                     GHOST DETECTION SYSTEM                               ║
║                   COMPREHENSIVE TEST SUITE                               ║
║                         SQL Tests v1.0                                   ║
╚══════════════════════════════════════════════════════════════════════════╝
' as banner;

-- Clear previous test results
TRUNCATE TABLE IF EXISTS TEST_RESULTS;

SELECT 'Cleared previous test results' as status;
SELECT '
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 1: STORED PROCEDURE UNIT TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
' as phase;

-- Run stored procedure tests
CALL RUN_ALL_STORED_PROCEDURE_TESTS();

-- Display detailed results
SELECT 
    '📊 Stored Procedure Test Results:' as summary;

SELECT 
    test_name,
    status,
    CONCAT(execution_time_ms, ' ms') as execution_time,
    COALESCE(error_message, 'N/A') as error_details
FROM TEST_RESULTS
WHERE test_category = 'Stored Procedure'
ORDER BY test_datetime DESC;

SELECT '
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE 2: SCHEMA INTEGRATION TESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
' as phase;

-- Run integration tests
CALL RUN_ALL_INTEGRATION_TESTS();

-- Display detailed results
SELECT 
    '📊 Integration Test Results:' as summary;

SELECT 
    test_name,
    status,
    CONCAT(execution_time_ms, ' ms') as execution_time,
    COALESCE(error_message, 'N/A') as error_details
FROM TEST_RESULTS
WHERE test_category = 'Schema Validation'
ORDER BY test_datetime DESC;

SELECT '
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPREHENSIVE TEST SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
' as summary_header;

-- Overall statistics
SELECT 
    COUNT(*) as total_tests,
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed,
    ROUND((SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END)::FLOAT / COUNT(*)) * 100, 2) as success_rate_percent,
    ROUND(AVG(execution_time_ms), 2) as avg_execution_time_ms,
    ROUND(SUM(execution_time_ms) / 1000.0, 2) as total_execution_time_sec
FROM TEST_RESULTS;

-- Results by category
SELECT 
    '📊 Results by Test Category:' as breakdown;

SELECT 
    test_category,
    COUNT(*) as total_tests,
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed,
    ROUND((SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END)::FLOAT / COUNT(*)) * 100, 2) as success_rate
FROM TEST_RESULTS
GROUP BY test_category
ORDER BY test_category;

-- Failed tests detail
SELECT 
    '❌ Failed Tests Detail:' as failed_tests_header;

SELECT 
    test_name,
    test_category,
    error_message,
    test_datetime
FROM TEST_RESULTS
WHERE status = 'FAIL'
ORDER BY test_datetime DESC;

-- Performance analysis
SELECT 
    '⚡ Performance Analysis:' as performance_header;

SELECT 
    test_name,
    CONCAT(execution_time_ms, ' ms') as execution_time,
    CASE 
        WHEN execution_time_ms < 100 THEN '🟢 Fast'
        WHEN execution_time_ms < 1000 THEN '🟡 Moderate'
        ELSE '🔴 Slow'
    END as performance_rating
FROM TEST_RESULTS
ORDER BY execution_time_ms DESC
LIMIT 10;

-- Test coverage summary
SELECT 
    '📈 Test Coverage Summary:' as coverage_header;

SELECT 
    'Stored Procedures Tested' as metric,
    COUNT(DISTINCT test_name) as count
FROM TEST_RESULTS
WHERE test_category = 'Stored Procedure'
UNION ALL
SELECT 
    'Schema Components Tested' as metric,
    COUNT(DISTINCT test_name) as count
FROM TEST_RESULTS
WHERE test_category = 'Schema Validation'
UNION ALL
SELECT 
    'Total Test Assertions' as metric,
    COUNT(*) as count
FROM TEST_RESULTS;

-- Final status
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM TEST_RESULTS WHERE status = 'FAIL') = 0 
        THEN '
╔══════════════════════════════════════════════════════════════════════════╗
║                       ✅ ALL TESTS PASSED! ✅                           ║
║                                                                          ║
║              Ghost Detection System is fully validated                  ║
║                   Ready for production deployment                       ║
╚══════════════════════════════════════════════════════════════════════════╝
'
        ELSE '
╔══════════════════════════════════════════════════════════════════════════╗
║                     ⚠️  SOME TESTS FAILED  ⚠️                          ║
║                                                                          ║
║         Please review failed tests above and address issues             ║
╚══════════════════════════════════════════════════════════════════════════╝
'
    END as final_status;

-- Export test results (optional)
-- CREATE OR REPLACE TABLE TEST_RESULTS_ARCHIVE AS
-- SELECT *, CURRENT_TIMESTAMP() as archive_datetime
-- FROM TEST_RESULTS;

SELECT 'Test execution completed. Results saved in TEST_RESULTS table.' as completion_message;

