# ⚡ Image Upload Quick Guide

## ✅ What Happens When You Upload Images

### 1. Upload Process
```
User uploads image → AI analyzes → Saves to stage → Creates embedding → Stores in DB
```

### 2. Tables Updated

| Table | What's Stored |
|-------|---------------|
| **GHOST_SIGHTINGS** | Sighting details, location, witness info |
| **GHOST_EVIDENCE** | Image reference in stage: `@GHOST_IMAGES_STAGE/file.jpg` |
| **GHOST_AI_ANALYSIS** | AI analysis + 1024-dimensional embedding vector |

### 3. Features

✅ **File Storage** - Uploaded to `@GHOST_IMAGES_STAGE`  
✅ **AI Analysis** - Cortex Complete analyzes each image  
✅ **Vectorization** - 1024D embeddings for similarity search  
✅ **Metadata** - JSON with filename, size, upload time  
✅ **Sentiment** - Cortex Sentiment analysis  

---

## 🚀 Quick Test

### Test Upload:
1. Open Streamlit app → ➕ New Sighting
2. Upload 1-3 test images
3. Fill in required fields
4. Submit

### Expected Result:
```
✅ Sighting reported and saved to database!

Sighting ID: SIGHT_A1B2C3D4
Activity Lvl: 8/10
Photos Uploaded: 3
AI Embeddings: 3

📸 3 images uploaded to GHOST_IMAGES_STAGE
🧠 3 AI embeddings created for similarity search
```

---

## 🔍 Verify Data

### Check Uploaded Files:
```sql
-- Recent uploads
SELECT 
    evidence_id,
    file_path,
    metadata:original_filename::STRING as filename
FROM GHOST_EVIDENCE
WHERE metadata:upload_source::STRING = 'streamlit'
ORDER BY capture_datetime DESC
LIMIT 5;
```

### Check Embeddings:
```sql
-- AI embeddings
SELECT 
    analysis_id,
    evidence_id,
    ARRAY_SIZE(embedding_vector) as dimensions
FROM GHOST_AI_ANALYSIS
WHERE embedding_vector IS NOT NULL
ORDER BY analysis_datetime DESC
LIMIT 5;
```

### Check Stage:
```sql
-- List uploaded files
LIST @GHOST_IMAGES_STAGE;
```

---

## 🎯 File Naming

**Format:** `{SIGHTING_ID}_{TIMESTAMP}_{FILENAME}`

**Example:**
- Original: `My Ghost Photo.jpg`
- Stored as: `SIGHT_A1B2_20251017_143045_My_Ghost_Photo.jpg`

---

## 🧠 Embeddings

**Model:** `snowflake-arctic-embed-l-v2.0-8k`  
**Dimensions:** 1024  
**Purpose:** Similarity search, clustering, pattern detection

**Use Case:**
```sql
-- Find similar evidence
SELECT 
    evidence_id,
    VECTOR_COSINE_SIMILARITY(
        embedding_vector,
        (SELECT embedding_vector FROM GHOST_AI_ANALYSIS WHERE analysis_id = 'AI_TARGET')
    ) as similarity
FROM GHOST_AI_ANALYSIS
WHERE similarity > 0.7
ORDER BY similarity DESC;
```

---

## ⚠️ Troubleshooting

### No embeddings created?
- Check Cortex AI is enabled
- Verify text analysis succeeded
- Look for errors in Streamlit UI

### File not in stage?
```sql
LIST @GHOST_IMAGES_STAGE;
-- If empty, check PUT permissions
```

### Missing data in tables?
```sql
-- Check recent sightings
SELECT * FROM GHOST_SIGHTINGS 
WHERE investigation_status = 'Pending'
ORDER BY sighting_datetime DESC
LIMIT 5;
```

---

## 📚 Full Documentation

See **`IMAGE_STORAGE_AND_VECTORIZATION.md`** for complete technical details.

---

**🎉 Complete image storage & vectorization system!** 📸🧠✨

