-- ============================================
-- FINAL FIX: Streamlit Package Conflicts
-- ============================================
-- This is the CORRECT configuration for the Ghost Detection Streamlit app
-- Run this to fix package conflicts immediately

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- CORRECT PACKAGES - Only specify what's NOT auto-included
-- ============================================

ALTER STREAMLIT GHOST_DETECTION_APP 
    SET PACKAGES = ('plotly', 'nbformat');

-- That's it! Just those two packages.

-- ============================================
-- WHY THIS WORKS
-- ============================================
/*
Snowflake Streamlit AUTOMATICALLY includes:
✅ snowflake-snowpark-python
✅ pandas  
✅ numpy
✅ streamlit

You ONLY need to add:
📦 plotly - for visualizations (NOT auto-included)
📦 nbformat - for notebook rendering (NOT auto-included)

CRITICAL RULES:
❌ DON'T specify: pandas, numpy, snowflake-snowpark-python
❌ DON'T use version numbers: plotly==6.3.0
✅ DO use simple names: plotly, nbformat

When you specify auto-included packages explicitly, it creates conflicts
with the versions Snowflake has already loaded.
*/

-- ============================================
-- VERIFY THE FIX
-- ============================================

DESCRIBE STREAMLIT GHOST_DETECTION_APP;

-- You should see only: plotly, nbformat in the packages
-- Pandas, numpy, snowpark are auto-included and won't show in PACKAGES

-- ============================================
-- TEST
-- ============================================

-- Restart your Streamlit app and it should work!
-- Access at: https://<your-account>.snowflakecomputing.com/streamlit/GHOST_DETECTION_APP

SELECT 'Fix applied! Restart your Streamlit app.' as status;

