# 🔧 Create Vocabulary & Taxonomy Tables

## ✅ Quick Setup Options

You have **3 easy options** to create the tables:

---

## Option 1: Snowflake Web UI (Easiest) ⭐

### Step 1: Open the SQL File
1. Open the file: `sql/08_business_vocabulary.sql`
2. Copy **ALL** the contents (Cmd+A, Cmd+C)

### Step 2: Run in Snowflake Worksheet
1. Go to: https://app.snowflake.com
2. Click **"Worksheets"** in left menu
3. Click **"+ Worksheet"** to create new worksheet
4. **Paste** all the SQL content
5. Click **"Run All"** (▶▶) button at top
6. Wait ~30 seconds for completion

### Step 3: Verify Tables Created
```sql
-- Run this to check
SELECT COUNT(*) FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY;
SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_TAXONOMY;

-- Should see rows returned ✅
```

---

## Option 2: SnowSQL Command Line

### Step 1: Configure SnowSQL (One-time)
```bash
# Create SnowSQL config
snowsql -a <your_account> -u <your_username>
# Example: snowsql -a xy12345.us-east-1 -u john_doe
```

### Step 2: Run the Script
```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
snowsql -f sql/08_business_vocabulary.sql
```

---

## Option 3: Python Script (Automated)

### Create and Run Setup Script:

Create file: `setup_vocabulary.py`
```python
import snowflake.connector
import os

# Configure your Snowflake connection
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse='COMPUTE_WH',
    database='GHOST_DETECTION',
    schema='APP'
)

cursor = conn.cursor()

# Read and execute the SQL file
with open('sql/08_business_vocabulary.sql', 'r') as f:
    sql_commands = f.read()
    
# Split by semicolons and execute each command
for command in sql_commands.split(';'):
    if command.strip():
        try:
            cursor.execute(command)
            print(f"✅ Executed: {command[:50]}...")
        except Exception as e:
            print(f"❌ Error: {e}")

cursor.close()
conn.close()
print("\n✅ Vocabulary tables created!")
```

Then run:
```bash
export SNOWFLAKE_USER="your_username"
export SNOWFLAKE_PASSWORD="your_password"
export SNOWFLAKE_ACCOUNT="your_account"

python setup_vocabulary.py
```

---

## 🎯 Recommended: Option 1 (Web UI)

**This is the fastest and easiest!**

1. ✅ No command-line setup needed
2. ✅ Visual feedback
3. ✅ Copy-paste in 30 seconds
4. ✅ Works immediately

---

## 📋 What Gets Created

### Tables (5):
1. ✅ **BUSINESS_VOCABULARY** - Ghost terminology definitions
2. ✅ **GHOST_TAXONOMY** - Ghost classification hierarchy
3. ✅ **TAXONOMY_ATTRIBUTES** - Detailed attributes
4. ✅ **GHOST_ONTOLOGY** - Ghost relationships
5. ✅ **ONTOLOGY_RELATIONSHIPS** - Relationship types

### Views (3):
1. ✅ **VW_TAXONOMY_HIERARCHY** - Tree view of classifications
2. ✅ **VW_ONTOLOGY_GRAPH** - Complete relationship graph
3. ✅ **VW_TERM_DEFINITIONS** - Searchable term definitions

### Functions (2):
1. ✅ **GET_TERM_RELATIONSHIPS(term_id)** - Find related terms
2. ✅ **SEARCH_VOCABULARY(search_term)** - Full-text search

### Sample Data:
- ✅ 30+ vocabulary terms
- ✅ 15+ taxonomy classifications
- ✅ 40+ taxonomy attributes
- ✅ 20+ ontology relationships

---

## ✅ Verification Script

After running the setup, verify with this SQL:

```sql
-- Check all tables exist and have data
SELECT 'BUSINESS_VOCABULARY' as table_name, COUNT(*) as row_count 
FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY
UNION ALL
SELECT 'GHOST_TAXONOMY', COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_TAXONOMY
UNION ALL
SELECT 'TAXONOMY_ATTRIBUTES', COUNT(*) 
FROM GHOST_DETECTION.APP.TAXONOMY_ATTRIBUTES
UNION ALL
SELECT 'GHOST_ONTOLOGY', COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_ONTOLOGY
UNION ALL
SELECT 'ONTOLOGY_RELATIONSHIPS', COUNT(*) 
FROM GHOST_DETECTION.APP.ONTOLOGY_RELATIONSHIPS;

-- Expected results:
-- BUSINESS_VOCABULARY: 30+ rows
-- GHOST_TAXONOMY: 15+ rows
-- TAXONOMY_ATTRIBUTES: 40+ rows
-- GHOST_ONTOLOGY: 15+ rows
-- ONTOLOGY_RELATIONSHIPS: 20+ rows
```

---

## 🐛 Troubleshooting

### Issue: "Database does not exist"
```sql
-- Create database first
CREATE DATABASE IF NOT EXISTS GHOST_DETECTION;
CREATE SCHEMA IF NOT EXISTS GHOST_DETECTION.APP;
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;
```

### Issue: "Permission denied"
```
Ask your Snowflake admin to grant you:
- CREATE TABLE permissions
- CREATE VIEW permissions
- CREATE FUNCTION permissions
```

### Issue: "Syntax error"
```
Make sure you copied the ENTIRE file content, including:
- All CREATE TABLE statements
- All INSERT statements
- All CREATE VIEW statements
- All CREATE FUNCTION statements
```

---

## 🎯 Quick Copy-Paste Instructions

### For Snowflake Web UI:

**Step-by-Step:**
1. Open `sql/08_business_vocabulary.sql` in your editor
2. Select All (Cmd+A / Ctrl+A)
3. Copy (Cmd+C / Ctrl+C)
4. Go to Snowflake Web UI
5. Worksheets → + New Worksheet
6. Paste (Cmd+V / Ctrl+V)
7. Click "Run All" button (▶▶)
8. Wait for completion (~30 seconds)
9. ✅ Done!

---

## 📊 What This Enables in Streamlit

Once tables are created, the Streamlit app will show:

### 📚 Vocabulary Page:
- ✅ Browse all ghost-related terms
- ✅ Search vocabulary with synonyms
- ✅ View taxonomy hierarchy
- ✅ Explore term relationships

### 🔍 Search Features:
- ✅ Full-text search across definitions
- ✅ Synonym matching
- ✅ Related term discovery

### 🌳 Taxonomy Browser:
- ✅ Ghost classification levels
- ✅ Parent-child relationships
- ✅ Detailed attributes
- ✅ Visual hierarchy

---

## ⏱️ Time Estimate

- **Copy-Paste Method:** 30 seconds
- **SnowSQL Method:** 2 minutes
- **Python Script:** 5 minutes (first time setup)

---

## ✅ After Creation

1. **Restart Streamlit:**
   ```bash
   pkill -f streamlit
   streamlit run streamlit_app/ghost_detection_app.py
   ```

2. **Test in Streamlit:**
   - Go to **📚 Vocabulary** page
   - Search for "ghost"
   - ✅ Should show matching terms

---

**🎊 Choose Option 1 (Web UI) for the quickest setup!** 📋✨

**Questions?** See `sql/08_business_vocabulary.sql` for the complete SQL code.

