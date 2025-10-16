-- ============================================
-- Ghost Detection Application - Agentic AI System
-- ============================================
-- Autonomous AI Agent for Ghost Detection and Response
-- This system enables AI agents to make decisions and take actions
-- independently based on ghost activity patterns and threat levels

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- AGENT SYSTEM TABLES
-- ============================================

-- AI Agent definitions
CREATE OR REPLACE TABLE AI_AGENTS (
    agent_id VARCHAR(50) PRIMARY KEY,
    agent_name VARCHAR(200) NOT NULL,
    agent_type VARCHAR(100), -- Monitoring, Analysis, Response, Investigation, Communication
    agent_role TEXT,
    capabilities ARRAY, -- List of actions the agent can perform
    authority_level VARCHAR(50), -- Read-Only, Suggest, Execute-Low-Risk, Execute-All
    llm_model VARCHAR(100) DEFAULT 'mistral-large2',
    system_prompt TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_action_date TIMESTAMP_NTZ
);

-- Agent actions and decisions
CREATE OR REPLACE TABLE AGENT_ACTIONS (
    action_id VARCHAR(50) PRIMARY KEY,
    agent_id VARCHAR(50),
    action_type VARCHAR(100), -- Analyze, Alert, Recommend, Execute, Communicate
    action_description TEXT,
    trigger_event VARCHAR(200),
    decision_reasoning TEXT, -- AI's explanation for the action
    action_parameters VARIANT, -- JSON parameters for the action
    risk_level VARCHAR(50), -- Low, Medium, High, Critical
    requires_approval BOOLEAN DEFAULT FALSE,
    approval_status VARCHAR(50), -- Pending, Approved, Rejected, Auto-Approved
    executed_date TIMESTAMP_NTZ,
    execution_result VARIANT,
    confidence_score FLOAT,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (agent_id) REFERENCES AI_AGENTS(agent_id)
);

