# 🚀 Deployment Guide - SnowGhost Breakers

Complete guide for deploying the Ghost Detection Application to Snowflake.

## Prerequisites

### Required Snowflake Features
- ✅ Snowflake account (Enterprise or Business Critical recommended)
- ✅ Cortex AI enabled (contact Snowflake if not available)
- ✅ Streamlit in Snowflake (SiS) access
- ✅ Snowpark-optimized warehouse

### Required Privileges
```sql
-- User needs these privileges
GRANT CREATE DATABASE ON ACCOUNT TO ROLE your_role;
GRANT CREATE WAREHOUSE ON ACCOUNT TO ROLE your_role;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE your_role;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE your_role;
```

### Recommended Setup
- **Warehouse Size**: Medium or Large for initial setup
- **Auto-suspend**: 5 minutes
- **Auto-resume**: Enabled
- **Multi-cluster**: Auto-scale (2-4 clusters) for production

## Step-by-Step Deployment

### Step 1: Verify Cortex AI Access

```sql
-- Test Cortex AI availability
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Hello, this is a test. Respond with OK if working.'
) as test_result;

-- Expected result: Should return AI-generated response
```

If this fails, contact your Snowflake account team to enable Cortex AI.

### Step 2: Create Compute Resources

```sql
-- Create warehouse for ghost detection workloads
CREATE WAREHOUSE IF NOT EXISTS GHOST_DETECTION_WH
WITH 
    WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Warehouse for Ghost Detection application';

-- Grant usage
GRANT USAGE ON WAREHOUSE GHOST_DETECTION_WH TO ROLE your_role;
GRANT OPERATE ON WAREHOUSE GHOST_DETECTION_WH TO ROLE your_role;
```

### Step 3: Run Database Setup Scripts

Execute scripts in this order:

#### A. Database and Schema Setup
```sql
-- Set warehouse
USE WAREHOUSE GHOST_DETECTION_WH;

-- Run setup script
!source sql/01_setup_database.sql
```

#### B. Create Tables
```sql
!source sql/02_create_tables.sql

-- Verify tables created
SHOW TABLES IN GHOST_DETECTION.APP;
```

Expected tables:
- GHOSTS
- GHOST_SIGHTINGS
- GHOST_EVIDENCE
- GHOST_AI_ANALYSIS
- SENSOR_READINGS
- INVESTIGATORS
- INVESTIGATIONS
- AUDIT_LOG

#### C. Load Sample Data
```sql
!source sql/03_sample_data.sql

-- Verify data loaded
SELECT COUNT(*) as ghost_count FROM GHOST_DETECTION.APP.GHOSTS;
SELECT COUNT(*) as sighting_count FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;
```

Expected results:
- 5 sample ghosts
- 5 sample sightings
- 5 sample evidence items

#### D. Create Stored Procedures
```sql
!source sql/04_stored_procedures.sql

-- Verify procedures created
SHOW PROCEDURES IN GHOST_DETECTION.APP;
```

#### E. Create Analytics Views
```sql
!source sql/05_semantic_views.sql

-- Verify views created
SHOW VIEWS IN GHOST_DETECTION.ANALYTICS;

-- Test a view
SELECT * FROM GHOST_DETECTION.ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY LIMIT 5;
```

#### F. Setup Cortex AI Functions
```sql
!source sql/06_cortex_ai_functions.sql

-- Test AI functionality
CALL GHOST_DETECTION.APP.CLASSIFY_GHOST_TYPE(
    'A translucent figure floating through walls making cold spots'
);
```

### Step 4: Deploy Streamlit Application

#### Option A: Streamlit in Snowflake (SiS) - Recommended

1. **Navigate to Streamlit**:
   - Log into Snowsight
   - Click "Streamlit" in left navigation
   - Click "+ Streamlit App"

2. **Configure App**:
   ```
   App name: Ghost Detection System
   Warehouse: GHOST_DETECTION_WH
   App location: 
     - Database: GHOST_DETECTION
     - Schema: APP
   ```

