# 📊 Enhanced Ghost Reports with Cortex AI

## 🎯 Overview

Generate detailed, AI-powered investigation reports for ghosts and store them in a dedicated table.

---

## 📋 Complete Solution

### Step 1: Create the Reports Table

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

CREATE TABLE IF NOT EXISTS GHOST_ENHANCED_REPORTS (
    report_id VARCHAR(50) PRIMARY KEY DEFAULT UUID_STRING(),
    ghost_id VARCHAR(50),
    ghost_name VARCHAR(200),
    ghost_type VARCHAR(100),
    enhanced_description TEXT,
    generated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    model_used VARCHAR(50) DEFAULT 'mistral-large2',
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);
```

### Step 2: Insert Enhanced Reports

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Write a detailed paranormal investigation report for: ',
            ghost_name, ' (', ghost_type, '). ',
            'Description: ', description, '. ',
            'Make it scientific and professional.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE status = 'Active'
LIMIT 5;
```

### Step 3: View the Reports

```sql
-- Preview all reports
SELECT 
    report_id,
    ghost_name,
    ghost_type,
    LEFT(enhanced_description, 200) as report_preview,
    generated_at
FROM GHOST_ENHANCED_REPORTS
ORDER BY generated_at DESC;

-- Get full report for specific ghost
SELECT 
    ghost_name,
    ghost_type,
    enhanced_description as full_report,
    generated_at
FROM GHOST_ENHANCED_REPORTS
WHERE ghost_id = 'GH001'
ORDER BY generated_at DESC
LIMIT 1;
```

---

## 🚀 Quick Start

### Option 1: Run the Complete Script

```sql
-- Execute the complete script
-- File: sql/generate_enhanced_reports.sql
!source sql/generate_enhanced_reports.sql
```

### Option 2: Step-by-Step in Worksheet

1. **Create table** (copy Step 1 above)
2. **Generate reports** (copy Step 2 above)
3. **View results** (copy Step 3 above)

---

## 💡 Advanced Usage

### Generate Reports for ALL Active Ghosts

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'Write a detailed paranormal investigation report for: ',
            ghost_name, ' (', ghost_type, '). ',
            'Description: ', description, '. ',
            'Threat Level: ', threat_level, '. ',
            'Origin: ', origin_story, '. ',
            'Make it scientific and professional with containment recommendations.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE status = 'Active'
AND ghost_id NOT IN (SELECT ghost_id FROM GHOST_ENHANCED_REPORTS);
```

### Generate Reports for High Threat Ghosts Only

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    ghost_id,
    ghost_name,
    ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            '⚠️ URGENT THREAT ASSESSMENT ⚠️\n',
            'Entity: ', ghost_name, ' (', ghost_type, ')\n',
            'Threat Level: ', threat_level, '\n',
            'Description: ', description, '\n',
            'Origin: ', origin_story, '\n\n',
            'Provide:\n',
            '1. Immediate threat assessment\n',
            '2. Containment protocols\n',
            '3. Required equipment\n',
            '4. Safety precautions\n',
            '5. Recommended team size\n',
            'Format as official incident report.'
        )
    ) as enhanced_description
FROM GHOSTS
WHERE status = 'Active'
AND threat_level IN ('High', 'Extreme');
```

### Regenerate Report for Specific Ghost

```sql
-- Delete old report
DELETE FROM GHOST_ENHANCED_REPORTS 
WHERE ghost_id = 'GH001';

-- Generate fresh report with more details
INSERT INTO GHOST_ENHANCED_REPORTS (
    ghost_id,
    ghost_name,
    ghost_type,
    enhanced_description
)
SELECT 
    g.ghost_id,
    g.ghost_name,
    g.ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE(
        'mistral-large2',
        CONCAT(
            'COMPREHENSIVE PARANORMAL INVESTIGATION REPORT\n\n',
            'Subject: ', g.ghost_name, '\n',
            'Classification: ', g.ghost_type, '\n',
            'Threat Level: ', g.threat_level, '\n',
            'Status: ', g.status, '\n',
            'Total Sightings: ', COUNT(s.sighting_id), '\n',
            'First Detected: ', g.first_detected_date, '\n\n',
            'Description: ', g.description, '\n\n',
            'Origin Story: ', g.origin_story, '\n\n',
            'Generate detailed report with:\n',
            '1. Executive Summary\n',
            '2. Behavioral Analysis\n',
            '3. Threat Assessment\n',
            '4. Historical Context\n',
            '5. Recommended Actions\n',
            '6. Containment Strategy'
        )
    ) as enhanced_description
FROM GHOSTS g
LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
WHERE g.ghost_id = 'GH001'
GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level, 
         g.status, g.description, g.origin_story, g.first_detected_date;
```

