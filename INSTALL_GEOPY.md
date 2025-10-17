# 📦 Installing geopy for SnowGhost Breakers

## ❌ Error

```
❌ Geocoding error: No module named 'geopy'
```

## ✅ Quick Fix

### **Option 1: Local Development (Recommended)**

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers

# Install all requirements
pip install -r requirements.txt

# Or install just geopy
pip install geopy>=2.4.0
```

### **Option 2: Streamlit Cloud Deployment**

The `requirements.txt` already includes geopy. Streamlit Cloud will automatically install it when you deploy.

**requirements.txt** (already configured):
```
geopy>=2.4.0
```

### **Option 3: Snowflake Streamlit**

For Snowflake Streamlit apps, use the `environment.yml` file (already created):

```yaml
dependencies:
  - geopy>=2.4.0
  - pip:
    - geopy>=2.4.0
```

Upload `environment.yml` with your Streamlit app to Snowflake.

---

## 🔧 Verification

After installation, test the geocoding feature:

```python
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="snowghost_breakers")
location = geolocator.geocode("New York, NY")
print(f"✅ Geocoding works: {location.latitude}, {location.longitude}")
```

Expected output:
```
✅ Geocoding works: 40.7127281, -74.0060152
```

---

## 📋 Related Files

- `requirements.txt` - Python package dependencies
- `environment.yml` - Conda environment for Snowflake Streamlit
- `streamlit_app/ghost_detection_app.py` - Uses geopy for address lookup

---

## 🚀 Re-run Streamlit

After installing:

```bash
streamlit run streamlit_app/ghost_detection_app.py
```

The geocoding feature should now work! ✅

