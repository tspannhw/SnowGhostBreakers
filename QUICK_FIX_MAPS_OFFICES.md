# ⚡ Quick Fix: Maps & Offices

## 🚀 Fast Deploy (3 Steps)

### **Step 1: Load Offices**
```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
snowsql -f sql/13_offices_table.sql
```

### **Step 2: Restart Streamlit**
```bash
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py
```

### **Step 3: Test**
1. Open browser → Streamlit app
2. Click: `🏢 Global Offices` → See world map with 27 offices
3. Click: `📍 Sightings` → Scroll to map section
4. Click: `📋 Investigations` → See investigation map

---

## ✅ What's Fixed

| Issue | Status | Location |
|-------|--------|----------|
| Sightings map not showing | ✅ FIXED | Sightings page |
| Investigations map missing | ✅ ADDED | Investigations page |
| ghostbusters.com emails | ✅ REMOVED | All files |
| Global offices missing | ✅ CREATED | New page + table |

---

## 🗺️ 3 New/Enhanced Maps

### **1. Sightings Map** (Enhanced)
- **Location:** `📍 Sightings` page
- **Shows:** Ghost sighting locations
- **New:** Debug messages, triple fallback, better errors

### **2. Investigations Map** (NEW)
- **Location:** `📋 Investigations` page  
- **Shows:** Active investigation locations
- **Colors:** Priority-based (Red=Critical, Orange=High, Yellow=Medium, Green=Low)

### **3. Global Offices Map** (NEW)
- **Location:** `🏢 Global Offices` page
- **Shows:** 27 worldwide offices
- **Colors:** Purple=HQ, Blue=Regional, Green=Field

---

## 🏢 27 New Offices

**Americas:** 7 offices  
**Europe & Middle East:** 13 offices  
**Asia-Pacific:** 7 offices  

**Cities include:** Menlo Park, Bellevue, Toronto, London, Berlin, Amsterdam, Warsaw, Tokyo, Singapore, Pune, Sydney, and more!

**Total Capacity:** 1,713 investigators worldwide

---

## 📧 Email Changes

**Old:** `@ghostbusters.com` ❌  
**New:** `@snowghostbreakers.com` ✅

**Updated in:**
- Sample data (5 investigators)
- Streamlit placeholders

---

## 🧪 Quick Test

```bash
# Verify offices loaded
snowsql -q "SELECT COUNT(*) FROM GHOST_DETECTION.APP.OFFICES;"
# Expected: 27

# Check emails
snowsql -q "SELECT email FROM GHOST_DETECTION.APP.INVESTIGATORS LIMIT 1;"
# Expected: @snowghostbreakers.com

# Open Streamlit
# Click: 🏢 Global Offices
# See: World map with 27 office locations
```

---

## 🎯 Quick Access

```
Streamlit App
├── 🏢 Global Offices (NEW)
│   ├── 🗺️ World map with 27 offices
│   ├── 🌎 By Region view
│   ├── 🏙️ All Offices directory
│   ├── 📊 Statistics charts
│   └── ➕ Add Office form
│
├── 📍 Sightings (ENHANCED)
│   └── 🗺️ Sightings Map (now with debugging)
│
└── 📋 Investigations (ENHANCED)
    └── 🗺️ Investigation Locations Map (NEW)
```

---

## 💡 Troubleshooting

### **Maps not showing?**
```sql
-- Check data exists
SELECT COUNT(*) FROM GHOST_SIGHTINGS WHERE LATITUDE IS NOT NULL;
SELECT COUNT(*) FROM INVESTIGATIONS;
SELECT COUNT(*) FROM OFFICES;

-- If counts are zero, load sample data:
snowsql -f sql/03_sample_data.sql
```

### **Offices page empty?**
```bash
# Run offices setup:
snowsql -f sql/13_offices_table.sql
```

### **Old emails still showing?**
```bash
# Reload investigators:
snowsql -q "TRUNCATE TABLE GHOST_DETECTION.APP.INVESTIGATORS;"
snowsql -f sql/03_sample_data.sql
```

---

## 📁 Files Changed

**Created:**
- `sql/13_offices_table.sql` (new)
- `MAPS_AND_OFFICES_FIX.md` (docs)

**Modified:**
- `sql/03_sample_data.sql` (emails)
- `streamlit_app/ghost_detection_app.py` (+271 lines)

---

## ✅ Success Checklist

- [ ] Run `sql/13_offices_table.sql`
- [ ] Restart Streamlit
- [ ] See "🏢 Global Offices" in menu
- [ ] Open Global Offices page
- [ ] See world map with 27 offices
- [ ] Check Sightings map works
- [ ] Check Investigations map appears
- [ ] Verify emails are @snowghostbreakers.com

---

## 🎉 Done!

**Maps:** ✅ Fixed & Enhanced  
**Offices:** ✅ 27 Locations Added  
**Emails:** ✅ All Updated  
**Status:** ✅ Ready to Use!

**Time to Deploy:** ~2 minutes  
**New Features:** 3 maps, 1 page, 27 offices  
**Lines Added:** ~450+ lines

---

**Quick Deploy:**
```bash
snowsql -f sql/13_offices_table.sql && \
pkill -f streamlit && \
streamlit run streamlit_app/ghost_detection_app.py
```

**Then:** Open browser → Test all 3 maps! 🗺️✨