---

## 📊 Example Queries

### View All Reports Summary

```sql
SELECT 
    COUNT(*) as total_reports,
    COUNT(DISTINCT ghost_id) as unique_ghosts,
    MIN(generated_at) as first_report,
    MAX(generated_at) as latest_report,
    AVG(LENGTH(enhanced_description)) as avg_report_length
FROM GHOST_ENHANCED_REPORTS;
```

### Find Longest Reports

```sql
SELECT 
    ghost_name,
    ghost_type,
    LENGTH(enhanced_description) as report_length,
    LEFT(enhanced_description, 100) as preview
FROM GHOST_ENHANCED_REPORTS
ORDER BY report_length DESC
LIMIT 5;
```

### Reports by Ghost Type

```sql
SELECT 
    ghost_type,
    COUNT(*) as report_count,
    AVG(LENGTH(enhanced_description)) as avg_length
FROM GHOST_ENHANCED_REPORTS
GROUP BY ghost_type
ORDER BY report_count DESC;
```

### Search Reports by Content

```sql
SELECT 
    ghost_name,
    ghost_type,
    enhanced_description
FROM GHOST_ENHANCED_REPORTS
WHERE enhanced_description ILIKE '%containment%'
   OR enhanced_description ILIKE '%dangerous%'
ORDER BY generated_at DESC;
```

---

## 🔄 Batch Processing with Stored Procedure

Create a procedure to automate report generation:

```sql
CREATE OR REPLACE PROCEDURE GENERATE_BATCH_REPORTS(ghost_status VARCHAR DEFAULT 'Active')
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    report_count INT;
BEGIN
    -- Generate reports for ghosts without existing reports
    INSERT INTO GHOST_ENHANCED_REPORTS (
        ghost_id,
        ghost_name,
        ghost_type,
        enhanced_description
    )
    SELECT 
        ghost_id,
        ghost_name,
        ghost_type,
        SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            CONCAT(
                'Write a detailed paranormal investigation report for: ',
                ghost_name, ' (', ghost_type, '). ',
                'Description: ', description, '. ',
                'Threat Level: ', threat_level, '. ',
                'Make it scientific and professional.'
            )
        ) as enhanced_description
    FROM GHOSTS
    WHERE status = :ghost_status
    AND ghost_id NOT IN (SELECT ghost_id FROM GHOST_ENHANCED_REPORTS);
    
    -- Count generated reports
    SELECT COUNT(*) INTO :report_count
    FROM GHOST_ENHANCED_REPORTS
    WHERE generated_at >= DATEADD(second, -60, CURRENT_TIMESTAMP());
    
    RETURN 'Generated ' || report_count || ' enhanced reports for ' || ghost_status || ' ghosts';
END;
$$;

-- Call the procedure
CALL GENERATE_BATCH_REPORTS('Active');
```

---

## 🎨 Custom Report Templates

### Template 1: Executive Summary

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (ghost_id, ghost_name, ghost_type, enhanced_description)
SELECT 
    ghost_id, ghost_name, ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE('mistral-large2',
        CONCAT('Executive Summary for ', ghost_name, ': Provide 3-paragraph overview covering threat, behavior, and recommendations.')
    )
FROM GHOSTS WHERE ghost_id = 'GH001';
```

### Template 2: Tactical Brief

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (ghost_id, ghost_name, ghost_type, enhanced_description)
SELECT 
    ghost_id, ghost_name, ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE('mistral-large2',
        CONCAT('Tactical Brief for ', ghost_name, ' (', ghost_type, ', ', threat_level, ' threat): ',
               'List required: 1) Equipment, 2) Team size, 3) Approach strategy, 4) Safety measures. Be concise and tactical.')
    )
FROM GHOSTS WHERE ghost_id = 'GH002';
```

