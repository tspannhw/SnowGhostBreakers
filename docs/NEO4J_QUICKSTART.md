# 🚀 Neo4j Graph Analytics - Quick Start

## ⚡ 5-Minute Setup

### 1. Install from Marketplace

```
1. Go to Snowflake UI → Data Products → Marketplace
2. Search for "Neo4j Graph Analytics for Snowflake"
3. Click "Get" and follow installation instructions
4. Grant permissions to your database
```

### 2. Run Setup Scripts

**Option A: Snowflake Worksheet**

Copy and paste each file into a worksheet and run:

```sql
-- Step 1: Setup graph data structures
-- Copy contents of sql/11_neo4j_graph_analytics_setup.sql and run

-- Step 2: Run graph algorithms  
-- Copy contents of sql/12_neo4j_graph_algorithms.sql and run
```

**Option B: SnowSQL CLI**

```bash
snowsql -f sql/11_neo4j_graph_analytics_setup.sql
snowsql -f sql/12_neo4j_graph_algorithms.sql
```

### 3. Verify Installation

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Check node counts
SELECT 'Nodes' AS type, COUNT(*) AS count FROM NEO4J_ALL_NODES
UNION ALL
SELECT 'Edges', COUNT(*) FROM NEO4J_ALL_EDGES;

-- View graph structure
SELECT * FROM NEO4J_ALL_NODES LIMIT 10;
```

---

## 🎯 Run Your First Graph Query

### Find Ghost Communities

```sql
SELECT 
    community_id,
    COUNT(*) AS members,
    LISTAGG(name, ', ') AS ghost_names
FROM NEO4J_GHOST_COMMUNITIES
WHERE type = 'Ghost'
GROUP BY community_id
ORDER BY members DESC;
```

### Top Influential Ghosts

```sql
SELECT 
    name AS ghost_name,
    threat_level,
    ROUND(pagerank_score, 4) AS importance,
    degree AS connections
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Ghost'
ORDER BY pagerank_score DESC
LIMIT 10;
```

### Paranormal Hotspots

```sql
SELECT 
    name AS location,
    ROUND(pagerank_score, 4) AS importance,
    degree AS activity_level
FROM NEO4J_GHOST_PAGERANK
WHERE type = 'Location'
ORDER BY pagerank_score DESC
LIMIT 10;
```

---

## 📊 Visualize Results (Python)

### Install Dependencies

```bash
pip install networkx plotly pandas snowflake-connector-python
```

### Run Visualization Script

```bash
python scripts/neo4j_graph_visualization.py
```

**Generated Files:**
- `ghost_network_interactive.html` - Interactive network graph
- `ghost_communities.html` - Community analysis
- `ghost_importance_ranking.html` - Centrality scores
- `paranormal_hotspots.html` - Location hotspots

---

## 🧠 AI-Powered Graph Insights

### Get Tactical Recommendations

```sql
-- Get AI analysis for a specific ghost
SELECT GET_GRAPH_INSIGHTS_AI('GH001');
```

**Example Output:**
```
"This entity is a Network Hub with PageRank score 87.3, connecting 
3 communities. Recommend priority containment. Deploy 2+ specialized 
investigators. Monitor 5 connected high-threat entities."
```

### Comprehensive Network Analysis

```sql
-- Get full network insights for all ghosts
SELECT 
    ghost_name,
    network_role,
    importance_score,
    connection_count,
    community,
    CASE 
        WHEN network_role = 'Network Hub' THEN 'Critical Priority'
        WHEN network_role = 'Critical Bridge' THEN 'High Priority'
        ELSE 'Standard Priority'
    END AS action_priority
