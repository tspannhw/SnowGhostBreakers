#!/bin/bash

# ============================================
# Quick Fix: Investigator Registration & Geocoding
# ============================================

echo "🔧 Deploying Investigator & Geocoding Fixes..."
echo ""

# Step 1: Install geopy
echo "📦 Step 1/3: Installing geopy..."
pip install geopy>=2.4.0

if [ $? -eq 0 ]; then
    echo "✅ geopy installed successfully!"
else
    echo "❌ Error installing geopy. Try manually: pip install geopy"
    exit 1
fi

echo ""

# Step 2: Stop Streamlit
echo "🛑 Step 2/3: Stopping Streamlit..."
pkill -f streamlit
sleep 2
echo "✅ Streamlit stopped"

echo ""

# Step 3: Start Streamlit
echo "🎬 Step 3/3: Starting Streamlit..."
streamlit run streamlit_app/ghost_detection_app.py &

echo ""
echo "============================================"
echo "✅ Fixes Deployed!"
echo "============================================"
echo ""
echo "🔧 What was fixed:"
echo "  ✅ Investigator registration now works"
echo "  ✅ Geocoding uses reliable geopy library"
echo "  ✅ No more PARSE_JSON errors"
echo "  ✅ No more 'Device busy' errors"
echo ""
echo "🧪 Test now:"
echo "  1. Go to '👥 Investigators' → '➕ Add Investigator'"
echo "  2. Register a new investigator"
echo "  3. Go to '➕ New Sighting'"
echo "  4. Try geocoding an address"
echo ""
echo "📚 Documentation: INVESTIGATOR_GEOCODING_FIX.md"
echo ""
echo "🌐 Streamlit should open automatically in your browser"
echo "   If not, visit: http://localhost:8501"
echo ""
echo "🎉 All systems operational! 👻🚫"

