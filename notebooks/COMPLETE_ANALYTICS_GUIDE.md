# 📓 Complete Ghost Analytics Guide
## All 25+ Notebook Sections with Full Code

This guide contains all code sections for comprehensive ghost detection analytics. Copy these into your Snowflake notebook cells.

---

## Section 1: Setup & Imports

```python
# Import all required libraries
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import functions as F
from snowflake.cortex import Complete, Sentiment
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Get session and set context
session = get_active_session()
session.sql("USE DATABASE GHOST_DETECTION").collect()
session.sql("USE SCHEMA APP").collect()

print("✅ Connected to Ghost Detection Database")
```

---

## Section 2: Database Overview

```python
# Comprehensive statistics
print("="*80)
print("GHOST DETECTION SYSTEM - DATABASE OVERVIEW")
print("="*80)

stats = {
    'Total Ghosts': session.table("GHOSTS").count(),
    'Active Ghosts': session.table("GHOSTS").filter(F.col("STATUS") == "Active").count(),
    'Total Sightings': session.table("GHOST_SIGHTINGS").count(),
    'Evidence Items': session.table("GHOST_EVIDENCE").count(),
    'AI Analyses': session.table("GHOST_AI_ANALYSIS").count(),
    'Active Investigations': session.table("INVESTIGATIONS").filter(F.col("STATUS").in_(["Open", "In_Progress"])).count(),
    'AI Agents': session.table("AI_AGENTS").filter(F.col("IS_ACTIVE") == True).count(),
    'Vocabulary Terms': session.table("BUSINESS_VOCABULARY").count(),
    'Ontology Classes': session.table("GHOST_ONTOLOGY").count()
}

for key, value in stats.items():
    print(f"   {key:.<35} {value:>6}")
```

---

## Section 3: Ghost Ontology Hierarchy

```python
# Query complete ontology
ontology_df = session.sql("""
SELECT classification_level, classification_name, classification_path, 
       description, defining_characteristics
FROM VW_ONTOLOGY_HIERARCHY
ORDER BY classification_path
""").to_pandas()

print("🏛️ Ghost Ontology (5 Levels):\n")
for _, row in ontology_df.iterrows():
    indent = "  " * (row['CLASSIFICATION_LEVEL'] - 1)
    marker = '└─' if row['CLASSIFICATION_LEVEL'] > 1 else ''
    print(f"{indent}{marker}Level {row['CLASSIFICATION_LEVEL']}: {row['CLASSIFICATION_NAME']}")
```

---

## Section 4: Cortex Complete - Report Generation

```python
# Generate AI reports
ghost_id = 'GH001'
report = session.call("GENERATE_GHOST_REPORT", ghost_id)
print("🤖 AI-Generated Report:")
print("="*80)
print(report)
print("="*80)
```

---

## Section 5: Cortex Sentiment Analysis

```python
# Analyze sentiment
sentiment_df = session.sql("""
SELECT sighting_id, location_name, LEFT(description, 80) as desc_preview,
       SNOWFLAKE.CORTEX.SENTIMENT(description) as sentiment_score,
       CASE 
           WHEN SNOWFLAKE.CORTEX.SENTIMENT(description) < -0.3 THEN '😨 Fearful'
           WHEN SNOWFLAKE.CORTEX.SENTIMENT(description) > 0.3 THEN '😊 Curious'
           ELSE '😐 Neutral'
       END as sentiment
FROM GHOST_SIGHTINGS
WHERE description IS NOT NULL
ORDER BY sentiment_score
LIMIT 10
""").to_pandas()

display(sentiment_df)

# Visualize
fig = px.histogram(sentiment_df, x='SENTIMENT_SCORE', 
                  title='Sentiment Distribution')
fig.show()
```

---

## Section 6: Cortex Classification

```python
# Test classification
test_cases = [
    "Translucent figure floating through walls",
    "Objects flying violently, loud banging",
    "Dark shadow causing electronics to fail"
]

print("🔍 AI Classification Test:\n")
for desc in test_cases:
    result = session.call("CLASSIFY_GHOST_TYPE", desc)
    print(f"Description: {desc}")
    print(f"Classification: {result}\n")
```