-- Agent decision rules and policies
CREATE OR REPLACE TABLE AGENT_POLICIES (
    policy_id VARCHAR(50) PRIMARY KEY,
    policy_name VARCHAR(200) NOT NULL,
    policy_category VARCHAR(100), -- Safety, Efficiency, Cost, Quality
    policy_rule TEXT, -- Natural language rule
    policy_logic TEXT, -- SQL or procedural logic
    applies_to_agents ARRAY, -- Which agents this policy applies to
    priority INT DEFAULT 100,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Agent learning and feedback
CREATE OR REPLACE TABLE AGENT_LEARNING (
    learning_id VARCHAR(50) PRIMARY KEY,
    agent_id VARCHAR(50),
    scenario_description TEXT,
    action_taken VARCHAR(200),
    outcome_result VARCHAR(100), -- Success, Failure, Partial
    feedback_score FLOAT, -- -1 to 1
    lessons_learned TEXT,
    adjustments_made TEXT,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (agent_id) REFERENCES AI_AGENTS(agent_id)
);

-- Agent communication log
CREATE OR REPLACE TABLE AGENT_COMMUNICATIONS (
    communication_id VARCHAR(50) PRIMARY KEY,
    from_agent_id VARCHAR(50),
    to_agent_id VARCHAR(50),
    to_human_user VARCHAR(200),
    message_type VARCHAR(100), -- Alert, Request, Response, Update, Recommendation
    message_content TEXT,
    priority VARCHAR(50), -- Low, Medium, High, Urgent
    requires_response BOOLEAN DEFAULT FALSE,
    response_content TEXT,
    response_date TIMESTAMP_NTZ,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (from_agent_id) REFERENCES AI_AGENTS(agent_id),
    FOREIGN KEY (to_agent_id) REFERENCES AI_AGENTS(agent_id)
);

-- Agent task queue
CREATE OR REPLACE TABLE AGENT_TASK_QUEUE (
    task_id VARCHAR(50) PRIMARY KEY,
    agent_id VARCHAR(50),
    task_type VARCHAR(100),
    task_description TEXT,
    task_parameters VARIANT,
    priority INT DEFAULT 100,
    status VARCHAR(50) DEFAULT 'Pending', -- Pending, In-Progress, Completed, Failed, Cancelled
    assigned_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    started_date TIMESTAMP_NTZ,
    completed_date TIMESTAMP_NTZ,
    result VARIANT,
    FOREIGN KEY (agent_id) REFERENCES AI_AGENTS(agent_id)
);

-- ============================================
-- INSERT AGENT DEFINITIONS
-- ============================================

-- Fixed: Using SELECT UNION ALL to allow ARRAY_CONSTRUCT
INSERT INTO AI_AGENTS (agent_id, agent_name, agent_type, agent_role, capabilities, authority_level, system_prompt)
SELECT 'AGENT_001', 'ThreatWatch AI', 'Monitoring', 
 'Continuously monitors ghost activity and identifies emerging threats',
 ARRAY_CONSTRUCT('Monitor Sightings', 'Detect Patterns', 'Assess Threats', 'Generate Alerts'),
 'Execute-Low-Risk',
 'You are ThreatWatch AI, an autonomous agent monitoring paranormal activity. Your role is to identify threats early and alert the team. Analyze patterns, assess risks, and recommend actions. Be proactive but cautious. Prioritize safety.'
UNION ALL
SELECT 'AGENT_002', 'InvestigatorAI', 'Analysis',
 'Analyzes evidence and sightings to provide investigative insights',
 ARRAY_CONSTRUCT('Analyze Evidence', 'Classify Ghosts', 'Find Patterns', 'Generate Reports', 'Recommend Strategies'),
 'Suggest',
 'You are InvestigatorAI, an analytical agent specialized in paranormal investigation. Review evidence, classify entities, identify patterns, and provide detailed insights. Be thorough and scientific in your approach.'
UNION ALL
SELECT 'AGENT_003', 'ResponseCoordinator AI', 'Response',
 'Coordinates investigation teams and resource allocation',
 ARRAY_CONSTRUCT('Assign Investigators', 'Schedule Cases', 'Allocate Resources', 'Track Progress'),
 'Execute-Low-Risk',
 'You are ResponseCoordinator AI, responsible for optimal team deployment. Match investigator skills to case requirements, balance workload, and ensure efficient resource usage. Prioritize high-threat cases.'
UNION ALL
SELECT 'AGENT_004', 'CommunicationAI', 'Communication',
 'Handles communications with investigators and generates reports',
 ARRAY_CONSTRUCT('Send Alerts', 'Generate Reports', 'Answer Questions', 'Provide Updates'),
 'Execute-All',
 'You are CommunicationAI, the interface between the AI system and human investigators. Communicate clearly, provide timely updates, answer questions accurately, and ensure critical information reaches the right people.'
UNION ALL
SELECT 'AGENT_005', 'PredictiveAI', 'Analysis',
 'Predicts future ghost activity based on patterns',
 ARRAY_CONSTRUCT('Forecast Activity', 'Identify Hotspots', 'Predict Patterns', 'Risk Assessment'),
 'Suggest',
 'You are PredictiveAI, specializing in forecasting paranormal events. Analyze historical data, identify trends, predict where and when activity will occur. Help the team stay ahead of threats.';

-- ============================================
-- INSERT AGENT POLICIES
-- ============================================

-- Fixed: Using SELECT UNION ALL to allow ARRAY_CONSTRUCT
INSERT INTO AGENT_POLICIES (policy_id, policy_name, policy_category, policy_rule, applies_to_agents, priority)
SELECT 'POL_001', 'Extreme Threat Auto-Alert', 'Safety',
 'Any ghost classified as Extreme threat with activity in last 24 hours triggers immediate alert to all investigators',
 ARRAY_CONSTRUCT('AGENT_001', 'AGENT_004'), 1
UNION ALL
SELECT 'POL_002', 'Evidence Auto-Analysis', 'Efficiency',
 'All new evidence is automatically analyzed within 1 hour of upload',
 ARRAY_CONSTRUCT('AGENT_002'), 50
UNION ALL
SELECT 'POL_003', 'Investigator Workload Balance', 'Efficiency',
 'No investigator should be assigned more than 5 active cases simultaneously',
 ARRAY_CONSTRUCT('AGENT_003'), 75
UNION ALL
SELECT 'POL_004', 'Require Approval for Containment', 'Safety',
 'Any recommendation for ghost containment requires human approval before execution',
 ARRAY_CONSTRUCT('AGENT_001', 'AGENT_002', 'AGENT_003'), 1
UNION ALL
SELECT 'POL_005', 'Daily Summary Report', 'Communication',
 'Generate and send daily summary report of ghost activity at 08:00 UTC',
 ARRAY_CONSTRUCT('AGENT_004'), 100;

-- ============================================
-- AGENTIC AI PROCEDURES
-- ============================================

-- Agent: Monitor and detect new threats
CREATE OR REPLACE PROCEDURE AGENT_MONITOR_THREATS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    threat_count INT;
    alert_message STRING;
    action_id STRING;
    ghost_details STRING;
    alert_prompt STRING;
    decision_reason STRING;
BEGIN
    action_id := 'ACT_' || UUID_STRING();
    
    -- Detect extreme threats with recent activity
    SELECT COUNT(*) INTO :threat_count
    FROM GHOSTS g
    JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
    WHERE g.threat_level = 'Extreme'
    AND g.status = 'Active'
    AND s.sighting_datetime >= DATEADD(hour, -24, CURRENT_TIMESTAMP());
    
    IF (threat_count > 0) THEN
        -- Get ghost details separately
        SELECT LISTAGG(ghost_info, '; ') INTO :ghost_details
        FROM (
            SELECT (g.ghost_name || ' (' || COUNT(s.sighting_id) || ' sightings)') as ghost_info
            FROM GHOSTS g
            JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
            WHERE g.threat_level = 'Extreme' 
            AND s.sighting_datetime >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
            GROUP BY g.ghost_id, g.ghost_name
        );
        
        -- Construct prompt
        alert_prompt := CONCAT(
            'ALERT: ', TO_CHAR(:threat_count), ' extreme-threat ghosts have been active in the last 24 hours. ',
            'Details: ', :ghost_details,
            '. Generate a professional alert message for investigators with recommended actions.'
        );
        
        -- Use AI to generate alert message
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', :alert_prompt) INTO :alert_message;
        
        -- Construct decision reasoning
        decision_reason := CONCAT('Detected ', TO_CHAR(:threat_count), ' extreme-threat entities with recent activity');
        
        -- Log the action
        INSERT INTO AGENT_ACTIONS (
            action_id, agent_id, action_type, action_description,
            trigger_event, decision_reasoning, risk_level, 
            approval_status, executed_date, confidence_score
        ) VALUES (
            :action_id, 'AGENT_001', 'Alert', :alert_message,
            'Extreme threat detection', 
            :decision_reason,
            'Critical', 'Auto-Approved', CURRENT_TIMESTAMP(), 0.95
        );
        
        -- Send communication
        INSERT INTO AGENT_COMMUNICATIONS (
            communication_id, from_agent_id, message_type,
            message_content, priority, requires_response
        )
        SELECT 
            'COMM_' || UUID_STRING(), 'AGENT_001', 'Alert',
            :alert_message, 'Urgent', FALSE;
        
        RETURN 'ALERT: ' || TO_CHAR(:threat_count) || ' extreme threats detected. Alert sent.';
    ELSE
        RETURN 'No immediate threats detected.';
    END IF;
END;
$$;

-- Agent: Analyze new sightings and classify
CREATE OR REPLACE PROCEDURE AGENT_ANALYZE_NEW_SIGHTINGS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    unanalyzed_count INT;
    results STRING DEFAULT '';
BEGIN
    -- Find sightings without AI analysis
    SELECT COUNT(*) INTO :unanalyzed_count
    FROM GHOST_SIGHTINGS s
    LEFT JOIN GHOST_AI_ANALYSIS a ON s.sighting_id = a.sighting_id
    WHERE a.analysis_id IS NULL
    AND s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP());
    
    IF (:unanalyzed_count > 0) THEN
        -- Analyze each sighting
        FOR sighting IN (
            SELECT s.sighting_id
            FROM GHOST_SIGHTINGS s
            LEFT JOIN GHOST_AI_ANALYSIS a ON s.sighting_id = a.sighting_id
            WHERE a.analysis_id IS NULL
            AND s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
            LIMIT 10
        ) DO
            CALL ANALYZE_SIGHTING_WITH_AI(sighting.sighting_id);
        END FOR;
        
        -- Log action
        INSERT INTO AGENT_ACTIONS (
            action_id, agent_id, action_type, action_description,
            trigger_event, decision_reasoning, risk_level,
            approval_status, executed_date, confidence_score
        )
        SELECT 
            'ACT_' || UUID_STRING(), 'AGENT_002', 'Analyze',
            CONCAT('Analyzed ', LEAST(:unanalyzed_count, 10), ' new sightings'),
            'New sighting detection',
            'Automated analysis of unprocessed sightings',
            'Low', 'Auto-Approved', CURRENT_TIMESTAMP(), 0.88;
        
        results := 'Analyzed ' || LEAST(:unanalyzed_count, 10) || ' sightings.';
    ELSE
        results := 'No new sightings to analyze.';
    END IF;
    
    RETURN results;
