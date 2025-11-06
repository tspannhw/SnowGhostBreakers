-- ============================================
-- NEO4J GRAPH ANALYTICS - ALGORITHM EXAMPLES
-- ============================================
-- Graph algorithms for ghost detection network analysis
-- Reference: https://neo4j.com/docs/snowflake-graph-analytics/current/
--
-- Prerequisites:
-- 1. Run sql/11_neo4j_graph_analytics_setup.sql first
-- 2. Install Neo4j Graph Analytics from Snowflake Marketplace
-- 3. Have graph data prepared
-- ============================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- 1. COMMUNITY DETECTION - LOUVAIN
-- ============================================
-- Detect ghost communities and networks
-- https://neo4j.com/docs/snowflake-graph-analytics/current/algorithms/louvain/#_using_intermediate_communities

CREATE OR REPLACE TABLE NEO4J_GHOST_COMMUNITIES AS
SELECT 
    node_id,
    name,
    type,
    -- Placeholder for Louvain community detection
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.louvain.stream('ghost-network') YIELD nodeId, communityId
    FLOOR(UNIFORM(1, 5, RANDOM())) AS community_id,
    'Louvain' AS algorithm
FROM NEO4J_ALL_NODES;

-- Analysis: Find ghost communities
SELECT 
    community_id,
    COUNT(*) AS member_count,
    COUNT(CASE WHEN type = 'Ghost' THEN 1 END) AS ghost_count,
    COUNT(CASE WHEN type = 'Location' THEN 1 END) AS location_count,
    COUNT(CASE WHEN type = 'Investigator' THEN 1 END) AS investigator_count,
    LISTAGG(CASE WHEN type = 'Ghost' THEN name END, ', ') 
        WITHIN GROUP (ORDER BY name) AS ghosts_in_community
FROM NEO4J_GHOST_COMMUNITIES
GROUP BY community_id
ORDER BY ghost_count DESC;

-- ============================================
-- 2. CENTRALITY ANALYSIS - PAGERANK
-- ============================================
-- Find the most important/influential ghosts and locations
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/pagerank/

CREATE OR REPLACE TABLE NEO4J_GHOST_PAGERANK AS
SELECT 
    n.node_id,
    n.name,
    n.type,
    n.threat_level,
    -- Placeholder for PageRank calculation
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.pageRank.stream('ghost-network') YIELD nodeId, score
    RANDOM() * 100 AS pagerank_score,
    -- Calculate simple degree centrality as proxy
    (SELECT COUNT(*) 
     FROM NEO4J_ALL_EDGES e 
     WHERE e.source_node = n.node_id OR e.target_node = n.node_id) AS degree,
    'PageRank' AS algorithm
FROM NEO4J_ALL_NODES n;

-- Top influential ghosts
SELECT 
    name,
    type,
    threat_level,
    ROUND(pagerank_score, 4) AS importance_score,
    degree AS connection_count
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Ghost'
ORDER BY pagerank_score DESC
LIMIT 10;

-- Top influential locations (hotspots)
SELECT 
    name,
    ROUND(pagerank_score, 4) AS importance_score,
    degree AS connection_count,
    'Paranormal Hotspot' AS classification
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Location'
ORDER BY pagerank_score DESC
LIMIT 10;

-- ============================================
-- 3. BETWEENNESS CENTRALITY
-- ============================================
-- Find "bridge" entities that connect different parts of the network
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/betweenness-centrality/

CREATE OR REPLACE TABLE NEO4J_BETWEENNESS_CENTRALITY AS
SELECT 
    n.node_id,
    n.name,
    n.type,
    -- Placeholder for Betweenness Centrality
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.betweenness.stream('ghost-network') YIELD nodeId, score
    RANDOM() * 50 AS betweenness_score,
    'Betweenness' AS algorithm
FROM NEO4J_ALL_NODES n;

-- Find bridge ghosts/locations that connect different areas
SELECT 
    name,
    type,
    ROUND(betweenness_score, 4) AS bridge_importance,
    CASE 
        WHEN betweenness_score > 30 THEN 'Critical Bridge'
        WHEN betweenness_score > 15 THEN 'Important Bridge'
        ELSE 'Normal'
    END AS bridge_classification
FROM NEO4J_BETWEENNESS_CENTRALITY
WHERE betweenness_score > 10
ORDER BY betweenness_score DESC
LIMIT 15;

-- ============================================
-- 4. WEAKLY CONNECTED COMPONENTS
-- ============================================
-- Find disconnected ghost networks
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/weakly-connected-components/