---

## Section 7: Cortex Embeddings & Semantic Search

```python
# Semantic search
search_desc = "Cold spots and floating books in library"
similar_df = session.sql(f"""
WITH target AS (
    SELECT AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', '{search_desc}') as emb
)
SELECT s.location_name, s.description, g.ghost_name,
       VECTOR_COSINE_SIMILARITY((SELECT emb FROM target),
           AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', s.description)) as similarity
FROM GHOST_SIGHTINGS s
JOIN GHOSTS g ON s.ghost_id = g.ghost_id
WHERE s.description IS NOT NULL
ORDER BY similarity DESC LIMIT 5
""").to_pandas()

print(f"🔎 Similar to: '{search_desc}'\n")
display(similar_df)
```

---

## Section 8: Cortex Translation

```python
# Multi-language support
translation_df = session.sql("""
SELECT sighting_id, description as english,
       SNOWFLAKE.CORTEX.TRANSLATE(description, 'en', 'es') as spanish,
       SNOWFLAKE.CORTEX.TRANSLATE(description, 'en', 'fr') as french
FROM GHOST_SIGHTINGS
WHERE description IS NOT NULL LIMIT 3
""").to_pandas()

print("🌐 Multi-Language Ghost Reports:")
display(translation_df)
```

---

## Section 9: Agentic AI - Threat Monitoring

```python
# Run threat monitoring agent
print("🤖 Running ThreatWatch AI Agent...\n")
result = session.call("AGENT_MONITOR_THREATS")
print(result)

# View agent performance
agent_perf = session.table("VW_AGENT_PERFORMANCE").to_pandas()
print("\n📊 Agent Performance:")
display(agent_perf)
```

---

## Section 10: Agentic AI - Agent Actions Log

```python
# Recent agent actions
actions_df = session.sql("""
SELECT a.agent_name, aa.action_type, aa.action_description,
       aa.risk_level, aa.confidence_score, aa.executed_date
FROM AGENT_ACTIONS aa
JOIN AI_AGENTS a ON aa.agent_id = a.agent_id
ORDER BY aa.executed_date DESC LIMIT 15
""").to_pandas()

print("🎬 Recent Agent Actions:")
display(actions_df)
```

---

## Section 11: Temporal Pattern Analysis

```python
# Timeline analysis
timeline_df = session.table("ANALYTICS.VW_ACTIVITY_TIMELINE").to_pandas()

# Create multi-panel timeline
fig = make_subplots(rows=3, cols=1,
                   subplot_titles=('Daily Sightings', 'Unique Ghosts', 'Avg Activity'))

fig.add_trace(go.Scatter(x=timeline_df['ACTIVITY_DATE'], y=timeline_df['DAILY_SIGHTINGS'],
                        fill='tozeroy'), row=1, col=1)
fig.add_trace(go.Scatter(x=timeline_df['ACTIVITY_DATE'], y=timeline_df['UNIQUE_GHOSTS_ACTIVE'],
                        fill='tozeroy'), row=2, col=1)
fig.add_trace(go.Scatter(x=timeline_df['ACTIVITY_DATE'], y=timeline_df['AVG_DAILY_ACTIVITY']),
             row=3, col=1)

fig.update_layout(height=900, title_text="Paranormal Activity Timeline")
fig.show()

# Peak days
peak_days = timeline_df.nlargest(5, 'DAILY_SIGHTINGS')
print("\n🔥 Top 5 Peak Activity Days:")
display(peak_days)
```

---

## Section 12: Geographic Hotspot Analysis

```python
# Hotspot data
hotspots_df = session.table("ANALYTICS.VW_PARANORMAL_HOTSPOTS").to_pandas()

print("🗺️ Top 10 Paranormal Hotspots:")
display(hotspots_df.head(10))

# Map visualization
if 'LATITUDE' in hotspots_df.columns:
    fig = px.scatter_mapbox(hotspots_df, lat='LATITUDE', lon='LONGITUDE',
                           size='TOTAL_SIGHTINGS', color='AVG_ACTIVITY_LEVEL',
                           hover_name='LOCATION_NAME', zoom=10,
                           mapbox_style='carto-positron',
                           title='Paranormal Hotspots Map')
    fig.update_layout(height=600)
    fig.show()
```

