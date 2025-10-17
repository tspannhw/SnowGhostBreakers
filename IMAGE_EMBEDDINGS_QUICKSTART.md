# 🚀 Image Embeddings & Similarity Search - Quick Start

## ✅ Status: FULLY WORKING

All image embedding functionality is now operational with custom cosine similarity function.

---

## 📋 Prerequisites

- Snowflake account with Cortex AI enabled
- JavaScript UDFs enabled (standard on most Snowflake editions)
- `GHOST_DETECTION` database and `APP` schema created
- Ghost tables populated with data

---

## ⚡ Quick Installation (3 Steps)

### **Step 1: Run the SQL Script**

```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Run the image embeddings setup
SOURCE sql/14_image_embeddings_table.sql;
```

This creates:
- ✅ `GHOST_IMAGE_EMBEDDINGS` table
- ✅ `COSINE_SIMILARITY` function (custom JavaScript)
- ✅ 5 stored procedures
- ✅ 3 views for statistics

### **Step 2: Generate Embeddings**

```sql
-- Generate embeddings for first 50 evidence items
CALL BATCH_GENERATE_EMBEDDINGS(50);
```

Output:
```
Processed 50 of 150 image embeddings
```

### **Step 3: Test Search**

```sql
-- Search for similar images by text
CALL FIND_SIMILAR_IMAGES('glowing orb', 5);
```

Expected output:
```
EMBEDDING_ID | EVIDENCE_ID | GHOST_ID | IMAGE_DESCRIPTION      | SIMILARITY | IMAGE_PATH
-------------|-------------|----------|------------------------|------------|------------
EMB_ABC123   | EV_001      | GH_001   | Bright orb of light... | 0.92       | /images/...
EMB_DEF456   | EV_012      | GH_003   | Glowing sphere...      | 0.87       | /images/...
...
```

---

## 🎯 Available Functions

### **1. Generate Single Embedding**
```sql
CALL GENERATE_IMAGE_EMBEDDING(
    'EV_001',                               -- evidence_id
    'Bright orb of light in the hallway'    -- description
);
```

### **2. Batch Generate Embeddings**
```sql
CALL BATCH_GENERATE_EMBEDDINGS(100);  -- Process up to 100 items
```

### **3. Text Search**
```sql
CALL FIND_SIMILAR_IMAGES(
    'ghost orb',    -- search query
    10              -- max results
);
```

### **4. Image-to-Image Search**
```sql
CALL FIND_SIMILAR_TO_IMAGE(
    'EMB_ABC123',   -- source embedding_id
    5               -- max results
);
```

### **5. Get Image Clusters**
```sql
CALL GET_IMAGE_CLUSTERS(0.7);  -- similarity threshold
```

### **6. Test Cosine Similarity**
```sql
SELECT COSINE_SIMILARITY(
    ARRAY_CONSTRUCT(1, 2, 3),
    ARRAY_CONSTRUCT(4, 5, 6)
) AS similarity;
-- Returns: 0.974
```

---

## 📊 Available Views

### **Statistics Dashboard**
```sql
SELECT * FROM VW_IMAGE_SIMILARITY_STATS;
```

Returns:
```
TOTAL_EMBEDDINGS | UNIQUE_GHOSTS | UNIQUE_SIGHTINGS | AVG_CONFIDENCE | AVG_SEARCHES | ...
-----------------|---------------|------------------|----------------|--------------|----
50               | 12            | 45               | 0.85           | 2.3          | ...
```

### **Popular Searches**
```sql
SELECT * FROM VW_POPULAR_IMAGE_SEARCHES LIMIT 10;
```

### **Performance Over Time**
```sql
SELECT * FROM VW_EMBEDDING_PERFORMANCE LIMIT 24;
```

---

## 🖥️ Streamlit App Integration

The Streamlit app already has full integration!

### **Navigate to: 🔍 Image Similarity**

**Tab 1: Text Search**
1. Enter search query: "ghost orb"
2. Adjust number of results: 5-20
3. Click **🔍 Search**
4. View results with similarity scores

**Tab 2: Image-to-Image**
1. Select a source image from dropdown
2. Set number of results
3. Click **🔍 Find Similar**
4. View matched images

