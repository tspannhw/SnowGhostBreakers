# 🔧 Fix for Package Conflict Error

## ❌ The Error You're Seeing

```
Error running Streamlit: [391546] SQL compilation error: 
Cannot create a Python function with the specified packages. 
One or more package conflicts were detected.
```

## 🎯 Root Cause

The `CREATE STREAMLIT ... PACKAGES = (...)` SQL syntax **doesn't work reliably** and causes package conflicts. Snowflake Streamlit apps require packages to be managed through the **Snowsight UI**, not SQL commands.

## ✅ THE FIX (3 Easy Steps)

### Step 1: Delete Existing App (if it exists)
```sql
DROP STREAMLIT IF EXISTS GHOST_DETECTION_APP;
```

### Step 2: Create via Snowsight UI

1. Open **Snowsight** in your browser
2. Navigate to: **Projects** → **Streamlit** → **+ Streamlit App**
3. Fill in:
   - **Name:** `GHOST_DETECTION_APP`
   - **Warehouse:** `COMPUTE_WH`
   - **Database:** `GHOST_DETECTION`
   - **Schema:** `APP`

### Step 3: Add Packages in UI

In the **Packages** section (usually left sidebar or toolbar):

**Type these exactly (one per line):**
```
plotly
nbformat
geopy
```

**⚠️ DO NOT ADD:**
- ~~pandas~~ (auto-included)
- ~~numpy~~ (auto-included) 
- ~~snowflake-snowpark-python~~ (auto-included)
- ~~streamlit~~ (auto-included)

### Step 4: Paste Your Code

Copy the entire contents of `streamlit_app/ghost_detection_app.py` and paste it into the Snowsight editor.

### Step 5: Run

Click the **"Run"** button. Your app should now start without package conflicts!

---

## 🔍 Why This Happens

Snowflake Streamlit has auto-included packages:
- `pandas`
- `numpy`
- `snowflake-snowpark-python`
- `streamlit`

When you try to specify these in `PACKAGES = (...)` via SQL, it creates conflicts because they're already included in different Python runtime versions.

**Solution:** Only specify packages that are NOT auto-included, and do it via the Snowsight UI, not SQL.

---

## 📋 Quick Checklist

- [ ] Deleted old app with `DROP STREAMLIT`
- [ ] Created new app via Snowsight UI
- [ ] Added ONLY: `plotly`, `nbformat`, `geopy`
- [ ] Did NOT add: pandas, numpy, snowpark
- [ ] Pasted code from `ghost_detection_app.py`
- [ ] Clicked "Run"

---

## 💡 Pro Tips

1. **Always use Snowsight UI for Streamlit packages** - SQL doesn't work
2. **Less is more** - Only add what's NOT auto-included
3. **Geocoding is optional** - The app will gracefully handle missing `geopy`
4. **If stuck** - Delete app and start fresh via UI

---

## 🆘 Still Having Issues?

### Can't find Packages section?
- Make sure you're in **Edit mode**
- Look for a **"+"** or **"Packages"** button in the left sidebar
- Try the **Settings** ⚙️ icon

### Packages still conflict?
- Remove ALL packages
- Add back ONLY: `plotly`, `nbformat`, `geopy`
- Make sure no versions are specified (e.g., `plotly==6.3.0` ❌, just `plotly` ✅)

### Want to skip geopy for now?
Just add:
```
plotly
nbformat
```
The geocoding feature will show a helpful message if `geopy` is missing.

---

## 📚 Related Files

- `deploy_streamlit_app.sql` - Updated deployment instructions
- `STREAMLIT_CORRECT_FIX.md` - Detailed troubleshooting guide
- `streamlit_app/packages.txt` - Reference list of required packages
- `streamlit_app/ghost_detection_app.py` - Now handles missing geopy gracefully

---

**Remember:** For Snowflake Streamlit, **always use Snowsight UI for packages**! 🎯

