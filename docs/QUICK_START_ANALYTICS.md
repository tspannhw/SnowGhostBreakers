# ⚡ Quick Start: Analytics & Bulk Processing

## 🚀 3-Minute Setup

Based on analytics from: https://github.com/tspannhw/AIM-Ghosts

---

## 📦 **Step 1: Prepare Sample Data**

### **Create Sample CSV** (30 seconds)
```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers

# Create sample sightings CSV
cat > sample_data/bulk_sightings.csv << 'EOF'
location_name,latitude,longitude,ghost_type,witness_name,activity_level,temperature_c,emf_reading,description
"Haunted Library",40.7589,-73.9851,"Phantom","Alice Smith",7,18.5,35.2,"Books moving on shelves"
"Old Cemetery",51.5074,-0.1278,"Wraith","Bob Johnson",9,12.3,48.7,"Shadowy figure observed"
"Abandoned Hospital",48.8566,2.3522,"Poltergeist","Carol Davis",8,15.1,42.1,"Medical equipment activating"
"Dark Forest Trail",35.6762,139.6503,"Apparition","David Lee",6,20.2,28.3,"Translucent form seen"
"Victorian Mansion",52.5200,13.4050,"Specter","Eve Martinez",7,16.8,33.9,"Cold spot detected"
EOF

mkdir -p sample_data
echo "✅ Sample CSV created"
```

---

## 🔄 **Step 2: Run Bulk Processor**

### **Process CSV Sightings** (1 minute)
```bash
# Process the CSV file
python scripts/bulk_ghost_processor.py \
    --mode csv \
    --input sample_data/bulk_sightings.csv
```

**Expected Output:**
```
====================================================================================
BULK GHOST PROCESSOR - SnowGhost Breakers
====================================================================================
Connecting to Snowflake...
✅ Connected successfully
Processing sightings from: sample_data/bulk_sightings.csv
Found 5 sightings to process
Processed 5/5 sightings...
Completed in 2.34s. Success: 5, Errors: 0

╔══════════════════════════════════════════════════════════════╗
║         BULK GHOST PROCESSING REPORT                         ║
╚══════════════════════════════════════════════════════════════╝

Processing Time:     2.34 seconds
Total Processed:     5 items
Successful:          5 items
Errors:              0 items
Success Rate:        100.0%

Items per second:    2.14

Status:              ✅ COMPLETE
```

---

## 📊 **Step 3: Verify in Snowflake** (30 seconds)

```sql
-- Check loaded data
USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Count new sightings
SELECT COUNT(*) as new_sightings 
FROM GHOST_SIGHTINGS 
WHERE sighting_id LIKE 'SIGHT%';

-- View loaded data
SELECT 
    location_name,
    paranormal_activity_level,
    temperature_celsius,
    emf_reading
FROM GHOST_SIGHTINGS
ORDER BY sighting_datetime DESC
LIMIT 5;
```

---

## 📥 **Alternative: Use Data Loader Notebook**

### **Option A: Snowflake Notebook**
1. Upload `notebooks/02_data_loader.ipynb` to Snowflake
2. Open in Snowflake Notebooks
3. Run all cells
4. Review generated data and statistics

### **Option B: Local Jupyter**
```bash
jupyter notebook notebooks/02_data_loader.ipynb
```

---

## 🖼️ **Process Images** (Optional)

### **Setup Image Directory**
```bash
# Create image directory
mkdir -p sample_data/ghost_images

# Add sample images (copy your own)
# Or download sample images
```

### **Batch Process Images**
```bash
python scripts/bulk_ghost_processor.py \
    --mode images \
    --input sample_data/ghost_images \
    --ghost-id GH001
```

---

## 📋 **Process JSON Batch** (Optional)

### **Create JSON Batch File**
```bash
cat > sample_data/batch_import.json << 'EOF'
{
  "sightings": [
    {
      "ghost_id": "GH001",
      "location_name": "Test Location",
      "latitude": 40.7589,
      "longitude": -73.9851,
      "witness_name": "Test Witness",
      "activity_level": 5,
      "temperature_c": 20,
      "emf_reading": 15,
      "description": "Test sighting"
    }
  ],
  "evidence": [
    {
      "sighting_id": "SIGHT0001",
      "ghost_id": "GH001",
      "type": "Photograph",
      "file_path": "@GHOST_DATA_STAGE/test.jpg"
    }
  ]
}
EOF
```

### **Import JSON Batch**
```bash
python scripts/bulk_ghost_processor.py \
    --mode json \
    --input sample_data/batch_import.json
```

---

## 🎯 **View Results in Streamlit**

### **Start Streamlit**
```bash
streamlit run streamlit_app/ghost_detection_app.py
```

### **Check Results**
1. Go to `📍 Sightings` page
2. See newly imported sightings
3. View on map (if coordinates valid)
4. Go to `📑 Reports` page
5. Generate **Sightings Analysis Report**
6. Review statistics and charts

---

## 📈 **Generate Analytics**

### **In Streamlit Reports:**
1. Click `📑 Reports`
2. Select: `📍 Sightings Analysis Report`
3. View:
   - Temporal analysis (hour/day patterns)
   - Activity level distribution
   - Geographic map of sightings
   - Top locations table

### **In Jupyter Notebook:**
1. Open `notebooks/01_ghost_analytics.ipynb`
2. Run Section 2: "Basic Statistics"
3. Run Section 11: "Time Series Analysis"
4. Review generated charts

---

## 🔍 **System Architecture Overview**

```bash
# View complete system diagram
cat SYSTEM_ARCHITECTURE_DIAGRAM.md

# View data flows
cat SYSTEM_ARCHITECTURE_DIAGRAM.md | grep -A 20 "Data Flow"
```

