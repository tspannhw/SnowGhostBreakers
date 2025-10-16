-- ============================================================================
-- INTEGRATION TESTS FOR DATABASE SCHEMA
-- ============================================================================
-- Purpose: Test database schema integrity, constraints, and relationships
-- Author: Ghost Detection Test Suite
-- Version: 1.0
-- ============================================================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================================================
-- SCHEMA VALIDATION TESTS
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_TABLE_EXISTS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    expected_tables ARRAY DEFAULT ARRAY_CONSTRUCT(
        'GHOSTS', 'GHOST_SIGHTINGS', 'GHOST_EVIDENCE', 
        'GHOST_AI_ANALYSIS', 'SENSOR_READINGS', 'INVESTIGATORS',
        'INVESTIGATIONS', 'AUDIT_LOG', 'AI_AGENTS', 'BUSINESS_VOCABULARY',
        'GHOST_ONTOLOGY', 'GHOST_TAXONOMY'
    );
    actual_count NUMBER;
    expected_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    expected_count := ARRAY_SIZE(:expected_tables);
    
    BEGIN
        SELECT COUNT(DISTINCT table_name) INTO actual_count
        FROM INFORMATION_SCHEMA.TABLES
        WHERE table_schema = 'APP'
        AND table_name IN (
            SELECT VALUE::VARCHAR
            FROM TABLE(FLATTEN(INPUT => :expected_tables))
        );
        
        IF (actual_count = expected_count) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Expected ' || expected_count || ' tables, found ' || actual_count;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_TABLE_EXISTS',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': All required tables exist';
END;
$$;

-- ============================================================================
-- TEST 2: Foreign Key Relationships
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_FOREIGN_KEY_INTEGRITY()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    orphan_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Check for orphaned sightings (no matching ghost)
        SELECT COUNT(*) INTO orphan_count
        FROM GHOST_SIGHTINGS s
        LEFT JOIN GHOSTS g ON s.ghost_id = g.ghost_id
        WHERE g.ghost_id IS NULL;
        
        IF (orphan_count > 0) THEN
            result_status := 'FAIL';
            error_msg := 'Found ' || orphan_count || ' orphaned sightings';
        ELSE
            -- Check for orphaned evidence
            SELECT COUNT(*) INTO orphan_count
            FROM GHOST_EVIDENCE e
            LEFT JOIN GHOSTS g ON e.ghost_id = g.ghost_id
            WHERE g.ghost_id IS NULL;
            
            IF (orphan_count > 0) THEN
                result_status := 'FAIL';
                error_msg := 'Found ' || orphan_count || ' orphaned evidence records';
            ELSE
                result_status := 'PASS';
            END IF;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_FOREIGN_KEY_INTEGRITY',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': Foreign key integrity check';
END;
$$;

-- ============================================================================
-- TEST 3: Data Type Validation
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_DATA_TYPE_VALIDATION()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    invalid_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Check for invalid EMF readings (should be 0-100)
        SELECT COUNT(*) INTO invalid_count
        FROM GHOST_SIGHTINGS
        WHERE emf_reading < 0 OR emf_reading > 100;
        
        IF (invalid_count > 0) THEN
            result_status := 'FAIL';
            error_msg := 'Found ' || invalid_count || ' invalid EMF readings';
        ELSE
            -- Check for invalid temperature readings (reasonable range: -50 to 150 F)
            SELECT COUNT(*) INTO invalid_count
            FROM GHOST_SIGHTINGS
            WHERE temperature < -50 OR temperature > 150;
            
            IF (invalid_count > 0) THEN
                result_status := 'FAIL';
                error_msg := 'Found ' || invalid_count || ' invalid temperature readings';
            ELSE
                result_status := 'PASS';
            END IF;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_DATA_TYPE_VALIDATION',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': Data type validation';
END;
$$;

-- ============================================================================
-- TEST 4: View Accessibility
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_VIEW_ACCESSIBILITY()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    view_count NUMBER;
    expected_views ARRAY DEFAULT ARRAY_CONSTRUCT(
        'VW_GHOST_ACTIVITY_SUMMARY',
        'VW_PARANORMAL_HOTSPOTS',
        'VW_EVIDENCE_ANALYSIS',
        'VW_ONTOLOGY_HIERARCHY'
    );
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Check if views exist
        SELECT COUNT(*) INTO view_count
        FROM INFORMATION_SCHEMA.VIEWS
        WHERE table_schema = 'APP'
        AND table_name IN (
            SELECT VALUE::VARCHAR
            FROM TABLE(FLATTEN(INPUT => :expected_views))
        );
        
        IF (view_count = ARRAY_SIZE(:expected_views)) THEN
            -- Try to query each view
            SELECT COUNT(*) FROM VW_GHOST_ACTIVITY_SUMMARY LIMIT 1;
            SELECT COUNT(*) FROM VW_PARANORMAL_HOTSPOTS LIMIT 1;
            SELECT COUNT(*) FROM VW_EVIDENCE_ANALYSIS LIMIT 1;
            SELECT COUNT(*) FROM VW_ONTOLOGY_HIERARCHY LIMIT 1;
            
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Expected ' || ARRAY_SIZE(:expected_views) || ' views, found ' || view_count;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_VIEW_ACCESSIBILITY',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': View accessibility';
END;
$$;