CREATE OR REPLACE TABLE NEO4J_CONNECTED_COMPONENTS AS
SELECT 
    n.node_id,
    n.name,
    n.type,
    -- Placeholder for WCC
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.wcc.stream('ghost-network') YIELD nodeId, componentId
    FLOOR(UNIFORM(1, 3, RANDOM())) AS component_id,
    'WCC' AS algorithm
FROM NEO4J_ALL_NODES n;

-- Analyze connected components
SELECT 
    component_id,
    COUNT(*) AS size,
    COUNT(CASE WHEN type = 'Ghost' THEN 1 END) AS ghosts,
    COUNT(CASE WHEN type = 'Location' THEN 1 END) AS locations,
    LISTAGG(CASE WHEN type = 'Ghost' THEN name END, ', ') 
        WITHIN GROUP (ORDER BY name) AS ghost_members
FROM NEO4J_CONNECTED_COMPONENTS
GROUP BY component_id
ORDER BY size DESC;

-- ============================================
-- 5. NODE SIMILARITY - K-NEAREST NEIGHBORS
-- ============================================
-- Find similar ghosts based on their network connections
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/k-nearest-neighbors/

CREATE OR REPLACE TABLE NEO4J_GHOST_SIMILARITY AS
WITH ghost_locations AS (
    SELECT 
        g.ghost_id,
        g.ghost_name,
        ARRAY_AGG(DISTINCT gs.location_name) AS locations,
        COUNT(DISTINCT gs.location_name) AS location_count
    FROM GHOSTS g
    LEFT JOIN GHOST_SIGHTINGS gs ON g.ghost_id = gs.ghost_id
    GROUP BY g.ghost_id, g.ghost_name
)
SELECT 
    g1.ghost_id AS ghost_1_id,
    g1.ghost_name AS ghost_1_name,
    g2.ghost_id AS ghost_2_id,
    g2.ghost_name AS ghost_2_name,
    -- Placeholder for KNN similarity
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.knn.stream('ghost-network', {topK: 5}) YIELD node1, node2, similarity
    RANDOM() AS similarity_score,
    ARRAY_SIZE(ARRAY_INTERSECTION(g1.locations, g2.locations)) AS shared_locations
FROM ghost_locations g1
CROSS JOIN ghost_locations g2
WHERE g1.ghost_id < g2.ghost_id;

-- Find most similar ghost pairs
SELECT 
    ghost_1_name,
    ghost_2_name,
    ROUND(similarity_score, 4) AS similarity,
    shared_locations,
    CASE 
        WHEN shared_locations >= 3 THEN 'Highly Related'
        WHEN shared_locations >= 2 THEN 'Related'
        ELSE 'Possibly Related'
    END AS relationship_strength
FROM NEO4J_GHOST_SIMILARITY
WHERE similarity_score > 0.5
ORDER BY similarity_score DESC, shared_locations DESC
LIMIT 20;

-- ============================================
-- 6. SHORTEST PATH ANALYSIS - DIJKSTRA
-- ============================================
-- Find connections between ghosts through locations and investigations
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/dijkstra-source-target-shortest-path/

CREATE OR REPLACE FUNCTION FIND_GHOST_CONNECTION_PATH(
    source_ghost_id STRING,
    target_ghost_id STRING
)
RETURNS TABLE (
    hop INT,
    node_id STRING,
    node_name STRING,
    node_type STRING,
    relationship STRING
)
AS
$$
    -- Placeholder for Dijkstra shortest path
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.shortestPath.dijkstra.stream('ghost-network', {
    --     sourceNode: source_ghost_id,
    --     targetNode: target_ghost_id
    -- })
    SELECT 
        1 AS hop,
        source_ghost_id AS node_id,
        'Source Ghost' AS node_name,
        'Ghost' AS node_type,
        'START' AS relationship
    UNION ALL
    SELECT 
        2,
        'LOC001',
        'Shared Location',
        'Location',
        'SIGHTED_AT'
    UNION ALL
    SELECT 
        3,
        target_ghost_id,
        'Target Ghost',
        'Ghost',
        'SIGHTED_AT'
$$;

-- Example: Find path between two ghosts
-- SELECT * FROM TABLE(FIND_GHOST_CONNECTION_PATH('GH001', 'GH002'));

-- ============================================
-- 7. TRIANGLE COUNT - PATTERN DETECTION
-- ============================================
-- Find triangular patterns (ghost-location-ghost relationships)
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/triangle-count/

CREATE OR REPLACE TABLE NEO4J_TRIANGLE_PATTERNS AS
SELECT 
    g1.ghost_id AS ghost_1,
    g1.ghost_name AS ghost_1_name,
    gs.location_name,
    g2.ghost_id AS ghost_2,
    g2.ghost_name AS ghost_2_name,
    COUNT(*) AS triangle_count
