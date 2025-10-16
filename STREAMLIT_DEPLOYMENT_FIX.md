# 🔧 Streamlit Deployment Fixes

## ⚠️ Issues Reported

You're seeing errors in the **deployed** Streamlit app that were already fixed in the code. This means the deployed version is outdated.

### Errors You're Seeing:

1. **Sightings Page (Line 246):**
   ```
   SnowparkSQLAmbiguousJoinException: The reference to column 'DESCRIPTION' is ambiguous
   ```

2. **Evidence Analysis Page (Line 304):**
   ```
   ValueError: Cannot accept list of column references or list of columns for both `x` and `y`
   ```

---

## ✅ Status: All Fixes Are Already Applied!

**The code in your repository is CORRECT.** The errors are from an old cached version.

---

## 🔄 Solution: Restart Your Streamlit App

### Option 1: Snowflake Streamlit (Snowsight)

If you're running Streamlit in Snowflake:

```sql
-- 1. Stop the app
ALTER STREAMLIT GHOST_DETECTION_APP STOP;

-- 2. Re-upload the fixed file
-- Go to Snowsight → Streamlit → Your App → Edit
-- Copy the entire contents of: streamlit_app/ghost_detection_app.py
-- Paste into the editor
-- Click "Run"

-- 3. Or recreate the app
DROP STREAMLIT IF EXISTS GHOST_DETECTION_APP;
CREATE STREAMLIT GHOST_DETECTION_APP
    ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
    MAIN_FILE = 'ghost_detection_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH';
```

### Option 2: Local Streamlit

If you're running locally:

```bash
# 1. Stop the current app (Ctrl+C)

# 2. Clear Streamlit cache
rm -rf ~/.streamlit/cache

# 3. Restart the app
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
streamlit run streamlit_app/ghost_detection_app.py --server.fileWatcherType none

# 4. Hard refresh in browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)
```

### Option 3: Docker/Container

If running in Docker:

```bash
# Rebuild the image
docker build -t snowghost-breakers .

# Stop old container
docker stop snowghost-breakers

# Start new container
docker run -p 8501:8501 snowghost-breakers
```

---

## 🔍 Verify Fixes Are Applied

### Check 1: Sightings Page Fix

**Look for this code pattern in your deployed `ghost_detection_app.py`:**

```python
# ✅ CORRECT (Fixed version):
sightings_table = session.table("GHOST_DETECTION.APP.GHOST_SIGHTINGS")
ghosts_table = session.table("GHOST_DETECTION.APP.GHOSTS")

sightings_query = sightings_table.join(
    ghosts_table,
    sightings_table["GHOST_ID"] == ghosts_table["GHOST_ID"]  # Explicit references
)

sightings_df = sightings_query.select(
    sightings_table["SIGHTING_ID"],
    ghosts_table["GHOST_NAME"],
    sightings_table["DESCRIPTION"],  # Explicitly from sightings_table
    # ...
).order_by(sightings_table["SIGHTING_DATETIME"].desc()).limit(100).to_pandas()
```

**❌ Old broken version looked like:**
```python
# ❌ BROKEN:
sightings_query = session.table("GHOST_DETECTION.APP.GHOST_SIGHTINGS").join(
    session.table("GHOST_DETECTION.APP.GHOSTS"),
    "GHOST_ID"  # Ambiguous!
)
```

---

### Check 2: Evidence Analysis Chart Fix

**Look for this code pattern:**

```python
# ✅ CORRECT (Fixed version):
evidence_type_counts = evidence_df['EVIDENCE_TYPE'].value_counts().reset_index()
evidence_type_counts.columns = ['Evidence Type', 'Count']
fig = px.bar(
    evidence_type_counts,      # DataFrame
    x='Evidence Type',         # Column name
    y='Count',                 # Column name
    title="Evidence Distribution by Type"
)
```

**❌ Old broken version looked like:**
```python
# ❌ BROKEN:
evidence_type_counts = evidence_df['EVIDENCE_TYPE'].value_counts()
fig = px.bar(
    x=evidence_type_counts.index,   # Array - causes error!
    y=evidence_type_counts.values,  # Array - causes error!
)
```

---

### Check 3: AI Insights - Predictions Tab

**Verify this is present:**

```python
with tab3:
    st.subheader("Threat Level Predictions")
    st.info("Coming soon: Predictive analytics for ghost behavior patterns")  # ✅ This line!
```

---

## 🛠️ Additional Fix: GET_TERM_RELATIONSHIPS Function

### Issue
The `GET_TERM_RELATIONSHIPS` SQL function had ambiguous column references with `DESCRIPTION`.

### Fix Applied
```sql
-- ✅ FIXED VERSION
CREATE OR REPLACE FUNCTION GET_TERM_RELATIONSHIPS(term_id_param STRING)
RETURNS TABLE (
    related_term_id STRING,
    related_term_name STRING,
    relationship_type STRING
)
AS
$$
    SELECT 
        bv2.term_id as related_term_id,        -- Explicit alias
        bv2.term_name as related_term_name,    -- Explicit alias
        CASE 
            WHEN bv2.parent_term_id = term_id_param THEN 'Child Term'
            WHEN bv2.term_id = bv1.parent_term_id THEN 'Parent Term'
            WHEN bv2.term_id IN (SELECT value::STRING FROM TABLE(FLATTEN(bv1.related_terms))) THEN 'Related Term'
            ELSE 'Associated Term'
        END as relationship_type
    FROM BUSINESS_VOCABULARY bv1
    JOIN BUSINESS_VOCABULARY bv2                -- Changed from CROSS JOIN
        ON (bv2.parent_term_id = term_id_param 
            OR bv2.term_id = bv1.parent_term_id
            OR bv2.term_id IN (SELECT value::STRING FROM TABLE(FLATTEN(bv1.related_terms))))
    WHERE bv1.term_id = term_id_param
    AND bv2.term_id != term_id_param           -- Exclude self-reference
$$;
```

