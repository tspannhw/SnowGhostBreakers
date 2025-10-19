# ⚡ Reports Quick Start

## 🚀 Access Reports

**Navigation:** `Streamlit App → 📑 Reports`

---

## 📊 6 Report Types

### 1. **📊 Executive Summary**
**What:** High-level KPIs and trends  
**Includes:** 6 metrics, threat pie chart, 30-day trend, hotspots map  
**Best For:** Quick overview, executive briefings

### 2. **👻 Ghost Registry Report**
**What:** Complete entity analysis  
**Includes:** Registry stats, types, status, threat treemap  
**Best For:** Entity management, threat assessment

### 3. **📍 Sightings Analysis Report**
**What:** Patterns and trends  
**Includes:** Temporal charts, activity levels, geographic map  
**Best For:** Pattern detection, hotspot monitoring

### 4. **🔬 Evidence Analysis Report**
**What:** Collection and AI review  
**Includes:** Evidence stats, types, AI performance, recent items  
**Best For:** Quality assurance, AI tracking

### 5. **📋 Investigations Report**
**What:** Case tracking and status  
**Includes:** Case stats, duration, investigator performance  
**Best For:** Case management, resource allocation

### 6. **👥 Investigators Performance Report**
**What:** Team metrics and performance  
**Includes:** Team composition, experience, top performers  
**Best For:** Performance reviews, team planning

---

## ⚡ Quick Access

```
1. Open Streamlit app
2. Click: 📑 Reports (sidebar)
3. Select report from dropdown
4. View automatically generated report
```

---

## 📊 What You Get

### Every Report Includes:
- ✅ **Summary Metrics** - Key numbers at top
- ✅ **Charts & Graphs** - Visual insights
- ✅ **Maps** (where relevant) - Geographic data
- ✅ **Data Tables** - Detailed information
- ✅ **Timestamp** - When report was generated

### Chart Types:
- 📊 Pie/Donut Charts
- 📈 Bar Charts
- 📉 Line Charts
- 🗺️ Interactive Maps
- 🎯 Treemaps
- 📋 Data Tables

---

## 🎯 Quick Use Cases

### Need to See:
- **Overall Status?** → Executive Summary
- **Ghost Details?** → Ghost Registry
- **Where Activity Occurs?** → Sightings Analysis
- **Evidence Quality?** → Evidence Analysis
- **Case Status?** → Investigations
- **Team Performance?** → Investigators Report

---

## 🗺️ Map Features

All maps include:
- **Bubble Size** = Count/Importance
- **Color** = Intensity/Activity
- **Hover** = Detailed info
- **Zoom/Pan** = Interactive exploration
- **No API Key** = Works immediately!

---

## 💡 Pro Tips

1. **Start with Executive Summary** - Get the big picture
2. **Hover over charts** - See detailed data
3. **Zoom maps** - Focus on specific regions
4. **Check timestamps** - Know when generated
5. **Cross-reference** - Compare multiple reports

---

## 🧪 Quick Test

```bash
# Restart Streamlit
pkill -f streamlit && streamlit run streamlit_app/ghost_detection_app.py

# Test:
1. Go to 📑 Reports
2. Select: 📊 Executive Summary
3. Check: All 6 metrics display
4. Verify: Map shows locations
5. Try: Hover over charts
✅ Working!
```

---

## 📈 Example Output

### Executive Summary:
```
🎯 Key Performance Indicators
┌─────────────┬──────────────┬──────────────┐
│Active Ghosts│Sightings(30d)│Evidence Items│
├─────────────┼──────────────┼──────────────┤
│     12      │      45      │     187      │
└─────────────┴──────────────┴──────────────┘

⚠️ Threat Level Distribution [Pie Chart]
🗺️ Geographic Hotspots [Interactive Map]
📈 30-Day Sighting Trend [Line Chart]
```

### Sightings Analysis:
```
📊 Sightings Overview
Total: 234 | Unique Ghosts: 18 | Locations: 45

📅 Temporal Analysis
- Sightings by Hour [Bar Chart]
- Sightings by Day [Bar Chart]

🗺️ Geographic Distribution [Interactive Map]
📍 Most Active Locations [Table]
```

---

## 🎨 Visual Elements

### Colors Mean:
- **Red** = High threat/activity
- **Orange** = Medium
- **Yellow** = Low-medium
- **Green** = Low/safe
- **Blue** = Informational

### Sizes Mean:
- **Larger bubbles** = More activity
- **Taller bars** = Higher counts
- **Bigger slices** = Larger proportion

---

## 💾 Export (Coming Soon)

Planned features:
- 📄 PDF Export
- 📊 Excel Export
- 📧 Email Delivery

Currently showing placeholder buttons.

---

## ✅ Success Indicators

Reports are working if you see:
- ✅ Metrics display with numbers
- ✅ Charts render visually
- ✅ Maps show with bubbles
- ✅ Tables populate with data
- ✅ No error messages
- ✅ Timestamp shows current date/time

---

## 🚨 Troubleshooting

### No data showing?
```sql
-- Check if tables have data:
SELECT COUNT(*) FROM GHOSTS;
SELECT COUNT(*) FROM GHOST_SIGHTINGS;
SELECT COUNT(*) FROM GHOST_EVIDENCE;

-- If empty, run:
!source sql/03_sample_data.sql
```

### Map not displaying?
- Check that sightings have valid coordinates
- Ensure latitude/longitude are populated
- Try zooming out on the map

### Charts not rendering?
- Refresh the page
- Check browser console for errors
- Restart Streamlit app

---

## 📚 Full Documentation

See `COMPREHENSIVE_REPORTS_GUIDE.md` for:
- Detailed report descriptions
- All visualization types
- SQL query patterns
- Use cases by role
- Future enhancements
- Complete testing guide

---

**🎉 6 comprehensive reports with 25+ visualizations ready to use!** 📊✨

**Quick Start:** 
```
📑 Reports → [Select Type] → View Insights!
```

**Status:** ✅ Production Ready  
**Time to Deploy:** Restart Streamlit  
**Learning Curve:** < 5 minutes

