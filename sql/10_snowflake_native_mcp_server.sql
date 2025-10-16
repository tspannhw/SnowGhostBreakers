-- ============================================================================
-- SNOWFLAKE NATIVE MCP SERVER CONFIGURATION
-- ============================================================================
-- Purpose: Create and configure Snowflake-managed MCP server
-- Reference: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents-mcp
-- Author: Ghost Detection Team
-- Version: 1.0
-- ============================================================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================================================
-- STEP 1: Create OAuth Security Integration for MCP Authentication
-- ============================================================================

-- Note: Replace <your_redirect_uri> with your actual OAuth redirect URI
-- For local development, use: http://localhost:3000/oauth/callback
-- For production, use your application's OAuth callback URL

CREATE OR REPLACE SECURITY INTEGRATION GHOST_MCP_OAUTH
    TYPE = OAUTH
    OAUTH_CLIENT = CUSTOM
    ENABLED = TRUE
    OAUTH_CLIENT_TYPE = 'CONFIDENTIAL'
    OAUTH_REDIRECT_URI = 'http://localhost:3000/oauth/callback'
    COMMENT = 'OAuth integration for Ghost Detection MCP Server';

-- Retrieve OAuth client credentials (save these securely!)
-- Note: Integration name must be in UPPERCASE
SELECT 'OAuth Configuration Created. Run the following to get credentials:' as status;
SELECT 'SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS(''GHOST_MCP_OAUTH'');' as next_step;

-- ============================================================================
-- STEP 2: Ensure Cortex Search Service Exists
-- ============================================================================

-- Create Cortex Search Service for ghost data if not exists
CREATE CORTEX SEARCH SERVICE IF NOT EXISTS GHOST_SEARCH_SERVICE
ON ghost_name, ghost_type, description, behavioral_pattern
ATTRIBUTES location_name, threat_level, status
WAREHOUSE = GHOST_WAREHOUSE
TARGET_LAG = '1 hour'
AS (
    SELECT 
        g.ghost_id,
        g.ghost_name,
        g.ghost_type,
        g.description,
        g.behavioral_pattern,
        g.threat_level,
        g.status,
        COALESCE(s.location_name, 'Unknown') as location_name,
        g.first_sighting_date,
        g.last_sighting_date
    FROM GHOSTS g
    LEFT JOIN (
        SELECT ghost_id, 
               LISTAGG(DISTINCT location_name, ', ') as location_name
        FROM GHOST_SIGHTINGS
        GROUP BY ghost_id
    ) s ON g.ghost_id = s.ghost_id
);

SELECT 'Cortex Search Service Created' as status;

-- ============================================================================
-- STEP 3: Create Semantic Model for Cortex Analyst (if not exists)
-- ============================================================================

-- The semantic model YAML file should already exist in cortex_analyst/ghost_semantic_model.yaml
-- This is referenced when creating the MCP server

SELECT 'Ensure semantic model exists at: cortex_analyst/ghost_semantic_model.yaml' as status;

-- ============================================================================
-- STEP 4: Create Snowflake-Managed MCP Server
-- ============================================================================

CREATE OR REPLACE MCP SERVER GHOST_DETECTION_MCP_SERVER
FROM SPECIFICATION $$
  tools:
    # Cortex Search Tool - For semantic search across ghost data
    - name: "ghost-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "GHOST_DETECTION.APP.GHOST_SEARCH_SERVICE"
      description: "Semantic search service for ghost detection data. Search for ghosts by name, type, description, behavior patterns, locations, and threat levels. Use this tool to find specific ghosts or ghost-related information."
      title: "Ghost Data Search"
    
    # Cortex Analyst Tool - For natural language queries
    - name: "ghost-analytics"
      type: "CORTEX_ANALYST_MESSAGE"
      identifier: "GHOST_DETECTION.APP.GHOST_SEMANTIC_MODEL"
      description: "Natural language interface to query ghost detection analytics. Ask questions about ghost statistics, sighting patterns, threat analysis, location hotspots, and investigation data. Supports complex analytical queries in plain English."
      title: "Ghost Analytics Assistant"
    
    # Additional Search - Sighting-specific search
    - name: "sighting-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "GHOST_DETECTION.APP.SIGHTING_SEARCH_SERVICE"
      description: "Search for ghost sightings by location, date, witness descriptions, and paranormal activity levels. Use this tool to find specific sighting events and patterns."
      title: "Sighting Data Search"
    
    # Evidence Search Tool
    - name: "evidence-search"
      type: "CORTEX_SEARCH_SERVICE_QUERY"
      identifier: "GHOST_DETECTION.APP.EVIDENCE_SEARCH_SERVICE"
      description: "Search ghost evidence including images, audio, video, and sensor data. Find evidence by type, processing status, ghost association, and capture details."
      title: "Evidence Repository Search"
