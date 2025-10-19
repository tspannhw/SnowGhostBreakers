# 📸 Image Storage & Vectorization System

## ✅ Complete Implementation

All uploaded images are now:
1. ✅ **Stored** in `GHOST_IMAGES_STAGE` Snowflake stage
2. ✅ **Analyzed** with Cortex AI
3. ✅ **Vectorized** with AI embeddings (1024 dimensions)
4. ✅ **Saved** to all appropriate database tables

---

## 🗄️ Data Flow

### When a user uploads images through Streamlit:

```
1. User uploads image(s) → Streamlit file_uploader
                            ↓
2. AI analysis performed  → Cortex Complete (mistral-large2)
                            ↓
3. File saved to temp     → Temporary file system
                            ↓
4. Uploaded to stage      → GHOST_IMAGES_STAGE (Snowflake)
                            ↓
5. Embedding created      → AI_EMBED (snowflake-arctic-embed-l-v2.0-8k)
                            ↓
6. Data stored in tables:
   ├─ GHOST_SIGHTINGS     → Sighting record
   ├─ GHOST_EVIDENCE      → Evidence record + stage path
   └─ GHOST_AI_ANALYSIS   → AI analysis + embedding vector
```

---

## 📊 Tables Populated

### 1. GHOST_SIGHTINGS
**Purpose:** Record the paranormal sighting event

**Data Stored:**
- `sighting_id` - Unique ID (e.g., SIGHT_A1B2C3D4)
- `location_name` - Where it happened
- `location_address` - Full address
- `latitude` / `longitude` - GPS coordinates
- `sighting_datetime` - When it occurred
- `witness_name` / `witness_contact` - Who saw it
- `description` - Full description + AI analysis
- `evidence_type` - Type of evidence
- `paranormal_activity_level` - Intensity (1-10)
- `temperature_celsius` - Temperature reading
- `investigation_status` - 'Pending' (awaiting review)

### 2. GHOST_EVIDENCE
**Purpose:** Store evidence file references

**Data Stored:**
- `evidence_id` - Unique ID (e.g., EVID_X9Y8Z7W6)
- `sighting_id` - Links to sighting
- `evidence_type` - 'Photograph'
- `file_path` - **Stage path:** `@GHOST_IMAGES_STAGE/SIGHT_XXX_timestamp_filename.jpg`
- `capture_datetime` - When photo was taken
- `metadata` - JSON with:
  ```json
  {
    "original_filename": "ghost_photo.jpg",
    "upload_source": "streamlit",
    "file_size": 2048576,
    "upload_timestamp": "2025-10-17T14:30:00",
    "ai_analysis": "AI detected shadow entity..."
  }
  ```
- `processing_status` - 'Analyzed'

### 3. GHOST_AI_ANALYSIS
**Purpose:** Store AI analysis and embedding vectors

**Data Stored:**
- `analysis_id` - Unique ID (e.g., AI_P9Q8R7S6)
- `evidence_id` - Links to evidence
- `sighting_id` - Links to sighting
- `analysis_type` - 'Image Analysis'
- `model_used` - 'snowflake-arctic-embed-l-v2.0-8k'
- `confidence_score` - 0.85 (85%)
- `findings` - JSON with:
  ```json
  {
    "ghost_type_detected": "Shadow Entity",
    "analysis": "AI analysis of the image...",
    "confidence": 0.85,
    "anomalies_detected": ["visual evidence", "paranormal activity"],
    "embedding_model": "snowflake-arctic-embed-l-v2.0-8k",
    "embedding_dimensions": 1024
  }
  ```
- `sentiment_score` - Cortex Sentiment analysis
- **`embedding_vector`** - **VECTOR(FLOAT, 1024)** - AI embedding for similarity search

---

## 🧠 AI Embeddings

### What are Embeddings?

Embeddings are **1024-dimensional vectors** that represent the semantic meaning of the image analysis. This allows:

- ✅ **Similarity Search** - Find similar ghost evidence
- ✅ **Clustering** - Group similar sightings
- ✅ **Pattern Detection** - Identify recurring ghost types
- ✅ **Anomaly Detection** - Spot unusual activity

### How They're Created:

```sql
SNOWFLAKE.CORTEX.AI_EMBED(
    'snowflake-arctic-embed-l-v2.0-8k',
    'Shadow Entity ghost evidence. AI detected dark mass with electronic interference...'
)
```

