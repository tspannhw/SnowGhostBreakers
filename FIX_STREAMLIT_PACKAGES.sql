-- ============================================
-- QUICK FIX: Streamlit Package Conflicts
-- ============================================
-- Run this if you're getting:
-- "Cannot create a Python function with the specified packages"
-- "One or more package conflicts were detected"

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Fix: Remove conflicting packages, keep only plotly
ALTER STREAMLIT GHOST_DETECTION_APP 
    SET PACKAGES = ('plotly');

-- Verify the fix
DESCRIBE STREAMLIT GHOST_DETECTION_APP;

-- ============================================
-- Why This Works
-- ============================================
/*
Snowflake Streamlit automatically includes:
- pandas
- numpy  
- snowflake-snowpark-python
- streamlit

When you specify these packages explicitly (especially with versions),
it creates conflicts with the auto-included versions.

Solution: Only specify packages that are NOT auto-included.
For this app, that's just 'plotly' for visualizations.

DO NOT specify versions like 'plotly==6.3.0' - just use 'plotly'
*/

-- ============================================
-- Test the App
-- ============================================
-- After running this fix:
-- 1. Refresh your Streamlit app in Snowsight
-- 2. The app should now load without package errors
-- 3. plotly visualizations will work