$$
COMMENT = 'Snowflake-managed MCP server for Ghost Detection System providing AI agents with secure access to ghost data, analytics, and search capabilities';

SELECT 'MCP Server Created Successfully!' as status;

-- ============================================================================
-- STEP 5: Create Additional Cortex Search Services
-- ============================================================================

-- Sighting Search Service
CREATE CORTEX SEARCH SERVICE IF NOT EXISTS SIGHTING_SEARCH_SERVICE
ON location_name, witness_description, environmental_conditions
ATTRIBUTES ghost_id, paranormal_activity_level, emf_reading, temperature
WAREHOUSE = GHOST_WAREHOUSE
TARGET_LAG = '1 hour'
AS (
    SELECT 
        s.sighting_id,
        s.ghost_id,
        g.ghost_name,
        g.ghost_type,
        s.location_name,
        s.location_coordinates,
        s.sighting_datetime,
        s.witness_count,
        s.paranormal_activity_level,
        s.emf_reading,
        s.temperature,
        s.environmental_conditions,
        s.witness_description,
        g.threat_level
    FROM GHOST_SIGHTINGS s
    JOIN GHOSTS g ON s.ghost_id = g.ghost_id
);

-- Evidence Search Service
CREATE CORTEX SEARCH SERVICE IF NOT EXISTS EVIDENCE_SEARCH_SERVICE
ON file_path, metadata, ai_description
ATTRIBUTES evidence_type, ghost_id, processing_status
WAREHOUSE = GHOST_WAREHOUSE
TARGET_LAG = '1 hour'
AS (
    SELECT 
        e.evidence_id,
        e.ghost_id,
        e.sighting_id,
        g.ghost_name,
        e.evidence_type,
        e.file_path,
        e.mime_type,
        e.file_size_bytes,
        e.capture_datetime,
        e.processing_status,
        e.metadata,
        COALESCE(a.analysis_result, '') as ai_description,
        g.threat_level
    FROM GHOST_EVIDENCE e
    JOIN GHOSTS g ON e.ghost_id = g.ghost_id
    LEFT JOIN GHOST_AI_ANALYSIS a ON e.evidence_id = a.evidence_id
);

SELECT 'All Cortex Search Services Created' as status;

-- ============================================================================
-- STEP 6: Grant Necessary Privileges
-- ============================================================================

-- Grant USAGE on MCP server to GHOSTBUSTER role
GRANT USAGE ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE GHOSTBUSTER;
GRANT USAGE ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE GHOST_ANALYST;

-- Grant USAGE on Cortex Search Services
GRANT USAGE ON CORTEX SEARCH SERVICE GHOST_SEARCH_SERVICE TO ROLE GHOSTBUSTER;
GRANT USAGE ON CORTEX SEARCH SERVICE GHOST_SEARCH_SERVICE TO ROLE GHOST_ANALYST;

GRANT USAGE ON CORTEX SEARCH SERVICE SIGHTING_SEARCH_SERVICE TO ROLE GHOSTBUSTER;
GRANT USAGE ON CORTEX SEARCH SERVICE SIGHTING_SEARCH_SERVICE TO ROLE GHOST_ANALYST;

GRANT USAGE ON CORTEX SEARCH SERVICE EVIDENCE_SEARCH_SERVICE TO ROLE GHOSTBUSTER;
GRANT USAGE ON CORTEX SEARCH SERVICE EVIDENCE_SEARCH_SERVICE TO ROLE GHOST_ANALYST;

-- Grant MODIFY privilege to admins
GRANT MODIFY ON MCP SERVER GHOST_DETECTION_MCP_SERVER TO ROLE GHOST_ADMIN;

SELECT 'Privileges Granted Successfully' as status;

-- ============================================================================
-- STEP 7: View MCP Server Configuration
-- ============================================================================

-- Describe the MCP server
DESCRIBE MCP SERVER GHOST_DETECTION_MCP_SERVER;

