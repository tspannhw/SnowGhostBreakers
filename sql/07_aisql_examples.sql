-- ============================================
-- Ghost Detection Application - AI SQL Examples
-- ============================================
-- Advanced examples of AI-powered SQL queries using Snowflake Cortex

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- 1. INTELLIGENT GHOST CLASSIFICATION
-- ============================================

-- Automatically classify and tag ghosts based on behavior patterns
WITH ghost_behavior AS (
    SELECT 
        g.ghost_id,
        g.ghost_name,
        g.description,
        COUNT(s.sighting_id) as sighting_frequency,
        AVG(s.paranormal_activity_level) as avg_activity,
        AVG(s.emf_reading) as avg_emf,
        AVG(s.temperature_celsius) as avg_temp,
        LISTAGG(DISTINCT s.evidence_type, ', ') as evidence_types
    FROM GHOSTS g
    LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
    GROUP BY g.ghost_id, g.ghost_name, g.description
)
SELECT 
    ghost_id,
    ghost_name,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Classify this paranormal entity and provide a behavior profile: ',
            'Name: ', ghost_name, '. ',
            'Description: ', description, '. ',
            'Activity metrics: ',
            'Sightings: ', sighting_frequency, ', ',
            'Avg Activity Level: ', avg_activity, '/10, ',
            'Avg EMF: ', avg_emf, ' mG, ',
            'Avg Temperature: ', avg_temp, '°C. ',
            'Evidence types: ', evidence_types, '. ',
            'Provide: 1) Entity classification, 2) Behavior pattern, ',
            '3) Threat assessment, 4) Recommended containment strategy.'
        )
    ) as ai_classification
FROM ghost_behavior
WHERE description IS NOT NULL;

-- ============================================
-- 2. PREDICTIVE SIGHTING ANALYSIS
-- ============================================

-- Predict likely sighting locations and times using AI analysis
WITH sighting_patterns AS (
    SELECT 
        location_name,
        EXTRACT(HOUR FROM sighting_datetime) as hour_of_day,
        EXTRACT(DOW FROM sighting_datetime) as day_of_week,
        COUNT(*) as occurrence_count,
        AVG(paranormal_activity_level) as avg_activity,
        LISTAGG(DISTINCT ghost_id, ', ') as ghost_ids
    FROM GHOST_SIGHTINGS
    GROUP BY location_name, hour_of_day, day_of_week
    HAVING COUNT(*) >= 2
)
SELECT 
    location_name,
    hour_of_day,
    day_of_week,
    occurrence_count,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Analyze this paranormal activity pattern and predict future occurrences: ',
            'Location: ', location_name, '. ',
            'Time: ', hour_of_day, ':00 hours, ',
            'Day: ', CASE day_of_week 
                WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday'
                WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday' 
                WHEN 5 THEN 'Friday' WHEN 6 THEN 'Saturday' END, '. ',
            'Historical occurrences: ', occurrence_count, '. ',
            'Average activity: ', avg_activity, '/10. ',
            'Provide prediction of next likely occurrence and recommended monitoring times.'
        )
    ) as prediction
FROM sighting_patterns
ORDER BY occurrence_count DESC
LIMIT 10;

-- ============================================
-- 3. MULTI-MODAL EVIDENCE CORRELATION
-- ============================================

-- Correlate different types of evidence to build comprehensive picture
WITH evidence_summary AS (
    SELECT 
        s.sighting_id,
        s.location_name,
        s.sighting_datetime,
        g.ghost_name,
        s.description as sighting_description,
        COUNT(DISTINCT e.evidence_id) as evidence_count,
        LISTAGG(DISTINCT e.evidence_type, ', ') as evidence_types,
        MAX(a.summary) as ai_analysis_summary,
        AVG(a.confidence_score) as avg_confidence
    FROM GHOST_SIGHTINGS s
    JOIN GHOSTS g ON s.ghost_id = g.ghost_id
    LEFT JOIN GHOST_EVIDENCE e ON s.sighting_id = e.sighting_id
    LEFT JOIN GHOST_AI_ANALYSIS a ON s.sighting_id = a.sighting_id
    GROUP BY s.sighting_id, s.location_name, s.sighting_datetime, 
             g.ghost_name, s.description
    HAVING COUNT(DISTINCT e.evidence_id) >= 2
)
SELECT 
    sighting_id,
    location_name,
    ghost_name,
    evidence_count,
    evidence_types,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Synthesize multiple evidence sources into a coherent analysis: ',
            'Ghost: ', ghost_name, '. ',
            'Location: ', location_name, '. ',
            'Witness description: ', sighting_description, '. ',
            'Evidence types available: ', evidence_types, '. ',
            'Prior AI analysis: ', ai_analysis_summary, '. ',
            'AI confidence: ', avg_confidence, '. ',
            'Provide integrated assessment combining all evidence sources.'
        )
    ) as integrated_analysis