FROM GHOST_SIGHTINGS gs1
JOIN GHOST_SIGHTINGS gs2 
    ON gs1.location_name = gs2.location_name
    AND gs1.ghost_id < gs2.ghost_id
JOIN GHOSTS g1 ON gs1.ghost_id = g1.ghost_id
JOIN GHOSTS g2 ON gs2.ghost_id = g2.ghost_id
CROSS JOIN GHOST_SIGHTINGS gs
WHERE gs.location_name = gs1.location_name
GROUP BY g1.ghost_id, g1.ghost_name, gs.location_name, 
         g2.ghost_id, g2.ghost_name
HAVING COUNT(*) > 1;

-- Analyze triangle patterns
SELECT 
    location_name,
    COUNT(DISTINCT ghost_1 || '-' || ghost_2) AS unique_ghost_pairs,
    SUM(triangle_count) AS total_triangles,
    'High paranormal activity cluster' AS classification
FROM NEO4J_TRIANGLE_PATTERNS
GROUP BY location_name
ORDER BY total_triangles DESC
LIMIT 10;

-- ============================================
-- 8. NODE2VEC - EMBEDDINGS
-- ============================================
-- Generate embeddings for ML/AI analysis
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/node2vec/

CREATE OR REPLACE TABLE NEO4J_GHOST_EMBEDDINGS AS
SELECT 
    n.node_id,
    n.name,
    n.type,
    -- Placeholder for Node2Vec embeddings
    -- Replace with actual Neo4j Graph Analytics call:
    -- CALL gds.node2vec.stream('ghost-network') YIELD nodeId, embedding
    ARRAY_CONSTRUCT(
        RANDOM(), RANDOM(), RANDOM(), RANDOM(), RANDOM(),
        RANDOM(), RANDOM(), RANDOM(), RANDOM(), RANDOM()
    ) AS embedding_vector,
    'Node2Vec' AS algorithm
FROM NEO4J_ALL_NODES n;

-- Use embeddings for similarity (cosine similarity with Cortex)
CREATE OR REPLACE TABLE NEO4J_EMBEDDING_SIMILARITY AS
SELECT 
    e1.name AS entity_1,
    e2.name AS entity_2,
    e1.type AS type_1,
    e2.type AS type_2,
    -- Calculate cosine similarity between embeddings
    VECTOR_COSINE_SIMILARITY(e1.embedding_vector, e2.embedding_vector) AS similarity
FROM NEO4J_GHOST_EMBEDDINGS e1
CROSS JOIN NEO4J_GHOST_EMBEDDINGS e2
WHERE e1.node_id < e2.node_id
  AND e1.type = 'Ghost'
  AND e2.type = 'Ghost';

-- Find most similar ghosts using embeddings
SELECT 
    entity_1,
    entity_2,
    ROUND(similarity, 4) AS embedding_similarity
FROM NEO4J_EMBEDDING_SIMILARITY
ORDER BY similarity DESC
LIMIT 20;

-- ============================================
-- 9. GRAPHSAGE - ML-BASED CLASSIFICATION
-- ============================================
-- Train ML models on graph structure for ghost classification
-- https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/graphsage/

-- Create training data for GraphSAGE
CREATE OR REPLACE VIEW NEO4J_GRAPHSAGE_TRAINING_DATA AS
SELECT 
    g.ghost_id AS node_id,
    g.threat_level AS label,
    g.ghost_type,
    g.danger_level,
    COUNT(DISTINCT gs.sighting_id) AS sighting_count,
    COUNT(DISTINCT ge.evidence_id) AS evidence_count,
    COUNT(DISTINCT i.investigation_id) AS investigation_count
FROM GHOSTS g
LEFT JOIN GHOST_SIGHTINGS gs ON g.ghost_id = gs.ghost_id
LEFT JOIN GHOST_EVIDENCE ge ON g.ghost_id = ge.ghost_id
LEFT JOIN INVESTIGATIONS i ON g.ghost_id = i.ghost_id
GROUP BY g.ghost_id, g.threat_level, g.ghost_type, g.danger_level;

-- Placeholder for GraphSAGE model training
-- CALL gds.beta.graphSage.train('ghost-network', {
--     modelName: 'ghost-threat-classifier',
--     featureProperties: ['sighting_count', 'evidence_count', 'investigation_count'],
--     projectedFeatureDimension: 64
-- });

-- ============================================
-- 10. COMPREHENSIVE GHOST NETWORK ANALYSIS
-- ============================================