**Tab 3: Statistics**
- View embedding statistics
- See popular searches
- Check performance charts

**Tab 4: Generate Embeddings**
- Batch generate embeddings
- Monitor progress
- View completion stats

---

## 🔍 Example Workflows

### **Workflow 1: First Time Setup**

```sql
-- 1. Create everything
SOURCE sql/14_image_embeddings_table.sql;

-- 2. Generate embeddings for all photos
CALL BATCH_GENERATE_EMBEDDINGS(1000);

-- 3. Check statistics
SELECT * FROM VW_IMAGE_SIMILARITY_STATS;

-- 4. Test search
CALL FIND_SIMILAR_IMAGES('apparition', 10);
```

### **Workflow 2: Add New Evidence**

```sql
-- 1. Insert new evidence (already done via Streamlit)

-- 2. Generate embedding for it
CALL GENERATE_IMAGE_EMBEDDING(
    'EV_NEW_001',
    'Shadow figure in doorway'
);

-- 3. Find similar existing images
CALL FIND_SIMILAR_IMAGES('shadow figure', 5);
```

### **Workflow 3: Research Similar Sightings**

```sql
-- 1. Start with a specific image
CALL FIND_SIMILAR_TO_IMAGE('EMB_ABC123', 20);

-- 2. View all related ghosts
SELECT DISTINCT g.*
FROM GHOST_IMAGE_EMBEDDINGS e
JOIN GHOSTS g ON e.ghost_id = g.ghost_id
WHERE COSINE_SIMILARITY(
    e.embedding_vector,
    (SELECT embedding_vector FROM GHOST_IMAGE_EMBEDDINGS WHERE embedding_id = 'EMB_ABC123')
) > 0.7;

-- 3. Find patterns across multiple sightings
SELECT 
    e.ghost_id,
    g.ghost_type,
    COUNT(*) as similar_images,
    AVG(COSINE_SIMILARITY(
        e.embedding_vector,
        (SELECT embedding_vector FROM GHOST_IMAGE_EMBEDDINGS WHERE embedding_id = 'EMB_ABC123')
    )) as avg_similarity
FROM GHOST_IMAGE_EMBEDDINGS e
JOIN GHOSTS g ON e.ghost_id = g.ghost_id
WHERE COSINE_SIMILARITY(
    e.embedding_vector,
    (SELECT embedding_vector FROM GHOST_IMAGE_EMBEDDINGS WHERE embedding_id = 'EMB_ABC123')
) > 0.6
GROUP BY e.ghost_id, g.ghost_type
ORDER BY avg_similarity DESC;
```

---

## 🧪 Verification Tests

### **Test 1: Function Exists**
```sql
SHOW USER FUNCTIONS LIKE 'COSINE_SIMILARITY';
-- Should return: 1 row
```

### **Test 2: Function Works**
```sql
SELECT COSINE_SIMILARITY(
    ARRAY_CONSTRUCT(1.0, 0.0, 0.0),
    ARRAY_CONSTRUCT(1.0, 0.0, 0.0)
);
-- Should return: 1.0 (perfect match)

SELECT COSINE_SIMILARITY(
    ARRAY_CONSTRUCT(1.0, 0.0),
    ARRAY_CONSTRUCT(0.0, 1.0)
);
-- Should return: 0.0 (no similarity)
```

### **Test 3: Procedures Exist**
```sql
SHOW PROCEDURES LIKE '%IMAGE%';
-- Should return: 5 procedures
```

### **Test 4: Table Created**
```sql
DESC TABLE GHOST_IMAGE_EMBEDDINGS;
-- Should show: 17 columns
```

### **Test 5: Views Work**
```sql
SELECT * FROM VW_IMAGE_SIMILARITY_STATS;
-- Should return: 1 row (even if all zeros)
```

---

## 🐛 Troubleshooting

### **Issue: JavaScript not enabled**

**Error:** `JavaScript UDFs are not enabled`

**Solution:**
```sql
-- Have your admin run:
ALTER ACCOUNT SET JAVASCRIPT_UDF = TRUE;
```

