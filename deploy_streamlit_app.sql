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

-- Create or replace the Streamlit app with required packages
CREATE OR REPLACE STREAMLIT GHOST_DETECTION_APP
    ROOT_LOCATION = '@GHOST_DETECTION.APP.STREAMLIT_STAGE'
    MAIN_FILE = 'ghost_detection_app.py'
    QUERY_WAREHOUSE = 'COMPUTE_WH'
    TITLE = '👻 Ghost Detection System'
    COMMENT = 'Interactive ghost detection and analysis application'
    PACKAGES = (
        'snowflake-snowpark-python',
        'pandas',
        'plotly',
        'numpy'
    );

-- Grant access to the app
GRANT USAGE ON STREAMLIT GHOST_DETECTION_APP TO ROLE ACCOUNTADMIN;
GRANT USAGE ON STREAMLIT GHOST_DETECTION_APP TO ROLE SYSADMIN;

-- ============================================
-- DEPLOYMENT INSTRUCTIONS
-- ============================================

/*
To deploy the Streamlit app:

1. From SnowSQL or terminal:
   PUT file:///Users/tspann/Downloads/code/cursorai/SnowGhostBreakers/streamlit_app/ghost_detection_app.py @GHOST_DETECTION.APP.STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

2. Run this SQL script to create the app

3. Access the app through Snowsight:
   - Navigate to: Streamlit > GHOST_DETECTION_APP
   - Or use: https://<your-account>.snowflakecomputing.com/streamlit/GHOST_DETECTION_APP

ALTERNATIVE - Deploy via Snowsight UI:
1. Go to Streamlit > + Streamlit App
2. Name: GHOST_DETECTION_APP
3. Warehouse: COMPUTE_WH
4. App location: Create new stage or use existing
5. Packages: Add plotly, pandas, numpy
6. Copy/paste the ghost_detection_app.py code

TROUBLESHOOTING:
- If plotly is not found, ensure it's in the PACKAGES list
- Check warehouse is running: SHOW WAREHOUSES;
- Verify stage exists: LIST @STREAMLIT_STAGE;
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


