# 🏗️ SnowGhost Breakers System Architecture

## 📊 Complete System Overview

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║                       SNOWGHOST BREAKERS v2.1                                      ║
║                 Complete Ghost Detection & Analysis Platform                       ║
╚══════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────────┐
│                                DATA INGESTION LAYER                                │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Streamlit │  │   Jupyter   │  │    Bulk     │  │   External  │            │
│  │   Forms     │  │  Notebooks  │  │  Processor  │  │     APIs    │            │
│  │   (Manual)  │  │  (Analysis) │  │   (Batch)   │  │  (MCP/REST) │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                │                │                │                      │
│         └────────────────┴────────────────┴────────────────┘                      │
│                              │                                                     │
└──────────────────────────────┼─────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            SNOWFLAKE DATA PLATFORM                                 │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                           STORAGE LAYER                                     │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐     │  │
│  │  │   File Stages    │   │   Image Stages   │   │   Data Stages    │     │  │
│  │  ├──────────────────┤   ├──────────────────┤   ├──────────────────┤     │  │
│  │  │ GHOST_DATA_STAGE │   │ GHOST_IMAGES     │   │ EXTERNAL_STAGE   │     │  │
│  │  │                  │   │ _STAGE           │   │                  │     │  │
│  │  │ - CSV Files      │   │ - Photos         │   │ - API Data       │     │  │
│  │  │ - JSON Files     │   │ - Videos         │   │ - Sensor Logs    │     │  │
│  │  │ - Evidence Logs  │   │ - Thermal Images │   │ - External Feeds │     │  │
│  │  └──────────────────┘   └──────────────────┘   └──────────────────┘     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                            DATABASE LAYER                                   │  │
│  │                         (GHOST_DETECTION.APP)                               │  │
│  │                                                                             │  │
│  │  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐              │  │
│  │  │ Core Tables    │  │ Reference Data │  │  System Tables │              │  │
│  │  ├────────────────┤  ├────────────────┤  ├────────────────┤              │  │
│  │  │ • GHOSTS       │  │ • INVESTIGATORS│  │ • AUDIT_LOG    │              │  │
│  │  │ • GHOST_       │  │ • OFFICES      │  │ • AI_AGENTS    │              │  │
│  │  │   SIGHTINGS    │  │ • VOCABULARY   │  │ • POLICIES     │              │  │
│  │  │ • GHOST_       │  │ • TAXONOMY     │  │ • AGENT_       │              │  │
│  │  │   EVIDENCE     │  │ • ONTOLOGY     │  │   ACTIONS      │              │  │
│  │  │ • GHOST_AI_    │  │                │  │                │              │  │
│  │  │   ANALYSIS     │  │                │  │                │              │  │
│  │  │ • SENSOR_      │  │                │  │                │              │  │
│  │  │   READINGS     │  │                │  │                │              │  │
│  │  │ • INVESTIGATIONS│ │                │  │                │              │  │
│  │  └────────────────┘  └────────────────┘  └────────────────┘              │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                          ANALYTICS LAYER                                    │  │
│  │                     (GHOST_DETECTION.ANALYTICS)                             │  │
│  │                                                                             │  │
│  │  ┌────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ Views & Aggregations                                                │   │  │
│  │  ├────────────────────────────────────────────────────────────────────┤   │  │
│  │  │ • VW_ACTIVITY_TIMELINE      │ • VW_INVESTIGATOR_STATS            │   │  │
│  │  │ • VW_INVESTIGATION_METRICS  │ • VW_THREAT_MATRIX                 │   │  │
│  │  │ • VW_GHOST_PROFILE          │ • VW_EVIDENCE_SUMMARY              │   │  │
│  │  │ • VW_HOTSPOTS               │ • VW_SENSOR_ANALYSIS               │   │  │
│  │  │ • VW_AI_MODEL_PERFORMANCE   │ • VW_PATTERN_DETECTION             │   │  │
│  │  └────────────────────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                         PROCESSING LAYER                                    │  │
│  │                                                                             │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐    │  │
│  │  │ Stored Procedures (18+)                                            │    │  │
│  │  ├───────────────────────────────────────────────────────────────────┤    │  │
│  │  │ • PROCESS_GHOST_EVIDENCE        • GENERATE_INVESTIGATION_SUMMARY │    │  │
│  │  │ • FIND_SIMILAR_SIGHTINGS        • CLASSIFY_THREAT_LEVEL          │    │  │
│  │  │ • ANALYZE_PATTERNS              • BATCH_PROCESS_EVIDENCE         │    │  │
│  │  │ • GENERATE_GHOST_REPORT         • CALCULATE_HOTSPOTS             │    │  │
│  │  │ • SEMANTIC_SEARCH_SIGHTINGS     • ASK_GHOST_DATABASE             │    │  │
│  │  │ • GENERATE_WEEKLY_REPORT        • SEARCH_VOCABULARY              │    │  │
│  │  └───────────────────────────────────────────────────────────────────┘    │  │
│  │                                                                             │  │
│  │  ┌───────────────────────────────────────────────────────────────────┐    │  │
│  │  │ User-Defined Functions                                             │    │  │
│  │  ├───────────────────────────────────────────────────────────────────┤    │  │
│  │  │ • CALCULATE_THREAT_SCORE        • EXTRACT_GHOST_FEATURES         │    │  │
│  │  │ • CLASSIFY_EVIDENCE_TYPE        • VALIDATE_EMF_READING           │    │  │
│  │  │ • GET_TERM_RELATIONSHIPS        • CALCULATE_SIMILARITY           │    │  │
│  │  └───────────────────────────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                          CORTEX AI LAYER                                    │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │  │
│  │  │  Text AI         │  │  Vision AI       │  │  Embeddings      │        │  │
│  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤        │  │
│  │  │ • COMPLETE       │  │ • Vision API     │  │ • AI_EMBED       │        │  │
│  │  │   (mistral-large)│  │ • Image Analysis │  │   (arctic-embed  │        │  │
│  │  │ • SENTIMENT      │  │ • Object         │  │    -l-v2.0-8k)   │        │  │
│  │  │ • TRANSLATE      │  │   Detection      │  │ • 1024-dim       │        │  │
│  │  │ • SUMMARIZE      │  │                  │  │   vectors        │        │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘        │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                               │  │
│  │  │  Semantic Layer  │  │  Cortex Search   │                               │  │
│  │  ├──────────────────┤  ├──────────────────┤                               │  │
│  │  │ • Semantic Model │  │ • Vector Search  │                               │  │
│  │  │   (YAML)         │  │ • Hybrid Search  │                               │  │
│  │  │ • Cortex Analyst │  │ • Similarity     │                               │  │
│  │  │ • Natural Lang   │  │   Search         │                               │  │
│  │  │   Queries        │  │                  │                               │  │
│  │  └──────────────────┘  └──────────────────┘                               │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                         AGENTIC AI SYSTEM                                   │  │
│  │                                                                             │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │  │
│  │  │   Threat     │  │  Assignment  │  │  Prediction  │  │    Summary   │  │  │
│  │  │   Monitor    │  │    Agent     │  │    Agent     │  │     Agent    │  │  │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤  ├──────────────┤  │  │
│  │  │ • Monitor    │  │ • Assign     │  │ • Predict    │  │ • Generate   │  │  │
│  │  │   activity   │  │   cases      │  │   patterns   │  │   reports    │  │  │
│  │  │ • Detect     │  │ • Match      │  │ • Forecast   │  │ • Summarize  │  │  │
│  │  │   threats    │  │   skills     │  │   trends     │  │   findings   │  │  │
│  │  │ • Alert      │  │ • Balance    │  │ • Recommend  │  │ • Distribute │  │  │
│  │  │   teams      │  │   workload   │  │   actions    │  │   insights   │  │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘  │  │
│  │                                                                             │  │
│  │  ┌────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ Policy Engine                                                       │   │  │
│  │  ├────────────────────────────────────────────────────────────────────┤   │  │
│  │  │ • Agent Policies    • Governance Rules    • Audit Trails          │   │  │
│  │  │ • Decision Logs     • Performance Metrics • Learning History       │   │  │
│  │  └────────────────────────────────────────────────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                         GRAPH ANALYTICS (Neo4j)                             │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │  │
│  │  │  Graph Data      │  │  Algorithms      │  │  Pattern Detection│       │  │
│  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤        │  │
│  │  │ • Nodes (Ghosts) │  │ • Louvain        │  │ • Community      │        │  │
│  │  │ • Relationships  │  │ • PageRank       │  │   Detection      │        │  │
│  │  │ • Properties     │  │ • Betweenness    │  │ • Influence      │        │  │
│  │  │ • Projections    │  │ • K-NN           │  │   Analysis       │        │  │
│  │  │                  │  │ • Node2Vec       │  │ • Path Finding   │        │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘        │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           PRESENTATION LAYER                                       │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                      STREAMLIT APPLICATION                                  │  │
│  │                                                                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│  │  │  Dashboard  │  │  Registry   │  │  Sightings  │  │  Evidence   │     │  │
│  │  │    Page     │  │    Page     │  │    Page     │  │    Page     │     │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │  │
│  │                                                                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│  │  │Investigations│ │ Investigators│ │   Offices   │  │ AI Insights │     │  │
│  │  │    Page     │  │    Page     │  │    Page     │  │    Page     │     │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │  │
│  │                                                                             │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│  │  │ New Sighting│  │  Analytics  │  │   Reports   │  │ Vocabulary  │     │  │
│  │  │    Page     │  │    Page     │  │    Page     │  │    Page     │     │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘     │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                      JUPYTER NOTEBOOKS                                      │  │
│  │                                                                             │  │
│  │  • 01_ghost_analytics.ipynb    - Advanced analytics & visualizations       │  │
│  │  • 02_data_loader.ipynb         - Bulk data loading & validation           │  │
│  │  • generate_notebook.py         - Notebook generation tools                │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                         BULK PROCESSOR                                      │  │
│  │                                                                             │  │
│  │  • bulk_ghost_processor.py      - Batch processing script                  │  │
│  │  • ghost_analytics.py           - Analytics automation                     │  │
│  │  • neo4j_graph_visualization.py - Graph visualization                      │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         INTEGRATION LAYER                                          │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                   MODEL CONTEXT PROTOCOL (MCP)                              │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐        │  │
│  │  │   MCP Server     │  │   MCP Tools      │  │  MCP Resources   │        │  │
│  │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤        │  │
│  │  │ • Snowflake      │  │ • Cortex Search  │  │ • Ghost Database │        │  │
│  │  │   Managed        │  │ • Cortex Analyst │  │ • Analytics Views│        │  │
│  │  │ • OAuth 2.0      │  │ • Query Builder  │  │ • Reports        │        │  │
│  │  │ • REST API       │  │ • Data Access    │  │ • Visualizations │        │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘        │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                    │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                         EXTERNAL APIS                                       │  │
│  │                                                                             │  │
│  │  • geopy (Nominatim)           - Geocoding service                         │  │
│  │  • Plotly                      - Interactive visualizations                │  │
│  │  • NetworkX                    - Graph algorithms                          │  │
│  └────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘

```

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│   INPUT     │
│   SOURCES   │
└──────┬──────┘
       │
       ├──────────────────────────────────────────────────────────┐
       │                                                           │
       ▼                                                           ▼
┌─────────────────┐                                        ┌─────────────────┐
│  Manual Entry   │                                        │  Bulk Import    │
│  (Streamlit)    │                                        │  (Scripts)      │
├─────────────────┤                                        ├─────────────────┤
│ • Sighting Form │                                        │ • CSV Files     │
│ • Evidence      │                                        │ • JSON Batch    │
│ • Investigator  │                                        │ • Image Dirs    │
│ • Office        │                                        │ • API Imports   │
└────────┬────────┘                                        └────────┬────────┘
         │                                                          │
         │        ┌──────────────────────────────┐                │
         └────────►    VALIDATION LAYER          ◄────────────────┘
                  ├──────────────────────────────┤
                  │ • Coordinate Validation      │
                  │ • Data Type Checks           │
                  │ • Business Rule Validation   │
                  │ • Duplicate Detection        │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │   SNOWFLAKE STORAGE          │
                  ├──────────────────────────────┤
                  │ • Stages (Files/Images)      │
                  │ • Tables (Structured Data)   │
                  │ • Views (Aggregations)       │
                  └──────────────┬───────────────┘
                                 │
                                 ├───────────────────────────────┐
                                 │                               │
                                 ▼                               ▼
                  ┌──────────────────────────┐   ┌──────────────────────────┐
                  │   AI PROCESSING          │   │  ANALYTICAL PROCESSING   │
                  ├──────────────────────────┤   ├──────────────────────────┤
                  │ • Cortex Vision          │   │ • Stored Procedures      │
                  │ • Cortex Complete        │   │ • UDFs                   │
                  │ • Cortex Embeddings      │   │ • Views                  │
                  │ • Sentiment Analysis     │   │ • Aggregations           │
                  └──────────────┬───────────┘   └──────────────┬───────────┘
                                 │                               │
                                 └───────────────┬───────────────┘
                                                 │
                                                 ▼
                                  ┌──────────────────────────────┐
                                  │   AGENTIC AI LAYER           │
                                  ├──────────────────────────────┤
                                  │ • Threat Monitoring          │
                                  │ • Case Assignment            │
                                  │ • Pattern Prediction         │
                                  │ • Report Generation          │
                                  └──────────────┬───────────────┘
                                                 │
                                                 ├──────────────────────────┐
                                                 │                          │
                                                 ▼                          ▼
                                  ┌──────────────────────┐   ┌──────────────────────┐
                                  │   VISUALIZATION      │   │   API ACCESS         │
                                  ├──────────────────────┤   ├──────────────────────┤
                                  │ • Streamlit App      │   │ • MCP Server         │
                                  │ • Jupyter Notebooks  │   │ • REST API           │
                                  │ • Reports (6 types)  │   │ • External Tools     │
                                  │ • Interactive Maps   │   │ • AI Agents          │
                                  └──────────────────────┘   └──────────────────────┘
```

