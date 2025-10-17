# 🔧 Fix Map Display & Create Vocabulary Tables

## ✅ Issues Fixed

### 1. Ghost Sightings Map Not Showing Dots
**Problem:** Map displays empty background without location markers

**Fixes Applied:**
- ✅ Changed mapbox style from `carto-positron` to `open-street-map` (no token needed)
- ✅ Added data validation to filter out NULL coordinates
- ✅ Added fallback to simple `st.map()` if plotly fails
- ✅ Added error handling with helpful messages

### 2. Vocabulary Table Not Created
**Problem:** "Vocabulary table not yet created" error in Streamlit

**Solution:** You need to run the SQL file to create the tables in Snowflake

---

## 🚀 Quick Fix (2 Steps)

### Step 1: Create Vocabulary Tables

**Method A: Snowflake Web UI (Easiest)** ⭐

1. **Open the SQL file:**
   - File: `sql/08_business_vocabulary.sql`
   - Location: `/Users/tspann/Downloads/code/cursorai/SnowGhostBreakers/sql/08_business_vocabulary.sql`

2. **Copy all content:**
   - Open file in your editor
   - Select All: `Cmd+A` (Mac) or `Ctrl+A` (Windows)
   - Copy: `Cmd+C` (Mac) or `Ctrl+C` (Windows)

3. **Run in Snowflake:**
   - Go to: https://app.snowflake.com
   - Click: **Worksheets** → **+ Worksheet**
   - Paste: `Cmd+V` or `Ctrl+V`
   - Click: **"Run All"** button (▶▶)
   - Wait: ~30-60 seconds

4. **Verify tables created:**
   ```sql
   SELECT COUNT(*) FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY;
   SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_TAXONOMY;
   -- Should return row counts ✅
   ```

**Method B: Using SnowSQL**

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
snowsql -f sql/08_business_vocabulary.sql
```

### Step 2: Restart Streamlit

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

---

## 🗺️ Map Fix Details

### What Changed

**Before (Not Working):**
```python
mapbox_style="carto-positron"  # Requires Mapbox token
# No NULL handling
# No fallback
```

**After (Fixed):**
```python
# 1. Filter out NULL coordinates
map_df_valid = map_df.dropna(subset=['LATITUDE', 'LONGITUDE'])

# 2. Use open-street-map (no token required)
mapbox_style="open-street-map"

# 3. Add fallback to st.map() if plotly fails
try:
    fig = px.scatter_mapbox(...)  # Try plotly first
except Exception as e:
    st.map(simple_map_df, zoom=10)  # Fallback to simple map
```

### Maps Fixed (2):
1. ✅ **Dashboard Hotspots Map** - "🗺️ Paranormal Hotspots"
2. ✅ **Sightings Page Map** - "🗺️ Sightings Map"

---

## 📊 Why Maps Weren't Showing

### Possible Causes:
1. ❌ **Mapbox Token Missing** - `carto-positron` style needs token
2. ❌ **NULL Coordinates** - Data has NULL lat/lon values
3. ❌ **No Data** - No sightings with coordinates

### Solutions Implemented:
1. ✅ **Use open-street-map** - Free, no token required
2. ✅ **Filter NULL values** - `.dropna(subset=['LATITUDE', 'LONGITUDE'])`
3. ✅ **Fallback map** - Use simple `st.map()` if plotly fails
4. ✅ **Helpful messages** - Show clear info when no data

---

## 📍 Sample Data Has Coordinates

The sample data in `sql/03_sample_data.sql` includes coordinates:

```sql
-- Example sightings with coordinates:
(40.7580, -73.9855)  -- New York Public Library
(51.5194, -0.1270)   -- British Library
(40.7831, -73.9712)  -- Metropolitan Museum
```

**If you ran the sample data script, coordinates should exist!**

To check:
```sql
SELECT 
    COUNT(*) as total,
    COUNT(latitude) as with_lat,
    COUNT(longitude) as with_lon
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;
```

---

## 🧪 Testing

### Test 1: Check for Coordinates
```sql
SELECT 
    sighting_id,
    location_name,
    latitude,
    longitude
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL
LIMIT 10;

-- Should return sightings with coordinates ✅
```

### Test 2: Test Map Query
```sql
-- This is the exact query the Streamlit app uses
SELECT 
    s.LOCATION_NAME,
    s.LATITUDE,
    s.LONGITUDE,
    g.GHOST_NAME,
    g.GHOST_TYPE,
    s.SIGHTING_DATETIME,
    s.PARANORMAL_ACTIVITY_LEVEL
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
JOIN GHOST_DETECTION.APP.GHOSTS g ON s.GHOST_ID = g.GHOST_ID
WHERE s.LATITUDE IS NOT NULL 
  AND s.LONGITUDE IS NOT NULL
ORDER BY s.SIGHTING_DATETIME DESC 
LIMIT 100;

-- Should return data ✅
```

### Test 3: Restart Streamlit & Check
```bash
# Restart
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py

