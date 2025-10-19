# 📊 Ghost Detection System - Standard Tables Guide

## ✅ Why Standard Tables?

The Ghost Detection System uses **standard Snowflake tables** (not hybrid tables) because:

- ✅ **Optimized for Analytics** - Perfect for aggregations, reports, and trends
- ✅ **Auto-Optimization** - Snowflake micro-partitions handle everything
- ✅ **Lower Cost** - More efficient for large analytical queries
- ✅ **No Index Management** - Zero maintenance required
- ✅ **Best for AI/ML** - Cortex AI works great with standard tables

---

## 🎯 What Are Standard Tables?

Standard Snowflake tables are **columnar analytical tables** optimized for:

### Core Features
- ✅ **Automatic micro-partitioning** for optimal performance
- ✅ **Metadata-based pruning** eliminates unnecessary scans
- ✅ **Time Travel** for data recovery and auditing
- ✅ **Zero-copy cloning** for instant copies
- ✅ **Automatic compression** reduces storage costs
- ✅ **Columnar storage** perfect for analytics

### Performance Optimization
Snowflake automatically:
- Creates micro-partitions (50-500 MB each)
- Maintains metadata for fast pruning
- Optimizes query plans
- Caches frequently accessed data
- Parallelizes queries across nodes

**No indexes needed!** Snowflake is already optimized.

---

## 📋 Tables in Ghost Detection System

### Core Tables (13 Total)

#### 1. **GHOSTS** - Master Registry
```sql
CREATE TABLE GHOSTS (
    ghost_id VARCHAR(50) PRIMARY KEY,
    ghost_name VARCHAR(200),
    ghost_type VARCHAR(100),
    threat_level VARCHAR(20),
    -- ... 9 more columns
);
```
**Purpose:** Main ghost entity registry  
**Key Queries:** Search by type, threat level, status

#### 2. **GHOST_SIGHTINGS** - Event Tracking
```sql
CREATE TABLE GHOST_SIGHTINGS (
    sighting_id VARCHAR(50) PRIMARY KEY,
    ghost_id VARCHAR(50),
    location_name VARCHAR(200),
    sighting_datetime TIMESTAMP_NTZ,
    -- ... 14 more columns
);
```
**Purpose:** Individual sighting events  
**Key Queries:** Timeline analysis, location hotspots

#### 3. **GHOST_EVIDENCE** - Multimedia Storage
```sql
CREATE TABLE GHOST_EVIDENCE (
    evidence_id VARCHAR(50) PRIMARY KEY,
    evidence_type VARCHAR(50),
    file_path VARCHAR(500),
    image_data VARCHAR,
    -- ... 10 more columns
);
```
**Purpose:** Images, audio, video, sensor data  
**Key Queries:** Evidence by type, processing status

#### 4. **GHOST_AI_ANALYSIS** - AI Results
```sql
CREATE TABLE GHOST_AI_ANALYSIS (
    analysis_id VARCHAR(50) PRIMARY KEY,
    analysis_type VARCHAR(100),
    model_used VARCHAR(100),
    results VARIANT,
    -- ... 10 more columns
);
```
**Purpose:** Cortex AI analysis results  
**Key Queries:** Confidence scores, anomaly detection

#### 5-13. Additional Tables
- **SENSOR_READINGS** - Equipment data
- **INVESTIGATORS** - Team members
- **INVESTIGATIONS** - Case management
- **AUDIT_LOG** - Change tracking
- **AI_AGENTS** - Agentic AI configuration
- **BUSINESS_VOCABULARY** - Data glossary
- **GHOST_ONTOLOGY** - Classification hierarchy
- **GHOST_TAXONOMY** - Type definitions
- **AI_AGENT_POLICIES** - Agent governance

---

## ⚡ Performance Tips

### Clustering Keys (Optional)
For very large tables (billions of rows), add clustering:

```sql
-- Improve filtering by type and status
ALTER TABLE GHOSTS CLUSTER BY (ghost_type, status);

-- Improve time-based queries
ALTER TABLE GHOST_SIGHTINGS CLUSTER BY (sighting_datetime);

-- Improve evidence queries
ALTER TABLE GHOST_EVIDENCE CLUSTER BY (evidence_type, processing_status);
```

### Search Columns (Optional)
For text search optimization:

```sql
-- Add search optimization service
ALTER TABLE GHOSTS ADD SEARCH OPTIMIZATION;
ALTER TABLE GHOST_SIGHTINGS ADD SEARCH OPTIMIZATION;
```

### Materialized Views
For frequently-run aggregations:

```sql
-- Create materialized view for hot queries
CREATE MATERIALIZED VIEW MV_DAILY_SIGHTINGS AS
SELECT 
    DATE(sighting_datetime) as sighting_date,
    ghost_type,
    COUNT(*) as sighting_count
FROM GHOST_SIGHTINGS
GROUP BY sighting_date, ghost_type;
```

---

## 🔍 Query Optimization

### 1. Use Partitioning Columns First
```sql
-- GOOD: Filters on datetime first (auto-partitioned)
SELECT * FROM GHOST_SIGHTINGS 
WHERE sighting_datetime >= '2024-01-01'
AND ghost_type = 'Poltergeist';

-- LESS OPTIMAL: Non-partitioning column first
SELECT * FROM GHOST_SIGHTINGS 
WHERE ghost_type = 'Poltergeist'
AND sighting_datetime >= '2024-01-01';
```

### 2. Leverage Result Caching
```sql
-- First run: Full scan
SELECT COUNT(*) FROM GHOSTS;

-- Second run: Instant (cached)
SELECT COUNT(*) FROM GHOSTS;
```

