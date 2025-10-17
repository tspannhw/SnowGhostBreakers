# 🗺️ Fix Streamlit Map Display Issues

## ✅ Issue Fixed - Enhanced Map with Debug Info

**Problem:** Carto map showing empty/white background in Streamlit  
**Status:** ✅ **Fixed with multiple fallbacks and debugging**

---

## 🔧 What Was Fixed

### Improvements Made:

1. ✅ **Better coordinate validation**
   - Added range checks: lat (-90 to 90), lon (-180 to 180)
   - Filter NULL and invalid coordinates

2. ✅ **Auto-centering**
   - Map now centers on average of all coordinates
   - Starts zoomed out (zoom=3) to show all markers

3. ✅ **Triple fallback system**
   - **Method 1:** Plotly scatter_mapbox with open-street-map
   - **Method 2:** Streamlit's built-in st.map()
   - **Method 3:** Table display of coordinates

4. ✅ **Debug information**
   - Shows count of sightings found
   - Displays error messages if map fails
   - Provides helpful tips

5. ✅ **Error handling**
   - Catches and displays all errors
   - Provides actionable troubleshooting steps

---

## 🚀 Quick Fix (Restart Streamlit)

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers

# Kill any running Streamlit instance
pkill -f streamlit

# Clear cache
rm -rf ~/.streamlit/cache

# Restart with updated code
streamlit run streamlit_app/ghost_detection_app.py
```

---

## 🧪 Test If You Have Coordinate Data

### Test 1: Check for coordinates in database

```sql
-- Run this in Snowflake to check your data
SELECT 
    COUNT(*) as total_sightings,
    COUNT(latitude) as with_latitude,
    COUNT(longitude) as with_longitude,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_both
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;

-- Expected: with_both > 0 for map to work
```

### Test 2: View actual coordinates

```sql
-- See what coordinates you have
SELECT 
    sighting_id,
    location_name,
    latitude,
    longitude,
    sighting_datetime
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL
ORDER BY sighting_datetime DESC
LIMIT 10;

-- Should show actual lat/lon values
```

---

## 🎯 What You'll See After Fix

### If Data Exists:
```
🗺️ Sightings Map

📊 Found 15 sightings with coordinates

[Interactive map with colored markers showing ghost sightings]

✅ Plotly map loaded successfully!
```

### If No Data:
```
🗺️ Sightings Map

ℹ️ No sightings with location coordinates found in database.

💡 Tip: Add coordinates when creating new sightings or run sample data:
snowsql -f sql/03_sample_data.sql
```

### If Map Has Issues:
```
🗺️ Sightings Map

📊 Found 15 sightings with coordinates

⚠️ Plotly map error: [error message]
🔄 Trying alternative map method...

📍 Sighting Locations:
[Simple Streamlit map displays]

✅ Simple map loaded!
```

---

## 🔍 Diagnostic Checklist

### Check 1: Do you have sample data?

```bash
# Load sample data (includes coordinates)
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
snowsql -f sql/03_sample_data.sql
```

Sample data includes sightings at:
- New York Public Library (40.7580, -73.9855)
- British Library, London (51.5194, -0.1270)
- Library of Congress (38.8889, -77.0047)
- And more...

### Check 2: Is Plotly installed?

```python
# In Python/Streamlit, check:
import plotly
print(f"Plotly version: {plotly.__version__}")
# Should be >= 5.0.0
```

### Check 3: Browser console errors?

1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for JavaScript errors
4. Common issues:
   - "mapbox" errors → Fixed by using open-street-map
   - Network errors → Check firewall/proxy

---

## 📊 Sample Data Coordinates

The sample data (`sql/03_sample_data.sql`) includes these locations:

```sql
-- New York Public Library
INSERT INTO GHOST_SIGHTINGS (..., latitude, longitude) 
VALUES (..., 40.7580, -73.9855);

-- British Library, London
VALUES (..., 51.5194, -0.1270);

-- Metropolitan Museum of Art
VALUES (..., 40.7831, -73.9712);

-- Library of Congress, DC
VALUES (..., 38.8889, -77.0047);

-- Bodleian Library, Oxford
VALUES (..., 51.7548, -1.2544);

-- Trinity College Library, Dublin
VALUES (..., 53.3439, -6.2546);
```

**If you've run sample data, you should have 6+ sightings with coordinates!**

---

## 🐛 Common Issues & Solutions

### Issue 1: "Map is white/empty"

**Cause:** No data with coordinates  
**Solution:**
```bash
# Run sample data
snowsql -f sql/03_sample_data.sql