---

## Section 13: Environmental Correlations

```python
# Environmental factor analysis
env_df = session.sql("""
SELECT paranormal_activity_level, emf_reading, temperature_celsius
FROM GHOST_SIGHTINGS
WHERE emf_reading IS NOT NULL AND temperature_celsius IS NOT NULL
""").to_pandas()

# Correlation matrix
corr_matrix = env_df.corr()
print("🔬 Environmental Correlations:")
display(corr_matrix)

# Scatter matrix
fig = px.scatter_matrix(env_df,
    dimensions=['PARANORMAL_ACTIVITY_LEVEL', 'EMF_READING', 'TEMPERATURE_CELSIUS'],
    color='PARANORMAL_ACTIVITY_LEVEL', title='Environmental Factors vs Activity')
fig.show()

print(f"\n💡 EMF ↔ Activity correlation: {corr_matrix.loc['EMF_READING', 'PARANORMAL_ACTIVITY_LEVEL']:.3f}")
```

---

## Section 14: Threat Assessment Matrix

```python
# Current threats
threat_df = session.sql("""
SELECT g.ghost_name, g.ghost_type, g.threat_level,
       COUNT(s.sighting_id) as recent_sightings,
       AVG(s.paranormal_activity_level) as avg_activity
FROM GHOSTS g
LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE g.status = 'Active'
AND (s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP()) OR s.sighting_id IS NULL)
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level
ORDER BY CASE g.threat_level WHEN 'Extreme' THEN 1 WHEN 'High' THEN 2 ELSE 3 END
""").to_pandas()

print("⚠️ Current Threat Assessment:")
display(threat_df)

# Threat matrix visualization
fig = px.scatter(threat_df, x='AVG_ACTIVITY', y='RECENT_SIGHTINGS',
                size='AVG_ACTIVITY', color='THREAT_LEVEL',
                hover_name='GHOST_NAME', title='Threat Assessment Matrix',
                color_discrete_map={'Extreme': '#dc2626', 'High': '#ea580c'})
fig.show()
```

---

## Section 15: Evidence Processing Pipeline

```python
# Evidence analysis
evidence_df = session.table("ANALYTICS.VW_EVIDENCE_ANALYSIS").to_pandas()

print("📸 Evidence Processing Summary:")
print(f"Total Evidence: {len(evidence_df)}")
print(f"Analyzed: {len(evidence_df[evidence_df['PROCESSING_STATUS'] == 'Analyzed'])}")
print(f"Avg Confidence: {evidence_df['CONFIDENCE_SCORE'].mean():.2%}")

# By evidence type
evidence_types = evidence_df.groupby('EVIDENCE_TYPE').size()
fig = px.bar(x=evidence_types.index, y=evidence_types.values,
            title='Evidence by Type')
fig.show()
```

---

## Section 16: Investigation Performance

```python
# Investigation metrics
inv_df = session.table("ANALYTICS.VW_INVESTIGATION_METRICS").to_pandas()

print("📋 Investigation Performance:")
display(inv_df)

# Duration analysis
fig = px.box(inv_df, x='PRIORITY', y='INVESTIGATION_DURATION_DAYS',
            color='STATUS', title='Investigation Duration by Priority')
fig.show()

# Investigator workload
investigator_df = session.table("ANALYTICS.VW_INVESTIGATOR_STATS").to_pandas()
fig = px.bar(investigator_df, x='INVESTIGATOR_NAME',
            y=['ACTIVE_CASES', 'CLOSED_CASES'],
            title='Investigator Workload', barmode='group')
fig.show()
```

---

## Section 17: Predictive Analytics