3. **Upload Code**:
   - Copy contents of `streamlit_app/ghost_detection_app.py`
   - Paste into the Streamlit editor
   - Click "Run"

#### Option B: Using Snowflake CLI

```bash
# Install Snowflake CLI
pip install snowflake-cli-labs

# Login
snow login

# Create Streamlit app
snow streamlit create \
    --name ghost_detection_system \
    --file streamlit_app/ghost_detection_app.py \
    --database GHOST_DETECTION \
    --schema APP \
    --warehouse GHOST_DETECTION_WH
```

### Step 5: Configure Cortex Analyst

1. **Upload Semantic Model**:
   ```sql
   -- Create stage for semantic model
   CREATE STAGE IF NOT EXISTS GHOST_DETECTION.APP.CORTEX_ANALYST_STAGE;
   
   -- Upload the YAML file via Snowsight or CLI
   PUT file://cortex_analyst/ghost_semantic_model.yaml 
       @GHOST_DETECTION.APP.CORTEX_ANALYST_STAGE 
       AUTO_COMPRESS=FALSE 
       OVERWRITE=TRUE;
   ```

2. **Create Cortex Analyst Service**:
   ```sql
   CREATE OR REPLACE CORTEX ANALYST SERVICE ghost_analyst
   SEMANTIC_MODEL_FILE = '@GHOST_DETECTION.APP.CORTEX_ANALYST_STAGE/ghost_semantic_model.yaml'
   WAREHOUSE = GHOST_DETECTION_WH;
   ```

3. **Test Cortex Analyst**:
   ```sql
   -- Test with a natural language question
   CALL SNOWFLAKE.CORTEX.ANALYST(
       'ghost_analyst',
       'What are the most active ghost types?'
   );
   ```

### Step 6: Setup Notebooks

#### Upload to Snowflake Notebooks

1. Navigate to "Notebooks" in Snowsight
2. Click "Create Notebook"
3. Name: "Ghost Analytics"
4. Upload `notebooks/01_ghost_analytics.ipynb`
5. Select warehouse: GHOST_DETECTION_WH
6. Run the notebook to verify

### Step 7: Configure Security (Optional but Recommended)

#### A. Create Roles

```sql
-- Role for Ghostbusters (full access)
CREATE ROLE IF NOT EXISTS GHOSTBUSTER;
GRANT ALL PRIVILEGES ON DATABASE GHOST_DETECTION TO ROLE GHOSTBUSTER;
GRANT ALL PRIVILEGES ON ALL SCHEMAS IN DATABASE GHOST_DETECTION TO ROLE GHOSTBUSTER;
GRANT ALL PRIVILEGES ON ALL TABLES IN DATABASE GHOST_DETECTION TO ROLE GHOSTBUSTER;
GRANT USAGE ON WAREHOUSE GHOST_DETECTION_WH TO ROLE GHOSTBUSTER;

-- Role for Investigators (read-write on cases)
CREATE ROLE IF NOT EXISTS GHOST_INVESTIGATOR;
GRANT USAGE ON DATABASE GHOST_DETECTION TO ROLE GHOST_INVESTIGATOR;
GRANT USAGE ON ALL SCHEMAS IN DATABASE GHOST_DETECTION TO ROLE GHOST_INVESTIGATOR;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA GHOST_DETECTION.APP TO ROLE GHOST_INVESTIGATOR;
GRANT USAGE ON WAREHOUSE GHOST_DETECTION_WH TO ROLE GHOST_INVESTIGATOR;

-- Role for Analysts (read-only)
CREATE ROLE IF NOT EXISTS GHOST_ANALYST;
GRANT USAGE ON DATABASE GHOST_DETECTION TO ROLE GHOST_ANALYST;
GRANT USAGE ON ALL SCHEMAS IN DATABASE GHOST_DETECTION TO ROLE GHOST_ANALYST;
GRANT SELECT ON ALL TABLES IN DATABASE GHOST_DETECTION TO ROLE GHOST_ANALYST;
GRANT SELECT ON ALL VIEWS IN DATABASE GHOST_DETECTION TO ROLE GHOST_ANALYST;
GRANT USAGE ON WAREHOUSE GHOST_DETECTION_WH TO ROLE GHOST_ANALYST;
```

