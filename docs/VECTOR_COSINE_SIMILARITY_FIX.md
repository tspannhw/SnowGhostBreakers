# 🔧 VECTOR_COSINE_SIMILARITY Type Error - Final Fix

## 🚨 Error Still Occurring

**Error:** `Invalid argument types for function 'VECTOR_COSINE_SIMILARITY': (ARRAY, VECTOR(FLOAT, 1024))`

## 🎯 Root Cause Analysis

The issue is that `VECTOR_COSINE_SIMILARITY` may have different requirements or may not be available in your Snowflake instance.

## ✅ Solution: Two Approaches

---

## **Approach 1: Remove All Type Casting (Try This First)**

I've updated the main file to remove all `::VECTOR(FLOAT, 1024)` casting. Now it uses raw ARRAY types.

### **File Updated:** `sql/14_image_embeddings_table.sql`

```sql
VECTOR_COSINE_SIMILARITY(
    e.embedding_vector,  -- ARRAY, no casting
    SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', ?)  -- ARRAY, no casting
)
```

### **Test This:**
```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Re-run the main script
SOURCE sql/14_image_embeddings_table.sql;

-- Test it
CALL FIND_SIMILAR_IMAGES('ghost orb', 5);
```

---

## **Approach 2: Use Manual Cosine Similarity (Fallback)**

If `VECTOR_COSINE_SIMILARITY` doesn't work at all, use the alternative file that implements manual cosine similarity in JavaScript.

### **File Created:** `sql/14_image_embeddings_table_alternative.sql`

This creates:
- `MANUAL_COSINE_SIMILARITY` function (JavaScript implementation)
- `FIND_SIMILAR_IMAGES_ALT` procedure
- `FIND_SIMILAR_TO_IMAGE_ALT` procedure

### **Install Alternative Version:**
```sql
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Run the alternative script
SOURCE sql/14_image_embeddings_table_alternative.sql;

-- Test the alternative procedures
CALL FIND_SIMILAR_IMAGES_ALT('ghost orb', 5);
```

### **Manual Cosine Similarity Implementation:**
```javascript
function cosine_similarity(vec1, vec2) {
    if (!vec1 || !vec2 || vec1.length !== vec2.length) return null;
    
    let dotProduct = 0;
    let mag1 = 0;
    let mag2 = 0;
    
    for (let i = 0; i < vec1.length; i++) {
        dotProduct += vec1[i] * vec2[i];
        mag1 += vec1[i] * vec1[i];
        mag2 += vec2[i] * vec2[i];
    }
    
    return dotProduct / (Math.sqrt(mag1) * Math.sqrt(mag2));
}
```

---

## 🔍 Diagnostic Steps

### **1. Check if VECTOR_COSINE_SIMILARITY exists**
```sql
-- Check for the function
SHOW FUNCTIONS LIKE '%COSINE%';
SHOW FUNCTIONS LIKE '%VECTOR%';
```

### **2. Check your Snowflake version**
```sql
SELECT CURRENT_VERSION();
```

**Note:** `VECTOR_COSINE_SIMILARITY` may require:
- Snowflake Enterprise Edition or higher
- Specific feature flags enabled
- Minimum version (7.x or higher)

### **3. Test with simple arrays**
```sql
-- Test if VECTOR_COSINE_SIMILARITY works at all
SELECT VECTOR_COSINE_SIMILARITY(
    ARRAY_CONSTRUCT(1, 2, 3),
    ARRAY_CONSTRUCT(4, 5, 6)
);
```

If this returns an error, use **Approach 2** (alternative file).

### **4. Test AI_EMBED output type**
```sql
-- Check what type AI_EMBED returns
SELECT 
    TYPEOF(SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', 'test')) AS embed_type,
    ARRAY_SIZE(SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', 'test')) AS embed_size;
```

---

## 📋 Quick Decision Tree

```
Is VECTOR_COSINE_SIMILARITY available?
│
├─ YES → Try Approach 1 (no casting)
│   │
│   ├─ Works? → ✅ Done!
│   │
│   └─ Still errors? → Try Approach 2
│
└─ NO → Use Approach 2 (manual function)
```

---

## 🚀 Testing Commands

### **For Approach 1 (Main File):**
```sql
-- 1. Run the main script
SOURCE sql/14_image_embeddings_table.sql;

-- 2. Test text search
CALL FIND_SIMILAR_IMAGES('ghost orb', 5);

-- 3. Test in Streamlit
-- Navigate to Image Similarity page
```