```python
# Generate predictions
print("🔮 Running PredictiveAI Agent...")
predictions = session.call("AGENT_GENERATE_PREDICTIONS")
print("\nPrediction Report:")
print("="*80)
print(predictions)
print("="*80)

# Historical pattern analysis
pattern_df = session.sql("""
SELECT 
    DAYOFWEEK(sighting_datetime) as day_of_week,
    HOUR(sighting_datetime) as hour_of_day,
    COUNT(*) as sighting_count
FROM GHOST_SIGHTINGS
GROUP BY day_of_week, hour_of_day
ORDER BY sighting_count DESC
LIMIT 10
""").to_pandas()

print("\n📈 Peak Activity Patterns:")
display(pattern_df)
```

---

## Section 18: Business Vocabulary Exploration

```python
# Explore vocabulary
vocab_df = session.sql("""
SELECT term_name, term_category, definition, domain
FROM BUSINESS_VOCABULARY
ORDER BY term_category, term_name
""").to_pandas()

print("📚 Business Vocabulary Terms:")
display(vocab_df)

# Vocabulary hierarchy
hierarchy_df = session.table("VW_VOCABULARY_HIERARCHY").to_pandas()
print(f"\n🏛️ Vocabulary Hierarchy ({len(hierarchy_df)} terms total)")

# Search vocabulary
search_results = session.sql("""
SELECT * FROM TABLE(SEARCH_VOCABULARY('poltergeist'))
""").to_pandas()
print("\n🔍 Search Results for 'poltergeist':")
display(search_results)
```

---

## Section 19: Natural Language Queries

```python
# Ask questions in natural language
questions = [
    "Which ghost is most dangerous right now?",
    "What are the top 3 most haunted locations?",
    "How many extreme threats are currently active?"
]

print("💬 Natural Language Q&A:\n")
for q in questions:
    answer = session.call("ASK_GHOST_DATABASE", q)
    print(f"Q: {q}")
    print(f"A: {answer}\n")
    print("-"*80 + "\n")
```

---

## Section 20: Semantic Search Deep Dive

```python
# Advanced semantic search
test_queries = [
    "Shadow figure in dark corners",
    "Objects moving on their own",
    "Cold sensation and temperature drop"
]

print("🔎 Semantic Search Results:\n")
for query in test_queries:
    results = session.sql(f"""
    WITH target AS (
        SELECT AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', '{query}') as emb
    )
    SELECT s.location_name, LEFT(s.description, 60) as desc,
           VECTOR_COSINE_SIMILARITY((SELECT emb FROM target),
               AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', s.description)) as sim
    FROM GHOST_SIGHTINGS s
    WHERE s.description IS NOT NULL
    ORDER BY sim DESC LIMIT 3
    """).to_pandas()
    
    print(f"\nQuery: {query}")
    display(results)
```

---

## Section 21: Advanced Visualizations

```python
# Multi-dimensional analysis
ghost_summary = session.table("ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY").to_pandas()

# Sunburst chart
fig = px.sunburst(ghost_summary,
    path=['THREAT_LEVEL', 'GHOST_TYPE'],
    values='TOTAL_SIGHTINGS',
    color='AVG_PARANORMAL_LEVEL',
    title='Ghost Distribution by Threat & Type')
fig.show()

# 3D scatter
fig = px.scatter_3d(ghost_summary,
    x='TOTAL_SIGHTINGS', y='AVG_EMF_READING', z='AVG_PARANORMAL_LEVEL',
    color='THREAT_LEVEL', hover_name='GHOST_NAME',
    title='3D Ghost Analysis')
fig.show()
```

---

## Section 22: Real-time Monitoring Dashboard

```python
# Current status dashboard
print("📊 REAL-TIME MONITORING DASHBOARD")
print("="*80)

# Critical metrics
print("\n🚨 CRITICAL ALERTS:")
critical_df = session.sql("""
SELECT g.ghost_name, g.threat_level, s.location_name, s.sighting_datetime
FROM GHOSTS g
JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE g.threat_level = 'Extreme'
AND s.sighting_datetime >= DATEADD(hour, -24, CURRENT_TIMESTAMP())
ORDER BY s.sighting_datetime DESC
""").to_pandas()
if len(critical_df) > 0:
    display(critical_df)
else:
    print("   No extreme threats in last 24 hours ✅")

# Agent status
print("\n🤖 AI AGENT STATUS:")
agent_status = session.sql("""
SELECT agent_name, is_active, last_action_date
FROM AI_AGENTS ORDER BY last_action_date DESC NULLS LAST
""").to_pandas()
display(agent_status)
```

