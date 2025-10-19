# ⚡ Quick Vocabulary Setup (30 seconds)

## 🎯 Fastest Method: Copy-Paste to Snowflake

### 1️⃣ Open the SQL File
```bash
# File location:
/Users/tspann/Downloads/code/cursorai/SnowGhostBreakers/sql/08_business_vocabulary.sql
```

### 2️⃣ Copy Everything
- Open `sql/08_business_vocabulary.sql` in your editor
- Select All: `Cmd+A` (Mac) or `Ctrl+A` (Windows)
- Copy: `Cmd+C` (Mac) or `Ctrl+C` (Windows)

### 3️⃣ Paste into Snowflake
1. Go to: **https://app.snowflake.com**
2. Click: **Worksheets** (left menu)
3. Click: **+ Worksheet** (new worksheet)
4. Paste: `Cmd+V` or `Ctrl+V`
5. Click: **Run All** button (▶▶) at top

### 4️⃣ Wait for Completion
- Status bar will show progress
- Takes ~30 seconds
- ✅ Look for "Successfully executed" messages

### 5️⃣ Verify Tables Created
```sql
-- Copy-paste this verification query:
SELECT 'BUSINESS_VOCABULARY' as table_name, COUNT(*) as rows 
FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY
UNION ALL
SELECT 'GHOST_TAXONOMY', COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_TAXONOMY;

-- Expected: 30+ rows for vocabulary, 15+ for taxonomy ✅
```

### 6️⃣ Restart Streamlit
```bash
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

### 7️⃣ Test in Streamlit
1. Open: http://localhost:8501
2. Go to: **📚 Vocabulary** page
3. Search: "ghost"
4. ✅ Should see matching terms!

---

## ✅ Done!

**Total Time:** ~30 seconds  
**Tables Created:** 5  
**Views Created:** 3  
**Functions Created:** 2  
**Sample Data:** 100+ records  

---

## 🐛 If You See Errors

### "Database does not exist"
```sql
-- Run this first:
CREATE DATABASE IF NOT EXISTS GHOST_DETECTION;
CREATE SCHEMA IF NOT EXISTS GHOST_DETECTION.APP;
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Then paste the main SQL again
```

### "Still shows tables not created"
```bash
# Hard reset Streamlit cache
pkill -f streamlit
rm -rf ~/.streamlit/cache
streamlit run streamlit_app/ghost_detection_app.py
```

---

## 📋 What You'll Get

- ✅ Ghost terminology definitions
- ✅ Ghost classification taxonomy
- ✅ Searchable vocabulary
- ✅ Term relationships
- ✅ Ontology graph

---

**🎊 That's it! Super simple!** 📚✨