---

## 🔄 Component Interaction Matrix

| Component | Reads From | Writes To | APIs Used | Output |
|-----------|------------|-----------|-----------|--------|
| **Streamlit App** | All Tables, Views | GHOSTS, SIGHTINGS, EVIDENCE, INVESTIGATORS, OFFICES | Snowpark, Plotly, geopy | Interactive UI |
| **Bulk Processor** | Stages, External Files | All Tables | Snowpark, Pandas | Batch Results |
| **Notebooks** | All Tables, Views | Analysis Results | Snowpark, Matplotlib, Plotly | Analytics, Reports |
| **Stored Procedures** | All Tables | AUDIT_LOG, Results Tables | Cortex AI | Processed Data |
| **Agentic AI** | All Tables, POLICIES | AGENT_ACTIONS, AUDIT_LOG | Cortex Complete | Decisions, Actions |
| **MCP Server** | All Tables, Views | None (Read-Only) | Cortex Search, Analyst | External Access |
| **Graph Analytics** | GHOSTS, SIGHTINGS | Graph Projections | Neo4j | Network Insights |
| **Cortex AI** | EVIDENCE, TEXT Data | AI_ANALYSIS | Vision, Complete, Embeddings | AI Results |

---

## 📂 File Structure

```
SnowGhostBreakers/
│
├── sql/                                    # SQL Scripts
│   ├── 01_setup_database.sql              # Database & schemas
│   ├── 02_create_tables.sql               # Core tables (13)
│   ├── 03_sample_data.sql                 # Sample data
│   ├── 04_stored_procedures.sql           # Stored procedures (18+)
│   ├── 05_semantic_views.sql              # Analytics views (11)
│   ├── 06_cortex_ai_functions.sql         # Cortex AI examples
│   ├── 07_aisql_examples.sql              # Advanced AI SQL
│   ├── 08_business_vocabulary.sql         # Vocabulary & taxonomy
│   ├── 09_agentic_ai_system.sql           # AI agents
│   ├── 10_snowflake_native_mcp_server.sql # MCP setup
│   ├── 11_neo4j_graph_analytics_setup.sql # Graph setup
│   ├── 12_neo4j_graph_algorithms.sql      # Graph algorithms
│   └── 13_offices_table.sql               # Global offices (27)
│
├── streamlit_app/                          # Streamlit Application
│   └── ghost_detection_app.py             # Main app (12 pages)
│
├── notebooks/                              # Jupyter Notebooks
│   ├── 01_ghost_analytics.ipynb           # Advanced analytics
│   ├── 02_data_loader.ipynb               # Bulk data loading
│   ├── generate_notebook.py               # Notebook generator
│   └── COMPLETE_ANALYTICS_GUIDE.md        # 26-section guide
│
├── scripts/                                # Python Scripts
│   ├── bulk_ghost_processor.py            # Batch processing
│   ├── ghost_analytics.py                 # Analytics automation
│   ├── neo4j_graph_visualization.py       # Graph viz
│   ├── install_all.py                     # Automated installer
│   └── upgrade_embeddings.py              # Embedding upgrade
│
├── cortex_analyst/                         # Cortex Analyst
│   └── ghost_semantic_model.yaml          # Semantic model
│
├── mcp/                                    # MCP Configuration
│   ├── snowflake_mcp_config.json          # MCP config
│   ├── mcp_server.py                      # MCP server
│   └── snowflake_native_mcp_client_config.json
│
├── tests/                                  # Test Suite
│   ├── sql/                               # SQL tests
│   └── python/                            # Python tests
│
└── Documentation (40+ files)               # Complete documentation
```