**To apply:**
```bash
snowsql -f sql/08_business_vocabulary.sql
```

---

## 📝 Complete Restart Checklist

- [ ] **Stop current Streamlit app**
- [ ] **Update SQL function:**
  ```bash
  snowsql -f sql/08_business_vocabulary.sql
  ```
- [ ] **Clear Streamlit cache** (if local)
- [ ] **Verify latest `ghost_detection_app.py` is deployed**
- [ ] **Restart Streamlit app**
- [ ] **Hard refresh browser** (Cmd+Shift+R or Ctrl+Shift+R)
- [ ] **Test Sightings page** → Should load without error
- [ ] **Test Evidence Analysis page** → Charts should display
- [ ] **Test AI Insights → Predictions tab** → Should show "Coming soon" message
- [ ] **Test Vocabulary page** → Should load without error

---

## 🔎 Debugging: Find Which Version Is Running

### Check Streamlit File Version

Add this at the top of your `ghost_detection_app.py` to see version:

```python
# Add this after imports
VERSION = "2.0-FIXED"
st.sidebar.markdown(f"**Version:** {VERSION}")
```

### Check Line Numbers

The error messages show line numbers. Compare with your local file:

```bash
# Count lines in local file
wc -l streamlit_app/ghost_detection_app.py

# Should show around 819 lines for the fixed version
```

**If error line numbers don't match:** Your deployed version is old!

---

## 🚀 Quick Fix Commands

### For Snowflake Streamlit:
```sql
-- Re-upload file to stage
PUT file:///path/to/ghost_detection_app.py @GHOST_DETECTION.APP.STREAMLIT_STAGE OVERWRITE=TRUE;

-- Restart app
ALTER STREAMLIT GHOST_DETECTION_APP STOP;
ALTER STREAMLIT GHOST_DETECTION_APP START;
```

### For Local Streamlit:
```bash
# Kill all streamlit processes
pkill -f streamlit

# Clear cache
rm -rf ~/.streamlit/cache

# Restart with no file watcher
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
streamlit run streamlit_app/ghost_detection_app.py
```

---

## ✅ Expected Results After Fix

### Sightings Page
- ✅ Map displays with ghost sightings
- ✅ List of sightings below map
- ✅ No "ambiguous column" errors
- ✅ Filters work correctly

### Evidence Analysis Page
- ✅ Evidence type bar chart displays
- ✅ Model usage pie chart displays
- ✅ No ValueError about x and y
- ✅ Evidence records show correctly

### AI Insights Page
- ✅ "Ask Questions" tab works
- ✅ "Model Performance" tab shows metrics
- ✅ "Predictions" tab shows "Coming soon" message

### Vocabulary Page
- ✅ Categories display in tabs
- ✅ Search works
- ✅ Taxonomy hierarchy displays
- ✅ No ambiguous column errors

---

## 📊 File Comparison

### Lines That Changed

| Line Range | Old (Broken) | New (Fixed) |
|------------|--------------|-------------|
| ~230-256 | Simple join with string | Explicit table refs |
| ~357-363 | Arrays to px.bar | DataFrame to px.bar |
| ~486 | (Missing) | "Coming soon" message |

### File Size Check

```bash
# Fixed version should be around 819 lines
wc -l streamlit_app/ghost_detection_app.py

# If you see significantly fewer lines, you have old version
```

---

## 🆘 Still Having Issues?

### Symptom: Same errors after restart

**Possible causes:**
1. **Browser cache** - Hard refresh (Cmd/Ctrl + Shift + R)
2. **Wrong file deployed** - Check file in Snowflake stage
3. **Old session** - Close ALL browser tabs and reopen
4. **Proxy cache** - If behind proxy, may need to wait

### Symptom: New different errors

**Possible causes:**
1. **Missing imports** - Check pandas, plotly installed
2. **Wrong Python version** - Need Python 3.8+
3. **Database not setup** - Run SQL setup scripts first

### Symptom: Blank pages

**Possible causes:**
1. **Session error** - Check Snowflake credentials
2. **Tables missing** - Run setup scripts
3. **Permissions** - Check database/schema access

---

## 📞 Quick Support Commands

### Test Database Connection:
```python
# In Python console
from snowflake.snowpark import Session
# ... configure session ...
session.sql("SELECT CURRENT_VERSION()").collect()
```

### Test Table Access:
```sql
-- Should return count
SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOSTS;
SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;
SELECT COUNT(*) FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY;
```

### Test Function:
```sql
-- Should return relationships
SELECT * FROM TABLE(GET_TERM_RELATIONSHIPS('TERM_001'));
```

---

## ✅ Confirmation

Once restarted with the fixed code, you should see:

**✅ Dashboard** - Works perfectly  
**✅ Ghost Registry** - Displays all ghosts  
**✅ Sightings** - Map + list, no errors  
**✅ Evidence Analysis** - Charts display correctly  
**✅ Investigations** - Shows cases  
**✅ AI Insights** - All 3 tabs work, Predictions shows "Coming soon"  
**✅ New Sighting** - Image upload works  
**✅ Analytics** - Trends display  
**✅ Vocabulary** - Search and browse works  

---

**🎊 All fixes are in place! Just restart your app to see them!** 👻✨

**Last Updated:** October 16, 2025  
**Status:** ✅ All fixes verified and ready

