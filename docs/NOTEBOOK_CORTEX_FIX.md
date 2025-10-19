# 🔧 Fix Snowflake Notebook Cortex Import Error

## ❌ Error

```
ModuleNotFoundError: Line 5: Module Not Found: snowflake.cortex
To import packages from Anaconda, install them first using the package selector at the top of the page.
```

---

## ✅ Fix Applied

### Problem:
The notebook tried to import Cortex AI functions as Python modules:
```python
from snowflake.cortex import Complete, Sentiment, Translate  # ❌ Doesn't work!
```

### Root Cause:
- `snowflake.cortex` is **NOT** a Python package
- It's a **SQL function namespace** in Snowflake
- Cannot be imported in Python code

### Solution:
**Remove the incorrect import line** from Cell 2 (Setup & Configuration).

---

## 🔧 How to Fix

### Option 1: Edit in Snowflake UI (Recommended)

1. Open notebook: `notebooks/01_ghost_analytics.ipynb` in Snowflake
2. Find **Cell 2** (Setup & Configuration)
3. **Delete this line:**
   ```python
   from snowflake.cortex import Complete, Sentiment, Translate
   ```
4. **Keep everything else** in that cell
5. Click **"Run Cell"** or **"Run All"**
6. ✅ Error should be gone!

### Correct Cell 2 Code:

```python
# Cell 2: Setup & Configuration

from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import functions as F
from snowflake.snowpark.types import StringType
# REMOVED: from snowflake.cortex import Complete, Sentiment, Translate  ← Delete this line!
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Get Snowflake session
session = get_active_session()

# Set context
session.sql("USE DATABASE GHOST_DETECTION").collect()
session.sql("USE SCHEMA APP").collect()

print("✅ Connected to Snowflake Ghost Detection Database")
print(f"📊 Session ID: {session.get_current_database()}")
print(f"🏢 Warehouse: {session.get_current_warehouse()}")
print(f"👤 User: {session.get_current_user()}")
```

---

## 📚 How to Use Cortex AI in Snowflake Notebooks

### ❌ WRONG Way (Python Import):
```python
from snowflake.cortex import Complete  # ❌ Doesn't exist!
result = Complete('mistral-large2', 'prompt')  # ❌ Won't work!
```

### ✅ CORRECT Way (SQL Functions):

#### Method 1: Using session.sql()
```python
# Text generation
result = session.sql("""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        'Describe a ghost sighting'
    ) as response
""").collect()[0]['RESPONSE']

print(result)
```

#### Method 2: Using SQL in queries
```python
# Analyze ghost descriptions
analysis_df = session.sql("""
    SELECT 
        ghost_name,
        SNOWFLAKE.CORTEX.SENTIMENT(description) as sentiment,
        SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            CONCAT('Summarize this ghost: ', description)
        ) as ai_summary
    FROM GHOSTS
    LIMIT 5
""").to_pandas()

print(analysis_df)
```

#### Method 3: Inline in DataFrame operations
```python
# Get ghosts and add AI analysis
ghosts_df = session.table("GHOSTS").to_pandas()

# For each ghost, call Cortex via SQL
for idx, ghost in ghosts_df.iterrows():
    analysis = session.sql(f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            'Analyze this ghost: {ghost["GHOST_NAME"]} - {ghost["DESCRIPTION"]}'
        ) as analysis
    """).collect()[0]['ANALYSIS']
    
    print(f"{ghost['GHOST_NAME']}: {analysis}")
```

---

## 📖 Complete Cortex AI Function Reference

### All Cortex Functions (SQL Only):

```python
# 1. Text Generation
session.sql("""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        'Your prompt here'
    ) as response
""")

# 2. Sentiment Analysis
session.sql("""
    SELECT SNOWFLAKE.CORTEX.SENTIMENT(text_column) as sentiment
    FROM your_table
""")

# 3. Translation
session.sql("""
    SELECT SNOWFLAKE.CORTEX.TRANSLATE(
        text_column,
        'en',  -- source language
        'es'   -- target language
    ) as translated
    FROM your_table
""")

# 4. Text Summarization
session.sql("""
    SELECT SNOWFLAKE.CORTEX.SUMMARIZE(long_text_column) as summary
    FROM your_table
""")

# 5. Text Embeddings
session.sql("""
    SELECT SNOWFLAKE.CORTEX.AI_EMBED(
        'snowflake-arctic-embed-l-v2.0-8k',
        text_column
    ) as embedding
    FROM your_table
""")

# 6. Answer Questions
session.sql("""
    SELECT SNOWFLAKE.CORTEX.ANSWER_QUESTION(
        context_text,
        'What is the question?'
    ) as answer
""")

# 7. Extract Entities
session.sql("""
    SELECT SNOWFLAKE.CORTEX.EXTRACT_ENTITIES(
        text_column,
        ['PERSON', 'LOCATION', 'ORGANIZATION']
    ) as entities
    FROM your_table
""")
```

---

## 🧪 Test After Fix