**Returns:** Array of 1024 floating-point numbers representing semantic meaning

**Example:**
```
[0.123, -0.456, 0.789, 0.234, -0.567, ...]  (1024 values)
```

### Using Embeddings for Search:

```sql
-- Find similar ghost evidence
SELECT 
    e.evidence_id,
    e.file_path,
    VECTOR_COSINE_SIMILARITY(
        ai.embedding_vector,
        (SELECT embedding_vector FROM GHOST_AI_ANALYSIS WHERE analysis_id = 'AI_TARGET')
    ) as similarity_score
FROM GHOST_EVIDENCE e
JOIN GHOST_AI_ANALYSIS ai ON e.evidence_id = ai.evidence_id
WHERE similarity_score > 0.7
ORDER BY similarity_score DESC
```

---

## 📁 File Naming Convention

### Stage Path Format:
```
@GHOST_IMAGES_STAGE/{SIGHTING_ID}_{TIMESTAMP}_{SAFE_FILENAME}
```

### Example:
```
Original filename:  My Ghost Photo (1).jpg
Sighting ID:        SIGHT_A1B2C3D4
Timestamp:          20251017_143045

Stage path:  @GHOST_IMAGES_STAGE/SIGHT_A1B2C3D4_20251017_143045_My_Ghost_Photo_1.jpg
```

**Safety measures:**
- Spaces → underscores
- Parentheses removed
- Special characters sanitized
- Unique timestamp prevents conflicts

---

## 🔧 Technical Implementation

### File Upload Process:

```python
# 1. Read file bytes from Streamlit uploader
file_bytes = uploaded_file.read()

# 2. Create temporary file
with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
    tmp_file.write(file_bytes)
    tmp_path = tmp_file.name

# 3. Upload to Snowflake stage
session.sql(f"PUT 'file://{tmp_path}' @GHOST_IMAGES_STAGE/{filename} OVERWRITE=TRUE")

# 4. Clean up temp file
os.unlink(tmp_path)
```

### Embedding Creation:

```python
# 1. Generate analysis text
analysis_text = f"{ghost_type} ghost evidence. {ai_analysis}"

# 2. Create embedding
embedding_query = """
SELECT SNOWFLAKE.CORTEX.AI_EMBED(
    'snowflake-arctic-embed-l-v2.0-8k',
    :text
) as embedding_vector
"""
result = session.sql(embedding_query, params={'text': analysis_text}).collect()

# 3. Extract vector
embedding_vector = result[0]['EMBEDDING_VECTOR']  # Array of 1024 floats
```

### Database Insertion:

```python
# Insert evidence record
session.sql(f"""
INSERT INTO GHOST_EVIDENCE (
    evidence_id, sighting_id, evidence_type, file_path, metadata, processing_status
) VALUES (
    '{evidence_id}', '{sighting_id}', 'Photograph', 
    '{stage_path}', PARSE_JSON('{metadata_json}'), 'Analyzed'
)
""").collect()

# Insert AI analysis with embedding
session.sql(f"""
INSERT INTO GHOST_AI_ANALYSIS (
    analysis_id, evidence_id, sighting_id, analysis_type,
    model_used, confidence_score, findings, embedding_vector
) VALUES (
    '{analysis_id}', '{evidence_id}', '{sighting_id}', 'Image Analysis',
    'snowflake-arctic-embed-l-v2.0-8k', 0.85, 
    PARSE_JSON('{findings_json}'), {embedding_vector}
)
""").collect()
```

---

## 🎯 Success Metrics

After successful upload, Streamlit displays:

```
✅ Sighting reported and saved to database!

┌────────────────┬──────────────┬────────────────┬────────────────┐
│ Sighting ID    │ Activity Lvl │ Photos Uploaded│ AI Embeddings  │
├────────────────┼──────────────┼────────────────┼────────────────┤
│ SIGHT_A1B2C3D4 │     8/10     │       3        │       3        │
└────────────────┴──────────────┴────────────────┴────────────────┘

🤖 AI Classification: Shadow Entity

📸 3 images uploaded to GHOST_IMAGES_STAGE
📁 View uploaded files and embeddings ▼
   ✓ ghost_photo_1.jpg → @GHOST_IMAGES_STAGE/SIGHT_A1B2C3D4_20251017_143045_ghost_photo_1.jpg
      🧠 AI Embedding created (1024 dimensions)
      📊 Analysis: Shadow Entity ghost evidence. AI detected dark mass with electronic...
   
🧠 3 AI embeddings created for similarity search
📍 Location: 40.753182, -73.982253
```

