# 🔧 FIND_SIMILAR_IMAGES Troubleshooting

## ✅ FIXED: WITH Clause Syntax Error

**Issue:** `Syntax error: unexpected 'WITH'. (line 137)`

**Solution:** For Snowflake table-valued functions, don't use WITH clauses or outer parentheses. Use direct SELECT statements instead.

**Status:** ✅ **RESOLVED** - All functions have been rewritten without WITH clauses

See `IMAGE_EMBEDDINGS_WITH_CLAUSE_FIX.md` for details.

---

## Common Errors & Fixes

### **Issue 1: VECTOR Type Not Supported**

**Error:** `SQL compilation error: Unknown data type VECTOR`

**Fix:** Use ARRAY instead of VECTOR casting

**Original:**
```sql
VECTOR_COSINE_SIMILARITY(
    e.embedding_vector::VECTOR(FLOAT, 1024),
    q.query_vector::VECTOR(FLOAT, 1024)
)
```

**Fixed:**
```sql
VECTOR_COSINE_SIMILARITY(
    e.embedding_vector,
    q.query_vector
)
```

---

### **Issue 2: Function Not Found**

**Error:** `SQL compilation error: Unknown function VECTOR_COSINE_SIMILARITY`

**Fix:** Use manual cosine similarity calculation

**Replace with:**
```sql
-- Manual cosine similarity
(
    SELECT SUM(a * b) / (
        SQRT(SUM(a * a)) * SQRT(SUM(b * b))
    )
    FROM (
        SELECT 
            e.embedding_vector[i]::FLOAT AS a,
            q.query_vector[i]::FLOAT AS b
        FROM TABLE(FLATTEN(ARRAY_GENERATE_RANGE(0, 1024))) AS idx(i)
    )
) AS similarity_score
```

---

### **Issue 3: AI_EMBED Not Available**

**Error:** `SQL compilation error: Unknown function SNOWFLAKE.CORTEX.AI_EMBED`

**Possible causes:**
- Cortex AI not enabled in your account
- Wrong function name
- Insufficient privileges

**Check:**
```sql
-- Check if Cortex is available
SHOW FUNCTIONS LIKE '%EMBED%';

-- Alternative: Use SNOWFLAKE.CORTEX.EMBED_TEXT_768
SELECT SNOWFLAKE.CORTEX.EMBED_TEXT_768('mistral-embed', 'test text');
```

---

### **Issue 4: Table Doesn't Exist**

**Error:** `SQL compilation error: Object 'GHOST_IMAGE_EMBEDDINGS' does not exist`

**Fix:** Create the table first
```sql
-- Run the full setup script
SOURCE sql/14_image_embeddings_table.sql;
```

---

## 🔧 Alternative Implementation

If the VECTOR functions don't work, use this simplified version:

```sql
CREATE OR REPLACE FUNCTION FIND_SIMILAR_IMAGES_SIMPLE(
    query_text VARCHAR,
    top_k INT
)
RETURNS TABLE (
    embedding_id VARCHAR,
    evidence_id VARCHAR,
    ghost_id VARCHAR,
    image_description TEXT,
    similarity_score FLOAT,
    image_path VARCHAR,
    ai_description TEXT
)
AS
$$
(
    SELECT 
        e.embedding_id,
        e.evidence_id,
        e.ghost_id,
        e.image_description,
        -- Simple similarity: just use text matching for now
        CASE 
            WHEN LOWER(e.image_description) LIKE LOWER('%' || query_text || '%') THEN 1.0
            ELSE 0.5
        END AS similarity_score,
        e.image_path,
        e.ai_description
    FROM GHOST_IMAGE_EMBEDDINGS e
    WHERE LOWER(e.image_description) LIKE LOWER('%' || query_text || '%')
    ORDER BY similarity_score DESC
    LIMIT top_k
)
$$;
```

---

## 🧪 Test Queries

### **Test 1: Check if function exists**
```sql
SHOW USER FUNCTIONS LIKE 'FIND_SIMILAR%';
```

### **Test 2: Check if table exists**
```sql
DESC TABLE GHOST_DETECTION.APP.GHOST_IMAGE_EMBEDDINGS;
```

### **Test 3: Check if embeddings exist**
```sql
SELECT COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_IMAGE_EMBEDDINGS;
```

### **Test 4: Try calling the function**
```sql
SELECT * FROM TABLE(
    GHOST_DETECTION.APP.FIND_SIMILAR_IMAGES('test', 5)
);
```

---

## 📋 What to Provide

To help fix your specific error, please provide:

1. **Complete error message**
2. **Snowflake version:** `SELECT CURRENT_VERSION();`
3. **Cortex availability:** `SHOW FUNCTIONS LIKE '%CORTEX%';`
4. **Table status:** `DESC TABLE GHOST_IMAGE_EMBEDDINGS;`

---

## 🔄 Quick Fixes

### **Fix 1: Remove VECTOR Casting**

If you get VECTOR type errors, edit the function:

```sql
-- Change line 166-167 from:
e.embedding_vector::VECTOR(FLOAT, 1024),
q.query_vector::VECTOR(FLOAT, 1024)

-- To:
e.embedding_vector,
q.query_vector
```

### **Fix 2: Use Alternative Similarity**

If VECTOR_COSINE_SIMILARITY doesn't exist:

```sql
-- Replace VECTOR_COSINE_SIMILARITY with:
ARRAY_INNER_PRODUCT(e.embedding_vector, q.query_vector) /
(ARRAY_SIZE(e.embedding_vector) * ARRAY_SIZE(q.query_vector))
```

---

## 📝 Provide Your Error

Please paste the full error message here so I can provide a specific fix:

```
Error line:
Error code:
Error message:
```

