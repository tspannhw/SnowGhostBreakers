# 🚨 URGENT FIX: Streamlit Package Conflicts

## The Problem

Your Streamlit app is failing with:
```
Cannot create a Python function with the specified packages.
'One or more package conflicts were detected.'
```

**Root Cause:** You're specifying packages that Snowflake already includes automatically.

---

## ✅ The Solution (Quick Fix)

Run this ONE command:

```sql
ALTER STREAMLIT GHOST_DETECTION_APP 
    SET PACKAGES = ('plotly', 'nbformat');
```

**That's it!** Then restart your Streamlit app.

---

## 📋 Understanding the Fix

### ❌ WRONG Configuration (Causes Conflicts)
```sql
PACKAGES = (
    'snowflake-snowpark-python',  -- ❌ Already auto-included
    'pandas',                      -- ❌ Already auto-included
    'plotly',                      -- ✅ Need this
    'nbformat',                    -- ✅ Need this
    'numpy'                        -- ❌ Already auto-included
);
```

### ✅ CORRECT Configuration
```sql
PACKAGES = ('plotly', 'nbformat');
```

---

## 🎯 Package Rules for Snowflake Streamlit

| Package | Status | Action |
|---------|--------|--------|
| `pandas` | ✅ Auto-included | **DON'T ADD** |
| `numpy` | ✅ Auto-included | **DON'T ADD** |
| `snowflake-snowpark-python` | ✅ Auto-included | **DON'T ADD** |
| `streamlit` | ✅ Auto-included | **DON'T ADD** |
| `plotly` | ❌ NOT auto-included | **ADD THIS** |
| `nbformat` | ❌ NOT auto-included | **ADD THIS** |

---

## 🔧 Three Ways to Fix

### Option 1: SQL Command (Fastest)
```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

ALTER STREAMLIT GHOST_DETECTION_APP 
    SET PACKAGES = ('plotly', 'nbformat');
```

### Option 2: Via Snowsight UI
1. Open your Streamlit app in Snowsight
2. Click **Settings** or **Edit**
3. Go to **Packages** section
4. **REMOVE:** pandas, numpy, snowflake-snowpark-python
5. **KEEP:** plotly, nbformat
6. Save and restart

### Option 3: Recreate the App
```sql
CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP
    ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
    MAIN_FILE = 'ghost_detection_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    PACKAGES = ('plotly', 'nbformat');
```

---

## ⚠️ Critical Rules

### ✅ DO:
- Only specify packages **NOT** auto-included
- Use simple package names: `plotly`
- Keep the list minimal

### ❌ DON'T:
- Specify version numbers: ~~`plotly==6.3.0`~~
- Add auto-included packages: ~~`pandas`, `numpy`~~
- Add multiple versions of the same package

---

## 🧪 Verify the Fix

After applying the fix, verify it worked:

```sql
DESCRIBE STREAMLIT GHOST_DETECTION_APP;
```

Look for the `PACKAGES` row - it should show only: `plotly, nbformat`

---

## 🎬 Complete Fix Steps

1. **Run the fix:**
   ```sql
   ALTER STREAMLIT GHOST_DETECTION_APP 
       SET PACKAGES = ('plotly', 'nbformat');
   ```

2. **Refresh your browser**
   - Navigate to your Streamlit app URL
   - Or click the app name in Snowsight

3. **Verify it loads**
   - The app should start without errors
   - Plotly charts will render correctly

---

## 💡 Why This Happens

Snowflake Streamlit uses a managed Python environment that **pre-installs** common packages:
- pandas
- numpy
- snowflake-snowpark-python
- streamlit

When you explicitly specify these packages in your `PACKAGES` list:
1. Snowflake tries to install them again
2. This creates version conflicts
3. The app fails to start

**Solution:** Only specify packages that are **NOT** pre-installed.

---

## 📊 Common Scenarios

### "But I need pandas!"
**Answer:** It's already there! Don't add it to PACKAGES.

### "What if I need a specific version?"
**Answer:** Use the pre-installed versions. If you need a different version, contact Snowflake support.

### "Can I add other packages?"
**Answer:** Yes, but only if they're NOT auto-included. Examples:
- `matplotlib` ✅
- `scikit-learn` ✅
- `requests` ✅
- `pandas` ❌ (already included)

---

## 🆘 Still Having Issues?

1. **Check warehouse is running:**
   ```sql
   SHOW WAREHOUSES LIKE 'COMPUTE_WH';
   ```

2. **Verify app exists:**
   ```sql
   SHOW STREAMLIT APPS LIKE 'GHOST_DETECTION_APP';
   ```

3. **Check for typos:**
   - Package names are case-sensitive
   - Use quotes: `('plotly', 'nbformat')`

4. **Restart completely:**
   ```sql
   -- Drop and recreate
   DROP STREAMLIT GHOST_DETECTION_APP;
   -- Then run the CREATE statement with correct packages
   ```

---

## 📝 Summary

**Quick Fix:**
```sql
ALTER STREAMLIT GHOST_DETECTION_APP SET PACKAGES = ('plotly', 'nbformat');
```

**Remember:** 
- pandas ✅ auto-included
- numpy ✅ auto-included  
- snowpark ✅ auto-included
- plotly ❌ must specify
- nbformat ❌ must specify

---

**Files Updated:**
- `STREAMLIT_FIX_FINAL.sql` - Run this to fix immediately
- `deploy_streamlit_app.sql` - Updated with correct config
- `STREAMLIT_PACKAGES_GUIDE.md` - This guide

**Status:** Ready to deploy! 🚀