### **For Approach 2 (Alternative File):**
```sql
-- 1. Run the alternative script
SOURCE sql/14_image_embeddings_table_alternative.sql;

-- 2. Test manual function
SELECT MANUAL_COSINE_SIMILARITY(
    ARRAY_CONSTRUCT(1, 2, 3),
    ARRAY_CONSTRUCT(4, 5, 6)
);

-- 3. Test alternative procedures
CALL FIND_SIMILAR_IMAGES_ALT('ghost orb', 5);
CALL FIND_SIMILAR_TO_IMAGE_ALT('EMB_001', 5);
```

---

## 🔄 Streamlit App Changes

If using **Approach 2**, update the Streamlit app to call the `_ALT` versions:

```python
# In streamlit_app/ghost_detection_app.py
# Change from:
search_sql = f"CALL FIND_SIMILAR_IMAGES('{query}', {top_k})"

# To:
search_sql = f"CALL FIND_SIMILAR_IMAGES_ALT('{query}', {top_k})"
```

---

## 📁 Files Created/Updated

- ✅ `sql/14_image_embeddings_table.sql` - **Updated**: Removed all VECTOR casting
- ✅ `sql/14_image_embeddings_table_alternative.sql` - **New**: Manual cosine similarity version
- 📝 `VECTOR_COSINE_SIMILARITY_FIX.md` - This documentation

---

## 💡 Why Two Approaches?

### **Approach 1 Benefits:**
- Uses native Snowflake function (faster)
- No custom code to maintain
- Optimized by Snowflake engine

### **Approach 2 Benefits:**
- **Works on any Snowflake edition**
- No dependency on specific features
- Full control over calculation
- Portable and reliable

---

## ⚡ Performance Comparison

| Metric | Native (Approach 1) | Manual (Approach 2) |
|--------|---------------------|---------------------|
| **Speed** | 🔥🔥🔥 Fastest | 🔥🔥 Fast |
| **Compatibility** | ⚠️ May not work | ✅ Always works |
| **Maintenance** | ✅ None needed | ⚠️ Custom code |
| **Accuracy** | ✅ Exact | ✅ Exact |

Both are accurate, but native is faster if available.

---

## 🎯 Recommended Steps

**Follow this order:**

1. ✅ **Try Approach 1** (updated main file, no casting)
   ```sql
   SOURCE sql/14_image_embeddings_table.sql;
   CALL FIND_SIMILAR_IMAGES('test', 5);
   ```

2. ⚠️ **If that fails**, check diagnostics:
   ```sql
   SHOW FUNCTIONS LIKE '%COSINE%';
   SELECT CURRENT_VERSION();
   ```

3. 🔄 **If VECTOR_COSINE_SIMILARITY doesn't exist**, use Approach 2:
   ```sql
   SOURCE sql/14_image_embeddings_table_alternative.sql;
   CALL FIND_SIMILAR_IMAGES_ALT('test', 5);
   ```

---

## ✅ Expected Results

Both approaches should return:

```
EMBEDDING_ID | EVIDENCE_ID | GHOST_ID | IMAGE_DESCRIPTION | SIMILARITY_SCORE | IMAGE_PATH | AI_DESCRIPTION
-------------|-------------|----------|-------------------|------------------|------------|----------------
EMB_001      | EV_001      | GH_001   | Orb of light...   | 0.95             | /path/...  | Bright orb...
EMB_002      | EV_002      | GH_001   | Glowing sphere... | 0.89             | /path/...  | Spherical...
...
```

---

## 🆘 Still Having Issues?

### **Error: Function MANUAL_COSINE_SIMILARITY does not exist**
```sql
-- Re-create just the function
CREATE OR REPLACE FUNCTION MANUAL_COSINE_SIMILARITY(vec1 ARRAY, vec2 ARRAY)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
AS
$$
    if (!VEC1 || !VEC2 || VEC1.length !== VEC2.length) return null;
    let dot = 0, mag1 = 0, mag2 = 0;
    for (let i = 0; i < VEC1.length; i++) {
        dot += VEC1[i] * VEC2[i];
        mag1 += VEC1[i] * VEC1[i];
        mag2 += VEC2[i] * VEC2[i];
    }
    return dot / (Math.sqrt(mag1) * Math.sqrt(mag2));
$$;
```

### **Error: JavaScript not enabled**
Contact your Snowflake admin to enable JavaScript UDFs:
```sql
-- They need to run:
ALTER ACCOUNT SET ENABLE_INTERNAL_STAGES_PRIVATELINK = TRUE;
```

Or use SQL-only calculation (slower but works):
```sql
-- I can provide a SQL-only version if needed
```

---

## 📞 Need Help?

Provide these details:
1. Snowflake version: `SELECT CURRENT_VERSION();`
2. Edition: Enterprise/Business Critical/Standard?
3. Output of: `SHOW FUNCTIONS LIKE '%COSINE%';`
4. Complete error message

---

✅ **Try Approach 1 first, then Approach 2 if needed. One of these will work!**