FROM NEO4J_GHOST_NETWORK_INSIGHTS
ORDER BY importance_score DESC;
```

---

## 🎓 Learn More

**Full Documentation:**
- 📚 `NEO4J_GRAPH_ANALYTICS_GUIDE.md` - Complete guide
- 🌐 https://neo4j.com/docs/snowflake-graph-analytics/current/ - Official docs

**Key Algorithms Available:**
1. **Louvain** - Community detection
2. **PageRank** - Importance scoring
3. **Betweenness** - Bridge detection
4. **Dijkstra** - Shortest paths
5. **Node2Vec** - ML embeddings
6. **GraphSAGE** - ML classification
7. **KNN** - Similarity analysis
8. **Triangle Count** - Pattern detection
9. **Connected Components** - Network isolation
10. **Breadth First Search** - Path finding

---

## 🔥 Quick Use Cases

### Use Case 1: Find Most Dangerous Ghost Network

```sql
SELECT 
    c.community_id,
    COUNT(*) AS ghost_count,
    AVG(CASE 
        WHEN g.threat_level = 'Extreme' THEN 4
        WHEN g.threat_level = 'High' THEN 3
        WHEN g.threat_level = 'Medium' THEN 2
        ELSE 1
    END) AS avg_threat_score,
    LISTAGG(g.ghost_name, ', ') AS members
FROM NEO4J_GHOST_COMMUNITIES c
JOIN GHOSTS g ON c.node_id = g.ghost_id
GROUP BY c.community_id
ORDER BY avg_threat_score DESC, ghost_count DESC
LIMIT 5;
```

### Use Case 2: Resource Allocation

```sql
-- Find understaffed high-importance locations
SELECT 
    l.name AS location,
    l.pagerank_score AS importance,
    COUNT(DISTINCT inv.investigator_id) AS investigators_assigned,
    CASE 
        WHEN l.pagerank_score > 50 AND COUNT(inv.investigator_id) < 2 
        THEN '⚠️ NEEDS MORE RESOURCES'
        ELSE '✓ Adequately Staffed'
    END AS status
FROM NEO4J_GHOST_PAGERANK l
LEFT JOIN GHOST_SIGHTINGS gs ON l.name = gs.location_name
LEFT JOIN INVESTIGATIONS i ON gs.ghost_id = i.ghost_id
LEFT JOIN INVESTIGATORS inv ON i.investigator_id = inv.investigator_id
WHERE l.type = 'Location'
GROUP BY l.name, l.pagerank_score
ORDER BY importance DESC
LIMIT 10;
```

### Use Case 3: Containment Strategy

```sql
-- Find optimal intervention points (bridge ghosts)
SELECT 
    g.ghost_name,
    g.threat_level,
    bc.betweenness_score AS bridge_importance,
    pr.pagerank_score AS influence,
    CONCAT(
        'Targeting this entity will disrupt ',
        FLOOR(bc.betweenness_score / 10),
        ' connected networks'
    ) AS tactical_impact
FROM NEO4J_BETWEENNESS_CENTRALITY bc
JOIN GHOSTS g ON bc.node_id = g.ghost_id
JOIN NEO4J_GHOST_PAGERANK pr ON bc.node_id = pr.node_id
WHERE bc.betweenness_score > 15
  AND g.status = 'Active'
ORDER BY bc.betweenness_score DESC
LIMIT 10;
```

---

## ✅ What's Next?

After running these queries, you can:

1. 📊 **Visualize** - Run Python scripts for interactive graphs
2. 🎯 **Optimize** - Use insights for resource allocation
3. 🧠 **Predict** - Train ML models with graph embeddings
4. 🔄 **Automate** - Schedule graph analysis tasks
5. 📈 **Monitor** - Track network evolution over time

---

## 💡 Pro Tips

1. **Start Small** - Test with sample data first
2. **Use Compute Pools** - For large-scale analysis
3. **Cache Results** - Store frequently used calculations
4. **Monitor Performance** - Track algorithm execution times
5. **Combine with AI** - Use Cortex for deeper insights

---

**Status:** ✅ Ready to Use  
**Setup Time:** ~5 minutes  
**Files:** 2 SQL scripts + 1 Python script  
**Algorithms:** 10+ graph analytics algorithms  

🕸️👻✨ **Start analyzing your ghost networks now!**

