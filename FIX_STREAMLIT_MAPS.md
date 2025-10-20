# 🗺️ Fix: Maps Not Showing in Streamlit

## Common Causes

1. **No valid coordinate data** in the database
2. **Plotly not loading properly** 
3. **Mapbox rendering issues** in Streamlit
4. **Data type mismatches** (coordinates as strings instead of floats)

---

## 🔍 Quick Diagnostics

Add this debug cell to check your data:

```python
# At the top of the map section, add:
st.write("**Debug: Map Data**")
st.write(f"Total rows: {len(hotspots_df)}")
st.write(f"Columns: {hotspots_df.columns.tolist()}")
if 'LATITUDE' in hotspots_df.columns:
    st.write(f"Valid coordinates: {hotspots_df[['LATITUDE', 'LONGITUDE']].dropna().shape[0]}")
    st.write(f"Sample coordinates:")
    st.write(hotspots_df[['LOCATION_NAME', 'LATITUDE', 'LONGITUDE']].head())
```

---

## ✅ Solutions

### Solution 1: Check Database Has Coordinate Data

Run this SQL to verify:

```sql
-- Check if sightings have coordinates
SELECT 
    COUNT(*) as total_sightings,
    COUNT(latitude) as with_latitude,
    COUNT(longitude) as with_longitude,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_both
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS;

-- View sample coordinates
SELECT 
    location_name,
    latitude,
    longitude
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL
LIMIT 10;
```

If no coordinates exist, add some sample data:

```sql
-- Add coordinates to existing sightings
UPDATE GHOST_DETECTION.APP.GHOST_SIGHTINGS
SET 
    latitude = 40.7128,
    longitude = -74.0060
WHERE sighting_id = 'YOUR_SIGHTING_ID';
```

### Solution 2: Use Streamlit's Built-in Map (Simpler)

Replace plotly maps with Streamlit's simpler map:

```python
# Instead of px.scatter_mapbox, use:
if not hotspots_valid.empty:
    # Convert to format st.map expects
    map_data = hotspots_valid[['LATITUDE', 'LONGITUDE']].copy()
    map_data.columns = ['lat', 'lon']
    
    # Display with Streamlit's built-in map
    st.map(map_data, zoom=3)
    
    # Show data table below
    st.dataframe(hotspots_valid[['LOCATION_NAME', 'LATITUDE', 'LONGITUDE', 'TOTAL_SIGHTINGS']])
```

### Solution 3: Fix Plotly Mapbox (If plotly is the issue)

Ensure plotly is properly configured:

```python
import plotly.express as px
import plotly.graph_objects as go

# Try with explicit config
fig = px.scatter_mapbox(
    hotspots_valid,
    lat='LATITUDE',
    lon='LONGITUDE',
    zoom=2,  # Start more zoomed out
    height=600,
    mapbox_style="open-street-map"
)

# Update layout for better rendering
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend=False
)

# Display with explicit config
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
```

### Solution 4: Validate Coordinate Data Types

Add data validation:

```python
# Ensure coordinates are numeric
if not hotspots_valid.empty:
    # Convert to float and validate range
    hotspots_valid['LATITUDE'] = pd.to_numeric(hotspots_valid['LATITUDE'], errors='coerce')
    hotspots_valid['LONGITUDE'] = pd.to_numeric(hotspots_valid['LONGITUDE'], errors='coerce')
    
    # Filter valid coordinates (lat: -90 to 90, lon: -180 to 180)
    hotspots_valid = hotspots_valid[
        (hotspots_valid['LATITUDE'].between(-90, 90)) & 
        (hotspots_valid['LONGITUDE'].between(-180, 180))
    ]
    
    if hotspots_valid.empty:
        st.warning("No valid coordinates found (must be: lat -90 to 90, lon -180 to 180)")
```

---

## 🎯 Recommended Quick Fix

Replace the map sections with this more robust version:

```python
# Paranormal Hotspots Map
st.subheader("🗺️ Paranormal Hotspots")

try:
    hotspots_df = session.table("GHOST_DETECTION.ANALYTICS.VW_PARANORMAL_HOTSPOTS").to_pandas()
    
    if hotspots_df.empty:
        st.info("ℹ️ No hotspot data available. Add sightings with coordinates first.")
    elif 'LATITUDE' not in hotspots_df.columns or 'LONGITUDE' not in hotspots_df.columns:
        st.warning("⚠️ Coordinate columns missing from hotspots data.")
    else:
        # Clean and validate coordinates
        hotspots_valid = hotspots_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
        hotspots_valid['LATITUDE'] = pd.to_numeric(hotspots_valid['LATITUDE'], errors='coerce')
        hotspots_valid['LONGITUDE'] = pd.to_numeric(hotspots_valid['LONGITUDE'], errors='coerce')
        hotspots_valid = hotspots_valid.dropna(subset=['LATITUDE', 'LONGITUDE'])
        hotspots_valid = hotspots_valid[
            (hotspots_valid['LATITUDE'].between(-90, 90)) & 
            (hotspots_valid['LONGITUDE'].between(-180, 180))
        ]
        
        if hotspots_valid.empty:
            st.info("ℹ️ No valid coordinates found. Add latitude/longitude to sightings.")
        else:
            st.success(f"✅ Found {len(hotspots_valid)} locations with coordinates")
            
            # Try Plotly first
            try:
                fig = px.scatter_mapbox(
                    hotspots_valid,
                    lat='LATITUDE',
                    lon='LONGITUDE',
                    size='TOTAL_SIGHTINGS' if 'TOTAL_SIGHTINGS' in hotspots_valid.columns else None,
                    hover_name='LOCATION_NAME' if 'LOCATION_NAME' in hotspots_valid.columns else None,
                    zoom=2,
                    height=500,
                    mapbox_style="open-street-map"
                )
                fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as plotly_error:
                # Fallback to Streamlit map
                st.info(f"📍 Using simple map view (plotly error: {str(plotly_error)[:100]})")
                map_data = hotspots_valid[['LATITUDE', 'LONGITUDE']].copy()
                map_data.columns = ['lat', 'lon']
                st.map(map_data)
            
            # Show data table
            with st.expander("📋 View Location Details"):
                display_cols = [col for col in ['LOCATION_NAME', 'LATITUDE', 'LONGITUDE', 'TOTAL_SIGHTINGS'] 
                               if col in hotspots_valid.columns]
                st.dataframe(hotspots_valid[display_cols], use_container_width=True)
                
except Exception as e:
    st.error(f"❌ Error loading map: {str(e)}")
    st.info("💡 Make sure VW_PARANORMAL_HOTSPOTS view exists and has coordinate data")
```

---

## 🧪 Test Your Fix

1. **Check if you see the success message**: "✅ Found N locations"
   - If NO → Your data has no valid coordinates (see Solution 1)
   - If YES but no map → Continue below

2. **Check for error messages**
   - Plotly error → Use Solution 2 (Streamlit map)
   - Column missing → Check your view/table structure

3. **Verify map appears**
   - Even simple `st.map()` should work if coordinates are valid

---

## 📊 Add Sample Coordinates (If Needed)

```sql
-- Quick test: Add a few sample locations
UPDATE GHOST_DETECTION.APP.GHOST_SIGHTINGS
SET latitude = 40.7128, longitude = -74.0060  -- New York
WHERE location_name LIKE '%Manhattan%';

UPDATE GHOST_DETECTION.APP.GHOST_SIGHTINGS
SET latitude = 51.5074, longitude = -0.1278   -- London
WHERE location_name LIKE '%London%';

UPDATE GHOST_DETECTION.APP.GHOST_SIGHTINGS
SET latitude = 35.6762, longitude = 139.6503  -- Tokyo
WHERE location_name LIKE '%Tokyo%';

-- Verify
SELECT location_name, latitude, longitude
FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
WHERE latitude IS NOT NULL;
```

---

## 🎬 Expected Result

After fixing, you should see:
- ✅ "Found N locations with coordinates" message
- ✅ Interactive map with location markers
- ✅ Fallback to simple map if plotly fails
- ✅ Data table below map showing locations

---

## 💡 Quick Checklist

- [ ] Verified coordinates exist in database
- [ ] Coordinates are numeric (not strings)
- [ ] Coordinates are in valid range (lat: -90 to 90, lon: -180 to 180)
- [ ] Plotly package is added in Snowsight UI
- [ ] Using robust error handling (see recommended fix above)
- [ ] Fallback to `st.map()` if plotly fails

---

**Most Common Issue:** No coordinate data in database. Run the SQL checks first! 📍

