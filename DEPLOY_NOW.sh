#!/bin/bash

# ============================================
# SnowGhost Breakers v2.1 - Quick Deployment
# Reports, Maps & Global Offices Edition
# ============================================

echo "🚀 Deploying SnowGhost Breakers v2.1..."
echo ""

# Step 1: Load Global Offices
echo "📍 Step 1/3: Loading 27 global offices..."
snowsql -f sql/13_offices_table.sql

if [ $? -eq 0 ]; then
    echo "✅ Offices loaded successfully!"
else
    echo "❌ Error loading offices. Check your Snowflake connection."
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
echo "✅ Deployment Complete!"
echo "============================================"
echo ""
echo "🎯 New Features Available:"
echo "  📊 6 Comprehensive Reports"
echo "  🗺️ 3 Interactive Maps"
echo "  🏢 27 Global Offices"
echo "  📧 Updated Email Domain"
echo ""
echo "📍 Quick Access:"
echo "  - Reports: Click '📑 Reports'"
echo "  - Sightings Map: Click '📍 Sightings'"
echo "  - Investigations Map: Click '📋 Investigations'"
echo "  - Global Offices: Click '🏢 Global Offices'"
echo ""
echo "📚 Documentation:"
echo "  - Complete Guide: COMPREHENSIVE_REPORTS_GUIDE.md"
echo "  - Quick Start: REPORTS_QUICK_START.md"
echo "  - Maps & Offices: MAPS_AND_OFFICES_FIX.md"
echo "  - Summary: SESSION_COMPLETE_SUMMARY.md"
echo ""
echo "🌐 Streamlit should open automatically in your browser"
echo "   If not, visit: http://localhost:8501"
echo ""
echo "🎉 Happy Ghost Hunting! 👻🚫"

