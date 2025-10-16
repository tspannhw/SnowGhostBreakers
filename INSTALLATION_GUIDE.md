# 📦 Ghost Detection System - Installation Guide

Complete installation instructions for all deployment methods.

---

## 🎯 Choose Your Installation Method

| Method | Time | Best For | Difficulty |
|--------|------|----------|------------|
| **Snowflake Worksheet** | 15 min | UI users, step-by-step control | ⭐ Easy |
| **Python Installer** | 5 min | Quick automated setup | ⭐⭐ Moderate |
| **SnowSQL CLI** | 10 min | Command-line users | ⭐⭐ Moderate |

---

## Method 1: Snowflake Worksheet (Recommended for UI Users)

### Step-by-Step Installation

**Time:** ~15 minutes  
**Prerequisites:** Snowflake account with ACCOUNTADMIN role

#### 1. Open Snowflake UI
Navigate to: https://app.snowflake.com/

#### 2. Create New Worksheet
Click **+ Worksheet** in the top left

#### 3. Execute Scripts in Order

Run each script below **in order** by copying the entire file content into a worksheet:

##### Script 1: Setup Database (2 min)
```sql
-- Open and run: sql/01_setup_database.sql
-- Creates database, schemas, roles, and warehouse
```

##### Script 2: Create Tables (2 min)
```sql
-- Open and run: sql/02_create_tables.sql
-- Creates all core tables
```

##### Script 3: Sample Data (1 min)
```sql
-- Open and run: sql/03_sample_data.sql
-- Inserts sample data
```

##### Script 4: Stored Procedures (3 min)
```sql
-- Open and run: sql/04_stored_procedures.sql
-- Creates all stored procedures
```

##### Script 5: Semantic Views (2 min)
```sql
-- Open and run: sql/05_semantic_views.sql
-- Creates analytics views
```

##### Script 6: Cortex AI Functions (2 min)
```sql
-- Open and run: sql/06_cortex_ai_functions.sql
-- Sets up Cortex AI integration
```

##### Script 7: AISQL Examples (Optional - 1 min)
```sql
-- Open and run: sql/07_aisql_examples.sql
-- Creates AISQL example queries
```

##### Script 8: Business Vocabulary (2 min)
```sql
-- Open and run: sql/08_business_vocabulary.sql
-- Creates vocabulary and ontology
```

##### Script 9: Agentic AI System (3 min)
```sql
-- Open and run: sql/09_agentic_ai_system.sql
-- Sets up AI agents
```

##### Script 10: Snowflake MCP Server (2 min)
```sql
-- Open and run: sql/10_snowflake_native_mcp_server.sql
-- Creates native MCP server
```

#### 4. Verify Installation

```sql
-- Check database exists
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Verify tables
SHOW TABLES IN GHOST_DETECTION.APP;

-- Count records
SELECT COUNT(*) FROM GHOSTS;
SELECT COUNT(*) FROM GHOST_SIGHTINGS;

-- Check MCP server
SHOW MCP SERVERS IN DATABASE GHOST_DETECTION;

-- Get OAuth credentials (save these!)
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');
```

#### 5. ✅ Installation Complete!

---

## Method 2: Python Installer (Fastest - Automated)

### Automated Installation Script

**Time:** ~5 minutes  
**Prerequisites:** 
- Python 3.8+
- snowflake-connector-python

#### 1. Install Dependencies

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
pip install snowflake-connector-python
```

#### 2. Run Installer

```bash
python scripts/install_all.py
```

#### 3. Provide Connection Details

The script will prompt you for:
- Snowflake account
- Username
- Password
- Warehouse (default: COMPUTE_WH)
- Role (default: ACCOUNTADMIN)

#### 4. Wait for Installation

The script will:
- ✅ Connect to Snowflake
- ✅ Execute all 10 SQL scripts in order
- ✅ Verify installation
- ✅ Provide summary

#### 5. ✅ Done!

```
✅ INSTALLATION COMPLETE!
🎉 Ghost Detection System is ready to use!
```

---

## Method 3: SnowSQL CLI

### Command-Line Installation

**Time:** ~10 minutes  
**Prerequisites:** 
- SnowSQL CLI installed
- Snowflake credentials configured

#### 1. Install SnowSQL (if needed)

```bash
# macOS
brew install snowflake-snowsql

