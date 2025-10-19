# 🚀 Quick Start Guide - SnowGhost Breakers

Get up and running in 10 minutes!

## ⚡ Fast Track Installation

### Step 1: Open Snowflake (1 minute)
1. Log into your Snowflake account via Snowsight
2. Click on "Worksheets" in the left navigation
3. Create a new worksheet

### Step 2: Run Setup Script (3 minutes)
Copy and paste this into your worksheet:

```sql
-- Set your warehouse
USE WAREHOUSE your_warehouse_name;

-- Run setup (execute each line)
!source /path/to/SnowGhostBreakers/sql/01_setup_database.sql
!source /path/to/SnowGhostBreakers/sql/02_create_tables.sql
!source /path/to/SnowGhostBreakers/sql/03_sample_data.sql
!source /path/to/SnowGhostBreakers/sql/04_stored_procedures.sql
!source /path/to/SnowGhostBreakers/sql/05_semantic_views.sql
!source /path/to/SnowGhostBreakers/sql/06_cortex_ai_functions.sql
```

Or use the master script:
```sql
!source /path/to/SnowGhostBreakers/setup.sql
```

### Step 3: Verify Installation (1 minute)
```sql
USE DATABASE GHOST_DETECTION;

-- Check tables
SHOW TABLES IN SCHEMA APP;

-- Check views
SHOW VIEWS IN SCHEMA ANALYTICS;

-- Query sample data
SELECT * FROM APP.GHOSTS;
SELECT * FROM APP.GHOST_SIGHTINGS;
```

Expected: You should see 5 ghosts and 5 sightings.

### Step 4: Test Cortex AI (2 minutes)
```sql
-- Test 1: Generate a report
CALL APP.GENERATE_GHOST_REPORT('GH001');

-- Test 2: Classify a description
CALL APP.CLASSIFY_GHOST_TYPE('Translucent figure floating through walls');

-- Test 3: Get sentiment
SELECT 
    description,
    SNOWFLAKE.CORTEX.SENTIMENT(description) as fear_level
FROM APP.GHOST_SIGHTINGS
LIMIT 1;

-- Test 4: View analytics
SELECT * FROM ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY;
```

### Step 5: Deploy Streamlit App (3 minutes)

#### Option A: Streamlit in Snowflake (Recommended)
1. Click "Streamlit" in left navigation
2. Click "+ Streamlit App"
3. Name: `Ghost Detection System`
4. Warehouse: Your warehouse
5. Database: `GHOST_DETECTION`
6. Schema: `APP`
7. Copy contents of `streamlit_app/ghost_detection_app.py`
8. Click "Run"

#### Option B: Create via SQL
```sql
CREATE STREAMLIT APP.GHOST_DETECTION_STREAMLIT
FROM '/path/to/streamlit_app'
MAIN_FILE = 'ghost_detection_app.py';
```

### Step 6: Explore! (∞ minutes)
You're ready! Try:

**In Streamlit:**
- 📊 View the Dashboard
- 👻 Browse the Ghost Registry
- 📍 Check Sightings on the map
- 🤖 Ask AI questions

**In SQL:**
```sql
-- Find most dangerous ghosts
SELECT * FROM APP.GHOSTS 
WHERE threat_level = 'Extreme';

-- Get hotspots
SELECT * FROM ANALYTICS.VW_PARANORMAL_HOTSPOTS
ORDER BY TOTAL_SIGHTINGS DESC;

-- Ask natural language question
CALL APP.ASK_GHOST_DATABASE('Which ghost is most active?');
```

## 🎯 Quick Examples

### Example 1: Generate AI Report
```sql
CALL APP.GENERATE_GHOST_REPORT('GH002');
```
Output: Comprehensive AI-generated report about Slimer

### Example 2: Find Similar Sightings
```sql
SELECT * FROM TABLE(
    APP.FIND_SIMILAR_INCIDENTS(
        'Green ghost eating food in kitchen'
    )
);
```

### Example 3: Threat Assessment
```sql
SELECT * FROM ANALYTICS.VW_REAL_TIME_THREAT_ASSESSMENT;
```

### Example 4: Natural Language Query
```sql
CALL APP.ASK_GHOST_DATABASE(
    'What are the top 3 most haunted locations?'
);
```

## 🔧 Troubleshooting

### Issue: "Object does not exist"
**Solution:** Make sure you ran all setup scripts in order.

### Issue: Cortex AI not working
**Solution:** 
```sql
-- Test if Cortex is enabled
SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', 'test');
```
If this fails, contact Snowflake support to enable Cortex.

### Issue: Insufficient privileges
**Solution:**
```sql
USE ROLE ACCOUNTADMIN;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE your_role;
```

### Issue: Streamlit won't load
**Solution:**
- Check warehouse is running
- Verify database/schema exist
- Check for syntax errors in code

## 📚 Next Steps

After quick start:
1. Read the full [README.md](README.md) for detailed features
2. Check [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production setup
3. Explore [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for architecture
4. Try examples in `sql/07_aisql_examples.sql`
5. Run analytics in `scripts/ghost_analytics.py`

## 🎓 Learn More

### Explore Features
- **AI Functions**: See `sql/06_cortex_ai_functions.sql`
- **Analytics**: See `sql/05_semantic_views.sql`
- **Procedures**: See `sql/04_stored_procedures.sql`
- **Advanced AI**: See `sql/07_aisql_examples.sql`

### Try These Queries
```sql
-- 1. Ghost activity over time
SELECT * FROM ANALYTICS.VW_ACTIVITY_TIMELINE
ORDER BY ACTIVITY_DATE DESC
LIMIT 30;

-- 2. Investigator performance
SELECT * FROM ANALYTICS.VW_INVESTIGATOR_STATS;

-- 3. AI model metrics
SELECT * FROM ANALYTICS.VW_AI_MODEL_METRICS;

-- 4. Threat matrix
SELECT * FROM ANALYTICS.VW_THREAT_MATRIX;
```

## 💡 Quick Tips

1. **Use the right warehouse size**: Start with MEDIUM, scale as needed
2. **Enable auto-suspend**: Set to 5 minutes to save costs
3. **Try natural language queries**: Use ASK_GHOST_DATABASE for easy access
4. **Explore the Streamlit app**: Most features are accessible via UI
5. **Check the analytics views**: Pre-built insights in ANALYTICS schema

## 🎉 Success Checklist

- [ ] Database created
- [ ] Tables populated with sample data
- [ ] Stored procedures working
- [ ] Analytics views accessible
- [ ] Cortex AI functions responding
- [ ] Streamlit app running
- [ ] Can query ghost data
- [ ] Can generate AI reports

If all checked, you're ready to catch ghosts! 👻🚫

## 🆘 Need Help?

1. **Check documentation**: README.md has detailed info
2. **Review examples**: sql/ folder has 50+ examples
3. **Test step-by-step**: Run each SQL script individually
4. **Check Snowflake docs**: https://docs.snowflake.com/cortex

## 🎬 You're Done!

Congratulations! You now have a fully functional ghost detection system powered by Snowflake Cortex AI.

**Time to start your investigation!** 👻🔍

---

*Total setup time: ~10 minutes*  
*Total lines of code: 3000+*  
*Total capabilities: Unlimited!*

**Happy Ghost Hunting!** 🎃

