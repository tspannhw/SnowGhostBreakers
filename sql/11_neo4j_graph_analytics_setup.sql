-- ============================================
-- NEO4J GRAPH ANALYTICS FOR SNOWFLAKE - SETUP
-- ============================================
-- Install Neo4j Graph Analytics from Snowflake Marketplace
-- Reference: https://neo4j.com/docs/snowflake-graph-analytics/current/
--
-- Prerequisites:
-- 1. Install "Neo4j Graph Analytics for Snowflake" from Snowflake Marketplace
-- 2. Grant necessary privileges to run graph algorithms
-- 3. Create compute pools for scaling out graph jobs
-- ============================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- 1. GRAPH DATA PREPARATION
-- ============================================

-- Create node tables for graph analytics
-- Ghosts as nodes
CREATE OR REPLACE VIEW NEO4J_GHOST_NODES AS
SELECT 
    ghost_id AS node_id,
    ghost_name AS name,
    ghost_type AS type,
    threat_level,
    status,
    danger_level,
    last_seen_location
FROM GHOSTS;

-- Locations as nodes
CREATE OR REPLACE VIEW NEO4J_LOCATION_NODES AS
SELECT DISTINCT
    MD5(location_name) AS node_id,
    location_name AS name,
    'Location' AS type,
    COUNT(*) AS sighting_count
FROM GHOST_SIGHTINGS
GROUP BY location_name;

-- Investigators as nodes
CREATE OR REPLACE VIEW NEO4J_INVESTIGATOR_NODES AS
SELECT 
    investigator_id AS node_id,
    investigator_name AS name,
    'Investigator' AS type,
    specialization,
    certification_level,
    status
FROM INVESTIGATORS;

-- ============================================
-- 2. GRAPH RELATIONSHIP EDGES
-- ============================================

-- Ghost-to-Ghost relationships (appear together at same location)
CREATE OR REPLACE VIEW NEO4J_GHOST_COOCCURRENCE_EDGES AS
SELECT DISTINCT
    g1.ghost_id AS source_node,
    g2.ghost_id AS target_node,
    'CO_OCCURS_WITH' AS relationship_type,
    COUNT(*) AS weight,
    LISTAGG(DISTINCT gs1.location_name, ', ') AS shared_locations
FROM GHOST_SIGHTINGS gs1
JOIN GHOST_SIGHTINGS gs2 
    ON gs1.location_name = gs2.location_name
    AND gs1.sighting_datetime::DATE = gs2.sighting_datetime::DATE
JOIN GHOSTS g1 ON gs1.ghost_id = g1.ghost_id
JOIN GHOSTS g2 ON gs2.ghost_id = g2.ghost_id
WHERE g1.ghost_id < g2.ghost_id  -- Avoid duplicates
GROUP BY g1.ghost_id, g2.ghost_id;

-- Ghost-to-Location relationships
CREATE OR REPLACE VIEW NEO4J_GHOST_LOCATION_EDGES AS
SELECT 
    ghost_id AS source_node,
    MD5(location_name) AS target_node,
    'SIGHTED_AT' AS relationship_type,
    COUNT(*) AS weight,
    MAX(sighting_datetime) AS last_sighting,
    AVG(danger_level) AS avg_danger_level
FROM GHOST_SIGHTINGS
GROUP BY ghost_id, location_name;

-- Investigator-to-Investigation relationships
CREATE OR REPLACE VIEW NEO4J_INVESTIGATOR_CASE_EDGES AS
SELECT 
    investigator_id AS source_node,
    investigation_id AS target_node,
    'WORKS_ON' AS relationship_type,
    1 AS weight
FROM INVESTIGATIONS;

-- Investigation-to-Ghost relationships
CREATE OR REPLACE VIEW NEO4J_INVESTIGATION_GHOST_EDGES AS
SELECT 
    investigation_id AS source_node,
    ghost_id AS target_node,
    'INVESTIGATES' AS relationship_type,
    1 AS weight,
    priority,
    status
FROM INVESTIGATIONS;

-- ============================================
-- 3. COMBINED GRAPH VIEW
-- ============================================

-- All nodes combined
CREATE OR REPLACE VIEW NEO4J_ALL_NODES AS
SELECT node_id, name, type, NULL AS threat_level, NULL AS status 
FROM NEO4J_LOCATION_NODES
UNION ALL
SELECT node_id, name, type, threat_level, status 
FROM NEO4J_GHOST_NODES
UNION ALL
SELECT node_id, name, type, NULL AS threat_level, status 
FROM NEO4J_INVESTIGATOR_NODES;