---

## 🔑 Key Technologies

### **Snowflake Core:**
- Snowpark Python
- Cortex AI (Complete, Sentiment, Vision, AI_EMBED)
- Cortex Search & Analyst
- Stages for file storage
- Tasks for automation

### **AI & ML:**
- mistral-large2 (text generation)
- snowflake-arctic-embed-l-v2.0-8k (1024-dim embeddings)
- llama3.1-70b (analysis)
- Custom UDFs for classification

### **Visualization:**
- Streamlit (12-page app)
- Plotly (interactive charts)
- Matplotlib (static charts)
- Pandas (data manipulation)

### **Graph Analytics:**
- Neo4j (marketplace add-on)
- NetworkX (Python graphs)
- 10+ graph algorithms

### **Integration:**
- Model Context Protocol (MCP)
- REST APIs
- geopy (geocoding)
- OAuth 2.0

---

## 📊 Data Flow by Use Case

### **Use Case 1: Report New Sighting**
```
User Input (Streamlit)
    → Geocoding (geopy) → Coordinates
    → Upload Images → GHOST_IMAGES_STAGE
    → AI Analysis (Cortex Vision) → Description
    → Generate Embeddings (AI_EMBED) → Vector
    → INSERT GHOST_SIGHTINGS
    → INSERT GHOST_EVIDENCE
    → INSERT GHOST_AI_ANALYSIS
    → Trigger Agent Monitoring
    → Display Confirmation
```