### **Issue: No embeddings found**

**Error:** Query returns 0 results

**Solution:**
```sql
-- Check if embeddings exist
SELECT COUNT(*) FROM GHOST_IMAGE_EMBEDDINGS;

-- If 0, generate them:
CALL BATCH_GENERATE_EMBEDDINGS(50);
```

### **Issue: Similarity too low**

**Problem:** All similarity scores are < 0.5

**Solution:** Lower the threshold in queries
```sql
-- Change from:
WHERE COSINE_SIMILARITY(...) > 0.5

-- To:
WHERE COSINE_SIMILARITY(...) > 0.3
```

### **Issue: Slow performance**

**Problem:** Queries take too long

**Solutions:**
1. Create an index:
```sql
CREATE INDEX idx_ghost_id ON GHOST_IMAGE_EMBEDDINGS(ghost_id);
```

2. Limit search scope:
```sql
-- Add WHERE clause to filter first
WHERE ghost_id IN (SELECT ghost_id FROM relevant_ghosts)
```

3. Use smaller batches:
```sql
CALL BATCH_GENERATE_EMBEDDINGS(25);  -- Instead of 100
```

---

## 📈 Performance Tips

### **Optimize Large Datasets**

**For 1000+ embeddings:**

1. **Create temp table for query vector:**
```sql
CREATE TEMP TABLE query_vec AS
SELECT SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', 'ghost orb') as vec;

SELECT 
    e.*,
    COSINE_SIMILARITY(e.embedding_vector, q.vec) as similarity
FROM GHOST_IMAGE_EMBEDDINGS e, query_vec q
WHERE COSINE_SIMILARITY(e.embedding_vector, q.vec) > 0.5
ORDER BY similarity DESC
LIMIT 10;
```

2. **Pre-filter by ghost type:**
```sql
WHERE ghost_type IN ('Orb', 'Apparition')
```

3. **Use clustering:**
```sql
-- Group by ghost_id first, then search within clusters
CALL GET_IMAGE_CLUSTERS(0.7);
```

---

## 📊 Expected Results

### **After Processing 50 Images:**

```sql
SELECT * FROM VW_IMAGE_SIMILARITY_STATS;
```

Expected:
- `TOTAL_EMBEDDINGS`: 50
- `UNIQUE_GHOSTS`: 10-15
- `UNIQUE_SIGHTINGS`: 40-50
- `AVG_CONFIDENCE`: 0.80-0.90
- `RECENT_EMBEDDINGS`: 50 (if just generated)

### **Search Quality:**

- **High similarity (>0.9):** Nearly identical images/descriptions
- **Medium similarity (0.7-0.9):** Related content
- **Low similarity (0.5-0.7):** Somewhat related
- **Very low (<0.5):** Different content

---

## 🎯 Success Criteria

✅ All functions created without errors
✅ `COSINE_SIMILARITY` returns values between 0 and 1
✅ Can generate embeddings successfully
✅ Search queries return results
✅ Views show statistics
✅ Streamlit app works

---

## 🚀 Next Steps

1. ✅ **Complete initial setup** (you've done this)
2. 🔄 **Generate embeddings** for all evidence
3. 🔍 **Test searches** in Streamlit app
4. 📊 **Review statistics** to understand data
5. 🎨 **Customize similarity thresholds** based on your needs
6. 📈 **Monitor performance** over time

---

## 📞 Support

If you encounter issues:

1. Check Snowflake version: `SELECT CURRENT_VERSION();`
2. Verify JavaScript enabled: `SHOW PARAMETERS LIKE 'JAVASCRIPT%';`
3. Review error messages carefully
4. Test with simple arrays first
5. Check that Cortex AI is enabled: `SHOW FUNCTIONS LIKE '%CORTEX%';`

---

## 🎉 You're All Set!

The image embeddings system is now fully operational with:
- ✅ Custom cosine similarity (works everywhere)
- ✅ AI-powered embeddings (Snowflake Arctic)
- ✅ Fast similarity search
- ✅ Comprehensive statistics
- ✅ Streamlit integration

**Start searching for similar ghost images now! 👻🔍**

