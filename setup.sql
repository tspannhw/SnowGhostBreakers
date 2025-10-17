-- ============================================
-- MASTER SETUP GUIDE
-- Ghost Detection Application for Snowflake v2.0
-- ============================================
-- This file provides instructions for setting up the complete application
-- including Agentic AI, MCP, and Business Vocabulary

-- ============================================
-- OPTION 1: SNOWFLAKE WORKSHEET (Recommended)
-- ============================================
-- Copy and paste each file's contents into a worksheet and run in this order:
--
-- 1. sql/01_setup_database.sql              (Database & schemas)
-- 2. sql/02_create_tables.sql               (Core tables)
-- 3. sql/03_sample_data.sql                 (Sample data)
-- 4. sql/04_stored_procedures.sql           (Procedures)
-- 5. sql/05_semantic_views.sql              (Analytics views)
-- 6. sql/06_cortex_ai_functions.sql         (Cortex AI)
-- 7. sql/07_aisql_examples.sql              (AISQL examples - optional)
-- 8. sql/08_business_vocabulary.sql         (Business vocabulary)
-- 9. sql/09_agentic_ai_system.sql           (Agentic AI)
-- 10. sql/10_snowflake_native_mcp_server.sql  (Snowflake MCP)
-- 11. sql/11_neo4j_graph_analytics_setup.sql  (Neo4j Graph - optional)
-- 12. sql/12_neo4j_graph_algorithms.sql       (Graph algorithms - optional)
-- 13. sql/13_offices_table.sql                (Global Offices - recommended)
-- 14. sql/14_image_embeddings_table.sql       (Image Embeddings & Similarity Search - recommended)

-- ============================================
-- OPTION 2: SNOWSQL CLI
-- ============================================
-- If using SnowSQL command-line tool, run:
-- snowsql -f setup_snowsql.sql

-- ============================================
-- OPTION 3: PYTHON SCRIPT
-- ============================================
-- Use the automated Python installer (recommended for quick setup):
-- python scripts/install_all.py

-- ============================================
-- QUICK START FOR WORKSHEET USERS
-- ============================================
-- Open each SQL file in order and run them in separate worksheet tabs.
-- This is the most reliable method for Snowflake UI users.

-- Verify setup
SELECT 'Database setup complete!' as status;
SELECT 'Version 2.0 - with Agentic AI, MCP, and Business Vocabulary' as version;

-- Show created objects
SHOW TABLES IN GHOST_DETECTION.APP;
SHOW VIEWS IN GHOST_DETECTION.ANALYTICS;
SHOW PROCEDURES IN GHOST_DETECTION.APP;
SHOW TASKS IN GHOST_DETECTION.APP;

-- Quick verification queries
SELECT COUNT(*) as total_ghosts FROM GHOST_DETECTION.APP.GHOSTS;
SELECT COUNT(*) as total_sightings FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;
SELECT COUNT(*) as global_offices FROM GHOST_DETECTION.APP.OFFICES;
SELECT COUNT(*) as vocabulary_terms FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY;
SELECT COUNT(*) as ontology_classes FROM GHOST_DETECTION.APP.GHOST_ONTOLOGY;
SELECT COUNT(*) as ai_agents FROM GHOST_DETECTION.APP.AI_AGENTS;

-- Display summary
SELECT 
    '========================================' as separator,
    'SnowGhost Breakers v2.0 Installed!' as status,
    '========================================' as separator2
UNION ALL
SELECT 
    'Core Tables: 13',
    'Analytics Views: 11',
    'Stored Procedures: 18'
UNION ALL
SELECT
    'AI Agents: 5',
    'MCP Resources: 8',
    'Documentation: 7 guides'
UNION ALL
SELECT
    '',
    'Next Steps:',
    ''
UNION ALL
SELECT
    '1. Deploy Streamlit app',
    '2. Review AGENTIC_AI_GUIDE.md',
    '3. Configure MCP (see MCP_GUIDE.md)'
UNION ALL
SELECT
    '4. Enable agent tasks (optional)',
    '5. Test with sample queries',
    '6. Start catching ghosts! 👻🚫'
UNION ALL
SELECT
    '',
    'Documentation: /QUICKSTART.md',
    '';

-- Test Cortex AI
SELECT 'Testing Cortex AI...' as test;
SELECT SNOWFLAKE.CORTEX.COMPLETE(
    'mistral-large2',
    'Say "Cortex AI is working!" if you can read this.'
) as cortex_test;

SELECT '✅ Setup Complete!' as final_status;