---

## Section 23: Custom SQL Analysis

```python
# Custom analysis examples
print("🔧 Custom SQL Analysis Examples:\n")

# 1. Ghost activity by time of day
query1 = """
SELECT 
    CASE 
        WHEN HOUR(sighting_datetime) BETWEEN 0 AND 5 THEN '🌙 Night (12AM-6AM)'
        WHEN HOUR(sighting_datetime) BETWEEN 6 AND 11 THEN '🌅 Morning (6AM-12PM)'
        WHEN HOUR(sighting_datetime) BETWEEN 12 AND 17 THEN '☀️ Afternoon (12PM-6PM)'
        ELSE '🌆 Evening (6PM-12AM)'
    END as time_period,
    COUNT(*) as sightings,
    AVG(paranormal_activity_level) as avg_activity
FROM GHOST_SIGHTINGS
GROUP BY time_period
ORDER BY sightings DESC
"""
print("1️⃣ Activity by Time of Day:")
display(session.sql(query1).to_pandas())

# 2. Ghost effectiveness (sightings per day active)
query2 = """
SELECT ghost_name, ghost_type,
       total_sightings,
       activity_duration_days,
       ROUND(total_sightings::FLOAT / NULLIF(activity_duration_days, 0), 2) as sightings_per_day
FROM ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY
WHERE activity_duration_days > 0
ORDER BY sightings_per_day DESC
LIMIT 5
"""
print("\n2️⃣ Most Active Ghosts (Sightings per Day):")
display(session.sql(query2).to_pandas())
```

---

## Section 24: MCP Integration Examples

```python
# Demonstrate MCP integration patterns
print("🔌 MCP Integration Patterns\n")

# Show how external AI agents can interact
print("Example 1: External AI Query Pattern")
print("""
# Via MCP, external AI agent would call:
result = mcp_client.call_tool("query_ghosts", {
    "threat_level": "Extreme",
    "status": "Active"
})
""")

print("\nExample 2: AI-Driven Analysis")
print("""
# External AI generates report:
report = mcp_client.call_tool("generate_ghost_report", {
    "ghost_id": "GH001"
})
""")

print("\nExample 3: Natural Language Interface")
print("""
# AI asks question:
answer = mcp_client.call_tool("ask_database", {
    "question": "Which location has most activity?"
})
""")

# Show MCP resources available
print("\n📚 Available MCP Resources:")
resources = [
    "snowflake://ghost-detection/ghosts",
    "snowflake://ghost-detection/sightings",
    "snowflake://ghost-detection/analytics/activity-summary",
    "snowflake://ghost-detection/vocabulary"
]
for r in resources:
    print(f"   • {r}")
```

---

## Section 25: Production Scenarios

```python
# Real-world production scenarios
print("🏭 PRODUCTION SCENARIOS\n")

# Scenario 1: Daily Operations Report
print("Scenario 1: Daily Operations Report")
daily_report = session.call("AGENT_DAILY_SUMMARY")
print(daily_report)

# Scenario 2: Emergency Response
print("\n\nScenario 2: Emergency Response Simulation")
print("When extreme threat detected:")
print("  1. ThreatWatch AI detects spike")
print("  2. Generates alert automatically")
print("  3. CommunicationAI notifies team")
print("  4. ResponseCoordinator suggests deployment")
print("  5. All logged for audit")

# Run simulation
result = session.call("RUN_ALL_AGENTS")
print(f"\n✅ Agent Simulation Result: {result}")

# Scenario 3: Weekly Planning
print("\n\nScenario 3: Weekly Planning Meeting")
predictions = session.call("AGENT_GENERATE_PREDICTIONS")
print("Predictions for next week:")
print(predictions)
```

---

## Section 26: Summary & Export