---

## 📊 **Common Tasks**

### **Task 1: Import Weekly Sightings**
```bash
# Prepare CSV from your data source
# Format: location_name, latitude, longitude, ghost_type, witness_name, activity_level, temperature_c, emf_reading, description

# Import
python scripts/bulk_ghost_processor.py --mode csv --input weekly_data.csv

# Verify
snowsql -q "SELECT COUNT(*) FROM GHOST_SIGHTINGS WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_DATE())"
```

### **Task 2: Batch Process Evidence**
```bash
# Organize images by ghost
mkdir -p evidence/GH001
mkdir -p evidence/GH002

# Process each batch
python scripts/bulk_ghost_processor.py --mode images --input evidence/GH001 --ghost-id GH001
python scripts/bulk_ghost_processor.py --mode images --input evidence/GH002 --ghost-id GH002
```

### **Task 3: Monthly Analytics**
```bash
# Open data loader notebook
jupyter notebook notebooks/02_data_loader.ipynb

# Run cells:
# - Summary Statistics
# - Activity Distribution
# - Geographic Analysis

# Export results
# File → Download as → HTML
```

---

## 🧪 **Test Commands**

### **Test 1: Small CSV Import**
```bash
echo "location_name,latitude,longitude,ghost_type,witness_name,activity_level,temperature_c,emf_reading,description
Test,40.7589,-73.9851,Phantom,Test,5,20,15,Test" > test.csv

python scripts/bulk_ghost_processor.py --mode csv --input test.csv
```

### **Test 2: Validation Check**
```bash
# In Python
python3 << 'PYEOF'
import pandas as pd
df = pd.read_csv('sample_data/bulk_sightings.csv')
print(f"✅ CSV Valid: {len(df)} records")
print(f"Columns: {list(df.columns)}")
PYEOF
```

### **Test 3: Database Connectivity**
```bash
snowsql -q "SELECT CURRENT_DATABASE(), CURRENT_SCHEMA(), CURRENT_VERSION()"
```

---

## 💡 **Tips & Tricks**

### **Tip 1: Validate Before Import**
```python
import pandas as pd

df = pd.read_csv('your_file.csv')

# Check for missing values
print(df.isnull().sum())

# Check coordinate ranges
invalid_coords = df[
    (df['latitude'] < -90) | (df['latitude'] > 90) |
    (df['longitude'] < -180) | (df['longitude'] > 180)
]
print(f"Invalid coordinates: {len(invalid_coords)}")
```

### **Tip 2: Monitor Progress**
```bash
# Run with output redirect for logging
python scripts/bulk_ghost_processor.py \
    --mode csv \
    --input large_file.csv \
    2>&1 | tee import_log.txt
```

### **Tip 3: Error Recovery**
```bash
# If import fails, check error log
grep "ERROR" import_log.txt

# Re-run with only failed records
# (manually create new CSV with failed rows)
```

---

## 📚 **Quick Reference**

### **Bulk Processor Modes:**
| Mode | Input | Output |
|------|-------|--------|
| `csv` | CSV file | GHOST_SIGHTINGS |
| `images` | Image directory | GHOST_EVIDENCE + AI_ANALYSIS |
| `json` | JSON file | Multiple tables |

### **Key Files:**
| File | Purpose |
|------|---------|
| `scripts/bulk_ghost_processor.py` | Batch processing |
| `notebooks/02_data_loader.ipynb` | Interactive loading |
| `SYSTEM_ARCHITECTURE_DIAGRAM.md` | System overview |

### **CSV Format:**
```
location_name        - String (required)
latitude             - Float, -90 to 90 (required)
longitude            - Float, -180 to 180 (required)
ghost_type           - String (optional)
witness_name         - String (required)
activity_level       - Integer, 1-10 (required)
temperature_c        - Float, -50 to 50 (required)
emf_reading          - Float, 0-100 (required)
description          - String (required)
```

---

## 🎯 **Next Steps**

After setup:
1. ✅ Test with sample data
2. ✅ Import your real data
3. ✅ Generate reports in Streamlit
4. ✅ Explore analytics in notebooks
5. ✅ Review system architecture
6. ✅ Customize for your needs

---

## 📞 **Quick Help**

### **Issue: Connection Failed**
```bash
# Check environment variables
echo $SNOWFLAKE_ACCOUNT
echo $SNOWFLAKE_USER

# Test connection
snowsql -q "SELECT 1"
```

### **Issue: CSV Format Error**
```bash
# Validate CSV format
head -5 your_file.csv

# Check for special characters
file your_file.csv
```

### **Issue: Permission Denied**
```sql
-- Check roles
SHOW GRANTS TO USER your_user;

-- Switch role if needed
USE ROLE ACCOUNTADMIN;
```

---

## ✅ **Success Checklist**

- [ ] Sample CSV created
- [ ] Bulk processor runs successfully
- [ ] Data visible in Snowflake
- [ ] Streamlit shows new sightings
- [ ] Reports generate correctly
- [ ] Notebook loads data
- [ ] System architecture reviewed

---

## 🎊 **You're Ready!**

**System:** ✅ Analytics & Bulk Processing  
**Status:** ✅ Operational  
**Performance:** ~100 records/sec  
**Documentation:** Complete  

**Start Processing:**
```bash
python scripts/bulk_ghost_processor.py --mode csv --input your_data.csv
```

---

**Last Updated:** October 17, 2025  
**Version:** 2.1  
**Feature:** Analytics & Bulk Processing  
**Ready:** ✅ Deploy Now!

