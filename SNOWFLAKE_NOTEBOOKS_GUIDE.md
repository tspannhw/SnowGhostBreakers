# 📓 Snowflake Notebooks Guide for SnowGhost Breakers

## 🎯 Overview

Two comprehensive Jupyter notebooks for Snowflake-native data analysis:

1. **`multimodal_ghost_analytics.ipynb`** - Advanced multimodal paranormal analysis
2. **`standard_ghost_load.ipynb`** - Standard data loading pipeline

Both notebooks are designed to run **natively in Snowflake Notebooks** or locally with Snowpark.

---

## 🚀 Running Notebooks in Snowflake

### Method 1: Snowflake Notebooks (Recommended)

#### Step 1: Upload Notebook
```sql
-- In Snowsight, navigate to:
Projects → Notebooks → Create → Import .ipynb file
```

1. Click **"Create"** → **"Notebook"**
2. Select **"Import from .ipynb file"**
3. Choose `multimodal_ghost_analytics.ipynb` or `standard_ghost_load.ipynb`
4. Select database: **GHOST_DETECTION**
5. Select schema: **APP**
6. Select warehouse: **COMPUTE_WH**

#### Step 2: Install Required Packages

**In the Snowflake Notebook UI:**

1. Click **"Packages"** button at the top right
2. Search and add these packages:
   - `snowflake-snowpark-python` (usually pre-installed)
   - `pandas`
   - `numpy`
   - `plotly`

**Important:** `snowflake.cortex` is **built-in** and does NOT need installation!

#### Step 3: Configure Session

The `session` variable is **automatically available** in Snowflake Notebooks. No configuration needed!

```python
# This works automatically in Snowflake Notebooks:
session.sql("SELECT CURRENT_VERSION()").collect()
```

#### Step 4: Run Cells

Click **"Run All"** or execute cells individually (Shift+Enter).

---

## ⚠️ Fix: ModuleNotFoundError: snowflake.cortex

### Problem
```
ModuleNotFoundError: Line 5: Module Not Found: snowflake.cortex
```

### ✅ Solution

**`snowflake.cortex` is NOT a Python module!**

In Snowflake Notebooks, Cortex AI functions are accessed via **SQL**, not Python imports.

#### ❌ WRONG (Python):
```python
from snowflake.cortex import Complete  # ❌ This doesn't exist!

result = Complete('mistral-large2', 'Analyze this ghost')
```

#### ✅ CORRECT (SQL via session):
```python
# Use SQL to call Cortex functions
result = session.sql("""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        'Analyze this paranormal evidence'
    ) as analysis
""").collect()[0]['ANALYSIS']

print(result)
```

#### ✅ CORRECT (For Streamlit):
```python
# In Streamlit, use the snowflake.cortex Python package:
from snowflake.cortex import Complete, Sentiment

# This works in Streamlit apps
analysis = Complete('mistral-large2', 'Analyze ghost data')
sentiment = Sentiment('This ghost is scary')
```

---

## 📚 Notebook Summaries

### 1️⃣ Multimodal Ghost Analytics

**Purpose:** Comprehensive multimodal paranormal investigation analysis

**Features:**
- 📸 **Image Analysis** - Cortex Vision AI for photo evidence
- 🔊 **Audio Analysis** - EVP and sound pattern detection
- 📊 **Sensor Correlation** - EMF/temperature/sound patterns
- 🧠 **Intelligence Fusion** - Multi-source data integration
- ⏰ **Temporal Analysis** - Time-based activity patterns
- 🗺️ **Geographic Mapping** - Location-based evidence distribution
- ⚠️ **Anomaly Detection** - Statistical outlier identification
- 📋 **Intelligence Reports** - Comprehensive field team reports

**Run Time:** ~5-10 minutes  
**Prerequisites:** Loaded ghost/evidence data

**Sample Output:**
```
📊 Collected 87 multimodal evidence records
🔍 Analyzed 15 images with Cortex Vision AI
🔊 Analyzed 12 audio evidence records
⚠️ Detected 8 anomalous readings
📊 Generated intelligence profiles for 5 high-priority ghosts
```

---

### 2️⃣ Standard Ghost Data Loading

**Purpose:** Load comprehensive paranormal investigation data

**Features:**
- 👻 **Ghost Entities** - 50 sample paranormal entities
- 📍 **Sightings** - 200+ location-based observations
- 🔬 **Evidence** - 100+ multimedia evidence files
- 📡 **Sensor Readings** - 1000+ EMF/temp/sound measurements
- 👥 **Investigators** - SnowGhost Breakers team members
- ✅ **Data Quality** - Referential integrity checks

**Run Time:** ~2-3 minutes  
**Output:** Fully populated database

**Sample Output:**
```
📊 SNOWGHOST BREAKERS DATA LOAD SUMMARY
============================================================
GHOSTS              50
GHOST_EVIDENCE      107
GHOST_SIGHTINGS     213
INVESTIGATORS       5
SENSOR_READINGS     1,284
============================================================
✅ Total records loaded: 1,659
🎯 SnowGhost Breakers database ready for operations!
```

---

## 🔧 Common Issues & Solutions

### Issue 1: Package Not Found

**Error:**
```
ModuleNotFoundError: No module named 'pandas'
```

**Solution:**
1. Click **"Packages"** button
2. Search for `pandas`
3. Click **"Add"**
4. Restart kernel if needed

---

### Issue 2: Table Not Found

