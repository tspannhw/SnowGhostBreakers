-- ============================================
-- Ghost Detection Application - Stored Procedures
-- ============================================
-- Stored procedures for ghost data processing and Cortex AI integration

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- Procedure: Process Ghost Evidence with Cortex AI
-- ============================================
CREATE OR REPLACE PROCEDURE PROCESS_GHOST_EVIDENCE(evidence_id_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    result_msg VARCHAR;
    evidence_type_var VARCHAR;
    ghost_id_var VARCHAR;
    sighting_id_var VARCHAR;
BEGIN
    -- Get evidence details
    SELECT evidence_type, ghost_id, sighting_id 
    INTO :evidence_type_var, :ghost_id_var, :sighting_id_var
    FROM GHOST_EVIDENCE 
    WHERE evidence_id = :evidence_id_param;
    
    -- Update processing status
    UPDATE GHOST_EVIDENCE 
    SET processing_status = 'Processing'
    WHERE evidence_id = :evidence_id_param;
    
    -- Process based on evidence type
    IF (evidence_type_var = 'Image') THEN
        -- Image analysis will be done via Cortex AI
        result_msg := 'Image evidence queued for Cortex Vision analysis';
    ELSEIF (evidence_type_var = 'Audio') THEN
        result_msg := 'Audio evidence queued for analysis';
    ELSEIF (evidence_type_var = 'Video') THEN
        result_msg := 'Video evidence queued for frame-by-frame analysis';
    ELSE
        result_msg := 'Evidence type processed';
    END IF;
    
    -- Update processing status to completed
    UPDATE GHOST_EVIDENCE 
    SET processing_status = 'Analyzed'
    WHERE evidence_id = :evidence_id_param;
    
    RETURN result_msg;
END;
$$;

-- ============================================
-- Procedure: Analyze Ghost Sighting with Cortex Complete
-- ============================================
CREATE OR REPLACE PROCEDURE ANALYZE_SIGHTING_WITH_AI(sighting_id_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    analysis_id_var VARCHAR;
    summary_text VARCHAR;
    threat_assessment VARCHAR;
BEGIN
    -- Generate analysis ID
    analysis_id_var := 'ANALYSIS_' || UUID_STRING();
    
    -- Get sighting description and analyze with Cortex Complete
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Analyze this ghost sighting and provide a brief threat assessment: ',
            description
        )
    ) INTO :summary_text
    FROM GHOST_SIGHTINGS
    WHERE sighting_id = :sighting_id_param;
    
    -- Extract sentiment
    SELECT SNOWFLAKE.CORTEX.SENTIMENT(description)
    INTO :threat_assessment
    FROM GHOST_SIGHTINGS
    WHERE sighting_id = :sighting_id_param;
    
    -- Insert analysis record
    INSERT INTO GHOST_AI_ANALYSIS (
        analysis_id, sighting_id, analysis_type, model_used,
        summary, sentiment_score, analysis_datetime
    )
    SELECT 
        :analysis_id_var,
        :sighting_id_param,
        'Sighting_Analysis',
        'mistral-large2',
        :summary_text,
        :threat_assessment,
        CURRENT_TIMESTAMP();
    
    RETURN 'Sighting analyzed successfully: ' || analysis_id_var;
END;
$$;

-- ============================================
-- Procedure: Generate Ghost Report
-- ============================================
CREATE OR REPLACE PROCEDURE GENERATE_GHOST_REPORT(ghost_id_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    report_text VARCHAR;
    sighting_count INT;
    ghost_name_var VARCHAR;
    ghost_type_var VARCHAR;
    threat_level_var VARCHAR;
    description_var TEXT;
    origin_story_var TEXT;
BEGIN
    -- Get sighting count
    SELECT COUNT(*) INTO :sighting_count
    FROM GHOST_SIGHTINGS
    WHERE ghost_id = :ghost_id_param;
    
    -- Get all ghost details in one query (use MAX to ensure single row even if duplicates exist)
    SELECT 
        MAX(ghost_name),
        MAX(ghost_type),
        MAX(threat_level),
        MAX(description),
        MAX(origin_story)
    INTO 
        :ghost_name_var,
        :ghost_type_var,
        :threat_level_var,
        :description_var,
        :origin_story_var
    FROM GHOSTS
    WHERE ghost_id = :ghost_id_param
    GROUP BY ghost_id;
    
    -- Generate comprehensive report using Cortex Complete
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Generate a detailed paranormal investigation report for a ghost with the following details: ',
            'Name: ', :ghost_name_var, ', ',
            'Type: ', :ghost_type_var, ', ',
            'Threat Level: ', :threat_level_var, ', ',
            'Description: ', :description_var, ', ',
            'Total Sightings: ', :sighting_count, '. ',
            'Origin: ', :origin_story_var,
            '. Provide recommendations for containment or monitoring.'
        )
    ) INTO :report_text;
    
    RETURN report_text;
END;
$$;