# Linux/Windows
# Download from: https://docs.snowflake.com/en/user-guide/snowsql-install-config
```

#### 2. Configure SnowSQL

Create/edit `~/.snowsql/config`:

```ini
[connections.ghost_detection]
accountname = <your_account>
username = <your_username>
password = <your_password>
warehouse = COMPUTE_WH
role = ACCOUNTADMIN
```

#### 3. Run Setup Script

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers

# Run master setup script
snowsql -c ghost_detection -f setup_snowsql.sql
```

#### 4. Verify Installation

```bash
snowsql -c ghost_detection -q "SHOW TABLES IN GHOST_DETECTION.APP;"
snowsql -c ghost_detection -q "SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOSTS;"
```

#### 5. ✅ Installation Complete!

---

## 🔍 Verification Checklist

After installation, verify these components exist:

### Database Objects

```sql
-- ✅ Database exists
SHOW DATABASES LIKE 'GHOST_DETECTION';

-- ✅ Tables (13 total)
SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'APP';

-- ✅ Views (11 total)
SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.VIEWS 
WHERE TABLE_SCHEMA = 'ANALYTICS';

-- ✅ Procedures (18+ total)
SELECT COUNT(*) FROM GHOST_DETECTION.INFORMATION_SCHEMA.PROCEDURES 
WHERE PROCEDURE_SCHEMA = 'APP';
```

### Data Verification

```sql
-- ✅ Sample data loaded
SELECT COUNT(*) as ghost_count FROM GHOST_DETECTION.APP.GHOSTS;
-- Expected: 10+

SELECT COUNT(*) as sighting_count FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;
-- Expected: 25+

SELECT COUNT(*) as evidence_count FROM GHOST_DETECTION.APP.GHOST_EVIDENCE;
-- Expected: 15+
```

### AI Components

```sql
-- ✅ AI Agents created
SELECT COUNT(*) FROM GHOST_DETECTION.APP.AI_AGENTS;
-- Expected: 5

-- ✅ Business vocabulary
SELECT COUNT(*) FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY;
-- Expected: 50+

-- ✅ Ontology classes
SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_ONTOLOGY;
-- Expected: 20+
```

### MCP Server

```sql
-- ✅ MCP Server exists
SHOW MCP SERVERS IN DATABASE GHOST_DETECTION;
-- Expected: GHOST_DETECTION_MCP_SERVER

-- ✅ OAuth integration
SHOW INTEGRATIONS LIKE 'GHOST_MCP_OAUTH';
-- Expected: GHOST_MCP_OAUTH

-- ✅ Cortex Search services
SHOW CORTEX SEARCH SERVICES IN SCHEMA APP;
-- Expected: 3 services
```

### Test Functionality

```sql
-- ✅ Test Cortex AI
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Say "Ghost Detection System is working!" if you can read this.'
) as test_result;

-- ✅ Test stored procedure
CALL CALCULATE_THREAT_SCORE(1);

-- ✅ Test search
SELECT * FROM TABLE(TEST_GHOST_SEARCH('shadow'));

-- ✅ Test view
SELECT * FROM VW_GHOST_ACTIVITY_SUMMARY LIMIT 5;
```

---

## 🚨 Troubleshooting

### Common Issues

#### Issue 1: "Insufficient privileges"

**Solution:**
```sql
-- Use ACCOUNTADMIN role
USE ROLE ACCOUNTADMIN;

-- Or grant privileges
GRANT CREATE DATABASE ON ACCOUNT TO ROLE <your_role>;
```

#### Issue 2: "Warehouse not running"

**Solution:**
```sql
-- Resume warehouse
ALTER WAREHOUSE GHOST_WAREHOUSE RESUME;

-- Or use existing warehouse
USE WAREHOUSE COMPUTE_WH;
```

#### Issue 3: "Cortex AI not available"

