# 🚀 Installation Quick Reference

You're absolutely right - `!source` doesn't work in Snowflake worksheets! Here are your options:

---

## ⭐ Option 1: Snowflake Worksheet (RECOMMENDED)

**Best for:** UI users who want step-by-step control  
**Time:** 15 minutes  
**Difficulty:** ⭐ Easy

### Steps:

1. **Open Snowflake UI** → Create new worksheet
2. **Copy & paste each SQL file** into worksheet (in order)
3. **Run each script** one at a time

### Order of Execution:

```
1. sql/01_setup_database.sql          ← Database & schemas
2. sql/02_create_tables.sql           ← Core tables
3. sql/03_sample_data.sql             ← Sample data
4. sql/04_stored_procedures.sql       ← Procedures
5. sql/05_semantic_views.sql          ← Views
6. sql/06_cortex_ai_functions.sql     ← Cortex AI
7. sql/07_aisql_examples.sql          ← AISQL (optional)
8. sql/08_business_vocabulary.sql     ← Vocabulary
9. sql/09_agentic_ai_system.sql       ← Agentic AI
10. sql/10_snowflake_native_mcp_server.sql  ← MCP Server
```

### Pro Tip:
Open each file in a separate worksheet tab for easy navigation!

---

## ⚡ Option 2: Python Automated Installer (FASTEST)

**Best for:** Quick automated setup  
**Time:** 5 minutes  
**Difficulty:** ⭐⭐ Moderate

### Steps:

```bash
# 1. Install dependencies
pip install snowflake-connector-python

# 2. Run installer
python scripts/install_all.py

# 3. Enter your Snowflake credentials when prompted
```

The script automatically:
- ✅ Connects to Snowflake
- ✅ Runs all 10 SQL scripts in order
- ✅ Verifies installation
- ✅ Shows completion summary

---

## 🖥️ Option 3: SnowSQL CLI

**Best for:** Command-line users  
**Time:** 10 minutes  
**Difficulty:** ⭐⭐ Moderate

### Steps:

```bash
# 1. Configure SnowSQL (one-time setup)
# Edit ~/.snowsql/config with your credentials

# 2. Run master setup script
snowsql -c your_connection -f setup_snowsql.sql
```

**Note:** This is the ONLY option where `!source` commands work!

---

## 📊 Comparison

| Feature | Worksheet | Python | SnowSQL |
|---------|-----------|--------|---------|
| **Setup Time** | 15 min | 5 min | 10 min |
| **Automation** | Manual | Automatic | Automatic |
| **Prerequisites** | None | Python + package | SnowSQL CLI |
| **Control** | Full | Automated | Automated |
| **Error Handling** | Manual | Shows errors | Shows errors |
| **Best For** | UI users | Quick setup | CLI users |

---

## ✅ After Installation

Verify everything worked:

```sql
-- Check database exists
USE DATABASE GHOST_DETECTION;

-- Count objects
SHOW TABLES IN GHOST_DETECTION.APP;
SHOW MCP SERVERS IN DATABASE GHOST_DETECTION;

-- Get OAuth credentials (SAVE THESE!)
SELECT SYSTEM$SHOW_OAUTH_CLIENT_SECRETS('GHOST_MCP_OAUTH');
```

---

## 🆘 Need More Help?

See **`INSTALLATION_GUIDE.md`** for:
- Detailed step-by-step instructions
- Troubleshooting common issues
- Verification checklist
- Post-installation steps

---

## 🎯 Recommended Path

**For most users:** Use **Option 1 (Snowflake Worksheet)**
- Most reliable
- Full control
- Works in any Snowflake account
- No additional tools needed

**For speed:** Use **Option 2 (Python Installer)**
- Fastest installation
- Automated verification
- Great for repeated deployments

---

**Questions?** Check `INSTALLATION_GUIDE.md` for complete instructions!