### Template 3: Research Report

```sql
INSERT INTO GHOST_ENHANCED_REPORTS (ghost_id, ghost_name, ghost_type, enhanced_description)
SELECT 
    ghost_id, ghost_name, ghost_type,
    SNOWFLAKE.CORTEX.COMPLETE('mistral-large2',
        CONCAT('Academic research report on ', ghost_name, ': ',
               'Type: ', ghost_type, '. ',
               'Origin: ', origin_story, '. ',
               'Include: Historical context, behavioral patterns, theoretical explanations, citations in APA format.')
    )
FROM GHOSTS WHERE ghost_id = 'GH003';
```

---

## 📈 Export Reports

### Export to CSV

```sql
-- Copy to stage
COPY INTO @GHOST_DATA_STAGE/enhanced_reports/
FROM (
    SELECT 
        ghost_id,
        ghost_name,
        ghost_type,
        enhanced_description,
        generated_at
    FROM GHOST_ENHANCED_REPORTS
)
FILE_FORMAT = (TYPE = CSV COMPRESSION = GZIP)
HEADER = TRUE
OVERWRITE = TRUE;
```

### Create View for Easy Access

```sql
CREATE OR REPLACE VIEW VW_LATEST_GHOST_REPORTS AS
SELECT 
    r.report_id,
    r.ghost_id,
    r.ghost_name,
    r.ghost_type,
    g.threat_level,
    g.status,
    r.enhanced_description,
    r.generated_at,
    DATEDIFF(day, r.generated_at, CURRENT_TIMESTAMP()) as days_old
FROM GHOST_ENHANCED_REPORTS r
JOIN GHOSTS g ON r.ghost_id = g.ghost_id
QUALIFY ROW_NUMBER() OVER (PARTITION BY r.ghost_id ORDER BY r.generated_at DESC) = 1;

-- Use the view
SELECT * FROM VW_LATEST_GHOST_REPORTS
WHERE threat_level IN ('High', 'Extreme')
ORDER BY generated_at DESC;
```

---

## ⚡ Performance Tips

### 1. Generate Reports in Batches

```sql
-- Process in batches of 10
INSERT INTO GHOST_ENHANCED_REPORTS (...)
SELECT ... FROM GHOSTS
WHERE status = 'Active'
AND ghost_id NOT IN (SELECT ghost_id FROM GHOST_ENHANCED_REPORTS)
LIMIT 10;
```

### 2. Schedule Regular Updates

```sql
-- Create task to generate weekly reports
CREATE OR REPLACE TASK WEEKLY_GHOST_REPORTS
  WAREHOUSE = GHOST_WAREHOUSE
  SCHEDULE = 'USING CRON 0 9 * * MON America/New_York'  -- Every Monday at 9 AM
AS
  CALL GENERATE_BATCH_REPORTS('Active');

-- Enable the task
ALTER TASK WEEKLY_GHOST_REPORTS RESUME;
```

### 3. Archive Old Reports

```sql
-- Archive reports older than 90 days
CREATE TABLE GHOST_ENHANCED_REPORTS_ARCHIVE AS
SELECT * FROM GHOST_ENHANCED_REPORTS
WHERE generated_at < DATEADD(day, -90, CURRENT_TIMESTAMP());

DELETE FROM GHOST_ENHANCED_REPORTS
WHERE generated_at < DATEADD(day, -90, CURRENT_TIMESTAMP());
```

---

## ✅ Summary

### What You Can Do:

1. ✅ **Store AI reports in table** - Persistent storage
2. ✅ **Query reports easily** - Standard SQL
3. ✅ **Track report history** - Version control
4. ✅ **Export reports** - CSV, JSON, etc.
5. ✅ **Automate generation** - Scheduled tasks
6. ✅ **Custom templates** - Different report types

### Files Created:

- ✅ `sql/generate_enhanced_reports.sql` - Complete script
- ✅ `ENHANCED_REPORTS_GUIDE.md` - This guide

---

**Ready to generate professional ghost investigation reports with AI!** 👻📊✨