# Or add coordinates to existing sightings
UPDATE GHOST_SIGHTINGS 
SET latitude = 40.7580, longitude = -73.9855
WHERE sighting_id = 'SIGHT001';
```

### Issue 2: "Found 0 sightings with coordinates"

**Cause:** Sightings exist but have NULL coordinates  
**Check:**
```sql
SELECT COUNT(*) FROM GHOST_SIGHTINGS WHERE latitude IS NULL;
```

**Solution:** Add coordinates when creating new sightings or update existing ones

### Issue 3: "Plotly map error"

**Cause:** Plotly issue or configuration  
**Solution:** App now automatically falls back to simple map

### Issue 4: Map shows but markers aren't visible

**Possible causes:**
1. **Coordinates out of range** → Now filtered (lat: -90 to 90, lon: -180 to 180)
2. **Zoom too high** → Now starts at zoom=3
3. **No centering** → Now auto-centers on data

### Issue 5: "Carto-positron requires token"

**Solution:** Already fixed! Now uses `open-street-map` (no token required)

---

## 💡 Troubleshooting Steps

### Step 1: Check Streamlit app output

Look for these messages:
```
📊 Found X sightings with coordinates
```

- If X = 0: No coordinate data
- If X > 0: Data exists, check map display

### Step 2: Check browser console

1. Press F12 (open DevTools)
2. Look for errors
3. Common fixes:
   - Refresh page (Ctrl+R)
   - Hard refresh (Ctrl+Shift+R)
   - Clear browser cache

### Step 3: Verify data

```sql
-- Quick verification query
SELECT 
    'Ghosts' as table_name, 
    COUNT(*) as count 
FROM GHOSTS
UNION ALL
SELECT 
    'Sightings', 
    COUNT(*) 
FROM GHOST_SIGHTINGS
UNION ALL
SELECT 
    'Sightings with coords', 
    COUNT(*) 
FROM GHOST_SIGHTINGS 
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL;
```

Expected output:
```
TABLE_NAME              COUNT
Ghosts                  5
Sightings              10
Sightings with coords   6  ← Must be > 0 for map!
```

---

## 🎨 Map Features

### Interactive Features:
- ✅ **Hover** to see ghost details
- ✅ **Color-coded** by ghost type
- ✅ **Size-scaled** by paranormal activity level
- ✅ **Clickable** markers with full info
- ✅ **Zoom/Pan** to explore

### Data Displayed:
- Location name
- Ghost name and type
- Sighting date/time
- Paranormal activity level (1-10)

---

## 🚀 Performance Tips

### For Large Datasets:

1. **Limit results**
   ```sql
   LIMIT 100  -- Already implemented
   ```

2. **Filter by date**
   ```sql
   WHERE sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())
   ```

3. **Use clustering**
   ```python
   # For 100+ markers, consider map clustering
   # (Future enhancement)
   ```

---

## ✅ Verification

### After restart, check:

- [ ] Navigate to "👻 Ghost Sightings" page
- [ ] Scroll to "🗺️ Sightings Map" section
- [ ] See message: "📊 Found X sightings with coordinates"
- [ ] Map displays with markers (or fallback method)
- [ ] Success message: "✅ Plotly map loaded successfully!"
- [ ] Can hover over markers to see details
- [ ] Can zoom and pan the map

---

## 📝 Files Modified

1. ✅ `streamlit_app/ghost_detection_app.py` - Enhanced map code
   - Lines ~274-382: Completely rewritten map section
   - Added triple fallback system
   - Added comprehensive error handling
   - Added debug information
   - Added coordinate validation

---

## 🔄 Alternative: Use Simple Map

If you prefer the simple Streamlit map over Plotly:

```python
# In streamlit_app.py, replace the map section with:
simple_map_df = map_df_valid[['LATITUDE', 'LONGITUDE']].copy()
simple_map_df.columns = ['lat', 'lon']
st.map(simple_map_df, zoom=3)
```

This always works and requires no external dependencies.

---

## 📞 Quick Commands

```bash
# Check if sample data is loaded
snowsql -q "SELECT COUNT(*) FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS WHERE latitude IS NOT NULL;"

# Load sample data (if not already loaded)
snowsql -f sql/03_sample_data.sql

# Restart Streamlit
pkill -f streamlit && streamlit run streamlit_app/ghost_detection_app.py

# Open in browser
# http://localhost:8501
```

---

## ✅ Summary

**Changes Made:**
- ✅ Added coordinate range validation
- ✅ Added auto-centering
- ✅ Changed zoom level (10 → 3) to see all markers
- ✅ Added triple fallback system (Plotly → st.map → table)
- ✅ Added comprehensive error handling
- ✅ Added debug information
- ✅ Added helpful tips and messages
- ✅ Improved user experience

**What to Do:**
1. Restart Streamlit app
2. Check if you have coordinate data
3. Map should now work with clear feedback
4. If not, error messages will guide you

**Time:** 1 minute to restart  
**Difficulty:** Easy  
**Result:** Working map with helpful debug info

---

**🎊 Your map is now much more robust with multiple fallbacks!** 🗺️✨

**Next Step:** Restart Streamlit and check the "👻 Ghost Sightings" page!

**Last Updated:** October 16, 2025  
**Issue:** Empty/white map display  
**Status:** ✅ Fixed with enhanced error handling

