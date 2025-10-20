-- ============================================
-- MASTER SETUP SCRIPT FOR SNOWSQL CLI
-- Ghost Detection Application for Snowflake v2.0
-- ============================================
-- Run this script with SnowSQL command-line tool:
-- snowsql -f setup_snowsql.sql

-- This script executes all setup scripts in order
-- Make sure you have the necessary privileges

-- Note: !source command only works with SnowSQL CLI, not in Snowflake worksheets

!source sql/01_setup_database.sql
!source sql/02_create_tables.sql
!source sql/03_sample_data.sql
!source sql/04_stored_procedures.sql
!source sql/05_semantic_views.sql
!source sql/06_cortex_ai_functions.sql
!source sql/07_aisql_examples.sql
!source sql/08_business_vocabulary.sql
!source sql/09_agentic_ai_system.sql
!source sql/10_snowflake_native_mcp_server.sql