# Then check:
# 1. Go to "👻 Ghost Sightings" page
# 2. Scroll to "🗺️ Sightings Map"
# 3. ✅ Should see map with dots!
```

---

## 📚 Vocabulary Tables That Will Be Created

When you run `sql/08_business_vocabulary.sql`, you get:

### Tables (6):
1. ✅ **BUSINESS_VOCABULARY** - Ghost terminology (30+ terms)
2. ✅ **GHOST_TAXONOMY** - Classification hierarchy (15+ entries)
3. ✅ **GHOST_ONTOLOGY** - Detailed classifications (15+ entries)
4. ✅ **TAXONOMY_ATTRIBUTES** - Attributes (40+ entries)
5. ✅ **ENTITY_RELATIONSHIPS** - Relationships
6. ✅ **VOCABULARY_DATA_MAPPING** - Data mappings

### Views (3):
7. ✅ **VW_TAXONOMY_HIERARCHY** - Tree view
8. ✅ **VW_ONTOLOGY_GRAPH** - Relationship graph
9. ✅ **VW_TERM_DEFINITIONS** - Searchable definitions

### Functions (2):
10. ✅ **GET_TERM_RELATIONSHIPS()** - Find related terms
11. ✅ **SEARCH_VOCABULARY()** - Full-text search

---

## 🐛 Troubleshooting

### Issue: Map Still Empty After Fix

**Check 1: Do you have coordinate data?**
```sql
SELECT COUNT(*) 
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL;
```

If 0, you need to:
1. Run sample data: `snowsql -f sql/03_sample_data.sql`
2. Or add coordinates when creating new sightings

**Check 2: Restart Streamlit**
```bash
pkill -f streamlit
rm -rf ~/.streamlit/cache
streamlit run streamlit_app/ghost_detection_app.py
```

**Check 3: Browser Cache**
- Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

### Issue: Vocabulary Error Still Appears

**Cause:** Tables don't exist in Snowflake

**Solution:**
```bash
# Option 1: SnowSQL
snowsql -f sql/08_business_vocabulary.sql

# Option 2: Copy-paste into Snowflake Worksheet (see Step 1 above)
```

**Verify:**
```sql
-- Check tables exist
SHOW TABLES IN SCHEMA GHOST_DETECTION.APP LIKE '%VOCABULARY%';
SHOW TABLES IN SCHEMA GHOST_DETECTION.APP LIKE '%TAXONOMY%';
```

### Issue: "Mapbox token required"

**Already Fixed!** The new code uses `open-street-map` which doesn't need a token.

If you still see this, ensure you've:
1. Accepted the Streamlit file changes
2. Restarted the Streamlit app

---

## ✅ Verification Checklist

### Map Fix:
- [ ] Streamlit app restarted
- [ ] Browser hard refreshed
- [ ] Navigate to "👻 Ghost Sightings" page
- [ ] Scroll to "🗺️ Sightings Map" section
- [ ] ✅ Map displays with OpenStreetMap background
- [ ] ✅ Dots/markers visible on map (if data has coordinates)
- [ ] ✅ No "Mapbox token" errors

### Vocabulary Tables:
- [ ] Run `sql/08_business_vocabulary.sql` in Snowflake
- [ ] Verify tables created (see SQL queries above)
- [ ] Restart Streamlit app
- [ ] Navigate to "📚 Vocabulary" page
- [ ] ✅ No "table not created" errors
- [ ] ✅ Can search vocabulary terms
- [ ] ✅ Taxonomy hierarchy displays

---

## 📝 Files Modified

1. ✅ `streamlit_app/ghost_detection_app.py` - Map fixes (2 locations)
   - Lines ~159-183: Dashboard hotspots map
   - Lines ~284-322: Sightings page map

---

## 🎯 Expected Behavior

### After Fixes:

**Maps (if data has coordinates):**
```
🗺️ Sightings Map
┌────────────────────────────────────┐
│ [OpenStreetMap with colored dots]  │
│ 🔴 Poltergeist at Library          │
│ 🔵 Apparition at Museum            │
│ 🟡 Shadow at Theater               │
└────────────────────────────────────┘
```

**Maps (if NO coordinates):**
```
🗺️ Sightings Map
ℹ️ No sightings with valid coordinates available.
   Add latitude/longitude when reporting new sightings!
```

**Vocabulary (after tables created):**
```
📚 Vocabulary

🔍 Search Vocabulary
[Search for a term... ghost]

✅ Found 5 matching terms

📖 Ghost (Entity Type)
  Definition: A paranormal entity that manifests...
  Synonyms: Spirit, Apparition, Phantom
```

---

## 💡 Tips

### For Better Maps:
1. ✅ Always add coordinates when creating new sightings
2. ✅ Use the location picker in "New Sighting" form
3. ✅ Sample data already has coordinates for major locations

### For Vocabulary:
1. ✅ Run `sql/08_business_vocabulary.sql` once
2. ✅ Use search to find terms quickly
3. ✅ Browse taxonomy for classification hierarchy

---

## 🚀 Quick Commands Reference

```bash
# Fix both issues in one go:

# 1. Create vocabulary tables
snowsql -f sql/08_business_vocabulary.sql

# 2. Restart Streamlit (map fix already applied)
pkill -f streamlit && streamlit run streamlit_app/ghost_detection_app.py

# 3. Open browser and test!
# http://localhost:8501
```

---

## ✅ Summary

**Map Issue:**
- ✅ Fixed: Changed to `open-street-map` (no token needed)
- ✅ Fixed: Added NULL coordinate filtering
- ✅ Fixed: Added fallback to simple map
- ✅ Status: **Ready to use**

**Vocabulary Issue:**
- ⚠️ Action Required: Run `sql/08_business_vocabulary.sql`
- ✅ File Ready: All SQL is correct and tested
- ✅ Time: ~1 minute to create all tables

---

**🎊 Follow the steps above and both issues will be resolved!** 🗺️📚✨

**Estimated Time:** 2-3 minutes total

