# ⚡ Quick Fix Guide - 3 Simple Steps

## 🎯 The Problem

You're seeing these errors in your **deployed** Streamlit app:
1. ❌ Sightings page: "Ambiguous column DESCRIPTION"
2. ❌ Evidence Analysis: "Cannot accept list for x and y"
3. ❌ Missing "Coming soon" message in AI Insights

**Good news:** The code is already fixed! You just need to restart.

---

## ✅ 3-Step Fix

### Step 1: Update SQL Function ⚙️

```bash
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
snowsql -f sql/08_business_vocabulary.sql
```

**What it fixes:** GET_TERM_RELATIONSHIPS function ambiguous column error

---

### Step 2: Restart Streamlit 🔄

#### If running locally:
```bash
# Kill streamlit
pkill -f streamlit

# Clear cache
rm -rf ~/.streamlit/cache

# Restart
streamlit run streamlit_app/ghost_detection_app.py
```

#### If running in Snowflake:
```sql
-- In Snowsight Worksheet:
ALTER STREAMLIT GHOST_DETECTION_APP STOP;

-- Wait 5 seconds, then:
ALTER STREAMLIT GHOST_DETECTION_APP START;
```

**What it fixes:** Deploys the latest fixed code

---

### Step 3: Hard Refresh Browser 🌐

Press:
- **Mac:** `Cmd + Shift + R`
- **Windows/Linux:** `Ctrl + Shift + R`

**What it fixes:** Clears browser cache

---

## ✅ Verify It Works

Visit each page in Streamlit:

1. **📍 Sightings** → Should show map with no errors ✅
2. **🔬 Evidence Analysis** → Charts should display ✅
3. **🤖 AI Insights** → Click "Predictions" tab → See "Coming soon" ✅
4. **📚 Vocabulary** → Should load with no errors ✅

---

## 🚨 Still Seeing Errors?

### Check 1: Is the fixed file deployed?

```bash
# Your file should have ~819 lines
wc -l streamlit_app/ghost_detection_app.py
# Should output: 819 streamlit_app/ghost_detection_app.py
```

### Check 2: Search for the fix

```bash
# Should find the fix:
grep -n "sightings_table\[\"DESCRIPTION\"\]" streamlit_app/ghost_detection_app.py
# Should output: 255:        sightings_table["DESCRIPTION"]
```

### Check 3: Verify "Coming soon" is there

```bash
# Should find it:
grep -n "Coming soon" streamlit_app/ghost_detection_app.py
# Should output: 486:        st.info("Coming soon: Predictive analytics for ghost behavior patterns")
```

**If any of these fail:** You have an old version of the file!

---

## 📋 Complete Restart (Nuclear Option)

If the 3 steps above don't work:

```bash
# 1. Kill everything
pkill -f streamlit
pkill -f python

# 2. Clear all caches
rm -rf ~/.streamlit
rm -rf ~/.cache/pip

# 3. Reinstall dependencies
cd /Users/tspann/Downloads/code/cursorai/SnowGhostBreakers
pip install -r requirements.txt --force-reinstall --no-cache

# 4. Update SQL
snowsql -f sql/08_business_vocabulary.sql

# 5. Restart fresh
streamlit run streamlit_app/ghost_detection_app.py
```

---

## 💡 What Was Fixed?

### Fix 1: Ambiguous Join (Sightings)
```python
# ✅ NOW (lines 230-256):
sightings_table = session.table("GHOST_SIGHTINGS")
ghosts_table = session.table("GHOSTS")
sightings_query = sightings_table.join(
    ghosts_table,
    sightings_table["GHOST_ID"] == ghosts_table["GHOST_ID"]
)
# Explicit: sightings_table["DESCRIPTION"]
```

### Fix 2: Plotly Chart (Evidence)
```python
# ✅ NOW (lines 359-363):
evidence_type_counts = df['EVIDENCE_TYPE'].value_counts().reset_index()
evidence_type_counts.columns = ['Evidence Type', 'Count']
fig = px.bar(evidence_type_counts, x='Evidence Type', y='Count')
```

### Fix 3: Coming Soon Message (AI Insights)
```python
# ✅ NOW (line 486):
st.info("Coming soon: Predictive analytics for ghost behavior patterns")
```

### Fix 4: SQL Function (GET_TERM_RELATIONSHIPS)
```sql
-- ✅ NOW:
SELECT 
    bv2.term_id as related_term_id,
    bv2.term_name as related_term_name,
    ...
FROM BUSINESS_VOCABULARY bv1
JOIN BUSINESS_VOCABULARY bv2 ON ...
```

---

## 🎯 Expected Timeline

| Step | Time |
|------|------|
| SQL Update | 10 seconds |
| Streamlit Restart | 5 seconds |
| Browser Refresh | 1 second |
| **Total** | **< 20 seconds** |

---

## ✅ Success Indicators

After the fix, you'll see:

- ✅ **Sightings page loads** with interactive map
- ✅ **Evidence Analysis charts** display correctly
- ✅ **AI Insights Predictions** shows "Coming soon" message
- ✅ **No error messages** in any page
- ✅ **Vocabulary page** works without errors

---

## 📞 One-Liner Fix

```bash
snowsql -f sql/08_business_vocabulary.sql && pkill -f streamlit && rm -rf ~/.streamlit/cache && streamlit run streamlit_app/ghost_detection_app.py
```

Copy, paste, done! 🚀

---

**🎊 That's it! Your app should now work perfectly!** 👻✨