### **Use Case 2: Bulk Data Import**
```
CSV/JSON Files
    → Validation Layer → Check formats
    → bulk_ghost_processor.py → Parse & Transform
    → Snowpark DataFrame → Type conversion
    → Batch INSERT → Multiple tables
    → Progress Tracking → Logs
    → Error Handling → Retry logic
    → Generate Report → Success/Failure stats
```

### **Use Case 3: Threat Analysis**
```
New Sighting Event
    → Trigger Agent_Monitor_Threats
    → Query Recent Activity → Aggregations
    → AI Analysis (Cortex Complete) → Threat Assessment
    → UPDATE Threat Levels
    → Assign Investigator (Agent_Assign)
    → Generate Alert
    → Log to AGENT_ACTIONS
    → Notify Team (via Streamlit/API)
```

### **Use Case 4: Generate Report**
```
User Selects Report Type (Streamlit)
    → Query Relevant Views
    → Aggregate Data → Statistics
    → Generate Charts (Plotly) → Visualizations
    → Create Maps (Mapbox) → Geographic
    → AI Summary (Cortex Complete) → Insights
    → Format Report → Professional layout
    → Display/Export → PDF/Excel (future)
```

---

## 🌟 System Capabilities

| Category | Capabilities |
|----------|--------------|
| **Data Input** | Streamlit forms, CSV import, JSON batch, API integration, Image upload |
| **Storage** | 13 core tables, 27 global offices, Unlimited file stages |
| **Processing** | 18+ stored procedures, 10+ UDFs, 5 AI agents, Real-time analysis |
| **AI Features** | Vision analysis, Text generation, Sentiment analysis, 1024-dim embeddings, Semantic search |
| **Analytics** | 11 views, 6 comprehensive reports, 25+ charts, Interactive maps |
| **Graph** | 10+ algorithms, Community detection, Influence analysis, Path finding |
| **Integration** | MCP server, REST API, OAuth 2.0, External AI agents |
| **Automation** | Scheduled tasks, Agent policies, Batch processing, Auto-reporting |