FROM evidence_summary;

-- ============================================
-- 4. SEMANTIC SEARCH FOR SIMILAR INCIDENTS
-- ============================================

-- Find similar ghost encounters using semantic embeddings
CREATE OR REPLACE FUNCTION FIND_SIMILAR_INCIDENTS(query_text STRING)
RETURNS TABLE (
    sighting_id STRING,
    similarity_score FLOAT,
    location STRING,
    description STRING,
    ghost_name STRING
)
AS
$$
    WITH query_embedding AS (
        SELECT SNOWFLAKE.CORTEX.AI_EMBED(
            'snowflake-arctic-embed-l-v2.0-8k',
            query_text
        ) as embedding
    ),
    sighting_embeddings AS (
        SELECT 
            s.sighting_id,
            s.location_name,
            s.description,
            g.ghost_name,
            SNOWFLAKE.CORTEX.AI_EMBED(
                'snowflake-arctic-embed-l-v2.0-8k',
                s.description
            ) as embedding
        FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
        JOIN GHOST_DETECTION.APP.GHOSTS g ON s.ghost_id = g.ghost_id
        WHERE s.description IS NOT NULL
    )
    SELECT 
        se.sighting_id,
        VECTOR_COSINE_SIMILARITY(qe.embedding, se.embedding) as similarity,
        se.location_name,
        se.description,
        se.ghost_name
    FROM sighting_embeddings se, query_embedding qe
    WHERE VECTOR_COSINE_SIMILARITY(qe.embedding, se.embedding) > 0.7
    ORDER BY similarity DESC
    LIMIT 10
$$;

-- Use the function
SELECT * FROM TABLE(FIND_SIMILAR_INCIDENTS(
    'Translucent figure floating near old books with cold sensation'
));

-- ============================================
-- 5. AUTOMATED THREAT LEVEL ADJUSTMENT
-- ============================================

-- Use AI to recommend threat level changes based on recent activity
WITH recent_activity AS (
    SELECT 
        g.ghost_id,
        g.ghost_name,
        g.ghost_type,
        g.threat_level as current_threat,
        COUNT(s.sighting_id) as sightings_last_30days,
        AVG(s.paranormal_activity_level) as avg_recent_activity,
        MAX(s.paranormal_activity_level) as max_recent_activity,
        SUM(CASE WHEN s.verified THEN 1 ELSE 0 END) as verified_sightings,
        COUNT(DISTINCT s.location_name) as location_spread
    FROM GHOSTS g
    LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
    WHERE s.sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())
       OR s.sighting_id IS NULL
    GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level
)
SELECT 
    ghost_id,
    ghost_name,
    current_threat,
    sightings_last_30days,
    avg_recent_activity,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Assess if threat level should be adjusted: ',
            'Ghost: ', ghost_name, ' (', ghost_type, '). ',
            'Current threat level: ', current_threat, '. ',
            'Recent activity (30 days): ',
            'Sightings: ', sightings_last_30days, ', ',
            'Avg activity: ', avg_recent_activity, '/10, ',
            'Peak activity: ', max_recent_activity, '/10, ',
            'Verified sightings: ', verified_sightings, ', ',
            'Location spread: ', location_spread, ' locations. ',
            'Should threat level change? Respond with: ',
            'UPGRADE to [level], DOWNGRADE to [level], or MAINTAIN [current]. ',
            'Then provide brief justification.'
        )
    ) as threat_recommendation
FROM recent_activity
WHERE sightings_last_30days > 0 OR current_threat IN ('High', 'Extreme');

-- ============================================
-- 6. INTELLIGENT INVESTIGATION PRIORITIZATION
-- ============================================

