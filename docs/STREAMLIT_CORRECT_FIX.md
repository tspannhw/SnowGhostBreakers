# ✅ CORRECT Fix for Streamlit Packages

## The Problem

You can't use `ALTER STREAMLIT ... SET PACKAGES` because that's not valid syntax for Snowflake Streamlit apps. Packages must be managed through Snowsight UI.

**Error:** `SQL compilation error: invalid property 'PACKAGES' for 'STREAMLIT'`

---

## ✅ The CORRECT Solution

### Option 1: Via Snowsight UI (Recommended)

1. **Open Snowsight** and go to **Streamlit Apps**
2. **Find your app** `GHOST_DETECTION_APP`
3. **Click the app** to open it
4. **Click "Edit"** or the **⚙️ Settings** button
5. **Look for "Packages"** section in the editor
6. **Add these packages:**
   ```
   plotly
   nbformat
   geopy
   ```
7. **Remove any other packages** (pandas, numpy, snowflake-snowpark-python)
8. **Click "Run"** or **"Save"**

---

## Option 2: Create a packages.txt file

If your Streamlit app reads from a stage, you can create a `packages.txt` file:

**File: `packages.txt`**
```
plotly
nbformat
geopy
```

Upload this file to your stage:
```sql
PUT file://streamlit_app/packages.txt @STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
```

---

## Option 3: Recreate the App via UI

1. **Go to Streamlit Apps** in Snowsight
2. **Click "+ Streamlit App"**
3. **Name:** GHOST_DETECTION_APP
4. **Warehouse:** COMPUTE_WH
5. **Database:** GHOST_DETECTION
6. **Schema:** APP
7. **In the Packages section, add:**
   - `plotly`
   - `nbformat`
   - `geopy`
8. **Paste your code** from `ghost_detection_app.py`
9. **Click "Run"**

---

## 🎯 What Packages to Add

In the Snowsight Packages section, add **ONLY** these three:

```
plotly
nbformat
geopy
```

**Do NOT add:**
- ~~pandas~~ (auto-included)
- ~~numpy~~ (auto-included)
- ~~snowflake-snowpark-python~~ (auto-included)
- ~~streamlit~~ (auto-included)

---

## 📸 Step-by-Step with Screenshots

### Step 1: Open Your App
Navigate to: **Projects** → **Streamlit** → **GHOST_DETECTION_APP**

### Step 2: Click Edit
Look for the **"Edit"** button in the top right corner

### Step 3: Find Packages Section
In the editor, look for the **"Packages"** button or section (usually in the left sidebar or top toolbar)

### Step 4: Add Packages
Type or paste:
```
plotly
nbformat
geopy
```

Each on a new line.

### Step 5: Remove Conflicting Packages
If you see these, **DELETE them:**
- pandas
- numpy  
- snowflake-snowpark-python

### Step 6: Save and Run
Click **"Run"** to apply the changes and restart the app

---

## 🔍 Troubleshooting

### "I don't see a Packages section"
- Make sure you're in **Edit mode** (click the Edit button)
- Look for a **"+"** button to add packages
- Try clicking on the **Settings** or **Configuration** icon

### "Packages still conflict"
- Make sure you **removed** pandas, numpy, and snowpark
- Only `plotly`, `nbformat`, and `geopy` should be listed
- Try deleting ALL packages and re-adding just those three

### "Can't edit the app"
- You might need appropriate permissions
- Contact your Snowflake admin to grant you edit access

---

## 💡 Why SQL Commands Don't Work

Snowflake Streamlit apps are different from UDFs:

| Type | Package Management |
|------|-------------------|
| **UDF/UDAF** | `CREATE FUNCTION ... PACKAGES = (...)` ✅ |
| **Stored Proc** | `CREATE PROCEDURE ... PACKAGES = (...)` ✅ |
| **Streamlit** | Via Snowsight UI only ❌ No SQL syntax |

Streamlit packages are managed through the **web interface**, not SQL commands.

---

## 🎬 Quick Summary

1. Open your Streamlit app in Snowsight
2. Click "Edit"
3. Go to "Packages" section
4. Add only: `plotly`, `nbformat`, and `geopy`
5. Remove: pandas, numpy, snowpark (if present)
6. Click "Run"

**That's it!** No SQL commands needed.

---

## 📝 Alternative: Delete and Recreate

If nothing works, delete and recreate:

```sql
-- Delete the app
DROP STREAMLIT GHOST_DETECTION_APP;
```

Then recreate via Snowsight UI with the correct packages from the start.

---

## ✅ Expected Result

After fixing, your app should:
- ✅ Load without errors
- ✅ Display plotly charts correctly
- ✅ Not have package conflicts
- ✅ Use auto-included pandas/numpy seamlessly

---

**Remember:** For Snowflake Streamlit, always manage packages through the **Snowsight UI**, not SQL commands!