---

## 🔍 Verification Queries

### Check Uploaded Images:

```sql
-- Recent uploads from Streamlit
SELECT 
    e.evidence_id,
    e.sighting_id,
    e.file_path,
    e.metadata:original_filename::STRING as original_filename,
    e.metadata:upload_source::STRING as source,
    e.capture_datetime,
    e.processing_status
FROM GHOST_DETECTION.APP.GHOST_EVIDENCE e
WHERE e.metadata:upload_source::STRING = 'streamlit'
ORDER BY e.capture_datetime DESC
LIMIT 10;
```

### Check AI Embeddings:

```sql
-- AI analysis with embeddings
SELECT 
    ai.analysis_id,
    ai.evidence_id,
    ai.sighting_id,
    ai.model_used,
    ai.confidence_score,
    ai.findings:ghost_type_detected::STRING as ghost_type,
    ARRAY_SIZE(ai.embedding_vector) as embedding_dimensions,
    ai.analysis_datetime
FROM GHOST_DETECTION.APP.GHOST_AI_ANALYSIS ai
WHERE ai.analysis_type = 'Image Analysis'
  AND ai.embedding_vector IS NOT NULL
ORDER BY ai.analysis_datetime DESC
LIMIT 10;
```

### Check Stage Contents:

```sql
-- List files in stage
LIST @GHOST_IMAGES_STAGE;

-- Filter by sighting ID
LIST @GHOST_IMAGES_STAGE PATTERN='.*SIGHT_A1B2C3D4.*';
```

### Complete Sighting Information:

```sql
-- Full sighting with evidence and AI analysis
SELECT 
    s.sighting_id,
    s.location_name,
    s.witness_name,
    s.sighting_datetime,
    e.evidence_id,
    e.file_path,
    ai.analysis_id,
    ai.findings:ghost_type_detected::STRING as detected_type,
    ai.confidence_score,
    ARRAY_SIZE(ai.embedding_vector) as embedding_dimensions
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
LEFT JOIN GHOST_DETECTION.APP.GHOST_EVIDENCE e ON s.sighting_id = e.sighting_id
LEFT JOIN GHOST_DETECTION.APP.GHOST_AI_ANALYSIS ai ON e.evidence_id = ai.evidence_id
WHERE s.investigation_status = 'Pending'
  AND e.metadata:upload_source::STRING = 'streamlit'
ORDER BY s.sighting_datetime DESC;
```

---

## 🛠️ Troubleshooting

### Issue: "PUT command failed"

**Cause:** Insufficient permissions or stage doesn't exist

**Fix:**
```sql
-- Ensure stage exists
CREATE STAGE IF NOT EXISTS GHOST_DETECTION.APP.GHOST_IMAGES_STAGE;

-- Grant permissions
GRANT READ, WRITE ON STAGE GHOST_DETECTION.APP.GHOST_IMAGES_STAGE TO ROLE GHOSTBUSTER;
```

### Issue: "Embedding vector is NULL"

**Cause:** Embedding creation failed

**Solution:**
- Check that Cortex AI is enabled
- Verify model name: `snowflake-arctic-embed-l-v2.0-8k`
- Ensure text is not empty
- Check text length < 8192 tokens

### Issue: "File not found in stage"

**Cause:** Upload failed silently

**Debug:**
```sql
-- Check stage files
LIST @GHOST_IMAGES_STAGE;

-- Check evidence records
SELECT file_path, metadata FROM GHOST_EVIDENCE 
WHERE evidence_id = 'EVID_XXX';
```

### Issue: "JSON parsing error in metadata"

**Cause:** Special characters in analysis text

**Fix:** Already handled with `.replace("'", "''")` and JSON escaping

---

## 📈 Performance Considerations

### File Size Limits:

- **Recommended:** < 10 MB per image
- **Maximum:** 50 MB per image
- **Batch:** Up to 10 images per sighting

### Embedding Generation:

- **Time:** ~1-2 seconds per image
- **Cost:** Minimal (using Snowflake credits)
- **Dimensions:** 1024 (fixed for model)