-- All edges combined
CREATE OR REPLACE VIEW NEO4J_ALL_EDGES AS
SELECT source_node, target_node, relationship_type, weight 
FROM NEO4J_GHOST_COOCCURRENCE_EDGES
UNION ALL
SELECT source_node, target_node, relationship_type, weight 
FROM NEO4J_GHOST_LOCATION_EDGES
UNION ALL
SELECT source_node, target_node, relationship_type, weight 
FROM NEO4J_INVESTIGATOR_CASE_EDGES
UNION ALL
SELECT source_node, target_node, relationship_type, weight 
FROM NEO4J_INVESTIGATION_GHOST_EDGES;

-- ============================================
-- 4. GRAPH PROJECTION FOR NEO4J
-- ============================================

-- Create a graph projection table for Neo4j algorithms
-- This represents the full ghost detection network
CREATE OR REPLACE TABLE NEO4J_GHOST_NETWORK_PROJECTION AS
SELECT 
    source_node,
    target_node,
    relationship_type,
    weight
FROM NEO4J_ALL_EDGES;

-- Add indexes for better performance
-- Note: These are logical indexes for querying, not Snowflake CREATE INDEX
ALTER TABLE NEO4J_GHOST_NETWORK_PROJECTION ADD SEARCH OPTIMIZATION;

-- ============================================
-- 5. COMPUTE POOL CONFIGURATION
-- ============================================

-- Example: Create compute pool for graph analytics
-- Uncomment and adjust based on your needs:

/*
CREATE COMPUTE POOL NEO4J_GRAPH_ANALYTICS_POOL
    MIN_NODES = 1
    MAX_NODES = 5
    INSTANCE_FAMILY = STANDARD_1
    AUTO_SUSPEND_SECS = 300
    AUTO_RESUME = TRUE
    COMMENT = 'Compute pool for Neo4j graph analytics jobs';
*/

-- ============================================
-- 6. GRANT PERMISSIONS
-- ============================================

-- Grant necessary permissions for graph analytics
-- Adjust role names as needed

-- GRANT USAGE ON DATABASE GHOST_DETECTION TO ROLE DATA_SCIENTIST;
-- GRANT USAGE ON SCHEMA APP TO ROLE DATA_SCIENTIST;
-- GRANT SELECT ON ALL VIEWS IN SCHEMA APP TO ROLE DATA_SCIENTIST;
-- GRANT SELECT ON ALL TABLES IN SCHEMA APP TO ROLE DATA_SCIENTIST;

-- ============================================
-- 7. VALIDATION QUERIES
-- ============================================

-- Check node counts
SELECT 'Total Nodes' AS metric, COUNT(*) AS count 
FROM NEO4J_ALL_NODES
UNION ALL
SELECT 'Ghost Nodes', COUNT(*) FROM NEO4J_GHOST_NODES
UNION ALL
SELECT 'Location Nodes', COUNT(*) FROM NEO4J_LOCATION_NODES
UNION ALL
SELECT 'Investigator Nodes', COUNT(*) FROM NEO4J_INVESTIGATOR_NODES;

-- Check edge counts
SELECT 'Total Edges' AS metric, COUNT(*) AS count 
FROM NEO4J_ALL_EDGES
UNION ALL
SELECT 'Ghost Co-occurrence Edges', COUNT(*) 
FROM NEO4J_GHOST_COOCCURRENCE_EDGES
UNION ALL
SELECT 'Ghost-Location Edges', COUNT(*) 
FROM NEO4J_GHOST_LOCATION_EDGES
UNION ALL
SELECT 'Investigator-Case Edges', COUNT(*) 
FROM NEO4J_INVESTIGATOR_CASE_EDGES
UNION ALL
SELECT 'Investigation-Ghost Edges', COUNT(*) 
FROM NEO4J_INVESTIGATION_GHOST_EDGES;

-- Check graph density
SELECT 
    (SELECT COUNT(*) FROM NEO4J_ALL_EDGES) AS total_edges,
    (SELECT COUNT(*) FROM NEO4J_ALL_NODES) AS total_nodes,
    ROUND(
        (SELECT COUNT(*) FROM NEO4J_ALL_EDGES)::FLOAT / 
        NULLIF((SELECT COUNT(*) FROM NEO4J_ALL_NODES), 0),
        4
    ) AS avg_degree;

-- Preview graph structure
SELECT 
    n1.name AS from_entity,
    n1.type AS from_type,
    e.relationship_type,
    n2.name AS to_entity,
    n2.type AS to_type,
    e.weight
FROM NEO4J_ALL_EDGES e
JOIN NEO4J_ALL_NODES n1 ON e.source_node = n1.node_id
JOIN NEO4J_ALL_NODES n2 ON e.target_node = n2.node_id
LIMIT 20;

-- ============================================
-- SETUP COMPLETE
-- ============================================

SELECT 
    '✓ Neo4j Graph Analytics Setup Complete!' AS status,
    'Run sql/12_neo4j_graph_algorithms.sql for graph analytics' AS next_step;