END;
$$;

-- Agent: Coordinate investigator assignments
CREATE OR REPLACE PROCEDURE AGENT_ASSIGN_INVESTIGATORS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    unassigned_cases INT;
    assignment_result STRING;
    cases_list STRING;
    investigators_list STRING;
    assignment_prompt STRING;
BEGIN
    -- Find open cases without assigned investigators
    SELECT COUNT(*) INTO :unassigned_cases
    FROM INVESTIGATIONS
    WHERE status = 'Open'
    AND lead_investigator_id IS NULL;
    
    IF (:unassigned_cases > 0) THEN
        -- Get unassigned cases list
        SELECT LISTAGG(case_name || ' (' || priority || ')', '; ') INTO :cases_list
        FROM INVESTIGATIONS 
        WHERE status = 'Open' AND lead_investigator_id IS NULL;
        
        -- Get available investigators list
        SELECT LISTAGG(investigator_name || ' (' || specialization || ')', '; ') INTO :investigators_list
        FROM INVESTIGATORS 
        WHERE active_status = TRUE;
        
        -- Construct prompt
        assignment_prompt := CONCAT(
            'You are ResponseCoordinator AI. Analyze these unassigned cases: ',
            :cases_list,
            '. Available investigators: ',
            :investigators_list,
            '. Recommend optimal investigator assignments considering skills and workload.'
        );
        
        -- Use AI to match investigators to cases
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', :assignment_prompt) INTO :assignment_result;
        
        -- Log recommendation
        INSERT INTO AGENT_ACTIONS (
            action_id, agent_id, action_type, action_description,
            decision_reasoning, risk_level, requires_approval,
            approval_status, created_date, confidence_score
        )
        SELECT 
            'ACT_' || UUID_STRING(), 'AGENT_003', 'Recommend',
            :assignment_result,
            'Optimal investigator-case matching based on skills and availability',
            'Low', TRUE, 'Pending', CURRENT_TIMESTAMP(), 0.82;
        
        RETURN 'Generated assignment recommendations for ' || TO_CHAR(:unassigned_cases) || ' cases.';
    ELSE
        RETURN 'All cases have assigned investigators.';
    END IF;
