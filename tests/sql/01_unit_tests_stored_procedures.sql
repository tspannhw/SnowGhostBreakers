-- ============================================================================
-- UNIT TESTS FOR STORED PROCEDURES
-- ============================================================================
-- Purpose: Test all stored procedures in the Ghost Detection System
-- Author: Ghost Detection Test Suite
-- Version: 1.0
-- ============================================================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Create test results table
CREATE OR REPLACE TABLE TEST_RESULTS (
    test_id NUMBER AUTOINCREMENT,
    test_name VARCHAR(200),
    test_category VARCHAR(50),
    status VARCHAR(20),
    error_message VARCHAR(500),
    execution_time_ms NUMBER,
    test_datetime TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (test_id)
);

-- Create test logging procedure
CREATE OR REPLACE PROCEDURE LOG_TEST_RESULT(
    test_name VARCHAR,
    test_category VARCHAR,
    status VARCHAR,
    error_msg VARCHAR,
    exec_time NUMBER
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO TEST_RESULTS (test_name, test_category, status, error_message, execution_time_ms)
    VALUES (:test_name, :test_category, :status, :error_msg, :exec_time);
    RETURN 'Test logged: ' || :test_name;
END;
$$;

-- ============================================================================
-- TEST 1: PROCESS_GHOST_EVIDENCE Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_PROCESS_GHOST_EVIDENCE()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    test_evidence_id NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Create test evidence
        INSERT INTO GHOST_EVIDENCE (
            sighting_id, ghost_id, evidence_type, file_path, 
            file_size_bytes, mime_type, capture_datetime, processing_status
        )
        SELECT 
            MIN(sighting_id), MIN(ghost_id), 'Image', '/test/evidence.jpg',
            1024000, 'image/jpeg', CURRENT_TIMESTAMP(), 'Pending'
        FROM GHOST_SIGHTINGS
        LIMIT 1;
        
        test_evidence_id := (SELECT MAX(evidence_id) FROM GHOST_EVIDENCE);
        
        -- Call procedure
        CALL PROCESS_GHOST_EVIDENCE(:test_evidence_id);
        
        -- Verify result
        SELECT processing_status INTO result_status
        FROM GHOST_EVIDENCE
        WHERE evidence_id = :test_evidence_id;
        
        IF (result_status = 'Analyzed') THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Evidence not marked as Analyzed. Status: ' || result_status;
        END IF;
        
        -- Cleanup
        DELETE FROM GHOST_EVIDENCE WHERE evidence_id = :test_evidence_id;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_PROCESS_GHOST_EVIDENCE',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': PROCESS_GHOST_EVIDENCE';
END;
$$;

-- ============================================================================
-- TEST 2: ANALYZE_SIGHTING_WITH_AI Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_ANALYZE_SIGHTING_WITH_AI()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    test_sighting_id NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    analysis_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Get existing sighting
        SELECT MIN(sighting_id) INTO test_sighting_id
        FROM GHOST_SIGHTINGS
        LIMIT 1;
        
        -- Call procedure
        CALL ANALYZE_SIGHTING_WITH_AI(:test_sighting_id);
        
        -- Verify AI analysis was created
        SELECT COUNT(*) INTO analysis_count
        FROM GHOST_AI_ANALYSIS
        WHERE sighting_id = :test_sighting_id
        AND analysis_datetime >= :start_time;
        
        IF (analysis_count > 0) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'No AI analysis created for sighting';
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_ANALYZE_SIGHTING_WITH_AI',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': ANALYZE_SIGHTING_WITH_AI';
END;
$$;

-- ============================================================================
-- TEST 3: GENERATE_GHOST_REPORT Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_GENERATE_GHOST_REPORT()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    test_ghost_id NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    report_text VARCHAR;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Get existing ghost
        SELECT MIN(ghost_id) INTO test_ghost_id
        FROM GHOSTS
        WHERE status = 'Active'
        LIMIT 1;
        
        -- Call procedure
        CALL GENERATE_GHOST_REPORT(:test_ghost_id);
        report_text := SQLROWCOUNT;
        
        -- Verify report was generated (should return VARCHAR)
        IF (report_text IS NOT NULL AND LENGTH(report_text) > 0) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Empty report generated';
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_GENERATE_GHOST_REPORT',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': GENERATE_GHOST_REPORT';
END;
$$;

-- ============================================================================
-- TEST 4: CREATE_INVESTIGATION Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_CREATE_INVESTIGATION()
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
    new_investigation_id NUMBER;
    investigation_count NUMBER;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Create test investigation
        CALL CREATE_INVESTIGATION(
            'Test Investigation',
            'Unit Test',
            'This is a test investigation'
        );
        
        -- Verify investigation was created
        SELECT MAX(investigation_id) INTO new_investigation_id
        FROM INVESTIGATIONS
        WHERE created_at >= :start_time;
        
        SELECT COUNT(*) INTO investigation_count
        FROM INVESTIGATIONS
        WHERE investigation_id = :new_investigation_id
        AND investigation_name = 'Test Investigation';
        
        IF (investigation_count = 1) THEN
            result_status := 'PASS';
            -- Cleanup
            DELETE FROM INVESTIGATIONS WHERE investigation_id = :new_investigation_id;
        ELSE
            result_status := 'FAIL';
            error_msg := 'Investigation not created correctly';
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_CREATE_INVESTIGATION',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': CREATE_INVESTIGATION';
END;
$$;

-- ============================================================================
-- TEST 5: UPDATE_GHOST_STATUS Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_UPDATE_GHOST_STATUS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    test_ghost_id NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    new_status VARCHAR;
    old_status VARCHAR;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Get test ghost
        SELECT MIN(ghost_id), status INTO test_ghost_id, old_status
        FROM GHOSTS
        WHERE status = 'Active'
        LIMIT 1;
        
        -- Update status
        CALL UPDATE_GHOST_STATUS(:test_ghost_id, 'Contained');
        
        -- Verify status changed
        SELECT status INTO new_status
        FROM GHOSTS
        WHERE ghost_id = :test_ghost_id;
        
        IF (new_status = 'Contained') THEN
            result_status := 'PASS';
            -- Restore original status
            UPDATE GHOSTS SET status = :old_status WHERE ghost_id = :test_ghost_id;
        ELSE
            result_status := 'FAIL';
            error_msg := 'Status not updated. Expected: Contained, Got: ' || new_status;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_UPDATE_GHOST_STATUS',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': UPDATE_GHOST_STATUS';
END;
$$;

-- ============================================================================
-- TEST 6: CALCULATE_THREAT_SCORE Procedure
-- ============================================================================

CREATE OR REPLACE PROCEDURE TEST_CALCULATE_THREAT_SCORE()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
    exec_time NUMBER;
    test_ghost_id NUMBER;
    result_status VARCHAR;
    error_msg VARCHAR DEFAULT NULL;
    threat_score FLOAT;
BEGIN
    start_time := CURRENT_TIMESTAMP();
    
    BEGIN
        -- Get test ghost
        SELECT MIN(ghost_id) INTO test_ghost_id
        FROM GHOSTS
        LIMIT 1;
        
        -- Calculate threat score
        CALL CALCULATE_THREAT_SCORE(:test_ghost_id);
        threat_score := SQLROWCOUNT;
        
        -- Verify score is within valid range (0-100)
        IF (threat_score >= 0 AND threat_score <= 100) THEN
            result_status := 'PASS';
        ELSE
            result_status := 'FAIL';
            error_msg := 'Invalid threat score: ' || threat_score;
        END IF;
        
    EXCEPTION
        WHEN OTHER THEN
            result_status := 'FAIL';
            error_msg := SQLERRM;
    END;
    
    end_time := CURRENT_TIMESTAMP();
    exec_time := DATEDIFF(millisecond, start_time, end_time);
    
    CALL LOG_TEST_RESULT(
        'TEST_CALCULATE_THREAT_SCORE',
        'Stored Procedure',
        :result_status,
        :error_msg,
        :exec_time
    );
    
    RETURN result_status || ': CALCULATE_THREAT_SCORE';
END;
$$;

-- ============================================================================
-- RUN ALL STORED PROCEDURE TESTS
-- ============================================================================

CREATE OR REPLACE PROCEDURE RUN_ALL_STORED_PROCEDURE_TESTS()
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
    -- Clear previous test results
    DELETE FROM TEST_RESULTS WHERE test_category = 'Stored Procedure';
    
    -- Run all tests
    CALL TEST_PROCESS_GHOST_EVIDENCE();
    CALL TEST_ANALYZE_SIGHTING_WITH_AI();
    CALL TEST_GENERATE_GHOST_REPORT();
    CALL TEST_CREATE_INVESTIGATION();
    CALL TEST_UPDATE_GHOST_STATUS();
    CALL TEST_CALCULATE_THREAT_SCORE();
    
    -- Calculate results
    SELECT COUNT(*), 
           SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END),
           SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END)
    INTO test_count, pass_count, fail_count
    FROM TEST_RESULTS
    WHERE test_category = 'Stored Procedure';
    
    result := '=== STORED PROCEDURE TESTS ===' || CHR(10) ||
              'Total Tests: ' || test_count || CHR(10) ||
              'Passed: ' || pass_count || CHR(10) ||
              'Failed: ' || fail_count || CHR(10) ||
              'Success Rate: ' || ROUND((pass_count::FLOAT / test_count) * 100, 2) || '%';
    
    RETURN result;
END;
$$;

-- Display test summary
SELECT 'Stored Procedure Unit Tests Created Successfully' as status;

