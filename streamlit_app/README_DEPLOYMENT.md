# 👻 Ghost Detection Streamlit App - Deployment Guide

## Quick Fix for Package Errors

### Error: "No module named 'plotly'"
You need to add plotly to your Streamlit app's packages.

### Error: "Package conflicts were detected" or "Cannot create a Python function"
**Solution:** Don't specify package versions - Snowflake Streamlit includes most packages by default. Only add `plotly` without version numbers.

---

## Option 1: Deploy via Snowsight UI (Easiest)

1. **Open Snowsight** and navigate to **Streamlit Apps**
2. Click **+ Streamlit App**
3. Configure:
   - **Name:** `GHOST_DETECTION_APP`
   - **Warehouse:** `COMPUTE_WH`
   - **Database:** `GHOST_DETECTION`
   - **Schema:** `APP`
4. **Add Packages** (Click "Packages" section):
   ```
   plotly
   ```
   _(Note: pandas, numpy, and snowflake-snowpark-python are auto-included)_
5. **Copy the code** from `ghost_detection_app.py` into the editor
6. Click **Run** or **Deploy**

---

## Option 2: Deploy via SQL (CREATE STREAMLIT)

### Step 1: Upload the file
```sql
-- From SnowSQL or Snowsight SQL worksheet
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Create stage
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE;

-- Upload file (from SnowSQL terminal)
PUT file://streamlit_app/ghost_detection_app.py 
    @STREAMLIT_STAGE 
    AUTO_COMPRESS=FALSE 
    OVERWRITE=TRUE;
```

### Step 2: Create the Streamlit app
```sql
CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP
    ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
    MAIN_FILE = 'ghost_detection_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    TITLE = '👻 Ghost Detection System'
    PACKAGES = ('plotly');
    
-- Note: pandas, numpy, and snowflake-snowpark-python are auto-included
-- Only specify additional packages you need
```

---

## Option 3: Update Existing App Packages

If you already deployed the app and need to add packages:

### Via Snowsight UI:
1. Open the Streamlit app in Snowsight
2. Click **⚙️ Settings** or **Edit**
3. Go to **Packages** section
4. Add: `plotly` (only - other packages are auto-included)
5. Save and restart the app

### Via SQL:
```sql
ALTER STREAMLIT GHOST_DETECTION_APP 
    SET PACKAGES = ('plotly');
    
-- Don't add pandas, numpy, or snowflake-snowpark-python
-- They're automatically included and specifying them can cause conflicts
```

---

## Required Packages

The app requires these packages to run:

| Package | Purpose | Installation |
|---------|---------|--------------|
| `plotly` | Interactive visualizations | **Add this in PACKAGES** |
| `pandas` | Data manipulation | Auto-included ✅ |
| `numpy` | Numerical operations | Auto-included ✅ |
| `snowflake-snowpark-python` | Snowflake connectivity | Auto-included ✅ |
| `streamlit` | Web framework | Auto-included ✅ |

**Important:** Only specify `plotly` in the PACKAGES parameter. Do NOT specify versions (like `plotly==6.3.0`) as this causes conflicts.

---

## Troubleshooting

### Error: "Package conflicts were detected"
**Full Error:** `Cannot create a Python function with the specified packages. One or more package conflicts were detected.`

**Solution:** Remove all packages except `plotly` from your PACKAGES list:
```sql
ALTER STREAMLIT GHOST_DETECTION_APP SET PACKAGES = ('plotly');
```

**Why this happens:**
- Snowflake Streamlit auto-includes pandas, numpy, and snowflake-snowpark-python
- Specifying them explicitly (especially with versions) causes conflicts
- Only add packages that aren't already included

### Error: "No module named 'plotly'"
**Solution:** Add `plotly` to the PACKAGES list (see options above)

### Error: "Invalid warehouse"
**Solution:** Make sure `COMPUTE_WH` warehouse exists and is running:
```sql
SHOW WAREHOUSES LIKE 'COMPUTE_WH';
ALTER WAREHOUSE COMPUTE_WH RESUME IF SUSPENDED;
```

### Error: "Object does not exist"
**Solution:** Ensure database and schema exist:
```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;
```

### App won't load or shows errors
**Solution:** Check app status:
```sql
SHOW STREAMLIT APPS LIKE 'GHOST_DETECTION_APP';
DESCRIBE STREAMLIT GHOST_DETECTION_APP;
```

### Need to update the app code
**Solution:** Re-upload the file and recreate:
```sql
-- Upload new version
PUT file://streamlit_app/ghost_detection_app.py @STREAMLIT_STAGE OVERWRITE=TRUE;

-- Recreate app (use CREATE OR REPLACE)
CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP ...
```

---

## Verification

After deployment, verify the app:

```sql
-- Check app exists
SHOW STREAMLIT APPS;

-- View app details
DESCRIBE STREAMLIT GHOST_DETECTION_APP;

-- Check packages
SELECT SYSTEM$GET_STREAMLIT_CONFIG('GHOST_DETECTION_APP');
```

---

## Access the App

Once deployed, access at:
- **Snowsight:** Navigate to Streamlit → GHOST_DETECTION_APP
- **URL:** `https://<your-account>.snowflakecomputing.com/streamlit/GHOST_DETECTION_APP`

---

## Files

- `ghost_detection_app.py` - Main application code
- `packages.txt` - Required packages list
- `deploy_streamlit_app.sql` - Deployment SQL script
- `README_DEPLOYMENT.md` - This file

---

## Support

For more information:
- [Snowflake Streamlit Documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Plotly Documentation](https://plotly.com/python/)