### 3. Use Column Pruning
```sql
-- GOOD: Only select needed columns
SELECT ghost_id, ghost_name, threat_level FROM GHOSTS;

-- BAD: Select * pulls all columns
SELECT * FROM GHOSTS;
```

---

## 📊 Monitoring Performance

### Check Micro-Partitions
```sql
-- See partition statistics
SELECT *
FROM TABLE(INFORMATION_SCHEMA.AUTOMATIC_CLUSTERING_HISTORY(
    DATE_RANGE_START => DATEADD('day', -7, CURRENT_DATE())
));
```

### Query Profile
```sql
-- Run your query, then check profile
SELECT * FROM GHOSTS WHERE ghost_type = 'Shadow Entity';

-- In Snowflake UI: Click "Query Profile" tab
-- Shows: partitions scanned, data volume, execution time
```

### Table Statistics
```sql
-- Check table size and row count
SELECT 
    table_name,
    row_count,
    bytes,
    ROUND(bytes/1024/1024/1024, 2) as size_gb
FROM INFORMATION_SCHEMA.TABLES
WHERE table_schema = 'APP'
AND table_type = 'BASE TABLE'
ORDER BY bytes DESC;
```

---

## 🆚 Standard vs Hybrid Tables

| Feature | Standard Tables (Our Choice) | Hybrid Tables |
|---------|----------------------------|---------------|
| **Use Case** | Analytics, AI/ML, Reporting | Transactional, Row-level ops |
| **Query Type** | Aggregations, scans | Single-row lookups |
| **Performance** | ⭐⭐⭐⭐⭐ Large scans | ⭐⭐⭐⭐⭐ Point queries |
| **Indexes** | ❌ Not needed | ✅ Supported |
| **Constraints** | ⚠️ Declared, not enforced | ✅ Enforced |
| **Cost** | 💰 Lower | 💰💰 Higher |
| **Maintenance** | Zero | Index management |
| **Storage** | Columnar | Row + Columnar hybrid |

**Our Decision:** Standard tables are perfect for the Ghost Detection System's analytical workload!

---

## ❌ Common Mistakes (Avoided)

### ❌ Don't Try to Create Indexes
```sql
-- This FAILS on standard tables!
CREATE INDEX idx_ghost_type ON GHOSTS(ghost_type);
-- Error: Table 'GHOSTS' is not a hybrid table
```

### ❌ Don't Assume Constraints are Enforced
```sql
-- PRIMARY KEY and FOREIGN KEY are declared but not enforced
-- The application should handle validation
CREATE TABLE GHOSTS (
    ghost_id VARCHAR(50) PRIMARY KEY,  -- Not enforced!
    -- ...
);
```

### ❌ Don't Over-Cluster
```sql
-- Clustering has costs - only use for very large tables
-- and frequently-filtered columns
ALTER TABLE SMALL_TABLE CLUSTER BY (col1, col2, col3);  -- Overkill!
```

---

## ✅ Best Practices

### 1. **Data Types**
```sql
-- Use appropriate types
ghost_id VARCHAR(50)           -- IDs
sighting_datetime TIMESTAMP_NTZ -- Dates without timezone
metadata VARIANT               -- JSON data
location_coordinates GEOGRAPHY -- Geospatial
```

### 2. **Naming Conventions**
- Tables: UPPERCASE with underscores (GHOST_SIGHTINGS)
- Columns: lowercase with underscores (sighting_datetime)
- IDs: {table}_id (ghost_id, sighting_id)

### 3. **Comments**
```sql
COMMENT ON TABLE GHOSTS IS 'Master registry of detected ghosts';
COMMENT ON COLUMN GHOSTS.threat_level IS 'Low, Medium, High, or Extreme';
```

### 4. **Defaults**
```sql
created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
status VARCHAR(50) DEFAULT 'Active'
```

---

## 🔧 Maintenance

### Minimal Maintenance Required!

Standard tables require almost zero maintenance:

✅ **Automatic:**
- Micro-partition creation
- Metadata updates
- Compression
- Statistics collection
- Query optimization

⚠️ **Manual (Optional):**
- Clustering key adjustments
- Search optimization
- Data retention policies

---

## 📈 Scaling

Standard tables scale automatically:

### Small Dataset (< 1 GB)
- Instant queries
- No optimization needed
- Automatic caching

### Medium Dataset (1-100 GB)
- Consider clustering keys
- Enable search optimization
- Use result caching

### Large Dataset (100 GB - 1 TB)
- Define clustering keys
- Create materialized views
- Use partition pruning
- Monitor warehouse size

### Very Large Dataset (> 1 TB)
- Aggressive clustering
- Multiple materialized views
- Larger warehouses
- Consider data retention policies

**The system handles it all automatically!**

---

## 🎯 Summary

The Ghost Detection System uses **standard Snowflake tables** because they provide:

✅ **Best Performance** for analytics and AI  
✅ **Lowest Cost** for our workload  
✅ **Zero Maintenance** - fully automatic  
✅ **Perfect for Cortex AI** integration  
✅ **Scalable** to any data volume  

**No indexes needed. No hybrid tables needed. Just pure Snowflake power!** 🚀

---

## 📚 Additional Resources

- [Snowflake Table Types](https://docs.snowflake.com/en/user-guide/tables-intro)
- [Performance Optimization](https://docs.snowflake.com/en/user-guide/performance-query-optimization)
- [Micro-Partitions](https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions)
- [Clustering Keys](https://docs.snowflake.com/en/user-guide/tables-clustering-keys)
- [Search Optimization](https://docs.snowflake.com/en/user-guide/search-optimization-service)

---

**File:** `sql/02_create_tables.sql`  
**Status:** ✅ All standard tables  
**Version:** 2.0