-- ============================================
-- Procedure: Update Ghost Threat Level
-- ============================================
CREATE OR REPLACE PROCEDURE UPDATE_GHOST_THREAT_LEVEL(ghost_id_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    avg_paranormal_level FLOAT;
    new_threat_level VARCHAR;
BEGIN
    -- Calculate average paranormal activity level from recent sightings
    SELECT AVG(paranormal_activity_level) INTO :avg_paranormal_level
    FROM GHOST_SIGHTINGS
    WHERE ghost_id = :ghost_id_param
    AND sighting_datetime > DATEADD(month, -3, CURRENT_TIMESTAMP());
    
    -- Determine threat level based on activity
    IF (:avg_paranormal_level >= 9) THEN
        new_threat_level := 'Extreme';
    ELSEIF (:avg_paranormal_level >= 7) THEN
        new_threat_level := 'High';
    ELSEIF (:avg_paranormal_level >= 4) THEN
        new_threat_level := 'Medium';
    ELSE
        new_threat_level := 'Low';
    END IF;
    
    -- Update ghost record
    UPDATE GHOSTS
    SET threat_level = :new_threat_level,
        updated_at = CURRENT_TIMESTAMP()
    WHERE ghost_id = :ghost_id_param;
    
    RETURN 'Threat level updated to: ' || new_threat_level;
END;
$$;

-- ============================================
-- Procedure: Search Similar Ghost Sightings (Using Cortex Embeddings)
-- ============================================
CREATE OR REPLACE PROCEDURE FIND_SIMILAR_SIGHTINGS(description_text VARCHAR, limit_count INT)
RETURNS TABLE (sighting_id VARCHAR, similarity_score FLOAT, description TEXT)
LANGUAGE SQL
AS
$$
BEGIN
    -- Use CTE to calculate similarity, then filter
    LET result RESULTSET := (
        WITH similarities AS (
            SELECT 
                s.sighting_id,
                VECTOR_COSINE_SIMILARITY(
                    AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', :description_text),
                    AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', s.description)
                ) as similarity_score,
                s.description
            FROM GHOST_SIGHTINGS s
        )
        SELECT 
            sighting_id,
            similarity_score,
            description
        FROM similarities
        WHERE similarity_score > 0.7
        ORDER BY similarity_score DESC
        LIMIT :limit_count
    );
    
    RETURN TABLE(result);
END;
$$;

-- ============================================
-- Procedure: Batch Process New Evidence
-- ============================================
CREATE OR REPLACE PROCEDURE BATCH_PROCESS_EVIDENCE()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    processed_count INT DEFAULT 0;
    evidence_cursor CURSOR FOR 
        SELECT evidence_id 
        FROM GHOST_EVIDENCE 
        WHERE processing_status = 'Pending';
    current_evidence_id VARCHAR;
BEGIN
    FOR record IN evidence_cursor DO
        current_evidence_id := record.evidence_id;
        CALL PROCESS_GHOST_EVIDENCE(:current_evidence_id::VARCHAR);
        processed_count := processed_count + 1;
    END FOR;
    
    RETURN 'Processed ' || processed_count || ' evidence records';
END;
$$;

-- ============================================
-- Procedure: Generate Investigation Summary
-- ============================================
CREATE OR REPLACE PROCEDURE GENERATE_INVESTIGATION_SUMMARY(investigation_id_param VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    summary_report VARCHAR;
BEGIN
    -- Generate comprehensive investigation summary using all data
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Generate an executive summary for ghost investigation case: ',
            i.case_name, '. ',
            'Lead Investigator: ', inv.investigator_name, '. ',
            'Ghost Type: ', g.ghost_type, '. ',
            'Status: ', i.status, '. ',
            'Priority: ', i.priority, '. ',
            'Evidence Count: ', i.evidence_count, '. ',
            'Case Summary: ', i.case_summary, '. ',
            'Provide key findings, threat assessment, and next steps.'
        )
    ) INTO :summary_report
    FROM INVESTIGATIONS i
    JOIN GHOSTS g ON i.ghost_id = g.ghost_id
    JOIN INVESTIGATORS inv ON i.lead_investigator_id = inv.investigator_id
    WHERE i.investigation_id = :investigation_id_param;
    
    RETURN summary_report;
END;
$$;

-- ============================================
-- Procedure: Classify Ghost Type from Description
-- ============================================
CREATE OR REPLACE PROCEDURE CLASSIFY_GHOST_TYPE(description_text VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    ghost_type_result VARCHAR;
BEGIN
    -- Use Cortex Complete to classify ghost type
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Based on this description, classify the ghost type as one of: ',
            'Apparition, Poltergeist, Shadow Entity, Orb, Ectoplasmic Entity, Residual Haunting, or Intelligent Haunting. ',
            'Description: ', :description_text, '. ',
            'Respond with only the classification type.'
        )
    ) INTO :ghost_type_result;
    
    RETURN ghost_type_result;
END;
$$;

-- ============================================
-- Function: Calculate Paranormal Activity Score
-- ============================================
CREATE OR REPLACE FUNCTION CALCULATE_ACTIVITY_SCORE(
    emf_reading FLOAT,
    temp_drop FLOAT,
    paranormal_level INT
)
RETURNS FLOAT
AS
$$
    -- Weighted scoring algorithm
    (emf_reading * 0.3) + (temp_drop * 0.2) + (paranormal_level * 5 * 0.5)
$$;

-- ============================================
-- Function: Get Ghost Risk Category
-- ============================================
CREATE OR REPLACE FUNCTION GET_RISK_CATEGORY(threat_level VARCHAR)
RETURNS VARCHAR
AS
$$
    CASE 
        WHEN threat_level = 'Extreme' THEN 'IMMEDIATE ACTION REQUIRED'
        WHEN threat_level = 'High' THEN 'High Priority Monitoring'
        WHEN threat_level = 'Medium' THEN 'Standard Monitoring'
        WHEN threat_level = 'Low' THEN 'Observation Only'
        ELSE 'Unclassified'
    END
$$;

COMMENT ON PROCEDURE PROCESS_GHOST_EVIDENCE IS 'Processes ghost evidence using Cortex AI capabilities';
COMMENT ON PROCEDURE ANALYZE_SIGHTING_WITH_AI IS 'Analyzes ghost sighting descriptions using Cortex Complete and Sentiment';
COMMENT ON PROCEDURE GENERATE_GHOST_REPORT IS 'Generates comprehensive ghost investigation reports';
COMMENT ON PROCEDURE BATCH_PROCESS_EVIDENCE IS 'Batch processes all pending evidence records';

