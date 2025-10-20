-- ============================================
-- DEPLOY GHOST DETECTION STREAMLIT APP
-- ============================================
-- Deploy the Ghost Detection Streamlit application to Snowflake
-- with required packages

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Create stage for Streamlit files (if not exists)
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE
    DIRECTORY = (ENABLE = TRUE)
    COMMENT = 'Stage for Ghost Detection Streamlit app files';

-- Upload the streamlit app file to the stage
-- (Run this from SnowSQL or Snowsight)
-- PUT file://streamlit_app/ghost_detection_app.py @STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- ⚠️ WARNING: CREATE STREAMLIT with PACKAGES parameter causes conflicts!
-- DO NOT USE THIS - Deploy via Snowsight UI instead (see instructions below)
--
-- CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP
--     ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
--     MAIN_FILE = 'ghost_detection_app.py'
--     QUERY_WAREHOUSE = 'COMPUTE_WH'
--     TITLE = '👻 Ghost Detection System'
--     COMMENT = 'Interactive ghost detection and analysis application'
--     PACKAGES = ('plotly', 'nbformat', 'geopy');  -- ❌ This causes package conflicts!
--
-- Instead, create the app WITHOUT PACKAGES in SQL:
CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP
    ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
    MAIN_FILE = 'ghost_detection_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    TITLE = '👻 Ghost Detection System'
    COMMENT = 'Interactive ghost detection and analysis application';
-- Then add packages via Snowsight UI (instructions below)

-- Grant access to the app
GRANT USAGE ON STREAMLIT GHOST_DETECTION_APP TO ROLE ACCOUNTADMIN;
GRANT USAGE ON STREAMLIT GHOST_DETECTION_APP TO ROLE SYSADMIN;

-- ============================================
-- DEPLOYMENT INSTRUCTIONS
-- ============================================

/*
🚀 RECOMMENDED: Deploy via Snowsight UI (avoids package conflicts)

METHOD 1: Snowsight UI (RECOMMENDED) ✅
========================================
1. Go to Snowsight → Streamlit → + Streamlit App
2. Name: GHOST_DETECTION_APP
3. Warehouse: COMPUTE_WH
4. Database: GHOST_DETECTION
5. Schema: APP
6. **PACKAGES (in UI):**
   - plotly
   - nbformat
   - geopy
   ⚠️ DO NOT add: pandas, numpy, snowflake-snowpark-python (auto-included)
7. Copy/paste code from ghost_detection_app.py
8. Click "Run"

METHOD 2: SQL + Manual Package Setup ⚠️
========================================
1. Run the SQL above to create the app structure
2. Upload file via SnowSQL:
   PUT file:///path/to/ghost_detection_app.py @GHOST_DETECTION.APP.STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
3. Go to Snowsight → Streamlit → GHOST_DETECTION_APP → Edit
4. Add packages in UI: plotly, nbformat, geopy
5. Click "Run"

ACCESS:
- Snowsight: Projects → Streamlit → GHOST_DETECTION_APP
- URL: https://<account>.snowflakecomputing.com/streamlit/GHOST_DETECTION_APP

TROUBLESHOOTING:
- Package conflicts? Remove pandas/numpy/snowpark from packages list
- Use ONLY: plotly, nbformat, geopy
- Geocoding not working? Check geopy is in packages list
*/

-- ============================================
-- VERIFY DEPLOYMENT
-- ============================================

-- Check if app exists
SHOW STREAMLIT APPS LIKE 'GHOST_DETECTION_APP';

-- Describe the app
DESCRIBE STREAMLIT GHOST_DETECTION_APP;

-- List files in stage
LIST @STREAMLIT_STAGE;

-- Open https://SFSENORTHAMERICA-TSPANN_AWS1.snowflakecomputing.com/streamlit/GHOST_DETECTION_APP 