---

## 📈 Performance Characteristics

| Metric | Value | Notes |
|--------|-------|-------|
| **Data Load Speed** | ~100 records/sec | Bulk processor |
| **Query Response** | < 1 second | Most views |
| **AI Analysis** | ~2-5 seconds | Per image/text |
| **Embedding Generation** | ~0.5 seconds | Per record |
| **Report Generation** | 5-10 seconds | Full report |
| **Map Rendering** | 2-3 seconds | 100+ points |
| **Agent Response** | 3-7 seconds | Per decision |
| **Concurrent Users** | 100+ | Streamlit |

---

## 🔒 Security & Governance

```
┌──────────────────────────────────────┐
│        SECURITY LAYERS               │
├──────────────────────────────────────┤
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Authentication & Authorization│ │
│  ├────────────────────────────────┤ │
│  │ • OAuth 2.0 (MCP)              │ │
│  │ • Role-Based Access Control    │ │
│  │ • User Management              │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Data Governance               │ │
│  ├────────────────────────────────┤ │
│  │ • Business Vocabulary          │ │
│  │ • Ghost Taxonomy & Ontology    │ │
│  │ • Data Quality Rules           │ │
│  │ • Audit Logging (all actions)  │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  AI Governance                 │ │
│  ├────────────────────────────────┤ │
│  │ • Agent Policies               │ │
│  │ • Decision Logging             │ │
│  │ • Performance Monitoring       │ │
│  │ • Explainability Tracking      │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │  Data Protection               │ │
│  ├────────────────────────────────┤ │
│  │ • No secrets in code           │ │
│  │ • Environment variables        │ │
│  │ • Secure stages                │ │
│  │ • Encrypted connections        │ │
│  └────────────────────────────────┘ │
└──────────────────────────────────────┘
```

---

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DEPLOYMENT LAYERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Production Environment                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ Streamlit  │  │ Snowflake  │  │   Neo4j    │          │
│  │   Cloud    │  │  Account   │  │ Marketplace│          │
│  └────────────┘  └────────────┘  └────────────┘          │
│        │               │                │                  │
│        └───────────────┴────────────────┘                  │
│                       │                                     │
│  Development Environment                                    │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   Local    │  │ Snowflake  │  │  Jupyter   │          │
│  │ Streamlit  │  │  Sandbox   │  │ Notebooks  │          │
│  └────────────┘  └────────────┘  └────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Related Documentation

- `README.md` - Project overview
- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT_GUIDE.md` - Deployment instructions
- `PROJECT_OVERVIEW.md` - Architecture details
- `FEATURES_SUMMARY.md` - Complete features list
- `COMPREHENSIVE_REPORTS_GUIDE.md` - Reports documentation
- `AGENTIC_AI_GUIDE.md` - AI agents guide
- `MCP_GUIDE.md` - MCP integration
- `NEO4J_GUIDE.md` - Graph analytics

---

**Last Updated:** October 17, 2025  
**Version:** 2.1  
**Status:** ✅ Production Ready