**Error:**
```
SQL compilation error: Object 'GHOST_DETECTION.APP.GHOSTS' does not exist
```

**Solution:**
Run the setup scripts first:
```bash
# In SnowSQL or Snowflake Worksheet
!source sql/01_setup_database.sql
!source sql/02_create_tables.sql
!source sql/03_sample_data.sql
```

Or run `standard_ghost_load.ipynb` to populate data.

---

### Issue 3: Session Not Found

**Error:**
```
NameError: name 'session' is not defined
```

**Solution:**

**In Snowflake Notebooks:** Session is automatic. This error shouldn't occur.

**In Local Jupyter:** Create session manually:
```python
from snowflake.snowpark import Session

connection_parameters = {
    "account": "YOUR_ACCOUNT",
    "user": "YOUR_USER",
    "password": "YOUR_PASSWORD",
    "role": "SYSADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "GHOST_DETECTION",
    "schema": "APP"
}

session = Session.builder.configs(connection_parameters).create()
```

---

### Issue 4: Cortex Functions Not Working

**Error:**
```
SQL compilation error: Unknown function SNOWFLAKE.CORTEX.COMPLETE
```

**Solution:**

Ensure you have Cortex AI access:
```sql
-- Check access
SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', 'Hello') as test;

-- If error, contact admin to enable Cortex AI
-- Requires Snowflake Enterprise Edition or higher
```

---

## 📊 Sample Notebook Workflow

### Complete Analysis Workflow

```python
# 1. Load fresh data
# Run: standard_ghost_load.ipynb

# 2. Analyze multimodal evidence  
# Run: multimodal_ghost_analytics.ipynb

# 3. View results in Streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

---

## 🎓 Best Practices

### 1. Data Loading
- ✅ Run `standard_ghost_load.ipynb` first
- ✅ Verify data quality after load
- ✅ Check for orphaned records

### 2. Multimodal Analysis
- ✅ Ensure evidence files are staged
- ✅ Use appropriate Cortex models
- ✅ Filter date ranges for performance

### 3. Performance
- ✅ Use LIMIT clauses for large datasets
- ✅ Create aggregated views for repeated queries
- ✅ Use appropriate warehouse size

### 4. Cortex AI Usage
- ✅ Use SQL syntax: `SNOWFLAKE.CORTEX.COMPLETE()`
- ✅ Choose appropriate models:
  - `llama3-70b` - Best quality
  - `mistral-large2` - Fast and accurate
  - `llama3-8b` - Fast for simple tasks

---

## 📈 Performance Optimization

### Warehouse Sizing

| Warehouse | Use Case | Cost |
|-----------|----------|------|
| **X-Small** | Testing, small datasets | $ |
| **Small** | Standard analysis | $$ |
| **Medium** | Large multimodal analysis | $$$ |
| **Large** | Full corpus processing | $$$$ |

### Query Optimization

```python
# ✅ GOOD: Filter early
df = session.table("GHOST_EVIDENCE").filter(
    col("CAPTURED_DATETIME") >= '2024-01-01'
).limit(100).to_pandas()

# ❌ BAD: Load all then filter in pandas
df = session.table("GHOST_EVIDENCE").to_pandas()
df = df[df['CAPTURED_DATETIME'] >= '2024-01-01'][:100]
```

---

## 🔗 Integration with Other Tools

### Export to Pandas
```python
df = session.sql("SELECT * FROM GHOSTS").to_pandas()
df.to_csv('ghosts_export.csv', index=False)
```

### Use with Matplotlib
```python
import matplotlib.pyplot as plt

df = session.table("GHOST_SIGHTINGS").to_pandas()
df['PARANORMAL_ACTIVITY_LEVEL'].hist(bins=10)
plt.title('Activity Level Distribution')
plt.show()
```

### Schedule Notebooks
```sql
-- Create task to run notebook daily
CREATE TASK daily_ghost_analysis
    WAREHOUSE = COMPUTE_WH
    SCHEDULE = 'USING CRON 0 2 * * * America/New_York'
AS
    EXECUTE NOTEBOOK multimodal_ghost_analytics;
```

---

## 🎯 Quick Start Checklist

- [ ] Upload notebooks to Snowflake
- [ ] Install required packages (pandas, numpy, plotly)
- [ ] Verify `session` variable works
- [ ] Run `standard_ghost_load.ipynb`
- [ ] Verify data with: `SELECT COUNT(*) FROM GHOSTS;`
- [ ] Run `multimodal_ghost_analytics.ipynb`
- [ ] Review generated intelligence reports
- [ ] View results in Streamlit app
- [ ] ✅ Start hunting ghosts!

---

## 📞 Support

**Common Errors:**
- `ModuleNotFoundError: snowflake.cortex` → Use SQL syntax, not Python import
- `Table not found` → Run setup scripts first
- `Session not defined` → Use Snowflake Notebooks or create session manually
- `Package not found` → Use Packages button to install

**Resources:**
- [Snowflake Notebooks Documentation](https://docs.snowflake.com/en/user-guide/ui-snowsight-notebooks)
- [Cortex AI Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex)
- [Snowpark Python Documentation](https://docs.snowflake.com/en/developer-guide/snowpark/python/index)

---

**🎊 Your SnowGhost Breakers notebooks are ready to analyze paranormal phenomena!** 👻📊✨

**Adapted from:** [Original AIM-Ghosts Repository](https://github.com/tspannhw/AIM-Ghosts)  
**Organization:** SnowGhost Breakers Paranormal Investigation Unit

