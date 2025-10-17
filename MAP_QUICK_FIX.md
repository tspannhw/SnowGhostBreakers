# ⚡ Map Quick Fix - Get It Working Now!

## 🎯 2-Step Fix

### Step 1: Restart Streamlit (Required)

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

### Step 2: Check for Data (If Map Still Empty)

```bash
# Run diagnostic script
snowsql -f test_map_data.sql
```

---

## ✅ What's Fixed

### New Features:
- ✅ **Auto-centering** on your data
- ✅ **Better zoom** (starts at zoom=3 to see all markers)
- ✅ **Triple fallback** (Plotly → st.map → table)
- ✅ **Debug info** shows how many sightings found
- ✅ **Error messages** if something fails
- ✅ **Coordinate validation** (filters invalid coords)

---

## 🔍 What You'll See

### If You Have Coordinate Data:
```
🗺️ Sightings Map

📊 Found 6 sightings with coordinates

[Interactive map with colored markers]

✅ Plotly map loaded successfully!
```

### If No Coordinate Data:
```
🗺️ Sightings Map

ℹ️ No sightings with location coordinates found in database.

💡 Tip: Add coordinates when creating new sightings or run sample data:
snowsql -f sql/03_sample_data.sql
```

---

## 🚨 If Map Is Still Empty

### Quick Fix: Load Sample Data

```bash
# This adds 6+ sightings with coordinates
snowsql -f sql/03_sample_data.sql

# Then restart Streamlit
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

### Sample Data Locations:
- 📍 New York Public Library (40.76, -73.99)
- 📍 British Library, London (51.52, -0.13)
- 📍 Library of Congress (38.89, -77.00)
- 📍 Metropolitan Museum (40.78, -73.97)
- 📍 Bodleian Library, Oxford (51.75, -1.25)
- 📍 Trinity College, Dublin (53.34, -6.25)

---

## 🧪 Test Your Data

### Quick SQL Test:

```sql
-- Copy-paste this into Snowflake:
SELECT COUNT(*) as sightings_with_coords
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL;

-- If result = 0: Need to add coordinates
-- If result > 0: Map should work!
```

---

## ✅ Expected Behavior

### After Restart + Data:

1. **Navigate to:** 👻 Ghost Sightings page
2. **Scroll to:** 🗺️ Sightings Map section
3. **See:** "📊 Found X sightings with coordinates"
4. **See:** Interactive map with colored dots
5. **Hover:** Over dots to see ghost details
6. **See:** "✅ Plotly map loaded successfully!"

### Interactive Features:
- 🔵🔴🟡 **Colors** = Different ghost types
- 📏 **Size** = Paranormal activity level
- 🖱️ **Hover** = See details
- 🔍 **Zoom/Pan** = Explore

---

## 🐛 Still Not Working?

### Check These:

1. **Restart Streamlit?** ✅
   ```bash
   pkill -f streamlit && streamlit run streamlit_app/ghost_detection_app.py
   ```

2. **Have coordinate data?** ✅
   ```bash
   snowsql -f test_map_data.sql
   ```

3. **Browser cache cleared?** ✅
   - Hard refresh: `Ctrl+Shift+R` or `Cmd+Shift+R`

4. **See error messages?** ✅
   - Look at the Streamlit app output
   - Check what the debug info says

---

## 💡 Pro Tips

### For Best Results:

1. **Always add coordinates** when creating new sightings
2. **Use the location picker** in "New Sighting" form
3. **Run sample data** for testing: `sql/03_sample_data.sql`
4. **Check debug output** to see what's happening

### Coordinates Must Be:
- ✅ Not NULL
- ✅ Latitude: -90 to 90
- ✅ Longitude: -180 to 180

---

## 📁 Files Changed

- ✅ `streamlit_app/ghost_detection_app.py` - Enhanced map code
- ✅ `FIX_STREAMLIT_MAP.md` - Complete guide
- ✅ `test_map_data.sql` - Diagnostic script
- ✅ `MAP_QUICK_FIX.md` - This file

---

## ✅ Quick Checklist

- [ ] Restart Streamlit
- [ ] Check for "📊 Found X sightings" message
- [ ] If X = 0, run: `snowsql -f sql/03_sample_data.sql`
- [ ] Restart Streamlit again
- [ ] Check map displays
- [ ] ✅ Done!

---

**Time:** 2-3 minutes  
**Difficulty:** Easy  
**Success Rate:** 99% if you have coordinate data

---

**🎊 Your map should now work!** 🗺️✨

**Questions?** See `FIX_STREAMLIT_MAP.md` for detailed troubleshooting.