### Test 1: Run the Fixed Cell
```python
# After removing the import line, run Cell 2
# Should print:
# ✅ Connected to Snowflake Ghost Detection Database
# 📊 Session ID: GHOST_DETECTION
# 🏢 Warehouse: COMPUTE_WH
# 👤 User: your_username
```

### Test 2: Test Cortex AI
```python
# In a new cell, test Cortex:
test_result = session.sql("""
    SELECT SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        'Say hello to the SnowGhost Breakers team!'
    ) as greeting
""").collect()[0]['GREETING']

print(test_result)
# Should print an AI-generated greeting ✅
```

### Test 3: Run All Cells
```
1. Remove the import line
2. Click "Run All" in notebook
3. ✅ Should complete without ModuleNotFoundError
```

---

## 📁 Files That Use Cortex Correctly

### Example 1: sql/07_aisql_examples.sql
```sql
-- Correct: Using SQL syntax
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Analyze ghost activity'
) as analysis
FROM GHOSTS;
```

### Example 2: streamlit_app/ghost_detection_app.py
```python
# Correct: Using session.sql() in Python
from snowflake.cortex import Complete  # ✅ This works in Streamlit!

# In Streamlit, you CAN import it (different environment)
summary = Complete('mistral-large2', prompt)
```

**Note:** The `snowflake.cortex` Python package **only works in Streamlit**, not in Snowflake Notebooks!

---

## 🎓 Key Differences

### Snowflake Notebooks:
- ❌ **Cannot** import `snowflake.cortex` as Python module
- ✅ **Must** use SQL functions via `session.sql()`
- ✅ **Must** use `SNOWFLAKE.CORTEX.FUNCTION_NAME()` syntax

### Streamlit in Snowflake:
- ✅ **Can** import `from snowflake.cortex import Complete`
- ✅ **Can** use Python API: `Complete('model', 'prompt')`
- ✅ Also supports SQL syntax

### External Python (Local):
- ✅ **Can** use `snowflake-snowpark-python[pandas]` package
- ✅ **Must** use `session.sql()` with SQL syntax
- ❌ **Cannot** import `snowflake.cortex` directly

---

## 💡 Best Practices

### DO ✅
```python
# Use session.sql() for Cortex functions
result = session.sql("""
    SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', 'prompt')
""").collect()

# Store results in DataFrame
df = session.sql("""
    SELECT 
        ghost_name,
        SNOWFLAKE.CORTEX.SENTIMENT(description) as sentiment
    FROM GHOSTS
""").to_pandas()

# Use Cortex in stored procedures (SQL)
session.sql("""
    CREATE OR REPLACE PROCEDURE analyze_ghost(ghost_id STRING)
    RETURNS STRING
    AS $$
        SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', 
            (SELECT description FROM GHOSTS WHERE ghost_id = :ghost_id)
        )
    $$
""").collect()
```

### DON'T ❌
```python
# Don't try to import in notebooks
from snowflake.cortex import Complete  # ❌ ModuleNotFoundError!

# Don't use Python API syntax in notebooks
result = Complete('model', 'prompt')  # ❌ Won't work!

# Don't forget SQL syntax
result = session.cortex.complete('model', 'prompt')  # ❌ No such method!
```

---

## 🐛 Troubleshooting

### Error: "Module Not Found: snowflake.cortex"
**Solution:** Remove the import line. Use SQL syntax instead.

### Error: "Complete is not defined"
**Cause:** You removed the import but still trying to use `Complete()` function  
**Solution:** Use `session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE(...)")`

### Error: "COMPLETE does not exist"
**Cause:** Missing `SNOWFLAKE.CORTEX.` prefix  
**Solution:** Always use full name: `SNOWFLAKE.CORTEX.COMPLETE()`

### Working Notebook Shows Different Import
**Explanation:** Some Snowflake environments may support Python API, but standard notebooks use SQL  
**Best Practice:** Use SQL syntax for maximum compatibility

---

## ✅ Quick Fix Summary

1. **Open** notebook in Snowflake
2. **Find** Cell 2 (Setup & Configuration)
3. **Delete** line: `from snowflake.cortex import Complete, Sentiment, Translate`
4. **Save** notebook
5. **Run** Cell 2
6. ✅ **No more error!**

**Time:** 30 seconds  
**Difficulty:** Easy  
**Impact:** Fixes all Cortex AI usage in notebook

---

## 📚 Related Documentation

- **Main Notebook Guide:** `SNOWFLAKE_NOTEBOOKS_GUIDE.md`
- **Cortex AI Examples:** `sql/06_cortex_ai_functions.sql`
- **AI SQL Examples:** `sql/07_aisql_examples.sql`
- **Complete Analytics:** `notebooks/COMPLETE_ANALYTICS_GUIDE.md`

---

**🎊 After this fix, your notebook will work perfectly with Cortex AI!** 🧠✨

**Last Updated:** October 16, 2025  
**Issue:** ModuleNotFoundError for snowflake.cortex  
**Fix:** Remove Python import, use SQL functions instead