-- Use AI to prioritize which cases need immediate attention
WITH case_metrics AS (
    SELECT 
        i.investigation_id,
        i.case_name,
        i.priority as current_priority,
        i.status,
        g.ghost_type,
        g.threat_level,
        DATEDIFF(day, i.start_date, CURRENT_DATE()) as days_open,
        i.evidence_count,
        COUNT(DISTINCT s.sighting_id) as related_sightings,
        MAX(s.sighting_datetime) as last_sighting,
        AVG(s.paranormal_activity_level) as avg_activity
    FROM INVESTIGATIONS i
    JOIN GHOSTS g ON i.ghost_id = g.ghost_id
    LEFT JOIN GHOST_SIGHTINGS s ON i.ghost_id = s.ghost_id
        AND s.sighting_datetime >= i.start_date
    WHERE i.status IN ('Open', 'In_Progress')
    GROUP BY i.investigation_id, i.case_name, i.priority, i.status,
             g.ghost_type, g.threat_level, i.start_date, i.evidence_count
)
SELECT 
    investigation_id,
    case_name,
    current_priority,
    threat_level,
    days_open,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Provide case prioritization recommendation: ',
            'Case: ', case_name, '. ',
            'Current priority: ', current_priority, '. ',
            'Threat level: ', threat_level, '. ',
            'Ghost type: ', ghost_type, '. ',
            'Days open: ', days_open, '. ',
            'Evidence collected: ', evidence_count, ' items. ',
            'Related sightings: ', related_sightings, '. ',
            'Avg activity: ', avg_activity, '/10. ',
            'Days since last sighting: ', DATEDIFF(day, last_sighting, CURRENT_DATE()), '. ',
            'Should priority be adjusted? Provide: ',
            '1) Recommended priority (Critical/High/Medium/Low), ',
            '2) Urgency score (1-10), ',
            '3) Specific next actions, ',
            '4) Resource requirements.'
        )
    ) as prioritization_analysis
FROM case_metrics
ORDER BY 
    CASE threat_level
        WHEN 'Extreme' THEN 1 WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3 ELSE 4
    END,
    days_open DESC;

-- ============================================
-- 7. ANOMALY DETECTION IN PATTERNS
-- ============================================

-- Detect unusual patterns that might indicate new ghost types or behaviors
WITH baseline_metrics AS (
    SELECT 
        ghost_type,
        AVG(emf_reading) as avg_emf,
        STDDEV(emf_reading) as stddev_emf,
        AVG(temperature_celsius) as avg_temp,
        STDDEV(temperature_celsius) as stddev_temp,
        AVG(paranormal_activity_level) as avg_activity,
        STDDEV(paranormal_activity_level) as stddev_activity
    FROM GHOST_SIGHTINGS s
    JOIN GHOSTS g ON s.ghost_id = g.ghost_id
    GROUP BY ghost_type
),
anomalous_sightings AS (
    SELECT 
        s.sighting_id,
        s.location_name,
        g.ghost_name,
        g.ghost_type,
        s.emf_reading,
        s.temperature_celsius,
        s.paranormal_activity_level,
        s.description,
        CASE 
            WHEN ABS(s.emf_reading - b.avg_emf) > 2 * b.stddev_emf THEN TRUE
            WHEN ABS(s.temperature_celsius - b.avg_temp) > 2 * b.stddev_temp THEN TRUE
            WHEN ABS(s.paranormal_activity_level - b.avg_activity) > 2 * b.stddev_activity THEN TRUE
            ELSE FALSE
        END as is_anomaly,
        b.avg_emf,
        b.avg_temp,
        b.avg_activity
    FROM GHOST_SIGHTINGS s
    JOIN GHOSTS g ON s.ghost_id = g.ghost_id
    JOIN baseline_metrics b ON g.ghost_type = b.ghost_type
    WHERE s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
)
SELECT 
    sighting_id,
    location_name,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Analyze this anomalous paranormal reading: ',
            'Ghost: ', ghost_name, ' (', ghost_type, '). ',
            'Location: ', location_name, '. ',
            'Description: ', description, '. ',
            'Readings - EMF: ', emf_reading, ' mG (baseline: ', avg_emf, '), ',
            'Temperature: ', temperature_celsius, '°C (baseline: ', avg_temp, '), ',
            'Activity: ', paranormal_activity_level, '/10 (baseline: ', avg_activity, '). ',
            'What could explain these anomalous readings? ',
            'Is this: 1) Normal variation, 2) Ghost behavior change, ',
            '3) New ghost type, 4) Environmental factors, or 5) Equipment malfunction?'
        )
    ) as anomaly_analysis
FROM anomalous_sightings
WHERE is_anomaly = TRUE;

-- ============================================
-- 8. NATURAL LANGUAGE QUERY INTERFACE
-- ============================================

