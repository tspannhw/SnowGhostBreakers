# Fix: nbformat Error in Snowflake Notebooks

## Error Message
```
ValueError: Mime type rendering requires nbformat>=4.2.0 but it is not installed
```

This error occurs when plotly tries to display charts in Jupyter/Snowflake Notebooks.

---

## Quick Fix for Snowflake Notebooks

### Option 1: Via Notebook UI (Easiest)

1. **Open your notebook** in Snowsight
2. **Click "Packages"** in the top toolbar
3. **Add package:** `nbformat`
4. Click **"Add"** or **"Install"**
5. **Restart the kernel** (if needed)
6. **Re-run the cells**

### Option 2: Add at Notebook Level

Add this at the top of your notebook:

```python
# Install nbformat if not available
import sys
!{sys.executable} -m pip install nbformat>=4.2.0
```

### Option 3: Via environment.yml

If you're managing packages via environment.yml:

```yaml
dependencies:
  - nbformat>=4.2.0
  - jupyter>=1.0.0
  - ipykernel>=6.25.0
  - plotly>=5.18.0
```

---

## For Local Jupyter Notebooks

```bash
pip install nbformat>=4.2.0
```

Or add to `requirements.txt`:
```
nbformat>=4.2.0
```

---

## Why This Happens

- **Plotly** needs `nbformat` to render interactive visualizations in notebooks
- `nbformat` provides the MIME type rendering for Jupyter notebooks
- Snowflake Notebooks use Jupyter under the hood, so they need it too

---

## Verify Installation

After installing, verify it works:

```python
import nbformat
print(f"nbformat version: {nbformat.__version__}")
```

Should show version 4.2.0 or higher.

---

## Alternative: Use Static Images

If you can't install packages, use static images instead:

```python
# Instead of:
fig.show()

# Use:
fig.write_image("chart.png")  # Requires kaleido
# or
import plotly.io as pio
pio.renderers.default = "png"
fig.show()
```

---

## Required Packages for Analytics Notebook

The `01_ghost_analytics.ipynb` notebook requires:

| Package | Purpose | Installation |
|---------|---------|--------------|
| `nbformat` | Notebook rendering | **Add this** |
| `plotly` | Interactive charts | Usually included |
| `pandas` | Data processing | Auto-included |
| `numpy` | Numerical operations | Auto-included |
| `jupyter` | Notebook environment | Usually included |
| `ipykernel` | Python kernel | Usually included |

---

## Still Having Issues?

1. **Check Python version:** Must be 3.8 or higher
2. **Restart kernel:** Sometimes needed after installing packages
3. **Check package conflicts:** Make sure no conflicting versions
4. **Try fresh notebook:** Create a new notebook and test

---

## For Production

Update your `environment.yml`:

```yaml
name: snowghost_breakers
channels:
  - snowflake
  - conda-forge
dependencies:
  - python=3.10
  - plotly>=5.18.0
  - nbformat>=4.2.0  # ADD THIS LINE
  - jupyter>=1.0.0
  - ipykernel>=6.25.0
```

Then deploy with the updated environment.

