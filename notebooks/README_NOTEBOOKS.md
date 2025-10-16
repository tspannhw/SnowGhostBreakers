# 📓 Ghost Detection Notebooks Guide

## Available Notebooks

### 1. `01_ghost_analytics.ipynb`
**Basic Analytics Notebook** - Interactive exploration (7+ cells started)
- Setup and imports
- Database overview
- Ghost ontology analysis  
- Cortex AI demonstrations
- Ready for expansion

**Status**: Foundation created, expandable  
**Use Case**: Quick analysis and exploration

---

### 2. `COMPLETE_ANALYTICS_GUIDE.md`
**Comprehensive 26-Section Guide** - Complete code reference
- All 26+ analysis sections
- 50+ complete code examples
- 30+ SQL queries
- 15+ visualizations
- Production-ready code

**Status**: ✅ Complete  
**Use Case**: Copy sections into your notebook

---

## How to Use

### Option 1: Build Your Own Notebook
1. Open `01_ghost_analytics.ipynb` in Snowflake
2. Copy sections from `COMPLETE_ANALYTICS_GUIDE.md`
3. Paste into new cells
4. Run and customize

### Option 2: Use the Complete Guide
1. Open `COMPLETE_ANALYTICS_GUIDE.md`
2. Find the analysis you need
3. Copy the code block
4. Paste into Snowflake SQL worksheet or notebook

### Option 3: Use the Generator Script
1. Run `notebooks/generate_notebook.py`
2. Creates full notebook programmatically
3. Import into Snowflake

---

## All 26 Sections Covered

### 🔧 Setup & Configuration (Sections 1-2)
1. Setup & Imports
2. Database Overview

### 🏛️ Data Exploration (Sections 3-4)
3. Ghost Ontology Analysis
4. Cortex AI - Text Generation

### 🤖 Cortex AI Capabilities (Sections 5-8)
5. Cortex AI - Sentiment Analysis
6. Cortex AI - Classification
7. Cortex AI - Embeddings & Search
8. Cortex AI - Translation

### 🦾 Agentic AI (Sections 9-10)
9. Agentic AI - Threat Monitoring
10. Agentic AI - Agent Performance

### 📊 Analytics (Sections 11-17)
11. Temporal Pattern Analysis
12. Geographic Hotspot Analysis
13. Environmental Correlations
14. Threat Assessment Matrix
15. Evidence Processing Pipeline
16. Investigation Performance
17. Predictive Analytics

### 📚 Vocabulary & Search (Sections 18-20)
18. Business Vocabulary Exploration
19. Natural Language Queries
20. Semantic Search Deep Dive

### 📈 Advanced Features (Sections 21-26)
21. Advanced Visualizations
22. Real-time Monitoring Dashboard
23. Custom SQL Analysis
24. MCP Integration Examples
25. Production Scenarios
26. Summary & Export

---

## Code Statistics

| Metric | Count |
|--------|-------|
| Total Sections | 26+ |
| Python Code Blocks | 30+ |
| SQL Queries | 30+ |
| Visualizations | 15+ |
| AI Examples | 20+ |
| Complete Examples | 50+ |

---

## Quick Start Examples

### Example 1: Run Complete Analysis
```python
# In Snowflake notebook
from snowflake.snowpark.context import get_active_session
session = get_active_session()
session.sql("USE DATABASE GHOST_DETECTION").collect()

# Now copy any section from COMPLETE_ANALYTICS_GUIDE.md
```

### Example 2: Generate Report
```python
# Generate AI report for a ghost
report = session.call("GENERATE_GHOST_REPORT", "GH001")
print(report)
```

### Example 3: Run Agent
```python
# Execute AI agent
result = session.call("AGENT_MONITOR_THREATS")
print(result)
```

---

## Section Dependencies

Most sections are **independent** and can run in any order after Section 1 (Setup).

### Required Order:
1. Section 1 (Setup) - **Must run first**
2. All other sections - **Can run in any order**

### Recommended Flow:
1. Setup (1)
2. Overview (2)
3. Ontology (3)
4. Cortex AI (4-8)
5. Agents (9-10)
6. Analytics (11-17)
7. Advanced (18-26)

---

## Tips for Best Results

### Performance
- Run on **Medium** or larger warehouse
- Use **AUTO_SUSPEND** for cost savings
- Cache results for repeated queries

### Visualizations
- Plotly charts are interactive
- Click, zoom, pan to explore
- Export as PNG or HTML

### AI Features
- Cortex AI requires proper permissions
- Some queries may take 5-10 seconds
- Results are non-deterministic (may vary slightly)

### Customization
- All code is modular
- Easy to modify queries
- Add your own sections

---

## Common Tasks

### Task 1: Check System Status
```python
stats = {
    'Ghosts': session.table("GHOSTS").count(),
    'Sightings': session.table("GHOST_SIGHTINGS").count(),
    'Investigations': session.table("INVESTIGATIONS").count()
}
print(stats)
```

### Task 2: Find Threats
```python
threats = session.sql("""
    SELECT ghost_name, threat_level, status
    FROM GHOSTS
    WHERE threat_level IN ('High', 'Extreme')
    AND status = 'Active'
""").to_pandas()
display(threats)
```

### Task 3: Generate Insights
```python
insights = session.call("AGENT_GENERATE_PREDICTIONS")
print(insights)
```

---

## Troubleshooting

### Issue: Import Errors
**Solution**: Ensure all libraries installed
```python
# Check imports
import snowflake.snowpark
import plotly
print("✅ Imports OK")
```

### Issue: Permission Denied
**Solution**: Check role has access
```sql
USE ROLE GHOSTBUSTER;
GRANT USAGE ON DATABASE GHOST_DETECTION TO ROLE current_role;
```

### Issue: Cortex AI Not Working
**Solution**: Verify Cortex enabled
```sql
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', 'test');
```

---

## Next Steps

1. **Start Small**: Begin with sections 1-5
2. **Explore AI**: Try Cortex AI sections (4-8)
3. **Enable Agents**: Test agentic AI (9-10)
4. **Go Deep**: Advanced analytics (11-26)
5. **Customize**: Add your own analyses

---

## Resources

- **Main README**: `/README.md` - Overall system
- **Agentic AI Guide**: `/AGENTIC_AI_GUIDE.md` - AI agents
- **MCP Guide**: `/MCP_GUIDE.md` - External integration
- **SQL Scripts**: `/sql/` - All database code
- **Streamlit App**: `/streamlit_app/` - Web interface

---

## Support

For issues or questions:
1. Check section comments in code
2. Review SQL script comments
3. See main documentation
4. Test queries in SQL worksheet first

---

**Happy Analyzing!** 📊👻

*26+ sections of comprehensive ghost detection analytics at your fingertips!*

