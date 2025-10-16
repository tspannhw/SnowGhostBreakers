-- ============================================
-- Ghost Detection Application - Cortex AI Integration
-- ============================================
-- SQL functions and examples using Snowflake Cortex AI

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- Create Cortex Search Service for Ghost Sightings
-- ============================================

-- Note: Cortex Search requires proper setup and permissions
-- Uncomment and configure based on your Snowflake account setup

/*
CREATE OR REPLACE CORTEX SEARCH SERVICE ghost_sightings_search
ON description
WAREHOUSE = COMPUTE_WH
TARGET_LAG = '1 minute'
AS (
    SELECT 
        sighting_id,
        ghost_id,
        location_name,
        description,
        sighting_datetime,
        paranormal_activity_level
    FROM GHOST_SIGHTINGS
);
*/

-- ============================================
-- Example Queries Using Cortex Complete
-- ============================================

-- Generate comprehensive ghost descriptions
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

-- ============================================
-- Sentiment Analysis on Sighting Descriptions
-- ============================================

-- Analyze the emotional tone of sighting reports
SELECT 
    sighting_id,
    location_name,
    witness_name,
    description,
    SNOWFLAKE.CORTEX.SENTIMENT(description) as sentiment_score,
    CASE 
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(description) > 0.3 THEN '😊 Positive'
        WHEN SNOWFLAKE.CORTEX.SENTIMENT(description) < -0.3 THEN '😨 Negative (Fearful)'
        ELSE '😐 Neutral'
    END as sentiment_category
FROM GHOST_SIGHTINGS
ORDER BY sighting_datetime DESC
LIMIT 10;

-- ============================================
-- Text Classification for Evidence Types
-- ============================================

-- Classify sighting descriptions to verify reported evidence types
SELECT 
    sighting_id,
    evidence_type as reported_type,
    description,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Classify this paranormal evidence as one of: Visual, Audio, EMF, Temperature, Multiple. ',
            'Evidence: ', description, '. ',
            'Respond with only the classification.'
        )
    ) as ai_classified_type
FROM GHOST_SIGHTINGS
LIMIT 10;

-- ============================================
-- Extract Entities from Sighting Descriptions
-- ============================================

-- Extract key information from descriptions
SELECT 
    sighting_id,
    description,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Extract key entities from this ghost sighting: ',
            description,
            '. List: ghost appearance, actions, environmental effects, time of day.'
        )
    ) as extracted_entities
FROM GHOST_SIGHTINGS
WHERE description IS NOT NULL
LIMIT 5;

-- ============================================
-- Summarize Multiple Sightings
-- ============================================

-- Create summary of all sightings for a specific ghost
SELECT 
    g.ghost_name,
    g.ghost_type,
    COUNT(s.sighting_id) as total_sightings,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Summarize these ghost sightings into a comprehensive profile. ',
            'Ghost: ', g.ghost_name, ' (', g.ghost_type, '). ',
            'Sightings: ', LISTAGG(s.description, ' | ') WITHIN GROUP (ORDER BY s.sighting_datetime),
            '. Provide a behavioral profile and threat assessment.'
        )
    ) as ghost_profile
FROM GHOSTS g
JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE g.ghost_id = 'GH001'
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type;

-- ============================================
-- Translate Descriptions (Multi-language Support)
-- ============================================

-- Translate sighting descriptions for international teams
SELECT 
    sighting_id,
    description as original_description,
    SNOWFLAKE.CORTEX.TRANSLATE(description, 'en', 'es') as spanish_translation,
    SNOWFLAKE.CORTEX.TRANSLATE(description, 'en', 'fr') as french_translation,
    SNOWFLAKE.CORTEX.TRANSLATE(description, 'en', 'de') as german_translation
FROM GHOST_SIGHTINGS
LIMIT 3;

-- ============================================
-- Q&A System Using Cortex Complete
-- ============================================

-- Answer questions about ghost data
WITH ghost_context AS (
    SELECT 
        CONCAT(
            'Ghost Database: ',
            'Total Ghosts: ', COUNT(DISTINCT g.ghost_id), ', ',
            'Active Ghosts: ', SUM(CASE WHEN g.status = 'Active' THEN 1 ELSE 0 END), ', ',
            'Total Sightings: ', COUNT(s.sighting_id), ', ',
            'Extreme Threats: ', SUM(CASE WHEN g.threat_level = 'Extreme' THEN 1 ELSE 0 END)
        ) as context
    FROM GHOSTS g
    LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
)
SELECT 
    context,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            context,
            '. Question: What is the current threat situation and which ghosts should we prioritize? ',
            'Provide specific recommendations.'
        )
    ) as ai_response
FROM ghost_context;

-- ============================================
-- Anomaly Detection in Sensor Readings
-- ============================================