#### B. Data Masking (for PII)

```sql
-- Mask witness contact information
CREATE OR REPLACE MASKING POLICY witness_info_mask AS (val STRING) 
RETURNS STRING ->
    CASE 
        WHEN CURRENT_ROLE() IN ('GHOSTBUSTER', 'ACCOUNTADMIN') THEN val
        ELSE '***REDACTED***'
    END;

-- Apply to witness contact columns
ALTER TABLE GHOST_DETECTION.APP.GHOST_SIGHTINGS 
    MODIFY COLUMN witness_contact 
    SET MASKING POLICY witness_info_mask;
```

### Step 8: Setup Monitoring

#### A. Create Resource Monitors

```sql
CREATE RESOURCE MONITOR ghost_detection_monitor
WITH 
    CREDIT_QUOTA = 100
    FREQUENCY = MONTHLY
    START_TIMESTAMP = IMMEDIATELY
    TRIGGERS 
        ON 75 PERCENT DO NOTIFY
        ON 90 PERCENT DO SUSPEND
        ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER WAREHOUSE GHOST_DETECTION_WH 
    SET RESOURCE_MONITOR = ghost_detection_monitor;
```

#### B. Create Alert for High Activity

```sql
-- Create task to check for extreme threats
CREATE OR REPLACE TASK monitor_extreme_threats
    WAREHOUSE = GHOST_DETECTION_WH
    SCHEDULE = '60 MINUTE'
AS
    INSERT INTO GHOST_DETECTION.APP.AUDIT_LOG (
        log_id, table_name, action, action_datetime, new_values
    )
    SELECT 
        UUID_STRING(),
        'GHOSTS',
        'ALERT_EXTREME_THREAT',
        CURRENT_TIMESTAMP(),
        OBJECT_CONSTRUCT(
            'ghost_id', ghost_id,
            'ghost_name', ghost_name,
            'threat_level', threat_level,
            'recent_sightings', COUNT(*)
        )
    FROM GHOST_DETECTION.APP.GHOSTS g
    JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
    WHERE g.threat_level = 'Extreme'
    AND s.sighting_datetime >= DATEADD(hour, -1, CURRENT_TIMESTAMP())
    GROUP BY g.ghost_id, g.ghost_name, g.threat_level
    HAVING COUNT(*) >= 3;

-- Enable task
ALTER TASK monitor_extreme_threats RESUME;
```

### Step 9: Test End-to-End

#### Comprehensive Test Suite

```sql
-- 1. Test data retrieval
SELECT * FROM GHOST_DETECTION.APP.GHOSTS LIMIT 1;

-- 2. Test stored procedure
CALL GHOST_DETECTION.APP.GENERATE_GHOST_REPORT('GH001');

-- 3. Test AI integration
SELECT SNOWFLAKE.CORTEX.SENTIMENT(description) 
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS 
LIMIT 1;

-- 4. Test views
SELECT * FROM GHOST_DETECTION.ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY LIMIT 5;

-- 5. Test geospatial
SELECT 
    location_name, 
    latitude, 
    longitude,
    ST_POINT(longitude, latitude) as geo_point
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
LIMIT 5;
```

### Step 10: Performance Tuning

#### A. Create Clustering Keys

```sql
-- Cluster sightings by date for time-series queries
ALTER TABLE GHOST_DETECTION.APP.GHOST_SIGHTINGS 
    CLUSTER BY (sighting_datetime);

-- Cluster evidence by ghost_id for join optimization
ALTER TABLE GHOST_DETECTION.APP.GHOST_EVIDENCE 
    CLUSTER BY (ghost_id);
```