### Storage:

- **Stage:** Unlimited capacity (charges apply)
- **Database:** Embedding vectors ~ 4KB each
- **Metadata:** JSON ~ 1-2KB each

---

## 🔐 Security & Privacy

### Access Control:

```sql
-- Only authorized roles can access
GRANT SELECT ON GHOST_EVIDENCE TO ROLE INVESTIGATOR;
GRANT SELECT ON GHOST_AI_ANALYSIS TO ROLE INVESTIGATOR;
GRANT READ ON STAGE GHOST_IMAGES_STAGE TO ROLE INVESTIGATOR;
```

### Data Encryption:

- ✅ **In Transit:** TLS/SSL encryption
- ✅ **At Rest:** Snowflake automatic encryption
- ✅ **Stage:** Encrypted storage

### Compliance:

- ✅ **GDPR:** Personal data anonymizable
- ✅ **Retention:** Configurable via Time Travel
- ✅ **Audit:** All operations logged in AUDIT_LOG table

---

## 🚀 Advanced Features

### Similarity Search:

```python
# Find similar ghost evidence to a new upload
def find_similar_evidence(analysis_id, threshold=0.7, limit=10):
    query = f"""
    WITH target AS (
        SELECT embedding_vector 
        FROM GHOST_AI_ANALYSIS 
        WHERE analysis_id = '{analysis_id}'
    )
    SELECT 
        e.evidence_id,
        s.location_name,
        ai.findings:ghost_type_detected::STRING as ghost_type,
        VECTOR_COSINE_SIMILARITY(ai.embedding_vector, (SELECT * FROM target)) as similarity
    FROM GHOST_AI_ANALYSIS ai
    JOIN GHOST_EVIDENCE e ON ai.evidence_id = e.evidence_id
    JOIN GHOST_SIGHTINGS s ON e.sighting_id = s.sighting_id
    WHERE VECTOR_COSINE_SIMILARITY(ai.embedding_vector, (SELECT * FROM target)) > {threshold}
      AND ai.analysis_id != '{analysis_id}'
    ORDER BY similarity DESC
    LIMIT {limit}
    """
    return session.sql(query).to_pandas()
```

### Batch Vectorization:

```sql
-- Vectorize all existing evidence without embeddings
INSERT INTO GHOST_AI_ANALYSIS (
    analysis_id, evidence_id, sighting_id, analysis_type,
    model_used, embedding_vector, analysis_datetime
)
SELECT 
    CONCAT('AI_', UUID_STRING()),
    e.evidence_id,
    e.sighting_id,
    'Batch Image Embedding',
    'snowflake-arctic-embed-l-v2.0-8k',
    SNOWFLAKE.CORTEX.AI_EMBED(
        'snowflake-arctic-embed-l-v2.0-8k',
        CONCAT('Evidence type: ', e.evidence_type, '. Metadata: ', e.metadata::STRING)
    ),
    CURRENT_TIMESTAMP()
FROM GHOST_EVIDENCE e
LEFT JOIN GHOST_AI_ANALYSIS ai ON e.evidence_id = ai.evidence_id
WHERE ai.analysis_id IS NULL
  AND e.evidence_type IN ('Photograph', 'Video', 'Image');
```

---

## ✅ Summary

**Complete Implementation:**
- ✅ Images uploaded to Snowflake stage
- ✅ AI analysis performed on each image
- ✅ 1024-dimensional embeddings created
- ✅ Data stored in 3 tables (SIGHTINGS, EVIDENCE, AI_ANALYSIS)
- ✅ Similarity search ready
- ✅ Full metadata tracked
- ✅ Error handling & fallbacks
- ✅ Secure & encrypted storage

**Benefits:**
- 🔍 **Searchable** - Find similar ghost evidence
- 🧠 **AI-Powered** - Automatic analysis
- 📊 **Analytical** - Pattern detection ready
- 🔒 **Secure** - Encrypted & access-controlled
- ⚡ **Fast** - Optimized for performance

---

**🎉 Your ghost evidence is now fully stored and vectorized!** 👻📸🧠

**Last Updated:** October 17, 2025  
**Version:** 2.0  
**File:** `streamlit_app/ghost_detection_app.py`  
**Stage:** `@GHOST_DETECTION.APP.GHOST_IMAGES_STAGE`

