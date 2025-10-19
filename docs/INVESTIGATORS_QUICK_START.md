# ⚡ Investigators Quick Start

## 🚀 Quick Access

**Navigation:** Streamlit App → `👥 Investigators`

---

## 📋 Three Tabs

### 1. Team Roster
**View all investigators**
- Filter by status (Active/Inactive)
- Filter by specialization
- Expandable cards with full details

### 2. Add Investigator
**Register new team member**
- Fill required fields: Name*, Email*, Specialization*, Experience*
- Optional: Phone, Notes
- Click "👥 Register Investigator"

### 3. Statistics
**View team analytics**
- Total team count
- Cases solved
- Specialization distribution
- Experience levels

---

## ⚡ Quick Add

```
1. Go to 👥 Investigators → ➕ Add Investigator
2. Fill form:
   Name: Dr. Jane Smith
   Email: jane@snowghostbreakers.com
   Specialization: EMF Expert
   Experience: 5 years
3. Click Register
4. ✅ Done!
```

---

## 🎯 Specializations

- Lead Investigator
- EMF Expert
- Medium/Psychic
- Technician
- EVP Specialist
- Demonologist
- Historian
- Field Researcher
- Data Analyst

---

## 🔍 Quick Queries

### All Investigators:
```sql
SELECT * FROM GHOST_DETECTION.APP.INVESTIGATORS;
```

### Active Only:
```sql
SELECT * FROM INVESTIGATORS WHERE active_status = TRUE;
```

### By Specialization:
```sql
SELECT * FROM INVESTIGATORS WHERE specialization = 'EMF Expert';
```

---

## ✅ Success Indicators

After adding an investigator:
- ✅ Success message appears
- 📊 ID, Specialization, Status displayed
- 🎈 Balloons animation
- 👤 Name confirmation

---

## 💡 Pro Tips

1. **Use professional emails** - Organization domain
2. **Accurate experience** - Don't round years
3. **Update status** - Mark inactive when leaving
4. **Add notes** - Document special skills
5. **Review statistics** - Check team balance

---

## 🔐 Database

**Table:** `GHOST_DETECTION.APP.INVESTIGATORS`  
**ID Format:** `INV_XXXXXXXX`  
**Audit:** All changes logged

---

## 🧪 Quick Test

```bash
# 1. Restart Streamlit
pkill -f streamlit
streamlit run streamlit_app/ghost_detection_app.py

# 2. Test
# - Go to 👥 Investigators
# - Add test investigator
# - View in Team Roster
# - Check Statistics tab
```

---

## 📊 Example Entry

```
Name: Dr. Sarah Mitchell
Email: sarah.mitchell@example.com
Phone: +1-555-0199
Specialization: EMF Expert
Experience: 8 years
Status: Active
```

**Result:** `INV_A1B2C3D4` created!

---

**🎉 Ready to build your ghost-hunting team!** 👥✨

**See `INVESTIGATORS_MANAGEMENT.md` for complete documentation**