#### B. Create Materialized Views (for heavy queries)

```sql
-- Materialized view for dashboard metrics
CREATE MATERIALIZED VIEW GHOST_DETECTION.ANALYTICS.MV_DAILY_METRICS AS
SELECT 
    DATE_TRUNC('day', sighting_datetime) as activity_date,
    COUNT(*) as daily_sightings,
    AVG(paranormal_activity_level) as avg_activity,
    COUNT(DISTINCT ghost_id) as unique_ghosts
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
GROUP BY DATE_TRUNC('day', sighting_datetime);

-- Refresh on schedule
CREATE TASK refresh_daily_metrics
    WAREHOUSE = GHOST_DETECTION_WH
    SCHEDULE = 'USING CRON 0 1 * * * UTC'
AS
    ALTER MATERIALIZED VIEW GHOST_DETECTION.ANALYTICS.MV_DAILY_METRICS REFRESH;

ALTER TASK refresh_daily_metrics RESUME;
```

#### C. Enable Search Optimization

```sql
-- Optimize search on text columns
ALTER TABLE GHOST_DETECTION.APP.GHOST_SIGHTINGS 
    ADD SEARCH OPTIMIZATION ON EQUALITY(location_name);

ALTER TABLE GHOST_DETECTION.APP.GHOSTS 
    ADD SEARCH OPTIMIZATION ON EQUALITY(ghost_name, ghost_type);
```

## Post-Deployment Checklist

- [ ] All SQL scripts executed successfully
- [ ] Sample data loaded and queryable
- [ ] Stored procedures callable
- [ ] Analytics views returning data
- [ ] Streamlit app running
- [ ] Cortex AI functions working
- [ ] Cortex Analyst responding to queries
- [ ] Security roles configured
- [ ] Resource monitors active
- [ ] Tasks scheduled and running
- [ ] Performance optimizations applied

## Troubleshooting

### Issue: Cortex AI Not Available
**Solution**: Contact Snowflake support to enable Cortex features on your account.

### Issue: Insufficient Privileges
**Solution**: 
```sql
USE ROLE ACCOUNTADMIN;
GRANT IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE TO ROLE your_role;
```

### Issue: Streamlit App Won't Load
**Solution**: 
- Check warehouse is running
- Verify database/schema permissions
- Check for Python package conflicts

### Issue: Slow Query Performance
**Solution**:
- Increase warehouse size
- Add clustering keys
- Create materialized views
- Enable search optimization

### Issue: High Costs
**Solution**:
- Reduce warehouse size
- Decrease auto-suspend time (minimum 60 seconds)
- Review resource monitor settings
- Use smaller warehouse for development

## Maintenance

### Daily Tasks
- Monitor credit usage
- Check for extreme threat alerts
- Review new sightings

### Weekly Tasks
- Analyze AI model performance
- Review investigation progress
- Check data quality

### Monthly Tasks
- Archive closed investigations
- Update threat assessments
- Review and optimize queries
- Analyze usage patterns

## Scaling for Production

### For 100+ Daily Sightings
- Increase warehouse to Large/X-Large
- Enable multi-cluster warehouse (2-4 clusters)
- Implement data retention policies
- Add more materialized views

### For Multiple Regions
- Set up replication groups
- Configure failover databases
- Implement geo-distributed stages

### For Enterprise Use
- Implement full RBAC model
- Add comprehensive audit logging
- Set up alerting integrations
- Create disaster recovery plan

## Support

For issues or questions:
1. Check Snowflake documentation
2. Review error logs in Snowsight
3. Check warehouse history
4. Review query profile for performance issues

## Version History

- v1.0.0 (2024-10-15): Initial release
  - Core tables and data model
  - Cortex AI integration
  - Streamlit application
  - Sample data and analytics

---

**Deployment Complete! Time to catch some ghosts!** 👻🚫

