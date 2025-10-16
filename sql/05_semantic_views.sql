-- ============================================
-- Ghost Detection Application - Semantic Views
-- ============================================
-- Semantic views for Cortex Analyst and business intelligence

USE DATABASE GHOST_DETECTION;
USE SCHEMA ANALYTICS;

-- ============================================
-- Semantic View: Ghost Activity Dashboard
-- ============================================
CREATE OR REPLACE VIEW VW_GHOST_ACTIVITY_SUMMARY AS
SELECT 
    g.ghost_id,
    g.ghost_name,
    g.ghost_type,
    g.threat_level,
    g.status,
    g.confidence_score,
    COUNT(DISTINCT s.sighting_id) as total_sightings,
    COUNT(DISTINCT e.evidence_id) as evidence_count,
    MAX(s.sighting_datetime) as last_sighting_date,
    MIN(s.sighting_datetime) as first_sighting_date,
    DATEDIFF(day, MIN(s.sighting_datetime), MAX(s.sighting_datetime)) as activity_duration_days,
    AVG(s.paranormal_activity_level) as avg_paranormal_level,
    AVG(s.emf_reading) as avg_emf_reading,
    AVG(s.temperature_celsius) as avg_temperature,
    COUNT(DISTINCT s.location_name) as unique_locations,
    LISTAGG(DISTINCT s.location_name, ', ') as haunted_locations
FROM GHOST_DETECTION.APP.GHOSTS g
LEFT JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_EVIDENCE e ON g.ghost_id = e.ghost_id
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level, g.status, g.confidence_score;

COMMENT ON VIEW VW_GHOST_ACTIVITY_SUMMARY IS 
'Comprehensive ghost activity metrics for dashboard visualization and analysis';

-- ============================================
-- Semantic View: Investigation Performance
-- ============================================
CREATE OR REPLACE VIEW VW_INVESTIGATION_METRICS AS
SELECT 
    i.investigation_id,
    i.case_name,
    i.status,
    i.priority,
    g.ghost_name,
    g.ghost_type,
    g.threat_level,
    inv.investigator_name as lead_investigator,
    inv.specialization,
    i.start_date,
    i.end_date,
    DATEDIFF(day, i.start_date, COALESCE(i.end_date, CURRENT_DATE())) as investigation_duration_days,
    i.evidence_count,
    COUNT(DISTINCT s.sighting_id) as sighting_count,
    COUNT(DISTINCT a.analysis_id) as analysis_count,
    AVG(a.confidence_score) as avg_ai_confidence
FROM GHOST_DETECTION.APP.INVESTIGATIONS i
JOIN GHOST_DETECTION.APP.GHOSTS g ON i.ghost_id = g.ghost_id
JOIN GHOST_DETECTION.APP.INVESTIGATORS inv ON i.lead_investigator_id = inv.investigator_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_AI_ANALYSIS a ON g.ghost_id = a.ghost_id
GROUP BY 
    i.investigation_id, i.case_name, i.status, i.priority, g.ghost_name, 
    g.ghost_type, g.threat_level, inv.investigator_name, inv.specialization,
    i.start_date, i.end_date, i.evidence_count;

COMMENT ON VIEW VW_INVESTIGATION_METRICS IS 
'Investigation case metrics and performance indicators';

-- ============================================
-- Semantic View: Hotspot Analysis
-- ============================================
CREATE OR REPLACE VIEW VW_PARANORMAL_HOTSPOTS AS
SELECT 
    s.location_name,
    s.location_address,
    s.latitude,
    s.longitude,
    COUNT(DISTINCT s.sighting_id) as total_sightings,
    COUNT(DISTINCT s.ghost_id) as unique_ghosts,
    AVG(s.paranormal_activity_level) as avg_activity_level,
    AVG(s.emf_reading) as avg_emf,
    AVG(s.temperature_celsius) as avg_temperature,
    MAX(s.sighting_datetime) as most_recent_sighting,
    LISTAGG(DISTINCT g.ghost_name, ', ') WITHIN GROUP (ORDER BY g.ghost_name) as ghosts_present,
    CASE 
        WHEN AVG(s.paranormal_activity_level) >= 8 THEN 'Critical Hotspot'
        WHEN AVG(s.paranormal_activity_level) >= 6 THEN 'Active Hotspot'
        WHEN AVG(s.paranormal_activity_level) >= 4 THEN 'Moderate Activity'
        ELSE 'Low Activity'
    END as hotspot_classification
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
JOIN GHOST_DETECTION.APP.GHOSTS g ON s.ghost_id = g.ghost_id
GROUP BY s.location_name, s.location_address, s.latitude, s.longitude
HAVING COUNT(DISTINCT s.sighting_id) >= 1;

COMMENT ON VIEW VW_PARANORMAL_HOTSPOTS IS 
'Geographic analysis of paranormal activity concentration';

-- ============================================
-- Semantic View: Evidence Analysis Summary
-- ============================================
CREATE OR REPLACE VIEW VW_EVIDENCE_ANALYSIS AS
SELECT 
    e.evidence_id,
    e.evidence_type,
    e.processing_status,
    g.ghost_name,
    g.ghost_type,
    s.location_name,
    s.sighting_datetime,
    a.analysis_type,
    a.model_used,
    a.confidence_score,
    a.anomaly_detected,
    a.summary as ai_summary,
    e.capture_datetime,
    DATEDIFF(minute, e.capture_datetime, a.analysis_datetime) as processing_time_minutes
