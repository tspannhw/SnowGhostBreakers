# 🕸️ Neo4j Graph Analytics for Ghost Detection

## 📚 Complete Guide to Graph Analytics Integration

Reference: [Neo4j Graph Analytics for Snowflake Documentation](https://neo4j.com/docs/snowflake-graph-analytics/current/)

---

## 🎯 Overview

This ghost detection application now includes **Neo4j Graph Analytics for Snowflake** to analyze:
- 👻 Ghost networks and relationships
- 📍 Location hotspots and patterns
- 🔗 Investigation connections
- 🧠 Community detection
- 📊 Centrality analysis
- 🎯 Predictive modeling

---

## 🚀 Quick Start

### 1. Install Neo4j Graph Analytics

From Snowflake Marketplace:

```sql
-- Search for "Neo4j Graph Analytics for Snowflake"
-- Install from Snowflake Marketplace UI
-- Follow provider's installation instructions
```

### 2. Run Setup Scripts

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Setup graph data structures
!source sql/11_neo4j_graph_analytics_setup.sql

-- Run graph algorithms
!source sql/12_neo4j_graph_algorithms.sql
```

### 3. Verify Installation

```sql
-- Check node counts
SELECT 'Nodes', COUNT(*) FROM NEO4J_ALL_NODES
UNION ALL
SELECT 'Edges', COUNT(*) FROM NEO4J_ALL_EDGES;

-- Preview graph structure
SELECT * FROM NEO4J_ALL_NODES LIMIT 10;
SELECT * FROM NEO4J_ALL_EDGES LIMIT 10;
```

---

## 📊 Graph Data Model

### Node Types

| Node Type | Description | Key Attributes |
|-----------|-------------|----------------|
| **Ghost** | Paranormal entities | ghost_id, name, type, threat_level |
| **Location** | Sighting locations | location_name, sighting_count |
| **Investigator** | Team members | investigator_id, name, specialization |
| **Investigation** | Active cases | investigation_id, status, priority |

### Relationship Types

| Relationship | Description | Properties |
|--------------|-------------|------------|
| **CO_OCCURS_WITH** | Ghosts appearing together | weight, shared_locations |
| **SIGHTED_AT** | Ghost → Location | weight, last_sighting |
| **WORKS_ON** | Investigator → Investigation | weight |
| **INVESTIGATES** | Investigation → Ghost | priority, status |

### Graph Structure

```
    Ghost ──SIGHTED_AT──> Location <──SIGHTED_AT── Ghost
      ↓                                               ↓
      CO_OCCURS_WITH ←→ ←→ ←→ ←→ ←→ CO_OCCURS_WITH
      ↓                                               ↓
  Investigation ←──WORKS_ON── Investigator
```

---

## 🧮 Graph Algorithms

### 1. Community Detection (Louvain)

**Purpose:** Find ghost communities and networks

```sql
-- View ghost communities
SELECT 
    community_id,
    COUNT(*) AS members,
    LISTAGG(name, ', ') AS ghost_names
FROM NEO4J_GHOST_COMMUNITIES
WHERE type = 'Ghost'
GROUP BY community_id
ORDER BY members DESC;
```

**Use Cases:**
- Identify ghost groups that operate together
- Find related paranormal phenomena
- Detect coordinated haunting patterns

**Neo4j Algorithm:**
```python
# Actual Neo4j call (when installed):
CALL gds.louvain.stream('ghost-network')
YIELD nodeId, communityId
```

### 2. PageRank Centrality

**Purpose:** Find most important/influential ghosts and locations

```sql
-- Top influential ghosts
SELECT 
    name,
    threat_level,
    ROUND(pagerank_score, 4) AS importance,
    degree AS connections
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Ghost'
ORDER BY pagerank_score DESC
LIMIT 10;

-- Paranormal hotspots
SELECT 
    name AS location,
    ROUND(pagerank_score, 4) AS importance,
    degree AS activity_level
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Location'
ORDER BY pagerank_score DESC
LIMIT 10;
```

**Insights:**
- 🎯 High PageRank = Central to network
- 📍 Hotspot locations require priority attention
- 🔗 Hub ghosts may influence others

**Neo4j Algorithm:**
```python
CALL gds.pageRank.stream('ghost-network')
YIELD nodeId, score
```

### 3. Betweenness Centrality

**Purpose:** Find "bridge" entities connecting different network parts

```sql
-- Critical bridge ghosts/locations
SELECT 
    name,
    type,
    ROUND(betweenness_score, 4) AS bridge_importance,
    CASE 
        WHEN betweenness_score > 30 THEN 'Critical Bridge'
        WHEN betweenness_score > 15 THEN 'Important Bridge'
        ELSE 'Normal'
    END AS classification
FROM NEO4J_BETWEENNESS_CENTRALITY
WHERE betweenness_score > 10
ORDER BY betweenness_score DESC;
```

**Tactical Value:**
- 🎯 Target bridge entities to disrupt network
- 🔗 Monitor critical connection points
- 📊 Understand information flow

**Neo4j Algorithm:**
```python
CALL gds.betweenness.stream('ghost-network')
YIELD nodeId, score
```

### 4. Connected Components

**Purpose:** Find isolated ghost networks

```sql
-- Analyze disconnected networks
SELECT 
    component_id,
    COUNT(*) AS size,
    COUNT(CASE WHEN type = 'Ghost' THEN 1 END) AS ghosts,
    LISTAGG(CASE WHEN type = 'Ghost' THEN name END, ', ') AS members
FROM NEO4J_CONNECTED_COMPONENTS
GROUP BY component_id
ORDER BY size DESC;
```

**Strategic Insights:**
- 🔍 Separate ghost networks = different phenomena
- 🎯 Each component may require different strategies
- 📊 Track network evolution over time

**Neo4j Algorithm:**
```python
CALL gds.wcc.stream('ghost-network')
YIELD nodeId, componentId
```

### 5. Node Similarity (K-Nearest Neighbors)

**Purpose:** Find similar ghosts based on behavior patterns

```sql
-- Most similar ghost pairs
SELECT 
    ghost_1_name,
    ghost_2_name,
    ROUND(similarity_score, 4) AS similarity,
    shared_locations,
    CASE 
        WHEN shared_locations >= 3 THEN 'Highly Related'
        WHEN shared_locations >= 2 THEN 'Related'
        ELSE 'Possibly Related'
    END AS relationship
FROM NEO4J_GHOST_SIMILARITY
WHERE similarity_score > 0.5
ORDER BY similarity_score DESC
LIMIT 20;
```

**Applications:**
- 🎯 Predict ghost behavior from similar entities
- 📊 Group ghosts for batch containment
- 🔍 Discover hidden relationships

**Neo4j Algorithm:**
```python
CALL gds.knn.stream('ghost-network', {topK: 5})
YIELD node1, node2, similarity
```

### 6. Shortest Path (Dijkstra)

**Purpose:** Find connections between ghosts through locations

```sql
-- Find path between two ghosts
SELECT * 
FROM TABLE(FIND_GHOST_CONNECTION_PATH('GH001', 'GH005'));
```

**Use Cases:**
- 🔍 Trace ghost influence chains
- 📍 Identify transmission paths
- 🎯 Plan intervention points

**Neo4j Algorithm:**
```python
CALL gds.shortestPath.dijkstra.stream('ghost-network', {
    sourceNode: source_ghost_id,
    targetNode: target_ghost_id
})
```

### 7. Triangle Count

**Purpose:** Detect clustering patterns (ghost-location-ghost)

```sql
-- Find high-activity triangle patterns
SELECT 
    location_name,
    COUNT(DISTINCT ghost_1 || '-' || ghost_2) AS ghost_pairs,
    SUM(triangle_count) AS total_triangles
FROM NEO4J_TRIANGLE_PATTERNS
GROUP BY location_name
ORDER BY total_triangles DESC
LIMIT 10;
```

**Insights:**
- 🔺 High triangle count = tight-knit community
- 📍 Locations with many triangles = hotspots
- 🎯 Clustering coefficient indicates network density

**Neo4j Algorithm:**
```python
CALL gds.triangleCount.stream('ghost-network')
YIELD nodeId, triangleCount
```

### 8. Node2Vec Embeddings

**Purpose:** Generate ML embeddings for AI analysis

```sql
-- Find similar ghosts using embeddings
SELECT 
    entity_1,
    entity_2,
    ROUND(similarity, 4) AS embedding_similarity
FROM NEO4J_EMBEDDING_SIMILARITY
WHERE type_1 = 'Ghost' AND type_2 = 'Ghost'
ORDER BY similarity DESC
LIMIT 20;
```

**Advanced Use Cases:**
- 🧠 Feed embeddings to ML models
- 🎯 Predict ghost behavior
- 📊 Cluster similar entities
- 🔍 Anomaly detection

**Neo4j Algorithm:**
```python
CALL gds.node2vec.stream('ghost-network', {
    embeddingDimension: 128,
    walkLength: 80,
    iterations: 10
})
YIELD nodeId, embedding
```

### 9. GraphSAGE (ML Classification)

**Purpose:** Train ML models on graph structure

```sql
-- View training data
SELECT * FROM NEO4J_GRAPHSAGE_TRAINING_DATA;
```

**ML Applications:**
- 🎯 Classify threat levels
- 🧠 Predict ghost behavior
- 📊 Feature learning from graph structure
- 🔍 Transfer learning across ghost types

**Neo4j Algorithm:**
```python
CALL gds.beta.graphSage.train('ghost-network', {
    modelName: 'ghost-threat-classifier',
    featureProperties: ['sighting_count', 'evidence_count'],
    projectedFeatureDimension: 64
})
```

---

## 🎯 Complete Network Analysis

### Comprehensive Ghost Network Insights

```sql
-- Get full network analysis for all ghosts
SELECT 
    ghost_name,
    ghost_type,
    threat_level,
    network_role,
    importance_score,
    connection_count,
    bridge_score,
    community,
    unique_locations,
    total_sightings
FROM NEO4J_GHOST_NETWORK_INSIGHTS
ORDER BY importance_score DESC;
```

### AI-Powered Recommendations

```sql
-- Get tactical AI recommendations based on network position
SELECT GET_GRAPH_INSIGHTS_AI('GH001');
```

**Example Output:**
```
"Based on network analysis, this entity is a Critical Bridge with high betweenness 
centrality (35.7). It connects 3 separate ghost communities. Recommendation: 
Prioritize containment to disrupt network. Coordinate with investigators monitoring 
connected entities. Deploy specialized equipment for Community 2 ghost types."
```

---

## 📊 Visualization

### Python Visualization

Use the provided Python script for interactive visualizations:

```bash
python scripts/neo4j_graph_visualization.py
```

**Generated Visualizations:**
1. 🕸️ **Interactive Network Graph** - Explore connections
2. 👥 **Community Detection** - See ghost groups
3. 📊 **Importance Ranking** - Top ghosts by PageRank
4. 🗺️ **Hotspot Map** - Location analysis

### Outputs

```
ghost_network_interactive.html    - Interactive network (Plotly)
ghost_communities.html             - Community analysis
ghost_importance_ranking.html      - Centrality scores
paranormal_hotspots.html          - Location hotspots
ghost_graph_export.json           - Data export for Neo4j
```

---

## 🔧 Advanced Configuration

### Create Graph Projections

```python
-- In Neo4j Graph Analytics (after installation)
CALL gds.graph.project(
    'ghost-network',              -- Graph name
    'NEO4J_ALL_NODES',            -- Node table
    'NEO4J_ALL_EDGES',            -- Edge table
    {
        nodeProperties: ['type', 'threat_level'],
        relationshipProperties: ['weight']
    }
);
```

### Create Compute Pool

```sql
CREATE COMPUTE POOL NEO4J_GRAPH_ANALYTICS_POOL
    MIN_NODES = 1
    MAX_NODES = 5
    INSTANCE_FAMILY = STANDARD_1
    AUTO_SUSPEND_SECS = 300
    AUTO_RESUME = TRUE
    COMMENT = 'For graph analytics jobs';
```

### Run Algorithms at Scale

```python
-- PageRank with configuration
CALL gds.pageRank.stream('ghost-network', {
    maxIterations: 20,
    dampingFactor: 0.85,
    relationshipWeightProperty: 'weight'
})
YIELD nodeId, score
```

---

## 📈 Use Cases

### 1. 🎯 Threat Assessment

```sql
-- Identify highest priority threats based on network position
SELECT 
    ghost_name,
    threat_level,
    importance_score,
    network_role,
    CASE 
        WHEN network_role = 'Network Hub' THEN 'Critical Priority'
        WHEN network_role = 'Critical Bridge' THEN 'High Priority'
        ELSE 'Standard Priority'
    END AS action_priority
FROM NEO4J_GHOST_NETWORK_INSIGHTS
WHERE threat_level IN ('Extreme', 'High')
ORDER BY importance_score DESC;
```

### 2. 📍 Resource Allocation

```sql
-- Optimize investigator deployment to hotspots
SELECT 
    l.name AS location,
    l.pagerank_score AS importance,
    COUNT(DISTINCT i.investigator_id) AS current_investigators,
    CASE 
        WHEN l.pagerank_score > 50 AND COUNT(i.investigator_id) < 2 
        THEN 'NEEDS MORE RESOURCES'
        ELSE 'Adequately Staffed'
    END AS staffing_status
FROM NEO4J_GHOST_PAGERANK l
LEFT JOIN GHOST_SIGHTINGS gs ON l.name = gs.location_name
LEFT JOIN INVESTIGATIONS inv ON gs.ghost_id = inv.ghost_id
LEFT JOIN INVESTIGATORS i ON inv.investigator_id = i.investigator_id
WHERE l.type = 'Location'
GROUP BY l.name, l.pagerank_score
ORDER BY importance DESC;
```

### 3. 🔍 Pattern Discovery

```sql
-- Find emerging ghost networks (new communities)
WITH new_sightings AS (
    SELECT ghost_id 
    FROM GHOST_SIGHTINGS 
    WHERE sighting_datetime > DATEADD(day, -7, CURRENT_TIMESTAMP())
)
SELECT 
    c.community_id,
    COUNT(DISTINCT ns.ghost_id) AS new_ghosts_in_community,
    COUNT(DISTINCT c.node_id) AS total_community_size,
    ROUND(COUNT(DISTINCT ns.ghost_id)::FLOAT / 
          COUNT(DISTINCT c.node_id) * 100, 2) AS percent_new
FROM NEO4J_GHOST_COMMUNITIES c
LEFT JOIN new_sightings ns ON c.node_id = ns.ghost_id
GROUP BY c.community_id
HAVING percent_new > 20
ORDER BY new_ghosts_in_community DESC;
```

### 4. 🎯 Containment Strategy

```sql
-- Identify optimal intervention points (bridge ghosts)
SELECT 
    g.ghost_name,
    g.threat_level,
    bc.betweenness_score AS bridge_importance,
    c.community_id,
    pr.pagerank_score AS influence,
    CONCAT(
        'Targeting ', g.ghost_name, 
        ' will disconnect ', 
        FLOOR(bc.betweenness_score / 10), 
        ' sub-networks'
    ) AS tactical_value
FROM NEO4J_BETWEENNESS_CENTRALITY bc
JOIN GHOSTS g ON bc.node_id = g.ghost_id
JOIN NEO4J_GHOST_COMMUNITIES c ON bc.node_id = c.node_id
JOIN NEO4J_GHOST_PAGERANK pr ON bc.node_id = pr.node_id
WHERE bc.betweenness_score > 15
  AND g.status = 'Active'
ORDER BY bc.betweenness_score DESC
LIMIT 10;
```

---

## 🧪 Testing Graph Analytics

### Validate Graph Structure

```sql
-- Check for orphaned nodes
SELECT 
    n.node_id,
    n.name,
    n.type
FROM NEO4J_ALL_NODES n
LEFT JOIN NEO4J_ALL_EDGES e1 ON n.node_id = e1.source_node
LEFT JOIN NEO4J_ALL_EDGES e2 ON n.node_id = e2.target_node
WHERE e1.source_node IS NULL AND e2.target_node IS NULL;

-- Check edge consistency
SELECT 
    COUNT(*) AS edges_with_missing_nodes
FROM NEO4J_ALL_EDGES e
LEFT JOIN NEO4J_ALL_NODES n1 ON e.source_node = n1.node_id
LEFT JOIN NEO4J_ALL_NODES n2 ON e.target_node = n2.node_id
WHERE n1.node_id IS NULL OR n2.node_id IS NULL;

-- Graph metrics
SELECT 
    'Nodes' AS metric,
    COUNT(*) AS value
FROM NEO4J_ALL_NODES
UNION ALL
SELECT 'Edges', COUNT(*) FROM NEO4J_ALL_EDGES
UNION ALL
SELECT 'Avg Degree', 
       ROUND(COUNT(*)::FLOAT * 2 / (SELECT COUNT(*) FROM NEO4J_ALL_NODES), 2)
FROM NEO4J_ALL_EDGES;
```

---

## 📚 Best Practices

### 1. ✅ Data Quality

- Ensure node IDs are unique
- Validate all edges reference valid nodes
- Regularly update graph projections
- Monitor for orphaned nodes

### 2. ⚡ Performance

- Use compute pools for large graphs
- Create appropriate indexes
- Limit result sets for interactive queries
- Cache frequently used projections

### 3. 🎯 Algorithm Selection

| Goal | Best Algorithm |
|------|----------------|
| Find communities | Louvain, Leiden |
| Identify important nodes | PageRank, Degree Centrality |
| Find bridges | Betweenness Centrality |
| Discover patterns | Triangle Count, Clustering |
| ML features | Node2Vec, GraphSAGE |
| Path analysis | Dijkstra, BFS |
| Similarity | KNN, Node Similarity |

### 4. 🔄 Update Frequency

```sql
-- Refresh graph daily
CREATE OR REPLACE TASK REFRESH_GRAPH_PROJECTIONS
    WAREHOUSE = GHOST_WAREHOUSE
    SCHEDULE = 'USING CRON 0 2 * * * UTC'  -- 2 AM daily
AS
    CREATE OR REPLACE TABLE NEO4J_GHOST_NETWORK_PROJECTION AS
    SELECT * FROM NEO4J_ALL_EDGES;
```

---

## 🔗 Resources

- **Neo4j Docs:** https://neo4j.com/docs/snowflake-graph-analytics/current/
- **Algorithms Guide:** https://neo4j.com/docs/snowflake-graph-analytics/current/graph-algorithms/
- **Visualization:** https://neo4j.com/docs/snowflake-graph-analytics/current/visualization/
- **Scaling Guide:** https://neo4j.com/docs/snowflake-graph-analytics/current/scaling-out-jobs/

---

## ✅ Summary

### What You Get

✅ **10+ Graph Algorithms** ready to use  
✅ **Community Detection** for ghost networks  
✅ **Centrality Analysis** for threat prioritization  
✅ **ML Embeddings** for predictive modeling  
✅ **Interactive Visualizations** in Python  
✅ **AI-Powered Insights** via Cortex  
✅ **Scalable Architecture** with compute pools  
✅ **Production-Ready** SQL scripts  

### Quick Commands

```sql
-- Setup
!source sql/11_neo4j_graph_analytics_setup.sql

-- Run algorithms
!source sql/12_neo4j_graph_algorithms.sql

-- Get insights
SELECT * FROM NEO4J_GHOST_NETWORK_INSIGHTS ORDER BY importance_score DESC;

-- AI recommendations
SELECT GET_GRAPH_INSIGHTS_AI('GH001');
```

---

**Status:** ✅ **Graph Analytics Integrated**  
**Files Created:** 3 (2 SQL, 1 Python, 1 Guide)  
**Algorithms:** 10+ Graph Analytics Algorithms  
**Date:** October 16, 2025  

🕸️👻✨ **Your ghost detection network is now graph-powered!**