-- Show all MCP servers in the schema
SHOW MCP SERVERS IN SCHEMA APP;

-- Show MCP servers in the database
SHOW MCP SERVERS IN DATABASE GHOST_DETECTION;

-- ============================================================================
-- STEP 8: Test MCP Server Endpoints (Documentation)
-- ============================================================================

SELECT 'MCP Server Endpoints:' as info;
SELECT 'Base URL: https://<account>.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER' as endpoint;

SELECT 'Available Methods:' as info;
SELECT '1. Initialize: POST /...mcp-servers/<name> with method: "initialize"' as method
UNION ALL
SELECT '2. List Tools: POST /...mcp-servers/<name> with method: "tools/list"'
UNION ALL
SELECT '3. Call Tool: POST /...mcp-servers/<name> with method: "tools/call"';

-- ============================================================================
-- STEP 9: Create Helper Functions for MCP Operations
-- ============================================================================

-- Helper function to test ghost search
CREATE OR REPLACE FUNCTION TEST_GHOST_SEARCH(search_query VARCHAR)
RETURNS TABLE (
    ghost_id NUMBER,
    ghost_name VARCHAR,
    ghost_type VARCHAR,
    description VARCHAR,
    threat_level VARCHAR
)
AS
$$
    SELECT 
        ghost_id,
        ghost_name,
        ghost_type,
        description,
        threat_level
    FROM TABLE(
        GHOST_DETECTION.APP.GHOST_SEARCH_SERVICE(
            QUERY => search_query,
            LIMIT => 10
        )
    )
$$;

-- Test the search
SELECT 'Test Ghost Search:' as test;
SELECT * FROM TABLE(TEST_GHOST_SEARCH('shadow entity'));

-- ============================================================================
-- STEP 10: Create Monitoring View for MCP Usage
-- ============================================================================

CREATE OR REPLACE VIEW VW_MCP_SERVER_INFO AS
SELECT 
    'GHOST_DETECTION_MCP_SERVER' as mcp_server_name,
    'GHOST_DETECTION.APP.GHOST_DETECTION_MCP_SERVER' as full_identifier,
    'https://' || CURRENT_ACCOUNT() || '.snowflakecomputing.com/api/v2/databases/GHOST_DETECTION/schemas/APP/mcp-servers/GHOST_DETECTION_MCP_SERVER' as endpoint_url,
    '2025-06-18' as mcp_protocol_version,
    4 as tool_count,
    ARRAY_CONSTRUCT(
        'ghost-search',
        'ghost-analytics', 
        'sighting-search',
        'evidence-search'
    ) as available_tools,
    'OAuth 2.0 via GHOST_MCP_OAUTH integration' as authentication_method,
    CURRENT_TIMESTAMP() as info_retrieved_at;

SELECT * FROM VW_MCP_SERVER_INFO;

-- ============================================================================
-- COMPLETION SUMMARY
-- ============================================================================

SELECT '
╔══════════════════════════════════════════════════════════════════════════╗
║              SNOWFLAKE NATIVE MCP SERVER CREATED!                        ║
║                                                                          ║
║  Server Name: GHOST_DETECTION_MCP_SERVER                                ║
║  Protocol: MCP 2025-06-18                                               ║
║  Tools: 4 (Search + Analytics)                                          ║
║  Authentication: OAuth 2.0                                               ║
║                                                                          ║
║  Next Steps:                                                            ║
║  1. Get OAuth credentials:                                              ║
║     SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS(''GHOST_MCP_OAUTH'');      ║
║                                                                          ║
║  2. Configure your MCP client with:                                     ║
║     - OAuth Client ID and Secret (from step 1)                          ║
║     - MCP Server endpoint URL                                           ║
║     - Redirect URI: http://localhost:3000/oauth/callback                ║
║                                                                          ║
║  3. Test the server using MCP client tools                             ║
║                                                                          ║
║  4. View configuration:                                                 ║
║     SELECT * FROM VW_MCP_SERVER_INFO;                                   ║
╚══════════════════════════════════════════════════════════════════════════╝
' as setup_complete;

-- Log creation in audit log
INSERT INTO AUDIT_LOG (table_name, operation_type, user_name, details)
VALUES (
    'MCP_SERVER',
    'CREATE',
    CURRENT_USER(),
    'Created Snowflake-managed MCP server GHOST_DETECTION_MCP_SERVER with 4 tools'
);

