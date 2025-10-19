# ✅ Run Vocabulary Setup - UPDATED FILE

## 🎯 The file has been FIXED!

**What was added:**
- ✅ GHOST_TAXONOMY table (was missing)
- ✅ 15+ taxonomy records with full hierarchy
- ✅ 5 classification levels (Kingdom → Species)

---

## 🚀 Quick Setup (Copy-Paste Method)

### Step 1: Open the UPDATED SQL File
```
File: sql/08_business_vocabulary.sql
Location: /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers/sql/08_business_vocabulary.sql
```

### Step 2: Copy Everything
- Open the file in your editor
- **Select All:** `Cmd+A` (Mac) or `Ctrl+A` (Windows)
- **Copy:** `Cmd+C` (Mac) or `Ctrl+C` (Windows)

### Step 3: Go to Snowflake Web UI
1. Visit: https://app.snowflake.com
2. Login to your account
3. Click **"Worksheets"** in the left menu
4. Click **"+ Worksheet"** button

### Step 4: Paste and Run
1. **Paste** the SQL: `Cmd+V` or `Ctrl+V`
2. Click **"Run All"** button (▶▶) at the top
3. Wait ~30-60 seconds for completion

### Step 5: Verify Tables Created
Copy-paste this verification query:

```sql
-- Check all tables were created
SELECT 'BUSINESS_VOCABULARY' as table_name, COUNT(*) as rows 
FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY
UNION ALL
SELECT 'GHOST_TAXONOMY', COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_TAXONOMY
UNION ALL
SELECT 'GHOST_ONTOLOGY', COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_ONTOLOGY
UNION ALL
SELECT 'TAXONOMY_ATTRIBUTES', COUNT(*) 
FROM GHOST_DETECTION.APP.TAXONOMY_ATTRIBUTES;

-- Expected results:
-- BUSINESS_VOCABULARY: 30+ rows ✅
-- GHOST_TAXONOMY: 15+ rows ✅  
-- GHOST_ONTOLOGY: 15+ rows ✅
-- TAXONOMY_ATTRIBUTES: 40+ rows ✅
```

### Step 6: Restart Streamlit
```bash
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

### Step 7: Test in Streamlit App
1. Open: http://localhost:8501
2. Go to: **📚 Vocabulary** page
3. ✅ No more "table not created" errors!
4. Search for: "ghost"
5. ✅ Should show taxonomy hierarchy

---

## 📊 What Gets Created

### Tables (5):
1. ✅ **BUSINESS_VOCABULARY** - Ghost terminology (30+ terms)
2. ✅ **GHOST_TAXONOMY** - Classification hierarchy (15+ entries) ← NEW!
3. ✅ **GHOST_ONTOLOGY** - Detailed classifications (15+ entries)
4. ✅ **TAXONOMY_ATTRIBUTES** - Attributes (40+ entries)
5. ✅ **ENTITY_RELATIONSHIPS** - Relationships
6. ✅ **VOCABULARY_DATA_MAPPING** - Data mappings

### Ghost Taxonomy Hierarchy (NEW):
```
Level 1 (Kingdom): Paranormal Entities
├── Level 2 (Class): Spectral Entities
│   ├── Level 3 (Order): Interactive Spirits
│   │   └── Level 4 (Family): Apparitions
│   │       ├── Level 5 (Species): Full Body Apparition
│   │       └── Level 5 (Species): Partial Apparition
│   ├── Level 3 (Order): Residual Imprints
│   │   └── Level 5 (Species): Residual Haunt
│   └── Level 3 (Order): Malevolent Entities
│       ├── Level 4 (Family): Poltergeists
│       │   └── Level 5 (Species): Class IV Full-Roaming Vapor
│       ├── Level 4 (Family): Shadow Figures
│       └── Level 5 (Species): Demon Entity
├── Level 2 (Class): Non-Human Entities
└── Level 2 (Class): Energy Phenomena
    └── Level 4 (Family): Orbs
```

### Views (3):
- ✅ VW_TAXONOMY_HIERARCHY
- ✅ VW_ONTOLOGY_GRAPH  
- ✅ VW_TERM_DEFINITIONS

### Functions (2):
- ✅ GET_TERM_RELATIONSHIPS()
- ✅ SEARCH_VOCABULARY()

---

## ✅ Success Indicators

After running, you should see in Streamlit:

### ❌ Before (Error):
```
Taxonomy table not yet created. Run: sql/08_business_vocabulary.sql
Vocabulary table not yet created. Run: sql/08_business_vocabulary.sql
```

### ✅ After (Working):
```
📚 Vocabulary

🔍 Browse Terms
- Apparition
- Poltergeist
- EMF Reading
- ...

🌳 Ghost Taxonomy
Level 1: Paranormal Entities
  Level 2: Spectral Entities
    Level 3: Interactive Spirits
      ...
```

---

## 🐛 Troubleshooting

### Error: "Database does not exist"
```sql
-- Run this FIRST, then run main SQL:
CREATE DATABASE IF NOT EXISTS GHOST_DETECTION;
CREATE SCHEMA IF NOT EXISTS GHOST_DETECTION.APP;
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;
```

### Error: "Still shows table not created"
```bash
# Clear Streamlit cache
pkill -f streamlit
rm -rf ~/.streamlit/cache
streamlit run streamlit_app/ghost_detection_app.py

# Hard refresh browser: Cmd+Shift+R or Ctrl+Shift+R
```

### Error: "Syntax error in INSERT"
```
Make sure you:
1. Copied the ENTIRE file
2. Didn't accidentally modify it
3. Pasted into a FRESH worksheet
4. Used "Run All" not just "Run"
```

---

## ⏱️ Time Estimate

- **Copy file:** 5 seconds
- **Paste in Snowflake:** 5 seconds  
- **Execution:** 30-60 seconds
- **Restart Streamlit:** 10 seconds
- **Total:** ~1-2 minutes

---

## 🎯 What Changed

**Original Issue:**
- SQL file was missing GHOST_TAXONOMY table
- Streamlit app expected GHOST_TAXONOMY but it didn't exist

**Fix Applied:**
- ✅ Added GHOST_TAXONOMY table definition
- ✅ Added 15+ taxonomy records with INSERT statements
- ✅ Includes all 5 classification levels
- ✅ Complete hierarchy from Kingdom to Species

**File Updated:**
- `sql/08_business_vocabulary.sql` (NOW 560+ lines)

---

## 📋 Quick Checklist

- [ ] Open `sql/08_business_vocabulary.sql`
- [ ] Copy all content (Cmd+A, Cmd+C)
- [ ] Go to Snowflake Worksheets
- [ ] Create new worksheet
- [ ] Paste SQL (Cmd+V)
- [ ] Click "Run All" (▶▶)
- [ ] Wait for completion (~30-60 sec)
- [ ] Run verification query
- [ ] Restart Streamlit
- [ ] Test Vocabulary page
- [ ] ✅ Done!

---

**🎊 Ready to run! The file is now complete with GHOST_TAXONOMY!** 📋✨

**Total Time:** 1-2 minutes  
**Difficulty:** Easy  
**Method:** Copy-Paste  