**Solution:**
- Verify Cortex is enabled in your Snowflake account
- Check account region supports Cortex
- Contact Snowflake support

#### Issue 4: "Table already exists"

**Solution:**
```sql
-- Drop existing database (⚠️ CAUTION: Deletes all data!)
DROP DATABASE IF EXISTS GHOST_DETECTION CASCADE;

-- Then re-run installation
```

#### Issue 5: "!source command not working"

**Problem:** You're using Snowflake worksheet, not SnowSQL  
**Solution:** Use Method 1 (Worksheet) or Method 2 (Python) instead

#### Issue 6: "MCP Server creation failed"

**Solution:**
```sql
-- Check if preview feature is enabled
-- MCP is currently in preview
-- Contact Snowflake support to enable if needed

-- Or wait for general availability
```

---

## 📊 Installation Summary

### What Gets Installed

| Component | Count | Description |
|-----------|-------|-------------|
| **Database** | 1 | GHOST_DETECTION |
| **Schemas** | 2 | APP, ANALYTICS |
| **Tables** | 13 | Core data tables |
| **Views** | 11 | Analytics views |
| **Procedures** | 18+ | Stored procedures |
| **Functions** | 10+ | Helper functions |
| **AI Agents** | 5 | Agentic AI agents |
| **MCP Server** | 1 | Native MCP server |
| **MCP Tools** | 4 | AI-powered tools |
| **Search Services** | 3 | Cortex Search |
| **OAuth Integration** | 1 | For MCP auth |
| **Roles** | 3 | GHOSTBUSTER, GHOST_ANALYST, GHOST_ADMIN |
| **Warehouse** | 1 | GHOST_WAREHOUSE |

### Disk Space

Approximate sizes:
- Database: ~50 MB (with sample data)
- Cortex Search indexes: ~10 MB
- Total: ~60 MB

### Credits Usage

Estimated credits for installation:
- Setup: < 0.1 credits
- Sample data: < 0.1 credits
- Cortex Search indexing: < 0.5 credits
- **Total: < 1 credit**

---

## 🎯 Post-Installation Steps

### 1. Get OAuth Credentials

```sql
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');
```

**Save these values securely!**

### 2. Configure MCP Client

Edit `mcp/snowflake_native_mcp_client_config.json` with your credentials.

### 3. Deploy Streamlit App (Optional)

```bash
cd streamlit_app
streamlit run ghost_detection_app.py
```

### 4. Review Documentation

- **Quick Start:** `QUICKSTART.md`
- **MCP Setup:** `SNOWFLAKE_MCP_QUICKSTART.md`
- **Full Guide:** `README.md`

### 5. Start Using!

```sql
-- Query ghosts
SELECT * FROM GHOSTS WHERE threat_level = 'Extreme';

-- Search with MCP
-- (see SNOWFLAKE_MCP_GUIDE.md)

-- Run analytics
SELECT * FROM VW_PARANORMAL_HOTSPOTS;
```

---

## 📚 Additional Resources

- **Main README:** `README.md`
- **Quick Start:** `QUICKSTART.md`
- **MCP Guide:** `SNOWFLAKE_MCP_GUIDE.md`
- **Agentic AI:** `AGENTIC_AI_GUIDE.md`
- **Test Suite:** `tests/README.md`
- **Features:** `FEATURES_SUMMARY.md`

---

## 🆘 Need Help?

1. **Check troubleshooting section above**
2. **Review error messages carefully**
3. **Verify prerequisites are met**
4. **Try running scripts one at a time**
5. **Check Snowflake documentation**

---

## ✅ Installation Complete!

If all verification checks pass, your Ghost Detection System is ready to use!

**Next Steps:**
1. ✅ Review `QUICKSTART.md` for usage examples
2. ✅ Set up MCP server (see `SNOWFLAKE_MCP_QUICKSTART.md`)
3. ✅ Deploy Streamlit app
4. ✅ Start catching ghosts! 👻🚫

---

**Installation Time:** 5-15 minutes (depending on method)  
**Difficulty:** Easy to Moderate  
**Status:** Production Ready ✅