FROM GHOST_DETECTION.APP.GHOST_EVIDENCE e
JOIN GHOST_DETECTION.APP.GHOSTS g ON e.ghost_id = g.ghost_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON e.sighting_id = s.sighting_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_AI_ANALYSIS a ON e.evidence_id = a.evidence_id;

COMMENT ON VIEW VW_EVIDENCE_ANALYSIS IS 
'Evidence processing and AI analysis results';

-- ============================================
-- Semantic View: Investigator Performance
-- ============================================
CREATE OR REPLACE VIEW VW_INVESTIGATOR_STATS AS
SELECT 
    inv.investigator_id,
    inv.investigator_name,
    inv.specialization,
    inv.experience_years,
    inv.cases_solved,
    COUNT(DISTINCT i.investigation_id) as active_cases,
    AVG(DATEDIFF(day, i.start_date, COALESCE(i.end_date, CURRENT_DATE()))) as avg_case_duration,
    SUM(CASE WHEN i.priority = 'Critical' THEN 1 ELSE 0 END) as critical_cases,
    SUM(CASE WHEN i.status = 'Closed' THEN 1 ELSE 0 END) as closed_cases,
    COUNT(DISTINCT s.sighting_id) as total_sightings_investigated
FROM GHOST_DETECTION.APP.INVESTIGATORS inv
LEFT JOIN GHOST_DETECTION.APP.INVESTIGATIONS i ON inv.investigator_id = i.lead_investigator_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON i.ghost_id = s.ghost_id
WHERE inv.active_status = TRUE
GROUP BY 
    inv.investigator_id, inv.investigator_name, inv.specialization, 
    inv.experience_years, inv.cases_solved;

COMMENT ON VIEW VW_INVESTIGATOR_STATS IS 
'Investigator performance metrics and workload analysis';

-- ============================================
-- Semantic View: Time Series Analysis
-- ============================================
CREATE OR REPLACE VIEW VW_ACTIVITY_TIMELINE AS
SELECT 
    DATE_TRUNC('day', s.sighting_datetime) as activity_date,
    COUNT(DISTINCT s.sighting_id) as daily_sightings,
    COUNT(DISTINCT s.ghost_id) as unique_ghosts_active,
    AVG(s.paranormal_activity_level) as avg_daily_activity,
    AVG(s.emf_reading) as avg_daily_emf,
    SUM(CASE WHEN s.verified = TRUE THEN 1 ELSE 0 END) as verified_sightings,
    COUNT(DISTINCT s.location_name) as locations_affected
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
GROUP BY DATE_TRUNC('day', s.sighting_datetime)
ORDER BY activity_date DESC;

COMMENT ON VIEW VW_ACTIVITY_TIMELINE IS 
'Time series analysis of paranormal activity patterns';

-- ============================================
-- Semantic View: Threat Assessment Matrix
-- ============================================
CREATE OR REPLACE VIEW VW_THREAT_MATRIX AS
SELECT 
    g.threat_level,
    g.ghost_type,
    COUNT(DISTINCT g.ghost_id) as ghost_count,
    AVG(g.confidence_score) as avg_confidence,
    COUNT(DISTINCT s.sighting_id) as total_sightings,
    AVG(s.paranormal_activity_level) as avg_activity_level,
    COUNT(DISTINCT i.investigation_id) as active_investigations,
    SUM(CASE WHEN s.sighting_datetime > DATEADD(day, -7, CURRENT_TIMESTAMP()) 
        THEN 1 ELSE 0 END) as recent_sightings_7days
FROM GHOST_DETECTION.APP.GHOSTS g
LEFT JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
LEFT JOIN GHOST_DETECTION.APP.INVESTIGATIONS i ON g.ghost_id = i.ghost_id
WHERE g.status = 'Active'
GROUP BY g.threat_level, g.ghost_type;

COMMENT ON VIEW VW_THREAT_MATRIX IS 
'Threat level distribution and assessment matrix';

-- ============================================
-- Semantic View: AI Model Performance
-- ============================================
CREATE OR REPLACE VIEW VW_AI_MODEL_METRICS AS
SELECT 
    a.model_used,
    a.analysis_type,
    COUNT(*) as total_analyses,
    AVG(a.confidence_score) as avg_confidence,
    MIN(a.confidence_score) as min_confidence,
    MAX(a.confidence_score) as max_confidence,
    SUM(CASE WHEN a.anomaly_detected THEN 1 ELSE 0 END) as anomalies_detected,
    COUNT(DISTINCT a.ghost_id) as unique_ghosts_analyzed,
    MAX(a.analysis_datetime) as last_used_datetime
FROM GHOST_DETECTION.APP.GHOST_AI_ANALYSIS a
GROUP BY a.model_used, a.analysis_type;

COMMENT ON VIEW VW_AI_MODEL_METRICS IS 
'AI model performance and usage metrics';