END;
$$;

-- Agent: Generate predictive insights
CREATE OR REPLACE PROCEDURE AGENT_GENERATE_PREDICTIONS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    prediction_report STRING;
    recent_sightings_count INT;
    active_locations STRING;
    active_ghosts STRING;
    prediction_prompt STRING;
BEGIN
    -- Get recent sightings count
    SELECT COUNT(*) INTO :recent_sightings_count
    FROM GHOST_SIGHTINGS 
    WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP());
    
    -- Get most active locations
    SELECT LISTAGG(location_name, ', ') INTO :active_locations
    FROM (
        SELECT location_name, COUNT(*) as cnt
        FROM GHOST_SIGHTINGS
        WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
        GROUP BY location_name
        ORDER BY cnt DESC
        LIMIT 3
    );
    
    -- Get most active ghosts
    SELECT LISTAGG(ghost_name, ', ') INTO :active_ghosts
    FROM (
        SELECT g.ghost_name, COUNT(*) as cnt
        FROM GHOSTS g
        JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
        WHERE s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
        GROUP BY g.ghost_id, g.ghost_name
        ORDER BY cnt DESC
        LIMIT 3
    );
    
    -- Construct prompt
    prediction_prompt := CONCAT(
        'You are PredictiveAI analyzing paranormal activity patterns. ',
        'Recent data: ',
        'Last 7 days sightings: ', TO_CHAR(:recent_sightings_count), '. ',
        'Most active locations: ', :active_locations, '. ',
        'Most active ghosts: ', :active_ghosts, '. ',
        'Predict: 1) Where activity will occur next, 2) Which ghosts will be most active, ',
        '3) Risk assessment for next 7 days, 4) Recommended monitoring locations.'
    );
    
    -- Analyze patterns and generate predictions
    SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', :prediction_prompt) INTO :prediction_report;
    
    -- Store prediction
    INSERT INTO AGENT_ACTIONS (
        action_id, agent_id, action_type, action_description,
        decision_reasoning, risk_level, approval_status,
        executed_date, confidence_score
    )
    SELECT 
        'ACT_' || UUID_STRING(), 'AGENT_005', 'Forecast',
        :prediction_report,
        'Pattern analysis and predictive modeling based on historical data',
        'Low', 'Auto-Approved', CURRENT_TIMESTAMP(), 0.75;
    
    RETURN 'Prediction report generated successfully.';