-- Identify unusual sensor patterns
SELECT 
    s.sighting_id,
    s.location_name,
    s.emf_reading,
    s.temperature_celsius,
    s.paranormal_activity_level,
    CASE 
        WHEN s.emf_reading > (SELECT AVG(emf_reading) + 2 * STDDEV(emf_reading) FROM GHOST_SIGHTINGS)
            THEN '⚠️ EMF Anomaly Detected'
        WHEN s.temperature_celsius < (SELECT AVG(temperature_celsius) - 2 * STDDEV(temperature_celsius) FROM GHOST_SIGHTINGS)
            THEN '❄️ Temperature Anomaly Detected'
        WHEN s.paranormal_activity_level >= 9
            THEN '🔥 Extreme Activity Detected'
        ELSE '✅ Normal Range'
    END as anomaly_status,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Analyze this sensor reading for paranormal activity: ',
            'EMF: ', s.emf_reading, ' mG, ',
            'Temperature: ', s.temperature_celsius, '°C, ',
            'Activity Level: ', s.paranormal_activity_level, '/10. ',
            'What does this indicate about the paranormal entity?'
        )
    ) as ai_analysis
FROM GHOST_SIGHTINGS s
WHERE s.emf_reading > 10 OR s.temperature_celsius < 15 OR s.paranormal_activity_level >= 8
ORDER BY s.sighting_datetime DESC
LIMIT 10;

-- ============================================
-- Generate Investigation Recommendations
-- ============================================

-- AI-powered recommendations for each investigation
SELECT 
    i.investigation_id,
    i.case_name,
    i.priority,
    g.ghost_type,
    g.threat_level,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Provide tactical recommendations for this ghost investigation: ',
            'Case: ', i.case_name, '. ',
            'Ghost Type: ', g.ghost_type, '. ',
            'Threat Level: ', g.threat_level, '. ',
            'Priority: ', i.priority, '. ',
            'Status: ', i.status, '. ',
            'Include equipment recommendations, team size, and safety protocols.'
        )
    ) as investigation_recommendations
FROM INVESTIGATIONS i
JOIN GHOSTS g ON i.ghost_id = g.ghost_id
WHERE i.status IN ('Open', 'In_Progress')
ORDER BY 
    CASE i.priority
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Medium' THEN 3
        WHEN 'Low' THEN 4
    END;

-- ============================================
-- Vector Embeddings for Similarity Search
-- ============================================

-- Create embeddings for ghost descriptions (for similarity search)
-- Note: This is an example - you would typically store these embeddings

SELECT 
    ghost_id,
    ghost_name,
    description,
    SNOWFLAKE.CORTEX.EMBED_TEXT_768(
        'snowflake-arctic-embed-l',
        description
    ) as description_embedding
FROM GHOSTS
LIMIT 5;

-- Find similar ghost sightings based on description
-- This example finds sightings similar to a specific description
WITH target_sighting AS (
    SELECT 
        SNOWFLAKE.CORTEX.EMBED_TEXT_768(
            'snowflake-arctic-embed-l',
            'Translucent figure moving books in library'
        ) as target_embedding
)
SELECT 
    s.sighting_id,
    s.location_name,
    s.description,
    VECTOR_COSINE_SIMILARITY(
        (SELECT target_embedding FROM target_sighting),
        SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-l', s.description)
    ) as similarity_score
FROM GHOST_SIGHTINGS s
ORDER BY similarity_score DESC
LIMIT 10;

-- ============================================
-- Batch Update Ghost Descriptions with AI Enhancement
-- ============================================

-- Enhance all ghost descriptions using AI (run carefully in production)
/*
UPDATE GHOSTS
SET description = SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    CONCAT(
        'Enhance this ghost description to be more detailed and scientific: ',
        description,
        '. Keep it factual and professional.'
    )
)
WHERE description IS NOT NULL
AND LENGTH(description) < 200;
*/

-- ============================================
-- Real-time Threat Assessment
-- ============================================

-- Create a view that provides real-time AI threat assessments
CREATE OR REPLACE VIEW VW_REAL_TIME_THREAT_ASSESSMENT AS
SELECT 
    g.ghost_id,
    g.ghost_name,
    g.ghost_type,
    g.threat_level,
    COUNT(s.sighting_id) as recent_sightings_7days,
    AVG(s.paranormal_activity_level) as avg_recent_activity,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Assess the current threat level for this ghost: ',
            g.ghost_name, ' (', g.ghost_type, '). ',
            'Recent sightings (7 days): ', COUNT(s.sighting_id), '. ',
            'Average activity level: ', AVG(s.paranormal_activity_level), '/10. ',
            'Current classification: ', g.threat_level, '. ',
            'Should the threat level be adjusted? Provide brief assessment.'
        )
    ) as ai_threat_assessment
FROM GHOSTS g
LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
   OR s.sighting_id IS NULL
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level;

-- Query the real-time assessment
SELECT * FROM VW_REAL_TIME_THREAT_ASSESSMENT
WHERE threat_level IN ('High', 'Extreme')
ORDER BY recent_sightings_7days DESC;

COMMENT ON VIEW VW_REAL_TIME_THREAT_ASSESSMENT IS 'Real-time AI-powered threat assessment for all active ghosts';