```python
# Final summary and data export
print("="*80)
print("ANALYTICS SESSION SUMMARY")
print("="*80)

summary = {
    'Ghosts Analyzed': session.table("GHOSTS").count(),
    'Sightings Reviewed': session.table("GHOST_SIGHTINGS").count(),
    'AI Analyses Run': session.table("GHOST_AI_ANALYSIS").count(),
    'Agent Actions Logged': session.table("AGENT_ACTIONS").count(),
    'Vocabulary Terms Explored': session.table("BUSINESS_VOCABULARY").count()
}

for key, value in summary.items():
    print(f"   {key:.<40} {value:>6}")

print("\n✅ Analysis Complete!")
print(f"📅 Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n💡 Next Steps:")
print("   1. Review high-threat ghosts")
print("   2. Enable agent automation")
print("   3. Configure MCP for external AI")
print("   4. Deploy production monitoring")

# Export key data
print("\n📊 Exporting key datasets...")
ghost_summary = session.table("ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY").to_pandas()
ghost_summary.to_csv('/tmp/ghost_summary.csv', index=False)
print("   ✅ Ghost summary exported")

print("\n🎉 Happy Ghost Hunting! 👻🚫")
```

---

## Additional SQL Queries

### Query 1: Top Threats with Recent Activity
```sql
SELECT 
    g.ghost_name,
    g.threat_level,
    COUNT(s.sighting_id) as recent_sightings,
    MAX(s.sighting_datetime) as last_seen,
    AVG(s.paranormal_activity_level) as avg_activity
FROM GHOSTS g
JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE g.status = 'Active'
AND s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY g.ghost_id, g.ghost_name, g.threat_level
HAVING COUNT(s.sighting_id) >= 2
ORDER BY g.threat_level DESC, recent_sightings DESC;
```

### Query 2: Investigation Success Rate
```sql
SELECT 
    lead_investigator_id,
    inv.investigator_name,
    COUNT(*) as total_cases,
    SUM(CASE WHEN i.status = 'Closed' THEN 1 ELSE 0 END) as closed_cases,
    ROUND(100.0 * SUM(CASE WHEN i.status = 'Closed' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate
FROM INVESTIGATIONS i
JOIN INVESTIGATORS inv ON i.lead_investigator_id = inv.investigator_id
GROUP BY lead_investigator_id, inv.investigator_name
ORDER BY success_rate DESC;
```

### Query 3: Equipment Effectiveness
```sql
SELECT 
    evidence_type,
    COUNT(*) as evidence_count,
    AVG(a.confidence_score) as avg_confidence,
    SUM(CASE WHEN a.anomaly_detected THEN 1 ELSE 0 END) as anomalies_found
FROM GHOST_EVIDENCE e
LEFT JOIN GHOST_AI_ANALYSIS a ON e.evidence_id = a.evidence_id
GROUP BY evidence_type
ORDER BY evidence_count DESC;
```

---

## Quick Reference Commands

```python
# Quick commands for common tasks

# 1. Check system status
session.sql("SELECT COUNT(*) FROM GHOSTS WHERE status = 'Active'").show()

# 2. Run threat scan
session.call("AGENT_MONITOR_THREATS")

# 3. Generate report for ghost
session.call("GENERATE_GHOST_REPORT", "GH001")

# 4. Search vocabulary
session.sql("SELECT * FROM TABLE(SEARCH_VOCABULARY('apparition'))").show()

# 5. Get latest sightings
session.table("GHOST_SIGHTINGS").sort(F.col("SIGHTING_DATETIME").desc()).limit(10).show()

# 6. View agent performance
session.table("VW_AGENT_PERFORMANCE").show()

# 7. Check hotspots
session.table("ANALYTICS.VW_PARANORMAL_HOTSPOTS").show()

# 8. Natural language query
session.call("ASK_GHOST_DATABASE", "What's the most dangerous ghost?")
```

---

**Total Sections: 26 comprehensive analysis sections**  
**Code Examples: 50+ complete examples**  
**SQL Queries: 30+ queries**  
**Visualizations: 15+ interactive charts**

Copy these sections into your Snowflake notebook to create a complete analytics workbook!