-- Create a stored procedure for natural language queries
CREATE OR REPLACE PROCEDURE ASK_GHOST_DATABASE(question STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    context STRING;
    ai_response STRING;
    total_ghosts INT;
    active_ghosts INT;
    total_sightings INT;
    open_investigations INT;
    ghost_types_list STRING;
    most_active_location STRING;
    extreme_threat_ghosts STRING;
BEGIN
    -- Build context from database statistics
    -- Get basic counts
    SELECT COUNT(*) INTO :total_ghosts FROM GHOSTS;
    SELECT COUNT(*) INTO :active_ghosts FROM GHOSTS WHERE status = 'Active';
    SELECT COUNT(*) INTO :total_sightings FROM GHOST_SIGHTINGS;
    SELECT COUNT(*) INTO :open_investigations FROM INVESTIGATIONS WHERE status IN ('Open', 'In_Progress');
    
    -- Get ghost types
    SELECT LISTAGG(DISTINCT ghost_type, ', ') INTO :ghost_types_list FROM GHOSTS;
    
    -- Get most active location
    SELECT location_name INTO :most_active_location
    FROM GHOST_SIGHTINGS 
    GROUP BY location_name 
    ORDER BY COUNT(*) DESC 
    LIMIT 1;
    
    -- Get extreme threat ghosts
    SELECT LISTAGG(ghost_name, ', ') INTO :extreme_threat_ghosts
    FROM GHOSTS 
    WHERE threat_level = 'Extreme';
    
    -- Build context string
    context := CONCAT(
        'Ghost Detection Database Context: ',
        'Total Ghosts: ', :total_ghosts, ', ',
        'Active Ghosts: ', :active_ghosts, ', ',
        'Total Sightings: ', :total_sightings, ', ',
        'Open Investigations: ', :open_investigations, '. ',
        'Ghost Types: ', COALESCE(:ghost_types_list, 'None'), '. ',
        'Most Active Location: ', COALESCE(:most_active_location, 'Unknown'), '. ',
        'Highest Threat Ghosts: ', COALESCE(:extreme_threat_ghosts, 'None'), '. '
    );
    
    -- Get AI response
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            :context,
            ' User Question: ', :question,
            '. Provide a clear, concise answer based on the database context.'
        )
    ) INTO :ai_response;
    
    RETURN ai_response;
END;
$$;

-- Example usage
CALL ASK_GHOST_DATABASE('Which ghost is the most dangerous right now?');
CALL ASK_GHOST_DATABASE('Where should we focus our investigations?');
CALL ASK_GHOST_DATABASE('What patterns do you see in the recent sightings?');

-- ============================================
-- 9. AUTOMATED REPORT GENERATION
-- ============================================

-- Generate comprehensive weekly reports
CREATE OR REPLACE PROCEDURE GENERATE_WEEKLY_REPORT()
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    weekly_summary STRING;
    report_prompt STRING;
    week_end_date DATE;
    sightings_count INT;
    new_ghosts_count INT;
    cases_opened_count INT;
    cases_closed_count INT;
    active_locations STRING;
BEGIN
    -- Get statistics with simple queries
    week_end_date := CURRENT_DATE();
    
    SELECT COUNT(*) INTO :sightings_count
    FROM GHOST_SIGHTINGS 
    WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP());
    
    SELECT COUNT(*) INTO :new_ghosts_count
    FROM GHOSTS 
    WHERE first_detected_date >= DATEADD(day, -7, CURRENT_TIMESTAMP());
    
    SELECT COUNT(*) INTO :cases_opened_count
    FROM INVESTIGATIONS 
    WHERE start_date >= DATEADD(day, -7, CURRENT_DATE());
    
    SELECT COUNT(*) INTO :cases_closed_count
    FROM INVESTIGATIONS 
    WHERE end_date >= DATEADD(day, -7, CURRENT_DATE());
    
    -- Get most active locations
    SELECT LISTAGG(location_name, ', ') WITHIN GROUP (ORDER BY cnt DESC) 
    INTO :active_locations
    FROM (
        SELECT location_name, COUNT(*) as cnt
        FROM GHOST_SIGHTINGS
        WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
        GROUP BY location_name
        ORDER BY cnt DESC
        LIMIT 3
    );
    
    -- Build report prompt using string concatenation with proper type casting
    report_prompt := CONCAT(
        'Generate a comprehensive weekly paranormal activity report: ',
        'Week ending: ', TO_CHAR(:week_end_date), '. ',
        'Total sightings this week: ', TO_CHAR(:sightings_count), '. ',
        'New ghosts detected: ', TO_CHAR(:new_ghosts_count), '. ',
        'Cases opened: ', TO_CHAR(:cases_opened_count), '. ',
        'Cases closed: ', TO_CHAR(:cases_closed_count), '. ',
        'Most active locations: ', COALESCE(:active_locations, 'None'), '. ',
        'Provide: Executive Summary, Key Incidents, Threat Assessment, ',
        'Resource Allocation Recommendations, Outlook for Next Week.'
    );
    
    -- Generate AI report
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        :report_prompt
    ) INTO :weekly_summary;
    
    RETURN :weekly_summary;
END;
$$;

-- Generate report
CALL GENERATE_WEEKLY_REPORT();

COMMENT ON PROCEDURE ASK_GHOST_DATABASE IS 'Natural language interface to query ghost database using Cortex AI';
COMMENT ON PROCEDURE GENERATE_WEEKLY_REPORT IS 'Automated weekly report generation using AI analysis';