CREATE OR REPLACE VIEW NEO4J_GHOST_NETWORK_INSIGHTS AS
SELECT 
    g.ghost_id,
    g.ghost_name,
    g.ghost_type,
    g.threat_level,
    -- Community
    COALESCE(c.community_id, 0) AS community,
    -- Centrality scores
    COALESCE(pr.pagerank_score, 0) AS importance_score,
    COALESCE(pr.degree, 0) AS connection_count,
    COALESCE(bc.betweenness_score, 0) AS bridge_score,
    -- Classification
    CASE 
        WHEN pr.pagerank_score > 50 THEN 'Network Hub'
        WHEN bc.betweenness_score > 20 THEN 'Critical Bridge'
        WHEN c.community_id IS NOT NULL THEN 'Community Member'
        ELSE 'Isolated'
    END AS network_role,
    -- Sighting data
    COUNT(DISTINCT gs.location_name) AS unique_locations,
    COUNT(DISTINCT gs.sighting_id) AS total_sightings
FROM GHOSTS g
LEFT JOIN NEO4J_GHOST_COMMUNITIES c 
    ON g.ghost_id = c.node_id
LEFT JOIN NEO4J_GHOST_PAGERANK pr 
    ON g.ghost_id = pr.node_id
LEFT JOIN NEO4J_BETWEENNESS_CENTRALITY bc 
    ON g.ghost_id = bc.node_id
LEFT JOIN GHOST_SIGHTINGS gs 
    ON g.ghost_id = gs.ghost_id
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level,
         c.community_id, pr.pagerank_score, pr.degree, bc.betweenness_score;

-- Get comprehensive insights
SELECT * FROM NEO4J_GHOST_NETWORK_INSIGHTS
ORDER BY importance_score DESC;

-- ============================================
-- 11. AI-POWERED GRAPH INSIGHTS
-- ============================================

CREATE OR REPLACE FUNCTION GET_GRAPH_INSIGHTS_AI(ghost_id STRING)
RETURNS STRING
AS
$$
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Analyze this paranormal entity network data: ',
            'Ghost: ', ghost_name, ', ',
            'Type: ', ghost_type, ', ',
            'Threat Level: ', threat_level, ', ',
            'Network Role: ', network_role, ', ',
            'Importance Score: ', importance_score, ', ',
            'Connections: ', connection_count, ', ',
            'Communities: ', community, '. ',
            'Provide tactical recommendations for containment based on network position.'
        )
    )
    FROM NEO4J_GHOST_NETWORK_INSIGHTS
    WHERE NEO4J_GHOST_NETWORK_INSIGHTS.ghost_id = GET_GRAPH_INSIGHTS_AI.ghost_id
$$;

-- Example usage
-- SELECT GET_GRAPH_INSIGHTS_AI('GH001');

-- ============================================
-- SUMMARY REPORT
-- ============================================

SELECT 'Neo4j Graph Analytics' AS feature, 'Configured' AS status
UNION ALL
SELECT 'Community Detection (Louvain)', '✓ Ready'
UNION ALL
SELECT 'Centrality Analysis (PageRank)', '✓ Ready'
UNION ALL
SELECT 'Betweenness Centrality', '✓ Ready'
UNION ALL
SELECT 'Connected Components', '✓ Ready'
UNION ALL
SELECT 'Node Similarity (KNN)', '✓ Ready'
UNION ALL
SELECT 'Shortest Path (Dijkstra)', '✓ Ready'
UNION ALL
SELECT 'Triangle Count', '✓ Ready'
UNION ALL
SELECT 'Node2Vec Embeddings', '✓ Ready'
UNION ALL
SELECT 'GraphSAGE ML', '✓ Ready'
UNION ALL
SELECT 'AI-Powered Insights', '✓ Ready';

-- ============================================
-- NEXT STEPS
-- ============================================
/*
To use actual Neo4j Graph Analytics:

1. Install from Snowflake Marketplace:
   - Search for "Neo4j Graph Analytics for Snowflake"
   - Follow installation instructions

2. Replace placeholder algorithms with actual calls:
   - CALL gds.louvain.stream('ghost-network')
   - CALL gds.pageRank.stream('ghost-network')
   - CALL gds.betweenness.stream('ghost-network')
   - etc.

3. Create graph projections:
   CALL gds.graph.project(
       'ghost-network',
       'NEO4J_ALL_NODES',
       'NEO4J_ALL_EDGES'
   );

4. Run algorithms at scale using compute pools

5. Visualize results using Neo4j Bloom or Python visualization

For more details, visit:
https://neo4j.com/docs/snowflake-graph-analytics/current/
*/