END;
$$;

-- Agent: Daily communication summary
CREATE OR REPLACE PROCEDURE AGENT_DAILY_SUMMARY()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    summary_report STRING;
    sightings_today INT;
    new_ghosts INT;
    active_investigations INT;
    extreme_threats INT;
    cases_closed INT;
    top_location STRING;
    summary_prompt STRING;
BEGIN
    -- Get daily metrics
    SELECT COUNT(*) INTO :sightings_today
    FROM GHOST_SIGHTINGS 
    WHERE DATE(sighting_datetime) = CURRENT_DATE();
    
    SELECT COUNT(*) INTO :new_ghosts
    FROM GHOSTS 
    WHERE DATE(first_detected_date) = CURRENT_DATE();
    
    SELECT COUNT(*) INTO :active_investigations
    FROM INVESTIGATIONS 
    WHERE status IN ('Open', 'In_Progress');
    
    SELECT COUNT(*) INTO :extreme_threats
    FROM GHOSTS 
    WHERE threat_level = 'Extreme' AND status = 'Active';
    
    SELECT COUNT(*) INTO :cases_closed
    FROM INVESTIGATIONS 
    WHERE DATE(end_date) = CURRENT_DATE();
    
    SELECT location_name INTO :top_location
    FROM GHOST_SIGHTINGS 
    WHERE DATE(sighting_datetime) = CURRENT_DATE()
    GROUP BY location_name 
    ORDER BY COUNT(*) DESC 
    LIMIT 1;
    
    -- Construct summary prompt
    summary_prompt := CONCAT(
        'Generate a professional daily summary report for ghost detection operations. ',
        'Date: ', TO_CHAR(CURRENT_DATE()), '. ',
        'Activity Summary: ',
        'Total Sightings Today: ', TO_CHAR(:sightings_today), '. ',
        'New Ghosts Detected: ', TO_CHAR(:new_ghosts), '. ',
        'Active Investigations: ', TO_CHAR(:active_investigations), '. ',
        'Extreme Threats: ', TO_CHAR(:extreme_threats), '. ',
        'Cases Closed Today: ', TO_CHAR(:cases_closed), '. ',
        'Top Active Location: ', COALESCE(:top_location, 'None'), '. ',
        'Format as: Executive Summary, Key Metrics, Notable Incidents, ',
        'Threat Assessment, Recommendations for Tomorrow.'
    );
    
    -- Generate comprehensive daily summary
    SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', :summary_prompt) INTO :summary_report;
    
    -- Send summary communication
    INSERT INTO AGENT_COMMUNICATIONS (
        communication_id, from_agent_id, message_type,
        message_content, priority, created_date
    )
    SELECT 
        'COMM_' || UUID_STRING(), 'AGENT_004', 'Update',
        :summary_report, 'Medium', CURRENT_TIMESTAMP();
    
    -- Log action
    INSERT INTO AGENT_ACTIONS (
        action_id, agent_id, action_type, action_description,
        decision_reasoning, risk_level, approval_status,
        executed_date, confidence_score
    )
    SELECT 
        'ACT_' || UUID_STRING(), 'AGENT_004', 'Communicate',
        'Daily summary report generated and distributed',
        'Scheduled daily communication per policy POL_005',
        'Low', 'Auto-Approved', CURRENT_TIMESTAMP(), 0.92;
    
    RETURN 'Daily summary report generated and sent.';
END;
$$;

-- ============================================
-- AGENT ORCHESTRATION
-- ============================================

-- Master agent coordinator - runs all agents
CREATE OR REPLACE PROCEDURE RUN_ALL_AGENTS()
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    threat_result VARCHAR;
    sighting_result VARCHAR;
    assignment_result VARCHAR;
    prediction_result VARCHAR;
    results VARIANT;