-- ============================================================================
-- TEST 5: Cortex AI Function Availability
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_CORTEX_AI_AVAILABILITY()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    test_result VARCHAR;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Test Cortex Complete
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            'Say "test successful" and nothing else.'
        ) INTO test_result;
        
        IF (test_result IS NOT NULL AND LENGTH(test_result) > 0) THEN
            -- Test Cortex Sentiment
            SELECT SNOWFLAKE.CORTEX.SENTIMENT('This is a test') INTO test_result;
            
            IF (test_result IS NOT NULL) THEN
                result_status := 'PASS';
            ELSE
                result_status := 'FAIL';
                error_msg := 'Cortex Sentiment not available';
            END IF;
        ELSE
            result_status := 'FAIL';
            error_msg := 'Cortex Complete not available';
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := 'Cortex AI not available: ' || SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_CORTEX_AI_AVAILABILITY',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': Cortex AI availability';
END;
$$;

-- ============================================================================
-- TEST 6: Business Vocabulary Integration
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_BUSINESS_VOCABULARY_INTEGRATION()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    vocab_count NUMBER;
    ontology_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Check business vocabulary table
        SELECT COUNT(*) INTO vocab_count
        FROM BUSINESS_VOCABULARY
        WHERE term_status = 'Active';
        
        -- Check ontology table
        SELECT COUNT(*) INTO ontology_count
        FROM GHOST_ONTOLOGY
        WHERE classification_level BETWEEN 1 AND 5;
        
        IF (vocab_count > 0 AND ontology_count > 0) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Vocabulary: ' || vocab_count || ', Ontology: ' || ontology_count;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_BUSINESS_VOCABULARY_INTEGRATION',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': Business vocabulary integration';
END;
$$;

-- ============================================================================
-- TEST 7: Agentic AI System Tables
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_AGENTIC_AI_SYSTEM()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    agent_count NUMBER;
    policy_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Check AI agents table
        SELECT COUNT(*) INTO agent_count
        FROM AI_AGENTS
        WHERE is_active = TRUE;
        
        -- Check policies table
        SELECT COUNT(*) INTO policy_count
        FROM AI_AGENT_POLICIES
        WHERE is_active = TRUE;
        
        IF (agent_count > 0 AND policy_count > 0) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Active Agents: ' || agent_count || ', Active Policies: ' || policy_count;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_AGENTIC_AI_SYSTEM',
        'Schema Validation',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': Agentic AI system';
END;
$$;

-- ============================================================================
-- RUN ALL INTEGRATION TESTS
-- ============================================================================

CREATE OR REPLACE PROCEDURE RUN_ALL_INTEGRATION_TESTS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    test_count NUMBER DEFAULT 0;
    pass_count NUMBER DEFAULT 0;
    fail_count NUMBER DEFAULT 0;
    result VARCHAR;
BEGIN
    -- Run all tests
    CALL TEST_TABLE_EXISTS();
    CALL TEST_FOREIGN_KEY_INTEGRITY();
    CALL TEST_DATA_TYPE_VALIDATION();
    CALL TEST_VIEW_ACCESSIBILITY();
    CALL TEST_CORTEX_AI_AVAILABILITY();
    CALL TEST_BUSINESS_VOCABULARY_INTEGRATION();
    CALL TEST_AGENTIC_AI_SYSTEM();
    
    -- Calculate results
    SELECT COUNT(*), 
           SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END),
           SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END)
    INTO test_count, pass_count, fail_count
    FROM TEST_RESULTS
    WHERE test_category = 'Schema Validation';
    
    result := '=== INTEGRATION TESTS ===' || CHR(10) ||
              'Total Tests: ' || test_count || CHR(10) ||
              'Passed: ' || pass_count || CHR(10) ||
              'Failed: ' || fail_count || CHR(10) ||
              'Success Rate: ' || ROUND((pass_count::FLOAT / test_count) * 100, 2) || '%';
    
    RETURN result;
END;
$$;

SELECT 'Integration Tests Created Successfully' as status;