BEGIN
    -- Run all active agents sequentially
    CALL AGENT_MONITOR_THREATS() INTO :threat_result;
    CALL AGENT_ANALYZE_NEW_SIGHTINGS() INTO :sighting_result;
    CALL AGENT_ASSIGN_INVESTIGATORS() INTO :assignment_result;
    CALL AGENT_GENERATE_PREDICTIONS() INTO :prediction_result;
    
    -- Construct results object
    results := OBJECT_CONSTRUCT(
        'threat_monitoring', :threat_result,
        'sighting_analysis', :sighting_result,
        'investigator_assignment', :assignment_result,
        'predictions', :prediction_result
    );
    
    RETURN 'All agents executed. Results: ' || TO_JSON(:results);
END;
$$;

-- ============================================
-- AGENT ANALYTICS VIEWS
-- ============================================

CREATE OR REPLACE VIEW VW_AGENT_PERFORMANCE AS
SELECT 
    a.agent_id,
    a.agent_name,
    a.agent_type,
    COUNT(DISTINCT aa.action_id) as total_actions,
    SUM(CASE WHEN aa.approval_status = 'Auto-Approved' THEN 1 ELSE 0 END) as auto_approved_actions,
    SUM(CASE WHEN aa.approval_status = 'Approved' THEN 1 ELSE 0 END) as human_approved_actions,
    SUM(CASE WHEN aa.approval_status = 'Rejected' THEN 1 ELSE 0 END) as rejected_actions,
    AVG(aa.confidence_score) as avg_confidence,
    MAX(aa.executed_date) as last_action_date
FROM AI_AGENTS a
LEFT JOIN AGENT_ACTIONS aa ON a.agent_id = aa.agent_id
WHERE a.is_active = TRUE
GROUP BY a.agent_id, a.agent_name, a.agent_type;

CREATE OR REPLACE VIEW VW_AGENT_COMMUNICATIONS_LOG AS
SELECT 
    ac.communication_id,
    fa.agent_name as from_agent,
    COALESCE(ta.agent_name, ac.to_human_user, 'All Users') as recipient,
    ac.message_type,
    ac.priority,
    ac.message_content,
    ac.requires_response,
    ac.created_date
FROM AGENT_COMMUNICATIONS ac
LEFT JOIN AI_AGENTS fa ON ac.from_agent_id = fa.agent_id
LEFT JOIN AI_AGENTS ta ON ac.to_agent_id = ta.agent_id
ORDER BY ac.created_date DESC;

-- ============================================
-- SCHEDULED TASKS FOR AGENTS
-- ============================================

-- Schedule threat monitoring (every 30 minutes)
CREATE OR REPLACE TASK TASK_AGENT_MONITOR
    WAREHOUSE = GHOST_DETECTION_WH
    SCHEDULE = '30 MINUTE'
AS
    CALL AGENT_MONITOR_THREATS();

-- Schedule sighting analysis (every hour)
CREATE OR REPLACE TASK TASK_AGENT_ANALYZE
    WAREHOUSE = GHOST_DETECTION_WH
    SCHEDULE = '60 MINUTE'
AS
    CALL AGENT_ANALYZE_NEW_SIGHTINGS();

-- Schedule daily summary (08:00 UTC)
CREATE OR REPLACE TASK TASK_AGENT_DAILY_SUMMARY
    WAREHOUSE = GHOST_DETECTION_WH
    SCHEDULE = 'USING CRON 0 8 * * * UTC'
AS
    CALL AGENT_DAILY_SUMMARY();

-- Enable tasks (commented out - enable when ready)
-- ALTER TASK TASK_AGENT_MONITOR RESUME;
-- ALTER TASK TASK_AGENT_ANALYZE RESUME;
-- ALTER TASK TASK_AGENT_DAILY_SUMMARY RESUME;

COMMENT ON TABLE AI_AGENTS IS 'Autonomous AI agents for ghost detection and response';
COMMENT ON TABLE AGENT_ACTIONS IS 'Log of all agent decisions and actions';
COMMENT ON TABLE AGENT_POLICIES IS 'Rules and policies governing agent behavior';
COMMENT ON PROCEDURE RUN_ALL_AGENTS IS 'Master orchestrator running all active AI agents';

