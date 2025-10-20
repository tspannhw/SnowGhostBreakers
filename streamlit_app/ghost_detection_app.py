"""
Ghost Detection and Analysis Application
Streamlit Application for Snowflake

Required packages (for Snowflake Streamlit):
- snowflake-snowpark-python (auto-included)
- pandas (auto-included)
- plotly
- nbformat
- geopy
"""

# When deploying to Snowflake, ensure these packages are available:
# CREATE STREAMLIT ghost_detection_app
# ROOT_LOCATION = '@ghost_detection.app.streamlit_stage'
# MAIN_FILE = 'ghost_detection_app.py'
# QUERY_WAREHOUSE = 'COMPUTE_WH'
# EXTERNAL_ACCESS_INTEGRATIONS = ()
# PACKAGES = ('snowflake-snowpark-python', 'pandas', 'plotly');

import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import functions as F
from snowflake.cortex import Complete, Sentiment
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="👻 Ghost Detection System",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .threat-extreme {
        color: #dc2626;
        font-weight: bold;
    }
    .threat-high {
        color: #ea580c;
        font-weight: bold;
    }
    .threat-medium {
        color: #ca8a04;
        font-weight: bold;
    }
    .threat-low {
        color: #16a34a;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session
@st.cache_resource
def get_session():
    return get_active_session()

session = get_session()

# Header
st.markdown('<div class="main-header">👻 Ghost Detection & Analysis System</div>', unsafe_allow_html=True)
st.markdown("### *Powered by Snowflake Cortex AI*")
st.markdown("---")

# Sidebar navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio(
    "Select View",
    ["📊 Dashboard", "👻 Ghost Registry", "📍 Sightings", "🔬 Evidence Analysis", 
     "📋 Investigations", "👥 Investigators", "🏢 Global Offices", "🤖 AI Insights", 
     "➕ New Sighting", "📈 Analytics", "📑 Reports", "📚 Vocabulary", "🔍 Image Similarity",
     "💬 SnowBreakers Chat"]
)

# Sidebar filters
st.sidebar.markdown("---")
st.sidebar.subheader("🎛️ Filters")

# Get data for filters
ghost_types_df = session.table("GHOST_DETECTION.APP.GHOSTS").select("GHOST_TYPE").distinct().collect()
ghost_types = ["All"] + [row["GHOST_TYPE"] for row in ghost_types_df]
selected_ghost_type = st.sidebar.selectbox("Ghost Type", ghost_types)

threat_levels = ["All", "Extreme", "High", "Medium", "Low"]
selected_threat = st.sidebar.selectbox("Threat Level", threat_levels)

date_range = st.sidebar.date_input(
    "Date Range",
    value=(datetime.now() - timedelta(days=30), datetime.now()),
    max_value=datetime.now()
)

# ============================================
# PAGE: DASHBOARD
# ============================================
if page == "📊 Dashboard":
    st.header("📊 Ghost Activity Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_ghosts = session.table("GHOST_DETECTION.APP.GHOSTS").count()
        st.metric("👻 Total Ghosts", total_ghosts)
    
    with col2:
        active_ghosts = session.table("GHOST_DETECTION.APP.GHOSTS").filter(
            F.col("STATUS") == "Active"
        ).count()
        st.metric("⚡ Active Ghosts", active_ghosts)
    
    with col3:
        total_sightings = session.table("GHOST_DETECTION.APP.GHOST_SIGHTINGS").count()
        st.metric("📍 Total Sightings", total_sightings)
    
    with col4:
        open_cases = session.table("GHOST_DETECTION.APP.INVESTIGATIONS").filter(
            F.col("STATUS").in_(["Open", "In_Progress"])
        ).count()
        st.metric("📋 Open Cases", open_cases)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ghost Types Distribution")
        ghost_type_df = session.table("GHOST_DETECTION.APP.GHOSTS").group_by("GHOST_TYPE").count().to_pandas()
        fig = px.pie(ghost_type_df, values='COUNT', names='GHOST_TYPE', 
                     color_discrete_sequence=px.colors.sequential.Purples_r)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Threat Level Distribution")
        threat_df = session.table("GHOST_DETECTION.APP.GHOSTS").group_by("THREAT_LEVEL").count().to_pandas()
        colors = {'Extreme': '#dc2626', 'High': '#ea580c', 'Medium': '#ca8a04', 'Low': '#16a34a'}
        fig = px.bar(threat_df, x='THREAT_LEVEL', y='COUNT', color='THREAT_LEVEL',
                     color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # Activity timeline
    st.subheader("📈 Sighting Activity Timeline")
    timeline_df = session.table("GHOST_DETECTION.ANALYTICS.VW_ACTIVITY_TIMELINE").limit(30).to_pandas()
    fig = px.line(timeline_df, x='ACTIVITY_DATE', y='DAILY_SIGHTINGS', 
                  title='Daily Ghost Sightings (Last 30 Days)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Hotspots map
    st.subheader("🗺️ Paranormal Hotspots")
    try:
        hotspots_df = session.table("GHOST_DETECTION.ANALYTICS.VW_PARANORMAL_HOTSPOTS").to_pandas()
        
        if hotspots_df.empty:
            st.info("ℹ️ No hotspot data available yet. Add sightings with coordinates first.")
        elif 'LATITUDE' not in hotspots_df.columns or 'LONGITUDE' not in hotspots_df.columns:
            st.warning("⚠️ Coordinate columns missing. Check VW_PARANORMAL_HOTSPOTS view.")
        else:
            # Clean and validate coordinates
            hotspots_valid = hotspots_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
            hotspots_valid['LATITUDE'] = pd.to_numeric(hotspots_valid['LATITUDE'], errors='coerce')
            hotspots_valid['LONGITUDE'] = pd.to_numeric(hotspots_valid['LONGITUDE'], errors='coerce')
            hotspots_valid = hotspots_valid.dropna(subset=['LATITUDE', 'LONGITUDE'])
            hotspots_valid = hotspots_valid[
                (hotspots_valid['LATITUDE'].between(-90, 90)) & 
                (hotspots_valid['LONGITUDE'].between(-180, 180))
            ]
            
            if hotspots_valid.empty:
                st.info("ℹ️ No valid coordinates found. Add latitude/longitude to your sightings.")
                st.code("UPDATE GHOST_SIGHTINGS SET latitude = 40.7128, longitude = -74.0060 WHERE ...", language="sql")
            else:
                st.success(f"✅ Found {len(hotspots_valid)} hotspots with coordinates")
                
                # Try Plotly scatter mapbox
                try:
                    fig = px.scatter_mapbox(
                        hotspots_valid,
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        size='TOTAL_SIGHTINGS' if 'TOTAL_SIGHTINGS' in hotspots_valid.columns else None,
                        color='HOTSPOT_CLASSIFICATION' if 'HOTSPOT_CLASSIFICATION' in hotspots_valid.columns else None,
                        hover_name='LOCATION_NAME' if 'LOCATION_NAME' in hotspots_valid.columns else None,
                        zoom=2,
                        height=500,
                        mapbox_style="open-street-map"
                    )
                    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as plotly_err:
                    # Fallback to Streamlit's simple map
                    st.info(f"📍 Using simple map (plotly: {str(plotly_err)[:50]}...)")
                    map_data = hotspots_valid[['LATITUDE', 'LONGITUDE']].copy()
                    map_data.columns = ['lat', 'lon']
                    st.map(map_data)
                
                # Show location details
                with st.expander("📋 View Hotspot Details"):
                    display_cols = [c for c in ['LOCATION_NAME', 'LATITUDE', 'LONGITUDE', 'TOTAL_SIGHTINGS', 'UNIQUE_GHOSTS'] 
                                   if c in hotspots_valid.columns]
                    st.dataframe(hotspots_valid[display_cols], use_container_width=True)
    except Exception as e:
        st.error(f"❌ Map error: {str(e)}")
        st.info("💡 Make sure VW_PARANORMAL_HOTSPOTS view exists with LATITUDE and LONGITUDE columns")

# ============================================
# PAGE: GHOST REGISTRY
# ============================================
elif page == "👻 Ghost Registry":
    st.header("👻 Ghost Registry")
    
    # Build query with filters
    ghosts_query = session.table("GHOST_DETECTION.ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY")
    
    if selected_ghost_type != "All":
        ghosts_query = ghosts_query.filter(F.col("GHOST_TYPE") == selected_ghost_type)
    
    if selected_threat != "All":
        ghosts_query = ghosts_query.filter(F.col("THREAT_LEVEL") == selected_threat)
    
    ghosts_df = ghosts_query.to_pandas()
    
    # Display count
    st.write(f"**Total Ghosts: {len(ghosts_df)}**")
    
    # Display ghosts as cards
    for idx, row in ghosts_df.iterrows():
        with st.expander(f"👻 {row['GHOST_NAME']} - {row['GHOST_TYPE']}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                threat_class = f"threat-{row['THREAT_LEVEL'].lower()}"
                st.markdown(f"**Threat Level:** <span class='{threat_class}'>{row['THREAT_LEVEL']}</span>", 
                           unsafe_allow_html=True)
                st.write(f"**Status:** {row['STATUS']}")
                st.write(f"**Confidence:** {row['CONFIDENCE_SCORE']:.2%}")
            
            with col2:
                st.write(f"**Total Sightings:** {row['TOTAL_SIGHTINGS']}")
                st.write(f"**Evidence Count:** {row['EVIDENCE_COUNT']}")
                st.write(f"**Active Days:** {row['ACTIVITY_DURATION_DAYS']}")
            
            with col3:
                st.write(f"**Avg Activity Level:** {row['AVG_PARANORMAL_LEVEL']:.1f}/10")
                st.write(f"**Avg EMF:** {row['AVG_EMF_READING']:.1f} mG")
                st.write(f"**Unique Locations:** {row['UNIQUE_LOCATIONS']}")
            
            st.write(f"**Haunted Locations:** {row['HAUNTED_LOCATIONS']}")
            
            # Generate AI report button
            if st.button(f"📄 Generate Report", key=f"report_{row['GHOST_ID']}"):
                with st.spinner("Generating AI report..."):
                    result = session.call("GHOST_DETECTION.APP.GENERATE_GHOST_REPORT", row['GHOST_ID'])
                    st.markdown("#### 📄 AI-Generated Report")
                    st.write(result)

# ============================================
# PAGE: SIGHTINGS
# ============================================
elif page == "📍 Sightings":
    st.header("📍 Ghost Sightings")
    
    # Query sightings with proper column disambiguation
    sightings_table = session.table("GHOST_DETECTION.APP.GHOST_SIGHTINGS")
    ghosts_table = session.table("GHOST_DETECTION.APP.GHOSTS")
    
    sightings_query = sightings_table.join(
        ghosts_table,
        sightings_table["GHOST_ID"] == ghosts_table["GHOST_ID"]
    )
    
    # Apply filters
    if selected_ghost_type != "All":
        sightings_query = sightings_query.filter(ghosts_table["GHOST_TYPE"] == selected_ghost_type)
    
    if selected_threat != "All":
        sightings_query = sightings_query.filter(ghosts_table["THREAT_LEVEL"] == selected_threat)
    
    # Select with explicit aliases to avoid any ambiguity
    sightings_df = sightings_query.select(
        sightings_table["SIGHTING_ID"].alias("SIGHTING_ID"), 
        ghosts_table["GHOST_NAME"].alias("GHOST_NAME"), 
        ghosts_table["GHOST_TYPE"].alias("GHOST_TYPE"), 
        ghosts_table["DESCRIPTION"].alias("GHOST_DESCRIPTION"),
        sightings_table["LOCATION_NAME"].alias("LOCATION_NAME"), 
        sightings_table["SIGHTING_DATETIME"].alias("SIGHTING_DATETIME"), 
        sightings_table["PARANORMAL_ACTIVITY_LEVEL"].alias("PARANORMAL_ACTIVITY_LEVEL"), 
        sightings_table["EMF_READING"].alias("EMF_READING"),
        sightings_table["TEMPERATURE_CELSIUS"].alias("TEMPERATURE_CELSIUS"), 
        sightings_table["VERIFIED"].alias("VERIFIED")
    ).order_by(sightings_table["SIGHTING_DATETIME"].desc()).limit(100).to_pandas()
    
    st.write(f"**Showing {len(sightings_df)} recent sightings**")
    
    # Add map view for sightings with location data
    st.markdown("---")
    st.subheader("🗺️ Sightings Map")
    
    # Query sightings with coordinates
    map_query = """
    SELECT 
        s.LOCATION_NAME,
        s.LATITUDE,
        s.LONGITUDE,
        g.GHOST_NAME,
        g.GHOST_TYPE,
        s.SIGHTING_DATETIME,
        s.PARANORMAL_ACTIVITY_LEVEL
    FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS s
    JOIN GHOST_DETECTION.APP.GHOSTS g ON s.GHOST_ID = g.GHOST_ID
    WHERE s.LATITUDE IS NOT NULL 
      AND s.LONGITUDE IS NOT NULL
      AND s.LATITUDE BETWEEN -90 AND 90
      AND s.LONGITUDE BETWEEN -180 AND 180
    ORDER BY s.SIGHTING_DATETIME DESC
    LIMIT 100
    """
    
    try:
        map_df = session.sql(map_query).to_pandas()
        
        if map_df.empty:
            st.info("ℹ️ No sightings with coordinates found. Add latitude/longitude to your sightings!")
            st.code("UPDATE GHOST_DETECTION.APP.GHOST_SIGHTINGS SET latitude = 40.7128, longitude = -74.0060 WHERE ...", language="sql")
        else:
            # Filter and validate coordinates
            map_df_valid = map_df.dropna(subset=['LATITUDE', 'LONGITUDE']).copy()
            map_df_valid['LATITUDE'] = pd.to_numeric(map_df_valid['LATITUDE'], errors='coerce')
            map_df_valid['LONGITUDE'] = pd.to_numeric(map_df_valid['LONGITUDE'], errors='coerce')
            map_df_valid = map_df_valid.dropna(subset=['LATITUDE', 'LONGITUDE'])
            
            st.success(f"✅ Found {len(map_df_valid)} sightings with valid coordinates")
            
            if not map_df_valid.empty:
                # Calculate center point for better map positioning
                center_lat = map_df_valid['LATITUDE'].mean()
                center_lon = map_df_valid['LONGITUDE'].mean()
                
                # Method 1: Try Plotly Scattermapbox
                try:
                    fig = px.scatter_mapbox(
                        map_df_valid,
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        size='PARANORMAL_ACTIVITY_LEVEL',
                        color='GHOST_TYPE',
                        hover_name='LOCATION_NAME',
                        hover_data={
                            'GHOST_NAME': True, 
                            'GHOST_TYPE': True, 
                            'SIGHTING_DATETIME': True, 
                            'PARANORMAL_ACTIVITY_LEVEL': True,
                            'LATITUDE': False, 
                            'LONGITUDE': False
                        },
                        zoom=3,  # Start zoomed out to see all markers
                        height=600,
                        center={"lat": center_lat, "lon": center_lon},
                        title=f"Recent Ghost Sightings ({len(map_df_valid)} locations)"
                    )
                    
                    # Use open-street-map style (no token required)
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":40,"l":0,"b":0}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as plotly_error:
                    # Fallback to Streamlit's built-in map
                    st.info(f"📍 Using simple map view (plotly: {str(plotly_error)[:50]}...)")
                    try:
                        simple_map_df = map_df_valid[['LATITUDE', 'LONGITUDE']].copy()
                        simple_map_df.columns = ['lat', 'lon']
                        st.map(simple_map_df, zoom=3)
                        
                        # Show location details
                        with st.expander("📋 View Sighting Details"):
                            for idx, row in map_df_valid.iterrows():
                                st.write(f"📍 **{row['LOCATION_NAME']}** - {row['GHOST_NAME']} ({row['GHOST_TYPE']}) - Activity: {row['PARANORMAL_ACTIVITY_LEVEL']}/10")
                    
                    except Exception as simple_error:
                        # Final fallback: show as table
                        st.warning(f"⚠️ Map display failed. Showing coordinates as table.")
                        display_df = map_df_valid[['LOCATION_NAME', 'GHOST_NAME', 'GHOST_TYPE', 'LATITUDE', 'LONGITUDE', 'PARANORMAL_ACTIVITY_LEVEL']]
                        st.dataframe(display_df, use_container_width=True)
            else:
                st.info("ℹ️ No valid coordinates after filtering. Check data quality.")
    
    except Exception as e:
        st.error(f"❌ Error loading map: {str(e)}")
        st.info("💡 Make sure GHOST_SIGHTINGS table exists with LATITUDE and LONGITUDE columns.")
    
    st.markdown("---")
    
    # Display sightings list
    st.subheader("📋 Sightings List")
    for idx, row in sightings_df.iterrows():
        # Convert Celsius to Fahrenheit
        temp_f = (row['TEMPERATURE_CELSIUS'] * 9/5) + 32
        
        with st.expander(
            f"📍 {row['LOCATION_NAME']} - {row['GHOST_NAME']} "
            f"({row['SIGHTING_DATETIME'].strftime('%Y-%m-%d %H:%M')})"
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Ghost:** {row['GHOST_NAME']} ({row['GHOST_TYPE']})")
                if pd.notna(row.get('GHOST_DESCRIPTION')):
                    st.write(f"**About Ghost:** {row['GHOST_DESCRIPTION']}")
            
            with col2:
                st.metric("Activity Level", f"{row['PARANORMAL_ACTIVITY_LEVEL']}/10")
                st.metric("EMF Reading", f"{row['EMF_READING']:.1f} mG")
                st.metric("Temperature", f"{temp_f:.1f}°F ({row['TEMPERATURE_CELSIUS']:.1f}°C)")
                
                verified_icon = "✅" if row['VERIFIED'] else "⏳"
                st.write(f"**Verified:** {verified_icon}")

# ============================================
# PAGE: EVIDENCE ANALYSIS
# ============================================
elif page == "🔬 Evidence Analysis":
    st.header("🔬 Evidence Analysis")
    
    evidence_df = session.table("GHOST_DETECTION.ANALYTICS.VW_EVIDENCE_ANALYSIS").to_pandas()
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Evidence", len(evidence_df))
    
    with col2:
        analyzed = len(evidence_df[evidence_df['PROCESSING_STATUS'] == 'Analyzed'])
        st.metric("Analyzed", analyzed)
    
    with col3:
        avg_confidence = evidence_df['CONFIDENCE_SCORE'].mean()
        st.metric("Avg Confidence", f"{avg_confidence:.2%}")
    
    with col4:
        anomalies = evidence_df['ANOMALY_DETECTED'].sum()
        st.metric("Anomalies Found", int(anomalies))
    
    st.markdown("---")
    
    # Evidence type distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Evidence Types")
        evidence_type_counts = evidence_df['EVIDENCE_TYPE'].value_counts().reset_index()
        evidence_type_counts.columns = ['Evidence Type', 'Count']
        fig = px.bar(evidence_type_counts, x='Evidence Type', y='Count',
                     title="Evidence Distribution by Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Analysis Models Used")
        model_counts = evidence_df['MODEL_USED'].value_counts()
        fig = px.pie(values=model_counts.values, names=model_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    
    # Evidence list
    st.subheader("📋 Evidence Records")
    
    for idx, row in evidence_df.iterrows():
        if pd.notna(row['AI_SUMMARY']):
            with st.expander(f"🔬 {row['EVIDENCE_TYPE']} - {row['GHOST_NAME']} - {row['LOCATION_NAME']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**AI Analysis Summary:**")
                    st.info(row['AI_SUMMARY'])
                    st.write(f"**Model:** {row['MODEL_USED']}")
                    st.write(f"**Analysis Type:** {row['ANALYSIS_TYPE']}")
                
                with col2:
                    st.metric("Confidence", f"{row['CONFIDENCE_SCORE']:.2%}")
                    anomaly_icon = "⚠️" if row['ANOMALY_DETECTED'] else "✅"
                    st.write(f"**Anomaly:** {anomaly_icon}")
                    st.write(f"**Processing Time:** {row['PROCESSING_TIME_MINUTES']:.0f} min")

# ============================================
# PAGE: INVESTIGATIONS
# ============================================
elif page == "📋 Investigations":
    st.header("📋 Active Investigations")
    
    investigations_df = session.table("GHOST_DETECTION.ANALYTICS.VW_INVESTIGATION_METRICS").to_pandas()
    
    # Add Investigation Locations Map
    st.markdown("---")
    st.subheader("🗺️ Investigation Locations Map")
    
    inv_map_query = """
    SELECT 
        i.CASE_NAME,
        gs.LOCATION_NAME,
        gs.LATITUDE,
        gs.LONGITUDE,
        g.GHOST_NAME,
        g.THREAT_LEVEL,
        i.STATUS,
        i.PRIORITY
    FROM GHOST_DETECTION.APP.INVESTIGATIONS i
    JOIN GHOST_DETECTION.APP.GHOSTS g ON i.GHOST_ID = g.GHOST_ID
    JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS gs ON g.GHOST_ID = gs.GHOST_ID
    WHERE gs.LATITUDE IS NOT NULL 
      AND gs.LONGITUDE IS NOT NULL
      AND gs.LATITUDE BETWEEN -90 AND 90
      AND gs.LONGITUDE BETWEEN -180 AND 180
      AND i.STATUS IN ('Open', 'In_Progress')
    ORDER BY i.START_DATE DESC
    LIMIT 100
    """
    
    try:
        inv_map_df = session.sql(inv_map_query).to_pandas()
        
        if not inv_map_df.empty:
            inv_map_valid = inv_map_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
            
            if not inv_map_valid.empty:
                st.write(f"📊 Found {len(inv_map_valid)} active investigation locations")
                
                try:
                    center_lat = inv_map_valid['LATITUDE'].mean()
                    center_lon = inv_map_valid['LONGITUDE'].mean()
                    
                    fig = px.scatter_mapbox(
                        inv_map_valid,
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        color='PRIORITY',
                        size_max=15,
                        hover_name='CASE_NAME',
                        hover_data={
                            'LOCATION_NAME': True,
                            'GHOST_NAME': True,
                            'THREAT_LEVEL': True,
                            'STATUS': True,
                            'PRIORITY': True,
                            'LATITUDE': False,
                            'LONGITUDE': False
                        },
                        zoom=3,
                        height=500,
                        center={"lat": center_lat, "lon": center_lon},
                        title=f"Active Investigations Map ({len(inv_map_valid)} locations)",
                        color_discrete_map={
                            'Critical': '#dc2626',
                            'High': '#f59e0b',
                            'Medium': '#eab308',
                            'Low': '#22c55e'
                        }
                    )
                    
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":40,"l":0,"b":0}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Investigation map loaded successfully!")
                    
                except Exception as map_error:
                    st.warning(f"⚠️ Map visualization error: {str(map_error)}")
                    st.info("🔄 Showing locations as table...")
                    st.dataframe(inv_map_valid[['CASE_NAME', 'LOCATION_NAME', 'GHOST_NAME', 'THREAT_LEVEL', 'STATUS', 'PRIORITY', 'LATITUDE', 'LONGITUDE']])
            else:
                st.info("ℹ️ No investigation locations with valid coordinates.")
        else:
            st.info("ℹ️ No active investigations with location data found.")
            
    except Exception as e:
        st.error(f"❌ Error loading investigation map: {str(e)}")
        st.info("💡 Make sure INVESTIGATIONS and GHOST_SIGHTINGS tables have data with coordinates.")
    
    st.markdown("---")
    
    # Status filter tabs
    status_filter = st.radio("Filter by Status", ["All", "Open", "In_Progress", "Closed"], horizontal=True)
    
    if status_filter != "All":
        investigations_df = investigations_df[investigations_df['STATUS'] == status_filter]
    
    # Priority indicators
    priority_colors = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
    
    for idx, row in investigations_df.iterrows():
        priority_icon = priority_colors.get(row['PRIORITY'], '⚪')
        
        with st.expander(
            f"{priority_icon} {row['CASE_NAME']} - {row['STATUS']}"
        ):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Ghost:** {row['GHOST_NAME']}")
                st.write(f"**Type:** {row['GHOST_TYPE']}")
                st.write(f"**Threat:** {row['THREAT_LEVEL']}")
            
            with col2:
                st.write(f"**Lead:** {row['LEAD_INVESTIGATOR']}")
                st.write(f"**Specialization:** {row['SPECIALIZATION']}")
                st.write(f"**Duration:** {row['INVESTIGATION_DURATION_DAYS']} days")
            
            with col3:
                st.write(f"**Evidence:** {row['EVIDENCE_COUNT']} items")
                st.write(f"**Sightings:** {row['SIGHTING_COUNT']}")
                st.write(f"**Analyses:** {row['ANALYSIS_COUNT']}")
            
            # Generate summary button
            if st.button("📄 Generate Summary", key=f"summary_{row['INVESTIGATION_ID']}"):
                with st.spinner("Generating investigation summary..."):
                    summary = session.call(
                        "GHOST_DETECTION.APP.GENERATE_INVESTIGATION_SUMMARY",
                        row['INVESTIGATION_ID']
                    )
                    st.markdown("#### 📄 Investigation Summary")
                    st.write(summary)

# ============================================
# PAGE: INVESTIGATORS
# ============================================
elif page == "👥 Investigators":
    st.header("👥 Paranormal Investigators")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["📋 Team Roster", "➕ Add Investigator", "📊 Statistics"])
    
    # TAB 1: Team Roster
    with tab1:
        st.subheader("🔍 Active Investigation Team")
        
        # Fetch investigators
        investigators_query = """
        SELECT 
            investigator_id,
            investigator_name,
            email,
            phone,
            specialization,
            experience_years,
            cases_solved,
            active_status,
            created_at
        FROM GHOST_DETECTION.APP.INVESTIGATORS
        ORDER BY active_status DESC, cases_solved DESC
        """
        
        try:
            investigators_df = session.sql(investigators_query).to_pandas()
            
            if not investigators_df.empty:
                # Filter controls
                col1, col2 = st.columns(2)
                with col1:
                    status_filter = st.selectbox(
                        "Status Filter",
                        ["All", "Active Only", "Inactive Only"]
                    )
                with col2:
                    spec_filter = st.selectbox(
                        "Specialization Filter",
                        ["All"] + sorted(investigators_df['SPECIALIZATION'].unique().tolist())
                    )
                
                # Apply filters
                filtered_df = investigators_df.copy()
                if status_filter == "Active Only":
                    filtered_df = filtered_df[filtered_df['ACTIVE_STATUS'] == True]
                elif status_filter == "Inactive Only":
                    filtered_df = filtered_df[filtered_df['ACTIVE_STATUS'] == False]
                
                if spec_filter != "All":
                    filtered_df = filtered_df[filtered_df['SPECIALIZATION'] == spec_filter]
                
                st.markdown(f"**Showing {len(filtered_df)} of {len(investigators_df)} investigators**")
                
                # Display investigators
                for idx, inv in filtered_df.iterrows():
                    status_icon = "✅" if inv['ACTIVE_STATUS'] else "⏸️"
                    
                    with st.expander(
                        f"{status_icon} {inv['INVESTIGATOR_NAME']} - {inv['SPECIALIZATION']} "
                        f"({inv['CASES_SOLVED']} cases solved)"
                    ):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.write(f"**ID:** `{inv['INVESTIGATOR_ID']}`")
                            st.write(f"**Name:** {inv['INVESTIGATOR_NAME']}")
                            st.write(f"**Specialization:** {inv['SPECIALIZATION']}")
                        
                        with col2:
                            st.write(f"**Email:** {inv['EMAIL']}")
                            st.write(f"**Phone:** {inv['PHONE']}")
                            st.write(f"**Experience:** {inv['EXPERIENCE_YEARS']} years")
                        
                        with col3:
                            st.write(f"**Cases Solved:** {inv['CASES_SOLVED']}")
                            st.write(f"**Status:** {'Active' if inv['ACTIVE_STATUS'] else 'Inactive'}")
                            st.write(f"**Joined:** {inv['CREATED_AT'].strftime('%Y-%m-%d') if pd.notna(inv['CREATED_AT']) else 'N/A'}")
            else:
                st.info("No investigators found. Add your first investigator in the 'Add Investigator' tab!")
                
        except Exception as e:
            st.error(f"Error loading investigators: {str(e)}")
    
    # TAB 2: Add New Investigator
    with tab2:
        st.subheader("➕ Register New Investigator")
        st.markdown("*Add a new paranormal investigator to the team*")
        
        with st.form("new_investigator_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                investigator_name = st.text_input(
                    "Full Name*",
                    placeholder="e.g., Dr. Jane Smith",
                    help="Investigator's full name"
                )
                
                email = st.text_input(
                    "Email Address*",
                    placeholder="jane.smith@snowghostbreakers.com",
                    help="Professional email address"
                )
                
                phone = st.text_input(
                    "Phone Number",
                    placeholder="+1-555-0123",
                    help="Contact phone number"
                )
            
            with col2:
                specialization = st.selectbox(
                    "Specialization*",
                    [
                        "Lead Investigator",
                        "EMF Expert",
                        "Medium/Psychic",
                        "Technician",
                        "EVP Specialist",
                        "Demonologist",
                        "Historian",
                        "Field Researcher",
                        "Data Analyst"
                    ],
                    help="Primary area of expertise"
                )
                
                experience_years = st.number_input(
                    "Years of Experience*",
                    min_value=0,
                    max_value=50,
                    value=1,
                    help="Years in paranormal investigation"
                )
                
                active_status = st.checkbox(
                    "Active Status",
                    value=True,
                    help="Is this investigator currently active?"
                )
            
            st.markdown("---")
            
            # Additional notes
            notes = st.text_area(
                "Notes (Optional)",
                placeholder="Any additional information about certifications, achievements, or special skills...",
                height=100
            )
            
            submitted = st.form_submit_button("👥 Register Investigator", use_container_width=True)
            
            if submitted:
                if investigator_name and email and specialization:
                    import uuid
                    
                    investigator_id = f"INV_{str(uuid.uuid4())[:8].upper()}"
                    
                    with st.spinner("🤖 Registering investigator..."):
                        try:
                            # Insert into database
                            insert_sql = f"""
                            INSERT INTO GHOST_DETECTION.APP.INVESTIGATORS (
                                investigator_id,
                                investigator_name,
                                email,
                                phone,
                                specialization,
                                experience_years,
                                cases_solved,
                                active_status,
                                created_at
                            ) VALUES (
                                '{investigator_id}',
                                '{investigator_name.replace("'", "''")}',
                                '{email.replace("'", "''")}',
                                '{phone.replace("'", "''") if phone else ""}',
                                '{specialization}',
                                {experience_years},
                                0,
                                {str(active_status).upper()},
                                CURRENT_TIMESTAMP()
                            )
                            """
                            
                            session.sql(insert_sql).collect()
                            
                            # Log to audit table
                            audit_id = f"AUDIT_{str(uuid.uuid4())[:8].upper()}"
                            audit_sql = f"""
                            INSERT INTO GHOST_DETECTION.APP.AUDIT_LOG (
                                log_id,
                                table_name,
                                record_id,
                                action,
                                user_name,
                                action_datetime,
                                new_values
                            )
                            SELECT 
                                '{audit_id}',
                                'INVESTIGATORS',
                                '{investigator_id}',
                                'INSERT',
                                CURRENT_USER(),
                                CURRENT_TIMESTAMP(),
                                PARSE_JSON('{{"investigator_name": "{investigator_name}", "specialization": "{specialization}", "experience_years": {experience_years}}}')
                            """
                            
                            session.sql(audit_sql).collect()
                            
                            st.success("✅ Investigator registered successfully!")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Investigator ID", investigator_id)
                            with col2:
                                st.metric("Specialization", specialization)
                            with col3:
                                st.metric("Status", "Active" if active_status else "Inactive")
                            
                            st.info(f"👤 **{investigator_name}** has been added to the team!")
                            
                            if notes:
                                st.text_area("📝 Notes", notes, disabled=True)
                            
                            st.balloons()
                            
                        except Exception as e:
                            st.error(f"Error registering investigator: {str(e)}")
                            with st.expander("Debug Info"):
                                st.code(str(e))
                else:
                    st.error("Please fill in all required fields marked with *")
    
    # TAB 3: Statistics
    with tab3:
        st.subheader("📊 Team Statistics")
        
        try:
            # Overall stats
            stats_query = """
            SELECT 
                COUNT(*) as total_investigators,
                SUM(CASE WHEN active_status = TRUE THEN 1 ELSE 0 END) as active_count,
                SUM(cases_solved) as total_cases_solved,
                ROUND(AVG(experience_years), 1) as avg_experience,
                COUNT(DISTINCT specialization) as specialization_count
            FROM GHOST_DETECTION.APP.INVESTIGATORS
            """
            
            stats = session.sql(stats_query).to_pandas().iloc[0]
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Team", int(stats['TOTAL_INVESTIGATORS']))
            with col2:
                st.metric("Active", int(stats['ACTIVE_COUNT']))
            with col3:
                st.metric("Cases Solved", int(stats['TOTAL_CASES_SOLVED']))
            with col4:
                st.metric("Avg Experience", f"{stats['AVG_EXPERIENCE']}y")
            with col5:
                st.metric("Specializations", int(stats['SPECIALIZATION_COUNT']))
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Specialization distribution
                spec_query = """
                SELECT 
                    specialization,
                    COUNT(*) as count
                FROM GHOST_DETECTION.APP.INVESTIGATORS
                WHERE active_status = TRUE
                GROUP BY specialization
                ORDER BY count DESC
                """
                
                spec_df = session.sql(spec_query).to_pandas()
                
                if not spec_df.empty:
                    fig = px.pie(
                        spec_df,
                        values='COUNT',
                        names='SPECIALIZATION',
                        title='Team Composition by Specialization'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Top performers
                top_query = """
                SELECT 
                    investigator_name,
                    cases_solved,
                    specialization
                FROM GHOST_DETECTION.APP.INVESTIGATORS
                WHERE active_status = TRUE
                ORDER BY cases_solved DESC
                LIMIT 10
                """
                
                top_df = session.sql(top_query).to_pandas()
                
                if not top_df.empty:
                    fig = px.bar(
                        top_df,
                        x='CASES_SOLVED',
                        y='INVESTIGATOR_NAME',
                        color='SPECIALIZATION',
                        title='Top 10 Investigators by Cases Solved',
                        orientation='h'
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # Experience distribution
            exp_query = """
            SELECT 
                CASE 
                    WHEN experience_years < 2 THEN 'Novice (0-1y)'
                    WHEN experience_years < 5 THEN 'Intermediate (2-4y)'
                    WHEN experience_years < 10 THEN 'Experienced (5-9y)'
                    WHEN experience_years < 20 THEN 'Veteran (10-19y)'
                    ELSE 'Master (20+y)'
                END as experience_level,
                COUNT(*) as count
            FROM GHOST_DETECTION.APP.INVESTIGATORS
            WHERE active_status = TRUE
            GROUP BY experience_level
            ORDER BY 
                CASE experience_level
                    WHEN 'Novice (0-1y)' THEN 1
                    WHEN 'Intermediate (2-4y)' THEN 2
                    WHEN 'Experienced (5-9y)' THEN 3
                    WHEN 'Veteran (10-19y)' THEN 4
                    ELSE 5
                END
            """
            
            exp_df = session.sql(exp_query).to_pandas()
            
            if not exp_df.empty:
                fig = px.bar(
                    exp_df,
                    x='EXPERIENCE_LEVEL',
                    y='COUNT',
                    title='Team Experience Distribution',
                    labels={'COUNT': 'Number of Investigators', 'EXPERIENCE_LEVEL': 'Experience Level'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")

# ============================================
# PAGE: GLOBAL OFFICES
# ============================================
elif page == "🏢 Global Offices":
    st.header("🏢 SnowGhost Breakers Global Offices")
    st.markdown("*Our worldwide network of paranormal investigation centers*")
    st.markdown("---")
    
    # Check if OFFICES table exists
    try:
        offices_df = session.table("GHOST_DETECTION.APP.OFFICES").to_pandas()
        
        if offices_df.empty:
            st.warning("⚠️ Offices table is empty. Please run: `sql/13_offices_table.sql`")
        else:
            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Total Offices", len(offices_df))
            with col2:
                st.metric("Active Offices", len(offices_df[offices_df['ACTIVE_STATUS'] == True]))
            with col3:
                st.metric("Regions", offices_df['REGION'].nunique())
            with col4:
                st.metric("Countries", offices_df['COUNTRY'].nunique())
            with col5:
                st.metric("Total Capacity", offices_df['CAPACITY'].sum())
            
            st.markdown("---")
            
            # Global offices map
            st.subheader("🗺️ Global Office Locations")
            
            offices_valid = offices_df.dropna(subset=['LATITUDE', 'LONGITUDE'])
            
            if not offices_valid.empty:
                try:
                    fig = px.scatter_mapbox(
                        offices_valid,
                        lat='LATITUDE',
                        lon='LONGITUDE',
                        size='CAPACITY',
                        color='OFFICE_TYPE',
                        hover_name='OFFICE_NAME',
                        hover_data={
                            'CITY': True,
                            'COUNTRY': True,
                            'REGION': True,
                            'CAPACITY': True,
                            'OFFICE_TYPE': True,
                            'LATITUDE': False,
                            'LONGITUDE': False
                        },
                        zoom=1,
                        height=600,
                        title=f"SnowGhost Breakers Global Network ({len(offices_valid)} offices)",
                        color_discrete_map={
                            'Headquarters': '#8b5cf6',
                            'Regional Office': '#3b82f6',
                            'Field Office': '#10b981'
                        },
                        size_max=30
                    )
                    
                    fig.update_layout(
                        mapbox_style="open-street-map",
                        margin={"r":0,"t":40,"l":0,"b":0}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("✅ Global office map loaded successfully!")
                    
                except Exception as map_error:
                    st.warning(f"⚠️ Map error: {str(map_error)}")
                    st.info("🔄 Showing offices as table...")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["🌎 By Region", "🏙️ All Offices", "📊 Statistics", "➕ Add Office"])
            
            with tab1:
                st.subheader("Offices by Region")
                
                region_filter = st.selectbox(
                    "Select Region",
                    ["All Regions"] + sorted(offices_df['REGION'].unique().tolist())
                )
                
                filtered_offices = offices_df if region_filter == "All Regions" else offices_df[offices_df['REGION'] == region_filter]
                
                # Group by region
                for region in sorted(filtered_offices['REGION'].unique()):
                    region_offices = filtered_offices[filtered_offices['REGION'] == region]
                    
                    with st.expander(f"🌍 {region} ({len(region_offices)} offices)"):
                        for idx, office in region_offices.iterrows():
                            st.markdown(f"### {office['OFFICE_NAME']}")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**📍 Location:** {office['CITY']}, {office['COUNTRY']}")
                                st.write(f"**🏢 Type:** {office['OFFICE_TYPE']}")
                                st.write(f"**👥 Capacity:** {office['CAPACITY']} investigators")
                            
                            with col2:
                                st.write(f"**🕐 Timezone:** {office['TIMEZONE']}")
                                if office['PHONE']:
                                    st.write(f"**📞 Phone:** {office['PHONE']}")
                                if office['EMAIL']:
                                    st.write(f"**📧 Email:** {office['EMAIL']}")
                            
                            with col3:
                                status_icon = "✅" if office['ACTIVE_STATUS'] else "❌"
                                st.write(f"**Status:** {status_icon} {'Active' if office['ACTIVE_STATUS'] else 'Inactive'}")
                                if office['OPENED_DATE']:
                                    st.write(f"**📅 Opened:** {office['OPENED_DATE']}")
                                if office['ADDRESS']:
                                    st.write(f"**📮 Address:** {office['ADDRESS']}")
                            
                            st.markdown("---")
            
            with tab2:
                st.subheader("All Offices Directory")
                
                # Search functionality
                search_term = st.text_input("🔍 Search offices", placeholder="Search by city, country, or office name...")
                
                if search_term:
                    search_mask = (
                        offices_df['OFFICE_NAME'].str.contains(search_term, case=False, na=False) |
                        offices_df['CITY'].str.contains(search_term, case=False, na=False) |
                        offices_df['COUNTRY'].str.contains(search_term, case=False, na=False)
                    )
                    display_offices = offices_df[search_mask]
                else:
                    display_offices = offices_df
                
                # Display as formatted table
                display_cols = ['OFFICE_NAME', 'CITY', 'COUNTRY', 'REGION', 'OFFICE_TYPE', 'CAPACITY', 'ACTIVE_STATUS', 'OPENED_DATE']
                st.dataframe(
                    display_offices[display_cols],
                    use_container_width=True,
                    hide_index=True
                )
                
                st.write(f"Showing {len(display_offices)} of {len(offices_df)} offices")
            
            with tab3:
                st.subheader("Office Statistics")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Offices by region
                    region_stats = offices_df.groupby('REGION').agg({
                        'OFFICE_ID': 'count',
                        'CAPACITY': 'sum'
                    }).reset_index()
                    region_stats.columns = ['Region', 'Office Count', 'Total Capacity']
                    
                    fig = px.bar(
                        region_stats,
                        x='Region',
                        y='Office Count',
                        color='Total Capacity',
                        title='Offices by Region',
                        color_continuous_scale='Viridis'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Offices by type
                    type_stats = offices_df['OFFICE_TYPE'].value_counts().reset_index()
                    type_stats.columns = ['Office Type', 'Count']
                    
                    fig = px.pie(
                        type_stats,
                        values='Count',
                        names='Office Type',
                        title='Offices by Type',
                        color='Office Type',
                        color_discrete_map={
                            'Headquarters': '#8b5cf6',
                            'Regional Office': '#3b82f6',
                            'Field Office': '#10b981'
                        }
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Country distribution
                st.markdown("### Offices by Country")
                country_stats = offices_df['COUNTRY'].value_counts().head(10).reset_index()
                country_stats.columns = ['Country', 'Office Count']
                
                fig = px.bar(
                    country_stats,
                    x='Country',
                    y='Office Count',
                    title='Top 10 Countries by Office Count'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with tab4:
                st.subheader("➕ Add New Office")
                st.info("💡 **Note:** This form will help you generate the SQL to add a new office to the database.")
                
                with st.form("new_office_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        office_name = st.text_input("Office Name*", placeholder="e.g., SnowGhost Breakers Tokyo")
                        city = st.text_input("City*", placeholder="e.g., Tokyo")
                        country = st.text_input("Country*", placeholder="e.g., Japan")
                        region = st.selectbox("Region*", ["Americas", "Europe & Middle East", "Asia-Pacific"])
                        
                    with col2:
                        office_type = st.selectbox("Office Type*", ["Headquarters", "Regional Office", "Field Office"])
                        capacity = st.number_input("Capacity (investigators)*", min_value=1, value=50)
                        latitude = st.number_input("Latitude", value=0.0, format="%.6f")
                        longitude = st.number_input("Longitude", value=0.0, format="%.6f")
                    
                    timezone = st.text_input("Timezone", placeholder="e.g., Asia/Tokyo")
                    address = st.text_area("Address (optional)", placeholder="Full street address")
                    phone = st.text_input("Phone (optional)", placeholder="e.g., +81-3-1234-5678")
                    email = st.text_input("Email (optional)", placeholder="e.g., tokyo@snowghostbreakers.com")
                    
                    submitted = st.form_submit_button("🎯 Generate SQL")
                    
                    if submitted:
                        if office_name and city and country:
                            # Generate office ID
                            import re
                            country_code = country[:2].upper()
                            city_code = re.sub(r'[^A-Za-z]', '', city)[:5].upper()
                            office_id = f"OFF_{country_code}_{city_code}"
                            
                            # Generate INSERT SQL
                            sql_statement = f"""
-- Add new office: {office_name}
INSERT INTO GHOST_DETECTION.APP.OFFICES (
    office_id, office_name, city, country, region, 
    latitude, longitude, timezone, office_type, capacity, 
    active_status, phone, email, address, opened_date
) VALUES (
    '{office_id}',
    '{office_name}',
    '{city}',
    '{country}',
    '{region}',
    {latitude},
    {longitude},
    '{timezone if timezone else 'UTC'}',
    '{office_type}',
    {capacity},
    TRUE,
    {f"'{phone}'" if phone else 'NULL'},
    {f"'{email}'" if email else 'NULL'},
    {f"'{address}'" if address else 'NULL'},
    CURRENT_DATE()
);
"""
                            st.success("✅ SQL generated successfully!")
                            st.code(sql_statement, language="sql")
                            st.info("📋 Copy this SQL and run it in Snowflake to add the office.")
                        else:
                            st.error("❌ Please fill in all required fields (marked with *)")
    
    except Exception as e:
        st.error(f"❌ Error loading offices: {str(e)}")
        st.info("💡 **Setup Required:**")
        st.code("snowsql -f sql/13_offices_table.sql", language="bash")
        st.markdown("Or copy and paste the contents of `sql/13_offices_table.sql` into a Snowflake worksheet.")

# ============================================
# PAGE: AI INSIGHTS
# ============================================
elif page == "🤖 AI Insights":
    st.header("🤖 AI-Powered Insights")
    
    tab1, tab2, tab3 = st.tabs(["💬 Ask Questions", "📊 Model Performance", "🔮 Predictions"])
    
    with tab1:
        st.subheader("Ask Questions About Ghost Data")
        user_question = st.text_input(
            "Enter your question:",
            placeholder="e.g., What are the most dangerous ghosts currently active?"
        )
        
        if st.button("🔍 Get Answer"):
            if user_question:
                with st.spinner("Analyzing data with Cortex AI..."):
                    # Query relevant data
                    context_data = session.table("GHOST_DETECTION.ANALYTICS.VW_GHOST_ACTIVITY_SUMMARY").to_pandas()
                    
                    prompt = f"""Based on the ghost detection data, answer this question: {user_question}
                    
                    Context: We have {len(context_data)} ghosts in our database with various threat levels,
                    types, and activity patterns. Provide a concise, informative answer."""
                    
                    # Use Cortex Complete
                    answer = Complete('mistral-large2', prompt)
                    
                    st.success("**Answer:**")
                    st.write(answer)
    
    with tab2:
        st.subheader("AI Model Performance Metrics")
        model_metrics_df = session.table("GHOST_DETECTION.ANALYTICS.VW_AI_MODEL_METRICS").to_pandas()
        
        st.dataframe(model_metrics_df, use_container_width=True)
        
        # Confidence distribution
        fig = px.box(model_metrics_df, x='MODEL_USED', y='AVG_CONFIDENCE',
                     title='Model Confidence Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("🔮 Threat Level Predictions")
        
        # Get ghost activity data for predictions
        prediction_query = """
        SELECT 
            g.ghost_id,
            g.ghost_name,
            g.ghost_type,
            g.threat_level,
            COUNT(DISTINCT gs.sighting_id) as sighting_count,
            AVG(gs.paranormal_activity_level) as avg_activity,
            MAX(gs.sighting_datetime) as last_sighting,
            COUNT(DISTINCT ge.evidence_id) as evidence_count,
            AVG(gs.emf_reading) as avg_emf,
            AVG(gs.temperature_celsius) as avg_temp
        FROM GHOST_DETECTION.APP.GHOSTS g
        INNER JOIN GHOST_DETECTION.APP.GHOST_SIGHTINGS gs ON g.ghost_id = gs.ghost_id
        LEFT JOIN GHOST_DETECTION.APP.GHOST_EVIDENCE ge ON g.ghost_id = ge.ghost_id
        WHERE g.status = 'Active'
        AND gs.sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())
        GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level
        HAVING COUNT(DISTINCT gs.sighting_id) > 0
        ORDER BY sighting_count DESC, avg_activity DESC
        LIMIT 10
        """
        
        try:
            pred_df = session.sql(prediction_query).to_pandas()
            
            if not pred_df.empty:
                st.markdown("### 📊 Top 10 Active Ghosts - Threat Analysis")
                
                # Display metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    high_threat_count = len(pred_df[pred_df['THREAT_LEVEL'].isin(['High', 'Extreme'])])
                    st.metric("High/Extreme Threats", high_threat_count)
                with col2:
                    total_sightings = pred_df['SIGHTING_COUNT'].sum()
                    st.metric("Total Sightings (30d)", int(total_sightings))
                with col3:
                    avg_activity_all = pred_df['AVG_ACTIVITY'].mean()
                    st.metric("Avg Activity Level", f"{avg_activity_all:.1f}/10")
                
                st.markdown("---")
                
                # Predict threat escalation for each ghost
                for idx, ghost in pred_df.iterrows():
                    with st.expander(
                        f"👻 {ghost['GHOST_NAME']} ({ghost['GHOST_TYPE']}) - Current: {ghost['THREAT_LEVEL']}"
                    ):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # AI prediction using Cortex
                            prediction_prompt = f"""
                            Analyze this ghost's activity and predict threat level changes:
                            
                            Ghost: {ghost['GHOST_NAME']} ({ghost['GHOST_TYPE']})
                            Current Threat: {ghost['THREAT_LEVEL']}
                            Recent Activity:
                            - Sightings (30 days): {ghost['SIGHTING_COUNT']}
                            - Avg Activity Level: {ghost['AVG_ACTIVITY']:.1f}/10
                            - Evidence Collected: {ghost['EVIDENCE_COUNT']}
                            - Avg EMF: {ghost['AVG_EMF']:.1f} mG
                            - Avg Temperature: {ghost['AVG_TEMP']:.1f}°C
                            
                            Provide:
                            1. Predicted threat level in next 7 days (Low/Medium/High/Extreme)
                            2. Confidence level (%)
                            3. Key indicators supporting prediction
                            4. Recommended actions
                            
                            Be concise (3-4 sentences).
                            """
                            
                            try:
                                prediction = Complete('mistral-large2', prediction_prompt)
                                st.markdown("**🤖 AI Threat Prediction:**")
                                st.write(prediction)
                            except Exception as e:
                                st.warning("AI prediction unavailable. Using statistical analysis.")
                                
                                # Fallback: Simple rule-based prediction
                                threat_score = (
                                    ghost['SIGHTING_COUNT'] * 2 +
                                    ghost['AVG_ACTIVITY'] * 3 +
                                    ghost['EVIDENCE_COUNT'] * 1.5
                                )
                                
                                if threat_score > 50:
                                    predicted_level = "Extreme"
                                    confidence = 85
                                elif threat_score > 30:
                                    predicted_level = "High"
                                    confidence = 75
                                elif threat_score > 15:
                                    predicted_level = "Medium"
                                    confidence = 65
                                else:
                                    predicted_level = "Low"
                                    confidence = 70
                                
                                st.info(f"**Predicted Threat:** {predicted_level} (Confidence: {confidence}%)")
                        
                        with col2:
                            st.metric("Sightings (30d)", int(ghost['SIGHTING_COUNT']))
                            st.metric("Activity Level", f"{ghost['AVG_ACTIVITY']:.1f}/10")
                            st.metric("Evidence Items", int(ghost['EVIDENCE_COUNT']))
                            
                            # Threat level indicator
                            threat_colors = {
                                'Low': '🟢',
                                'Medium': '🟡',
                                'High': '🟠',
                                'Extreme': '🔴'
                            }
                            st.write(f"**Current:** {threat_colors.get(ghost['THREAT_LEVEL'], '⚪')} {ghost['THREAT_LEVEL']}")
                
                # Trend visualization
                st.markdown("---")
                st.markdown("### 📈 Activity vs Threat Level")
                
                fig = px.scatter(
                    pred_df,
                    x='SIGHTING_COUNT',
                    y='AVG_ACTIVITY',
                    size='EVIDENCE_COUNT',
                    color='THREAT_LEVEL',
                    hover_name='GHOST_NAME',
                    hover_data={'GHOST_TYPE': True, 'THREAT_LEVEL': True},
                    title='Ghost Activity Patterns (Last 30 Days)',
                    labels={
                        'SIGHTING_COUNT': 'Number of Sightings',
                        'AVG_ACTIVITY': 'Average Activity Level',
                        'EVIDENCE_COUNT': 'Evidence Count'
                    },
                    color_discrete_map={
                        'Low': 'green',
                        'Medium': 'yellow',
                        'High': 'orange',
                        'Extreme': 'red'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.info("No recent ghost activity data available for predictions. Need at least 30 days of sighting data.")
                
        except Exception as e:
            st.error(f"Unable to generate predictions: {str(e)}")
            st.info("💡 Tip: Ensure you have ghost sightings and evidence data in the database.")

# ============================================
# PAGE: NEW SIGHTING
# ============================================
elif page == "➕ New Sighting":
    st.header("➕ Report New Ghost Sighting")
    
    # Image upload section (outside form for preview)
    st.subheader("📸 Upload Evidence Photos")
    uploaded_files = st.file_uploader(
        "Upload photos of the paranormal activity",
        type=['png', 'jpg', 'jpeg'],
        accept_multiple_files=True,
        help="Upload images showing evidence of paranormal activity. AI will analyze them automatically."
    )
    
    # Display uploaded images and run AI analysis
    image_analysis_results = []
    uploaded_files_data = []  # Store file bytes for later upload
    
    if uploaded_files:
        st.markdown("### 🔍 AI Image Analysis")
        cols = st.columns(min(len(uploaded_files), 3))
        
        for idx, uploaded_file in enumerate(uploaded_files):
            col = cols[idx % 3]
            with col:
                st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
                
                # Store file data for later upload to stage
                file_bytes = uploaded_file.read()
                uploaded_file.seek(0)  # Reset pointer for display
                uploaded_files_data.append({
                    'name': uploaded_file.name,
                    'bytes': file_bytes,
                    'type': uploaded_file.type
                })
                
                # Run AI analysis on image
                with st.spinner(f"Analyzing {uploaded_file.name}..."):
                    try:
                        # Using Complete for demonstration
                        analysis = Complete(
                            'mistral-large2',
                            f"You are a paranormal investigator analyzing evidence photo '{uploaded_file.name}'. "
                            f"Identify: 1) Type of anomaly (orb, shadow, mist, apparition, light anomaly), "
                            f"2) Severity (1-10), 3) Notable features, 4) Authenticity assessment. Be brief."
                        )
                        
                        st.success("Analysis complete!")
                        with st.expander("View AI Analysis"):
                            st.write(analysis)
                        
                        image_analysis_results.append({
                            'filename': uploaded_file.name,
                            'analysis': analysis
                        })
                    except Exception as e:
                        st.warning(f"Could not analyze image: {str(e)}")
        
        st.markdown("---")
    
    # Geocoding section (outside form)
    st.subheader("🌍 Optional: Get Coordinates from Address")
    with st.expander("📍 Click here to geocode an address"):
        geocode_col1, geocode_col2 = st.columns([3, 1])
        
        with geocode_col1:
            geocode_input = st.text_input(
                "Enter address or location",
                placeholder="e.g., 'Tower of London, UK' or '123 Main St, New York'",
                key="geocode_address"
            )
        
        with geocode_col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            if st.button("🔍 Lookup", use_container_width=True):
                if geocode_input:
                    with st.spinner("Looking up coordinates..."):
                        try:
                            try:
                                from geopy.geocoders import Nominatim
                                from geopy.exc import GeocoderTimedOut, GeocoderServiceError
                            except ImportError:
                                st.error("❌ Geocoding feature requires 'geopy' package")
                                st.info("💡 Add 'geopy' to your Streamlit app packages in Snowsight UI, or enter coordinates manually below.")
                                st.stop()
                            import time
                            
                            # Function to geocode with retry logic
                            def geocode_with_retry(address, max_retries=3):
                                for attempt in range(max_retries):
                                    try:
                                        # Use geopy Nominatim geocoder - no API key required
                                        # Add a small delay to respect rate limits
                                        if attempt > 0:
                                            time.sleep(2 ** attempt)  # Exponential backoff: 2s, 4s
                                        
                                        geolocator = Nominatim(
                                            user_agent="SnowGhostBreakers-v2.1",
                                            timeout=15  # Increased timeout
                                        )
                                        
                                        # Geocode the address
                                        location = geolocator.geocode(address, timeout=15)
                                        return location
                                        
                                    except GeocoderTimedOut:
                                        if attempt < max_retries - 1:
                                            continue
                                        raise
                                    except GeocoderServiceError as e:
                                        if "429" in str(e) or "rate limit" in str(e).lower():
                                            if attempt < max_retries - 1:
                                                time.sleep(5)  # Wait longer for rate limits
                                                continue
                                        raise
                                    except Exception as e:
                                        # Connection errors, etc.
                                        if attempt < max_retries - 1:
                                            time.sleep(3)
                                            continue
                                        raise
                                
                                return None
                            
                            # Try to geocode with retry
                            location = geocode_with_retry(geocode_input)
                            
                            if location:
                                found_lat = location.latitude
                                found_lon = location.longitude
                                display_name = location.address
                                
                                # Store in session state to update the number inputs
                                st.session_state['geocoded_lat'] = found_lat
                                st.session_state['geocoded_lon'] = found_lon
                                
                                st.success(f"✅ Found: {display_name}")
                                st.info(f"📍 Coordinates: {found_lat:.6f}, {found_lon:.6f}")
                                st.info("💡 The coordinates have been set below. You can now fill out the sighting form.")
                            else:
                                st.warning("⚠️ Location not found. Try a more specific address.")
                                st.info("💡 Examples: 'Tower of London, UK', '1600 Pennsylvania Ave, Washington DC', 'Eiffel Tower, Paris'")
                                
                        except GeocoderTimedOut:
                            st.error("❌ Geocoding service timed out. Please try again in a moment.")
                            st.info("💡 The service may be experiencing high traffic. Try again or enter coordinates manually.")
                        except GeocoderServiceError as e:
                            st.error(f"❌ Geocoding service error: {str(e)}")
                            st.info("💡 The geocoding service may be temporarily unavailable. Enter coordinates manually below.")
                        except ConnectionError as e:
                            st.error("❌ Connection error: Unable to reach geocoding service")
                            st.info("💡 Check your internet connection or enter coordinates manually below.")
                            st.info("Note: Nominatim requires an active internet connection")
                        except Exception as e:
                            error_msg = str(e)
                            if "Device or resource busy" in error_msg:
                                st.error("❌ Network busy: Too many concurrent requests")
                                st.info("💡 Wait a moment and try again, or enter coordinates manually")
                            elif "Max retries exceeded" in error_msg:
                                st.error("❌ Connection failed: Network is busy or unavailable")
                                st.info("💡 Enter coordinates manually below or try again later")
                            else:
                                st.error(f"❌ Geocoding error: {error_msg}")
                                st.info("💡 Enter coordinates manually in the form below")
                else:
                    st.warning("⚠️ Please enter an address first")
    
    st.markdown("---")
    
    with st.form("new_sighting_form"):
        st.subheader("📍 Location Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location_name = st.text_input("Location Name*", help="e.g., 'Old Victorian Mansion'")
            location_address = st.text_area("Full Address", height=80, 
                                           help="Enter full address (used for record keeping)")
            
            witness_name = st.text_input("Witness Name*")
            witness_contact = st.text_input("Witness Contact", help="Email or phone")
        
        with col2:
            st.markdown("**📍 Location Coordinates**")
            use_map = st.checkbox("📍 Show location on map", value=True)
            
            # Use geocoded coordinates if available
            default_lat = st.session_state.get('geocoded_lat', 40.7128)
            default_lon = st.session_state.get('geocoded_lon', -74.0060)
            
            col_lat, col_lon = st.columns(2)
            with col_lat:
                latitude = st.number_input("Latitude", value=default_lat, format="%.6f")
            with col_lon:
                longitude = st.number_input("Longitude", value=default_lon, format="%.6f")
            
            # Show mini map
            if use_map and latitude != 0 and longitude != 0:
                loc_df = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
                st.map(loc_df, zoom=13)
        
        st.markdown("---")
        st.subheader("🕐 Sighting Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sighting_date = st.date_input("Sighting Date*", max_value=datetime.now().date())
            sighting_time = st.time_input("Sighting Time*")
            evidence_type = st.selectbox(
                "Evidence Type*",
                ["Visual", "Photograph", "Video", "Audio", "EMF", "Temperature", "Multiple"]
            )
        
        with col2:
            paranormal_level = st.slider("Activity Level*", 1, 10, 5)
            temperature_f = st.number_input("Temperature (°F)", value=68.0, help="Room temperature default")
            # Convert F to C for storage
            temperature = (temperature_f - 32) * 5/9
            emf_reading = st.number_input("EMF Reading (mG)", value=0.0)
        
        st.markdown("---")
        description = st.text_area("Detailed Description*", height=150)
        environmental = st.text_area("Environmental Conditions", height=100)
        
        if image_analysis_results:
            st.info(f"📸 {len(image_analysis_results)} photo(s) uploaded and analyzed")
        
        submitted = st.form_submit_button("📝 Submit Sighting Report", use_container_width=True)
        
        if submitted:
            if location_name and witness_name and description:
                import uuid
                from datetime import datetime as dt
                
                sighting_id = f"SIGHT_{str(uuid.uuid4())[:8].upper()}"
                sighting_datetime = datetime.combine(sighting_date, sighting_time)
                
                # Combine description with image analysis
                full_desc = description
                if image_analysis_results:
                    full_desc += "\n\n--- AI IMAGE ANALYSIS ---\n"
                    for img in image_analysis_results:
                        full_desc += f"\n{img['filename']}:\n{img['analysis']}\n"
                
                with st.spinner("🤖 Analyzing with AI and saving data..."):
                    try:
                        classification = Complete(
                            'mistral-large2',
                            f"Classify this paranormal sighting as: Apparition, Poltergeist, Shadow Figure, "
                            f"Orb, Residual Haunt, Intelligent Haunt, Demonic, or Unknown. "
                            f"Description: {full_desc}. Location: {location_name}. Activity: {paranormal_level}/10. "
                            f"Return ONLY the classification type (one or two words) without explanation."
                        )
                        
                        # Clean classification
                        ghost_type = classification.strip().split('.')[0].strip()
                        
                        # Upload images to GHOST_IMAGES_STAGE and create embeddings
                        stage_paths = []
                        image_embeddings = []
                        
                        if uploaded_files_data:
                            st.info(f"📤 Uploading {len(uploaded_files_data)} images to Snowflake stage...")
                            
                            for idx, file_data in enumerate(uploaded_files_data):
                                try:
                                    # Generate unique filename
                                    timestamp = dt.now().strftime("%Y%m%d_%H%M%S")
                                    safe_filename = file_data['name'].replace(' ', '_').replace('(', '').replace(')', '')
                                    stage_filename = f"{sighting_id}_{timestamp}_{safe_filename}"
                                    stage_path = f"@GHOST_IMAGES_STAGE/{stage_filename}"
                                    
                                    # Write file to temporary location and upload to stage
                                    import tempfile
                                    import os
                                    
                                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(safe_filename)[1]) as tmp_file:
                                        tmp_file.write(file_data['bytes'])
                                        tmp_path = tmp_file.name
                                    
                                    try:
                                        # Upload to Snowflake stage using PUT
                                        put_result = session.sql(f"PUT 'file://{tmp_path}' @GHOST_IMAGES_STAGE/{stage_filename} OVERWRITE=TRUE").collect()
                                        
                                        # Clean up temp file
                                        os.unlink(tmp_path)
                                        
                                        # Store path info
                                        stage_paths.append({
                                            'filename': safe_filename,
                                            'stage_path': stage_path,
                                            'original_name': file_data['name'],
                                            'file_size': len(file_data['bytes'])
                                        })
                                        
                                        # Create embedding from image analysis text (metadata-based)
                                        # In production, you could use actual image embeddings from Cortex Vision
                                        if idx < len(image_analysis_results):
                                            analysis_text = f"{ghost_type} ghost evidence. {image_analysis_results[idx]['analysis']}"
                                            
                                            # Create AI embedding vector
                                            embedding_query = f"""
                                            SELECT AI_EMBED(
                                                'snowflake-arctic-embed-l-v2.0-8k',
                                                '{analysis_text.replace("'", "''")[:5000]}'
                                            ) as embedding_vector
                                            """
                                            embedding_result = session.sql(embedding_query).collect()
                                            
                                            if embedding_result:
                                                image_embeddings.append({
                                                    'filename': safe_filename,
                                                    'embedding': str(embedding_result[0]['EMBEDDING_VECTOR']),
                                                    'analysis_text': analysis_text[:1000]
                                                })
                                        
                                    except Exception as stage_err:
                                        # Fallback: just store the reference without actual upload
                                        os.unlink(tmp_path) if os.path.exists(tmp_path) else None
                                        st.warning(f"Stage upload failed for {file_data['name']}, storing reference only")
                                        stage_paths.append({
                                            'filename': safe_filename,
                                            'stage_path': stage_path,
                                            'original_name': file_data['name'],
                                            'file_size': len(file_data['bytes'])
                                        })
                                    
                                except Exception as upload_err:
                                    st.warning(f"Could not process {file_data['name']}: {str(upload_err)}")
                        
                        # Insert sighting into database
                        insert_sighting_sql = f"""
                        INSERT INTO GHOST_DETECTION.APP.GHOST_SIGHTINGS (
                            sighting_id, 
                            ghost_id,
                            location_name,
                            location_address,
                            latitude,
                            longitude,
                            sighting_datetime,
                            witness_name,
                            witness_contact,
                            description,
                            evidence_type,
                            paranormal_activity_level,
                            environmental_conditions,
                            temperature_celsius,
                            emf_reading,
                            investigation_status
                        ) VALUES (
                            '{sighting_id}',
                            NULL,  -- Will be linked later after ghost creation
                            '{location_name.replace("'", "''")}',
                            '{location_address.replace("'", "''") if location_address else ""}',
                            {latitude},
                            {longitude},
                            '{sighting_datetime.strftime("%Y-%m-%d %H:%M:%S")}',
                            '{witness_name.replace("'", "''")}',
                            '{witness_contact.replace("'", "''") if witness_contact else ""}',
                            '{full_desc.replace("'", "''")}',
                            '{evidence_type}',
                            {paranormal_level},
                            'Reported via Streamlit',
                            {temperature_celsius},
                            0.0,
                            'Pending'
                        )
                        """
                        
                        session.sql(insert_sighting_sql).collect()
                        
                        # Insert evidence records for uploaded images
                        evidence_ids = []
                        for idx, stage_info in enumerate(stage_paths):
                            evidence_id = f"EVID_{str(uuid.uuid4())[:8].upper()}"
                            evidence_ids.append(evidence_id)
                            
                            # Prepare metadata JSON
                            metadata_obj = {
                                "original_filename": stage_info['original_name'],
                                "upload_source": "streamlit",
                                "file_size": stage_info.get('file_size', 0),
                                "upload_timestamp": dt.now().isoformat()
                            }
                            
                            if idx < len(image_analysis_results):
                                metadata_obj["ai_analysis"] = image_analysis_results[idx]['analysis'][:500]
                            
                            import json
                            metadata_json = json.dumps(metadata_obj).replace("'", "''")
                            
                            insert_evidence_sql = f"""
                            INSERT INTO GHOST_DETECTION.APP.GHOST_EVIDENCE (
                                evidence_id,
                                sighting_id,
                                ghost_id,
                                evidence_type,
                                file_path,
                                capture_datetime,
                                metadata,
                                processing_status
                            ) VALUES (
                                '{evidence_id}',
                                '{sighting_id}',
                                NULL,
                                'Photograph',
                                '{stage_info['stage_path']}',
                                '{sighting_datetime.strftime("%Y-%m-%d %H:%M:%S")}',
                                PARSE_JSON('{metadata_json}'),
                                'Analyzed'
                            )
                            """
                            
                            session.sql(insert_evidence_sql).collect()
                        
                        # Insert AI analysis records with embeddings
                        for idx, embedding_info in enumerate(image_embeddings):
                            if idx < len(evidence_ids):
                                analysis_id = f"AI_{str(uuid.uuid4())[:8].upper()}"
                                evidence_id = evidence_ids[idx]
                                
                                # Get AI sentiment analysis
                                try:
                                    sentiment_query = f"""
                                    SELECT SNOWFLAKE.CORTEX.SENTIMENT(
                                        '{embedding_info['analysis_text'].replace("'", "''")}'
                                    ) as sentiment_score
                                    """
                                    sentiment_result = session.sql(sentiment_query).collect()
                                    sentiment_score = sentiment_result[0]['SENTIMENT_SCORE'] if sentiment_result else 0.0
                                except:
                                    sentiment_score = 0.0
                                
                                # Prepare findings JSON
                                findings = {
                                    "ghost_type_detected": ghost_type,
                                    "analysis": embedding_info['analysis_text'],
                                    "confidence": 0.85,
                                    "anomalies_detected": ["visual evidence", "paranormal activity"],
                                    "embedding_model": "snowflake-arctic-embed-l-v2.0-8k",
                                    "embedding_dimensions": 1024
                                }
                                findings_json = json.dumps(findings).replace("'", "''")
                                
                                insert_ai_analysis_sql = f"""
                                INSERT INTO GHOST_DETECTION.APP.GHOST_AI_ANALYSIS (
                                    analysis_id,
                                    evidence_id,
                                    ghost_id,
                                    sighting_id,
                                    analysis_type,
                                    model_used,
                                    confidence_score,
                                    findings,
                                    analysis_datetime,
                                    sentiment_score,
                                    embedding_vector
                                ) VALUES (
                                    '{analysis_id}',
                                    '{evidence_id}',
                                    NULL,
                                    '{sighting_id}',
                                    'Image Analysis',
                                    'snowflake-arctic-embed-l-v2.0-8k',
                                    0.85,
                                    PARSE_JSON('{findings_json}'),
                                    '{dt.now().strftime("%Y-%m-%d %H:%M:%S")}',
                                    {sentiment_score},
                                    {embedding_info['embedding']}
                                )
                                """
                                
                                session.sql(insert_ai_analysis_sql).collect()
                        
                        st.success("✅ Sighting reported and saved to database!")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Sighting ID", sighting_id)
                        with col2:
                            st.metric("Activity Level", f"{paranormal_level}/10")
                        with col3:
                            st.metric("Photos Uploaded", len(stage_paths))
                        with col4:
                            st.metric("AI Embeddings", len(image_embeddings))
                        
                        st.info(f"🤖 **AI Classification:** {ghost_type}")
                        
                        if stage_paths:
                            st.success(f"📸 {len(stage_paths)} images uploaded to GHOST_IMAGES_STAGE")
                            with st.expander("📁 View uploaded files and embeddings"):
                                for idx, path_info in enumerate(stage_paths):
                                    st.text(f"✓ {path_info['original_name']} → {path_info['stage_path']}")
                                    if idx < len(image_embeddings):
                                        st.text(f"   🧠 AI Embedding created (1024 dimensions)")
                                        st.text(f"   📊 Analysis: {image_embeddings[idx]['analysis_text'][:100]}...")
                        
                        if image_embeddings:
                            st.success(f"🧠 {len(image_embeddings)} AI embeddings created for similarity search")
                        
                        if latitude != 0 or longitude != 0:
                            st.success(f"📍 Location: {latitude:.6f}, {longitude:.6f}")
                        
                        st.balloons()
                        
                        # Clear session state for new entry
                        if 'geocoded_lat' in st.session_state:
                            del st.session_state['geocoded_lat']
                        if 'geocoded_lon' in st.session_state:
                            del st.session_state['geocoded_lon']
                        
                    except Exception as e:
                        st.error(f"Error saving sighting: {str(e)}")
                        st.error("Please ensure all required tables exist and you have proper permissions")
                        with st.expander("Debug Info"):
                            st.code(str(e))
            else:
                st.error("Please fill in all required fields marked with *")

# ============================================
# PAGE: ANALYTICS
# ============================================
elif page == "📈 Analytics":
    st.header("📈 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investigator Performance")
        investigator_df = session.table("GHOST_DETECTION.ANALYTICS.VW_INVESTIGATOR_STATS").to_pandas()
        
        fig = px.bar(investigator_df, x='INVESTIGATOR_NAME', y='CASES_SOLVED',
                     color='SPECIALIZATION', title='Cases Solved by Investigator')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Threat Matrix")
        threat_matrix_df = session.table("GHOST_DETECTION.ANALYTICS.VW_THREAT_MATRIX").to_pandas()
        
        fig = px.scatter(threat_matrix_df, x='GHOST_TYPE', y='AVG_ACTIVITY_LEVEL',
                        size='GHOST_COUNT', color='THREAT_LEVEL',
                        title='Ghost Type vs Activity Level')
        st.plotly_chart(fig, use_container_width=True)
    
    # Time series analysis
    st.subheader("Activity Trends")
    timeline_df = session.table("GHOST_DETECTION.ANALYTICS.VW_ACTIVITY_TIMELINE").limit(90).to_pandas()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=timeline_df['ACTIVITY_DATE'], y=timeline_df['DAILY_SIGHTINGS'],
                             name='Sightings', line=dict(color='#667eea')))
    fig.add_trace(go.Scatter(x=timeline_df['ACTIVITY_DATE'], y=timeline_df['UNIQUE_GHOSTS_ACTIVE'],
                             name='Unique Ghosts', line=dict(color='#764ba2')))
    fig.update_layout(title='90-Day Activity Trend', xaxis_title='Date', yaxis_title='Count')
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# PAGE: REPORTS
# ============================================
elif page == "📑 Reports":
    st.header("📑 Comprehensive Data Reports")
    st.markdown("*Detailed analytics and visualizations for all major data categories*")
    
    # Report selector
    report_type = st.selectbox(
        "Select Report Type",
        [
            "📊 Executive Summary",
            "👻 Ghost Registry Report",
            "📍 Sightings Analysis Report",
            "🔬 Evidence Analysis Report",
            "📋 Investigations Report",
            "👥 Investigators Performance Report"
        ]
    )
    
    st.markdown("---")
    
    # ============================================
    # EXECUTIVE SUMMARY REPORT
    # ============================================
    if report_type == "📊 Executive Summary":
        st.subheader("📊 Executive Summary Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Key Metrics
        st.markdown("### 🎯 Key Performance Indicators")
        
        kpi_query = """
        SELECT 
            (SELECT COUNT(*) FROM GHOSTS WHERE status = 'Active') as active_ghosts,
            (SELECT COUNT(*) FROM GHOST_SIGHTINGS WHERE sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())) as recent_sightings,
            (SELECT COUNT(*) FROM GHOST_EVIDENCE) as total_evidence,
            (SELECT COUNT(*) FROM INVESTIGATIONS WHERE status IN ('Open', 'In_Progress')) as active_investigations,
            (SELECT COUNT(*) FROM INVESTIGATORS WHERE active_status = TRUE) as active_investigators,
            (SELECT AVG(paranormal_activity_level) FROM GHOST_SIGHTINGS WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())) as avg_activity_7d
        """
        
        kpis = session.sql(kpi_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Active Ghosts", int(kpis['ACTIVE_GHOSTS']))
        with col2:
            st.metric("Recent Sightings", int(kpis['RECENT_SIGHTINGS']), 
                     delta="Last 30 days")
        with col3:
            st.metric("Evidence Items", int(kpis['TOTAL_EVIDENCE']))
        with col4:
            st.metric("Active Cases", int(kpis['ACTIVE_INVESTIGATIONS']))
        with col5:
            st.metric("Team Members", int(kpis['ACTIVE_INVESTIGATORS']))
        with col6:
            st.metric("Avg Activity", f"{kpis['AVG_ACTIVITY_7D']:.1f}/10",
                     delta="7-day average")
        
        st.markdown("---")
        
        # Threat Level Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚠️ Threat Level Distribution")
            threat_query = """
            SELECT 
                threat_level,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
            FROM GHOSTS
            WHERE status = 'Active'
            GROUP BY threat_level
            ORDER BY CASE threat_level 
                WHEN 'Extreme' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END
            """
            threat_df = session.sql(threat_query).to_pandas()
            
            fig = px.pie(threat_df, values='COUNT', names='THREAT_LEVEL',
                        title='Active Ghosts by Threat Level',
                        color='THREAT_LEVEL',
                        color_discrete_map={
                            'Extreme': '#dc2626',
                            'High': '#f59e0b',
                            'Medium': '#eab308',
                            'Low': '#22c55e'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 30-Day Sighting Trend")
            trend_query = """
            SELECT 
                DATE(sighting_datetime) as date,
                COUNT(*) as sightings
            FROM GHOST_SIGHTINGS
            WHERE sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())
            GROUP BY DATE(sighting_datetime)
            ORDER BY date
            """
            trend_df = session.sql(trend_query).to_pandas()
            
            fig = px.line(trend_df, x='DATE', y='SIGHTINGS',
                         title='Daily Sightings - Last 30 Days')
            fig.update_traces(line_color='#667eea', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        # Geographic Hotspots
        st.markdown("### 🗺️ Geographic Hotspots")
        hotspot_query = """
        SELECT 
            location_name,
            COUNT(*) as sighting_count,
            AVG(paranormal_activity_level) as avg_activity,
            AVG(latitude) as latitude,
            AVG(longitude) as longitude
        FROM GHOST_SIGHTINGS
        WHERE latitude BETWEEN -90 AND 90 
          AND longitude BETWEEN -180 AND 180
          AND location_name IS NOT NULL
        GROUP BY location_name
        HAVING COUNT(*) > 1
        ORDER BY sighting_count DESC
        LIMIT 20
        """
        
        hotspot_df = session.sql(hotspot_query).to_pandas()
        
        if not hotspot_df.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Map visualization
                fig = px.scatter_mapbox(
                    hotspot_df,
                    lat='LATITUDE',
                    lon='LONGITUDE',
                    size='SIGHTING_COUNT',
                    color='AVG_ACTIVITY',
                    hover_name='LOCATION_NAME',
                    hover_data={'SIGHTING_COUNT': True, 'AVG_ACTIVITY': ':.1f',
                               'LATITUDE': False, 'LONGITUDE': False},
                    color_continuous_scale='Reds',
                    size_max=30,
                    zoom=3,
                    mapbox_style='open-street-map',
                    title='Sighting Hotspots Map'
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Top 10 Locations:**")
                for idx, row in hotspot_df.head(10).iterrows():
                    st.write(f"**{row['LOCATION_NAME']}**")
                    st.write(f"   Sightings: {int(row['SIGHTING_COUNT'])}")
                    st.write(f"   Avg Activity: {row['AVG_ACTIVITY']:.1f}/10")
                    st.markdown("---")
    
    # ============================================
    # GHOST REGISTRY REPORT
    # ============================================
    elif report_type == "👻 Ghost Registry Report":
        st.subheader("👻 Ghost Registry Comprehensive Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary Statistics
        st.markdown("### 📊 Registry Statistics")
        
        stats_query = """
        SELECT 
            COUNT(*) as total_ghosts,
            SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_count,
            SUM(CASE WHEN status = 'Contained' THEN 1 ELSE 0 END) as contained_count,
            SUM(CASE WHEN status = 'Banished' THEN 1 ELSE 0 END) as banished_count,
            COUNT(DISTINCT ghost_type) as unique_types,
            COUNT(DISTINCT origin_location) as unique_origins
        FROM GHOSTS
        """
        
        stats = session.sql(stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Registered", int(stats['TOTAL_GHOSTS']))
        with col2:
            st.metric("Active", int(stats['ACTIVE_COUNT']), 
                     delta=f"{stats['ACTIVE_COUNT']/stats['TOTAL_GHOSTS']*100:.1f}%")
        with col3:
            st.metric("Contained", int(stats['CONTAINED_COUNT']))
        with col4:
            st.metric("Banished", int(stats['BANISHED_COUNT']))
        with col5:
            st.metric("Ghost Types", int(stats['UNIQUE_TYPES']))
        with col6:
            st.metric("Origin Locations", int(stats['UNIQUE_ORIGINS']))
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Ghost Types Distribution")
            type_query = """
            SELECT 
                ghost_type,
                COUNT(*) as count,
                ROUND(AVG(CASE threat_level
                    WHEN 'Extreme' THEN 4
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    ELSE 1
                END), 2) as avg_threat_score
            FROM GHOSTS
            GROUP BY ghost_type
            ORDER BY count DESC
            """
            type_df = session.sql(type_query).to_pandas()
            
            fig = px.bar(type_df, x='GHOST_TYPE', y='COUNT',
                        color='AVG_THREAT_SCORE',
                        title='Ghost Types and Threat Levels',
                        color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Status Breakdown")
            status_query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM GHOSTS
            GROUP BY status
            ORDER BY count DESC
            """
            status_df = session.sql(status_query).to_pandas()
            
            fig = px.pie(status_df, values='COUNT', names='STATUS',
                        title='Ghost Status Distribution',
                        hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        
        # Threat Level Analysis
        st.markdown("### ⚠️ Threat Level Analysis")
        
        threat_detail_query = """
        SELECT 
            threat_level,
            ghost_type,
            COUNT(*) as count
        FROM GHOSTS
        WHERE status = 'Active'
        GROUP BY threat_level, ghost_type
        ORDER BY 
            CASE threat_level 
                WHEN 'Extreme' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END,
            count DESC
        """
        
        threat_detail_df = session.sql(threat_detail_query).to_pandas()
        
        fig = px.treemap(threat_detail_df,
                        path=['THREAT_LEVEL', 'GHOST_TYPE'],
                        values='COUNT',
                        title='Active Ghosts by Threat Level and Type',
                        color='COUNT',
                        color_continuous_scale='Reds')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Top Threats Table
        st.markdown("### 🚨 Top Threat Entities")
        
        top_threats_query = """
        SELECT 
            ghost_name,
            ghost_type,
            threat_level,
            origin_location,
            first_documented,
            status
        FROM GHOSTS
        WHERE threat_level IN ('Extreme', 'High')
          AND status = 'Active'
        ORDER BY 
            CASE threat_level 
                WHEN 'Extreme' THEN 1
                ELSE 2
            END,
            first_documented DESC
        LIMIT 10
        """
        
        top_threats_df = session.sql(top_threats_query).to_pandas()
        st.dataframe(top_threats_df, use_container_width=True, hide_index=True)
    
    # ============================================
    # SIGHTINGS ANALYSIS REPORT
    # ============================================
    elif report_type == "📍 Sightings Analysis Report":
        st.subheader("📍 Sightings Analysis Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary Statistics
        st.markdown("### 📊 Sightings Overview")
        
        sightings_stats_query = """
        SELECT 
            COUNT(*) as total_sightings,
            COUNT(DISTINCT ghost_id) as unique_ghosts,
            COUNT(DISTINCT location_name) as unique_locations,
            AVG(paranormal_activity_level) as avg_activity,
            MAX(paranormal_activity_level) as max_activity,
            COUNT(*) FILTER (WHERE sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP())) as last_7_days,
            COUNT(*) FILTER (WHERE sighting_datetime >= DATEADD(day, -30, CURRENT_TIMESTAMP())) as last_30_days
        FROM GHOST_SIGHTINGS
        """
        
        sighting_stats = session.sql(sightings_stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Sightings", int(sighting_stats['TOTAL_SIGHTINGS']))
        with col2:
            st.metric("Unique Ghosts", int(sighting_stats['UNIQUE_GHOSTS']))
        with col3:
            st.metric("Locations", int(sighting_stats['UNIQUE_LOCATIONS']))
        with col4:
            st.metric("Last 7 Days", int(sighting_stats['LAST_7_DAYS']))
        with col5:
            st.metric("Last 30 Days", int(sighting_stats['LAST_30_DAYS']))
        
        st.markdown("---")
        
        # Temporal Analysis
        st.markdown("### 📅 Temporal Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Hour of day distribution
            hour_query = """
            SELECT 
                HOUR(sighting_datetime) as hour,
                COUNT(*) as sightings
            FROM GHOST_SIGHTINGS
            GROUP BY HOUR(sighting_datetime)
            ORDER BY hour
            """
            hour_df = session.sql(hour_query).to_pandas()
            
            fig = px.bar(hour_df, x='HOUR', y='SIGHTINGS',
                        title='Sightings by Hour of Day')
            fig.update_layout(xaxis_title='Hour (24h)', yaxis_title='Number of Sightings')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Day of week distribution
            dow_query = """
            SELECT 
                DAYNAME(sighting_datetime) as day_name,
                DAYOFWEEK(sighting_datetime) as day_num,
                COUNT(*) as sightings
            FROM GHOST_SIGHTINGS
            GROUP BY day_name, day_num
            ORDER BY day_num
            """
            dow_df = session.sql(dow_query).to_pandas()
            
            fig = px.bar(dow_df, x='DAY_NAME', y='SIGHTINGS',
                        title='Sightings by Day of Week')
            st.plotly_chart(fig, use_container_width=True)
        
        # Activity Level Heatmap
        st.markdown("### 🔥 Activity Level Analysis")
        
        activity_query = """
        SELECT 
            paranormal_activity_level as level,
            COUNT(*) as count
        FROM GHOST_SIGHTINGS
        GROUP BY paranormal_activity_level
        ORDER BY paranormal_activity_level
        """
        activity_df = session.sql(activity_query).to_pandas()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(activity_df, x='LEVEL', y='COUNT',
                        title='Distribution of Paranormal Activity Levels',
                        color='LEVEL',
                        color_continuous_scale='Reds')
            fig.update_layout(xaxis_title='Activity Level (1-10)', 
                            yaxis_title='Number of Sightings')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("**Activity Statistics:**")
            st.metric("Average Level", f"{sighting_stats['AVG_ACTIVITY']:.2f}/10")
            st.metric("Maximum Level", f"{int(sighting_stats['MAX_ACTIVITY'])}/10")
            
            high_activity = len(activity_df[activity_df['LEVEL'] >= 7])
            st.metric("High Activity Events", high_activity)
        
        # Geographic Distribution
        st.markdown("### 🗺️ Geographic Distribution")
        
        geo_query = """
        SELECT 
            location_name,
            latitude,
            longitude,
            COUNT(*) as sighting_count,
            AVG(paranormal_activity_level) as avg_activity,
            MAX(sighting_datetime) as last_sighting
        FROM GHOST_SIGHTINGS
        WHERE latitude BETWEEN -90 AND 90 
          AND longitude BETWEEN -180 AND 180
          AND location_name IS NOT NULL
        GROUP BY location_name, latitude, longitude
        ORDER BY sighting_count DESC
        LIMIT 50
        """
        
        geo_df = session.sql(geo_query).to_pandas()
        
        if not geo_df.empty:
            fig = px.scatter_mapbox(
                geo_df,
                lat='LATITUDE',
                lon='LONGITUDE',
                size='SIGHTING_COUNT',
                color='AVG_ACTIVITY',
                hover_name='LOCATION_NAME',
                hover_data={
                    'SIGHTING_COUNT': True,
                    'AVG_ACTIVITY': ':.2f',
                    'LAST_SIGHTING': True,
                    'LATITUDE': False,
                    'LONGITUDE': False
                },
                title='Sightings Geographic Distribution',
                color_continuous_scale='Reds',
                size_max=40,
                zoom=2,
                mapbox_style='open-street-map'
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        # Top Locations Table
        st.markdown("### 📍 Most Active Locations")
        
        top_locations_query = """
        SELECT 
            location_name,
            COUNT(*) as total_sightings,
            AVG(paranormal_activity_level) as avg_activity,
            MAX(sighting_datetime) as most_recent,
            COUNT(DISTINCT ghost_id) as different_ghosts
        FROM GHOST_SIGHTINGS
        WHERE location_name IS NOT NULL
        GROUP BY location_name
        ORDER BY total_sightings DESC
        LIMIT 15
        """
        
        top_loc_df = session.sql(top_locations_query).to_pandas()
        st.dataframe(top_loc_df, use_container_width=True, hide_index=True)
    
    # ============================================
    # EVIDENCE ANALYSIS REPORT
    # ============================================
    elif report_type == "🔬 Evidence Analysis Report":
        st.subheader("🔬 Evidence Analysis Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary Statistics
        st.markdown("### 📊 Evidence Overview")
        
        evidence_stats_query = """
        SELECT 
            COUNT(*) as total_evidence,
            COUNT(DISTINCT evidence_type) as unique_types,
            COUNT(*) FILTER (WHERE processing_status = 'Analyzed') as analyzed_count,
            COUNT(*) FILTER (WHERE processing_status = 'Pending') as pending_count,
            COUNT(DISTINCT ghost_id) as ghosts_with_evidence,
            COUNT(DISTINCT sighting_id) as sightings_with_evidence
        FROM GHOST_EVIDENCE
        """
        
        evidence_stats = session.sql(evidence_stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Evidence", int(evidence_stats['TOTAL_EVIDENCE']))
        with col2:
            st.metric("Evidence Types", int(evidence_stats['UNIQUE_TYPES']))
        with col3:
            st.metric("Analyzed", int(evidence_stats['ANALYZED_COUNT']))
        with col4:
            st.metric("Pending", int(evidence_stats['PENDING_COUNT']))
        with col5:
            st.metric("Ghosts Documented", int(evidence_stats['GHOSTS_WITH_EVIDENCE']))
        with col6:
            st.metric("Sightings Documented", int(evidence_stats['SIGHTINGS_WITH_EVIDENCE']))
        
        st.markdown("---")
        
        # Evidence Type Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📷 Evidence Types")
            type_query = """
            SELECT 
                evidence_type,
                COUNT(*) as count
            FROM GHOST_EVIDENCE
            GROUP BY evidence_type
            ORDER BY count DESC
            """
            type_df = session.sql(type_query).to_pandas()
            
            fig = px.pie(type_df, values='COUNT', names='EVIDENCE_TYPE',
                        title='Evidence Type Distribution',
                        hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚙️ Processing Status")
            status_query = """
            SELECT 
                processing_status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as percentage
            FROM GHOST_EVIDENCE
            GROUP BY processing_status
            ORDER BY count DESC
            """
            status_df = session.sql(status_query).to_pandas()
            
            fig = px.bar(status_df, x='PROCESSING_STATUS', y='COUNT',
                        title='Evidence Processing Status',
                        text='PERCENTAGE')
            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Analysis Statistics
        st.markdown("### 🤖 AI Analysis Statistics")
        
        ai_stats_query = """
        SELECT 
            COUNT(*) as total_analyses,
            COUNT(DISTINCT model_used) as unique_models,
            AVG(confidence_score) as avg_confidence,
            COUNT(DISTINCT analysis_type) as analysis_types,
            COUNT(*) FILTER (WHERE embedding_vector IS NOT NULL) as with_embeddings
        FROM GHOST_AI_ANALYSIS
        """
        
        ai_stats = session.sql(ai_stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("AI Analyses", int(ai_stats['TOTAL_ANALYSES']))
        with col2:
            st.metric("Models Used", int(ai_stats['UNIQUE_MODELS']))
        with col3:
            st.metric("Avg Confidence", f"{ai_stats['AVG_CONFIDENCE']:.2%}")
        with col4:
            st.metric("Analysis Types", int(ai_stats['ANALYSIS_TYPES']))
        with col5:
            st.metric("With Embeddings", int(ai_stats['WITH_EMBEDDINGS']))
        
        # Model Performance
        st.markdown("### 🎯 Model Performance Comparison")
        
        model_perf_query = """
        SELECT 
            model_used,
            COUNT(*) as analyses,
            AVG(confidence_score) as avg_confidence,
            COUNT(DISTINCT analysis_type) as analysis_types
        FROM GHOST_AI_ANALYSIS
        GROUP BY model_used
        ORDER BY analyses DESC
        """
        
        model_perf_df = session.sql(model_perf_query).to_pandas()
        
        if not model_perf_df.empty:
            fig = px.bar(model_perf_df, x='MODEL_USED', y='ANALYSES',
                        color='AVG_CONFIDENCE',
                        title='AI Model Usage and Confidence',
                        color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        
        # Recent Evidence Table
        st.markdown("### 📋 Recent Evidence Collected")
        
        recent_evidence_query = """
        SELECT 
            e.evidence_id,
            e.evidence_type,
            g.ghost_name,
            e.capture_datetime,
            e.processing_status,
            ai.model_used,
            ai.confidence_score
        FROM GHOST_EVIDENCE e
        LEFT JOIN GHOSTS g ON e.ghost_id = g.ghost_id
        LEFT JOIN GHOST_AI_ANALYSIS ai ON e.evidence_id = ai.evidence_id
        ORDER BY e.capture_datetime DESC
        LIMIT 20
        """
        
        recent_evidence_df = session.sql(recent_evidence_query).to_pandas()
        st.dataframe(recent_evidence_df, use_container_width=True, hide_index=True)
    
    # ============================================
    # INVESTIGATIONS REPORT
    # ============================================
    elif report_type == "📋 Investigations Report":
        st.subheader("📋 Investigations Status Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary Statistics
        st.markdown("### 📊 Investigations Overview")
        
        inv_stats_query = """
        SELECT 
            COUNT(*) as total_investigations,
            COUNT(*) FILTER (WHERE status = 'Open') as open_count,
            COUNT(*) FILTER (WHERE status = 'In_Progress') as in_progress_count,
            COUNT(*) FILTER (WHERE status = 'Closed') as closed_count,
            AVG(DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE()))) as avg_duration_days
        FROM INVESTIGATIONS
        """
        
        inv_stats = session.sql(inv_stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Cases", int(inv_stats['TOTAL_INVESTIGATIONS']))
        with col2:
            st.metric("Open", int(inv_stats['OPEN_COUNT']))
        with col3:
            st.metric("In Progress", int(inv_stats['IN_PROGRESS_COUNT']))
        with col4:
            st.metric("Closed", int(inv_stats['CLOSED_COUNT']))
        with col5:
            st.metric("Avg Duration", f"{inv_stats['AVG_DURATION_DAYS']:.0f} days")
        
        st.markdown("---")
        
        # Status Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Case Status")
            status_query = """
            SELECT 
                status,
                COUNT(*) as count
            FROM INVESTIGATIONS
            GROUP BY status
            ORDER BY 
                CASE status
                    WHEN 'Open' THEN 1
                    WHEN 'In_Progress' THEN 2
                    WHEN 'Closed' THEN 3
                    ELSE 4
                END
            """
            status_df = session.sql(status_query).to_pandas()
            
            fig = px.pie(status_df, values='COUNT', names='STATUS',
                        title='Investigation Status Distribution',
                        color='STATUS',
                        color_discrete_map={
                            'Open': '#3b82f6',
                            'In_Progress': '#f59e0b',
                            'Closed': '#22c55e',
                            'Archived': '#6b7280'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⏱️ Investigation Duration")
            duration_query = """
            SELECT 
                CASE 
                    WHEN DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE())) < 7 THEN '< 1 week'
                    WHEN DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE())) < 30 THEN '1-4 weeks'
                    WHEN DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE())) < 90 THEN '1-3 months'
                    ELSE '3+ months'
                END as duration_range,
                COUNT(*) as count
            FROM INVESTIGATIONS
            GROUP BY duration_range
            ORDER BY MIN(DATEDIFF(day, start_date, COALESCE(end_date, CURRENT_DATE())))
            """
            duration_df = session.sql(duration_query).to_pandas()
            
            fig = px.bar(duration_df, x='DURATION_RANGE', y='COUNT',
                        title='Investigation Duration Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Lead Investigator Performance
        st.markdown("### 👥 Lead Investigator Performance")
        
        investigator_perf_query = """
        SELECT 
            inv.investigator_name,
            inv.specialization,
            COUNT(*) as total_cases,
            COUNT(*) FILTER (WHERE i.status = 'Closed') as closed_cases,
            AVG(DATEDIFF(day, i.start_date, COALESCE(i.end_date, CURRENT_DATE()))) as avg_duration
        FROM INVESTIGATIONS i
        JOIN INVESTIGATORS inv ON i.lead_investigator_id = inv.investigator_id
        GROUP BY inv.investigator_name, inv.specialization
        ORDER BY total_cases DESC
        LIMIT 10
        """
        
        investigator_perf_df = session.sql(investigator_perf_query).to_pandas()
        
        if not investigator_perf_df.empty:
            fig = px.bar(investigator_perf_df, 
                        x='INVESTIGATOR_NAME', 
                        y=['TOTAL_CASES', 'CLOSED_CASES'],
                        title='Top Investigators by Case Load',
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        # Active Investigations Table
        st.markdown("### 🔍 Active Investigations")
        
        active_inv_query = """
        SELECT 
            i.case_name,
            g.ghost_name,
            g.threat_level,
            inv.investigator_name as lead_investigator,
            i.start_date,
            DATEDIFF(day, i.start_date, CURRENT_DATE()) as days_open,
            i.status,
            i.priority
        FROM INVESTIGATIONS i
        LEFT JOIN GHOSTS g ON i.ghost_id = g.ghost_id
        LEFT JOIN INVESTIGATORS inv ON i.lead_investigator_id = inv.investigator_id
        WHERE i.status IN ('Open', 'In_Progress')
        ORDER BY 
            CASE i.priority
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                ELSE 4
            END,
            i.start_date
        LIMIT 20
        """
        
        active_inv_df = session.sql(active_inv_query).to_pandas()
        st.dataframe(active_inv_df, use_container_width=True, hide_index=True)
    
    # ============================================
    # INVESTIGATORS PERFORMANCE REPORT
    # ============================================
    elif report_type == "👥 Investigators Performance Report":
        st.subheader("👥 Investigators Performance Report")
        st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Summary Statistics
        st.markdown("### 📊 Team Overview")
        
        team_stats_query = """
        SELECT 
            COUNT(*) as total_investigators,
            COUNT(*) FILTER (WHERE active_status = TRUE) as active_count,
            SUM(cases_solved) as total_cases_solved,
            AVG(experience_years) as avg_experience,
            AVG(cases_solved) as avg_cases_per_investigator
        FROM INVESTIGATORS
        """
        
        team_stats = session.sql(team_stats_query).to_pandas().iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Team", int(team_stats['TOTAL_INVESTIGATORS']))
        with col2:
            st.metric("Active", int(team_stats['ACTIVE_COUNT']))
        with col3:
            st.metric("Cases Solved", int(team_stats['TOTAL_CASES_SOLVED']))
        with col4:
            st.metric("Avg Experience", f"{team_stats['AVG_EXPERIENCE']:.1f}y")
        with col5:
            st.metric("Cases per Investigator", f"{team_stats['AVG_CASES_PER_INVESTIGATOR']:.1f}")
        
        st.markdown("---")
        
        # Specialization Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Team Composition")
            spec_query = """
            SELECT 
                specialization,
                COUNT(*) as count,
                AVG(experience_years) as avg_experience
            FROM INVESTIGATORS
            WHERE active_status = TRUE
            GROUP BY specialization
            ORDER BY count DESC
            """
            spec_df = session.sql(spec_query).to_pandas()
            
            fig = px.pie(spec_df, values='COUNT', names='SPECIALIZATION',
                        title='Active Team by Specialization')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Experience Levels")
            exp_query = """
            SELECT 
                CASE 
                    WHEN experience_years < 2 THEN 'Novice (0-1y)'
                    WHEN experience_years < 5 THEN 'Intermediate (2-4y)'
                    WHEN experience_years < 10 THEN 'Experienced (5-9y)'
                    WHEN experience_years < 20 THEN 'Veteran (10-19y)'
                    ELSE 'Master (20+y)'
                END as experience_level,
                COUNT(*) as count
            FROM INVESTIGATORS
            WHERE active_status = TRUE
            GROUP BY experience_level
            ORDER BY MIN(experience_years)
            """
            exp_df = session.sql(exp_query).to_pandas()
            
            fig = px.bar(exp_df, x='EXPERIENCE_LEVEL', y='COUNT',
                        title='Experience Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Top Performers
        st.markdown("### 🏆 Top Performers")
        
        top_perf_query = """
        SELECT 
            investigator_name,
            specialization,
            cases_solved,
            experience_years,
            ROUND(cases_solved::FLOAT / NULLIF(experience_years, 0), 2) as cases_per_year
        FROM INVESTIGATORS
        WHERE active_status = TRUE
          AND cases_solved > 0
        ORDER BY cases_solved DESC
        LIMIT 15
        """
        
        top_perf_df = session.sql(top_perf_query).to_pandas()
        
        fig = px.bar(top_perf_df, 
                    x='INVESTIGATOR_NAME', 
                    y='CASES_SOLVED',
                    color='SPECIALIZATION',
                    title='Top 15 Investigators by Cases Solved',
                    hover_data=['EXPERIENCE_YEARS', 'CASES_PER_YEAR'])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance Table
        st.markdown("### 📊 Detailed Performance Metrics")
        st.dataframe(top_perf_df, use_container_width=True, hide_index=True)
    
    # Export options
    st.markdown("---")
    st.markdown("### 💾 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export to PDF", help="Coming soon"):
            st.info("PDF export feature coming soon!")
    
    with col2:
        if st.button("📊 Export to Excel", help="Coming soon"):
            st.info("Excel export feature coming soon!")
    
    with col3:
        if st.button("📧 Email Report", help="Coming soon"):
            st.info("Email functionality coming soon!")

# Footer
# ============================================
# PAGE: VOCABULARY
# ============================================
elif page == "📚 Vocabulary":
    st.header("📚 Ghost Ontology & Business Vocabulary")
    
    # Vocabulary terms
    st.subheader("🏷️ Business Vocabulary")
    vocab_query = """
    SELECT 
        term_name,
        term_category,
        definition,
        synonyms,
        related_terms,
        usage_examples
    FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY
    ORDER BY term_category, term_name
    """
    
    try:
        df_vocab = session.sql(vocab_query).to_pandas()
        
        if not df_vocab.empty:
            # Group by category
            categories = df_vocab['TERM_CATEGORY'].unique()
            
            # Create tabs for each category
            tabs = st.tabs(list(categories))
            
            for idx, category in enumerate(categories):
                with tabs[idx]:
                    st.markdown(f"### {category}")
                    category_terms = df_vocab[df_vocab['TERM_CATEGORY'] == category]
                    
                    for _, term in category_terms.iterrows():
                        with st.expander(f"📖 {term['TERM_NAME']}"):
                            st.write(f"**Definition:** {term['DEFINITION']}")
                            
                            if pd.notna(term['SYNONYMS']):
                                st.write(f"**Synonyms:** {term['SYNONYMS']}")
                            
                            if pd.notna(term['RELATED_TERMS']):
                                st.write(f"**Related Terms:** {term['RELATED_TERMS']}")
                            
                            if pd.notna(term['USAGE_EXAMPLES']):
                                st.info(f"**Usage Example:** {term['USAGE_EXAMPLES']}")
        else:
            st.info("No vocabulary terms found. Run the business vocabulary setup script.")
    except Exception as e:
        st.warning(f"Vocabulary table not yet created. Run: sql/08_business_vocabulary.sql")
    
    st.markdown("---")
    
    # Ghost Taxonomy
    st.subheader("🔬 Ghost Classification Taxonomy")
    
    taxonomy_query = """
    SELECT 
        classification_name,
        classification_level,
        parent_classification,
        description,
        key_attributes
    FROM GHOST_DETECTION.APP.GHOST_TAXONOMY
    ORDER BY classification_level, classification_name
    """
    
    try:
        df_taxonomy = session.sql(taxonomy_query).to_pandas()
        
        if not df_taxonomy.empty:
            # Display as hierarchical tree
            st.markdown("#### Classification Hierarchy")
            
            # Top-level classifications
            top_level = df_taxonomy[df_taxonomy['PARENT_CLASSIFICATION'].isna()]
            
            for _, top in top_level.iterrows():
                st.markdown(f"### 👻 {top['CLASSIFICATION_NAME']}")
                st.write(f"*{top['DESCRIPTION']}*")
                
                # Show attributes
                if pd.notna(top['KEY_ATTRIBUTES']):
                    st.write(f"**Key Attributes:** {top['KEY_ATTRIBUTES']}")
                
                # Show children
                children = df_taxonomy[df_taxonomy['PARENT_CLASSIFICATION'] == top['CLASSIFICATION_NAME']]
                if not children.empty:
                    cols = st.columns(min(len(children), 3))
                    for idx, (_, child) in enumerate(children.iterrows()):
                        with cols[idx % 3]:
                            with st.container():
                                st.markdown(f"**{child['CLASSIFICATION_NAME']}**")
                                st.caption(child['DESCRIPTION'])
                
                st.markdown("---")
        else:
            st.info("No taxonomy data found. Run the business vocabulary setup script.")
    except Exception as e:
        st.warning(f"Taxonomy table not yet created. Run: sql/08_business_vocabulary.sql")
    
    st.markdown("---")
    
    # Search vocabulary
    st.subheader("🔍 Search Vocabulary")
    search_term = st.text_input("Search for a term...")
    
    if search_term:
        # Use ARRAY_TO_STRING to search within array columns
        search_query = f"""
        SELECT 
            term_name,
            term_category,
            definition,
            ARRAY_TO_STRING(synonyms, ', ') as synonyms_text
        FROM GHOST_DETECTION.APP.BUSINESS_VOCABULARY
        WHERE LOWER(term_name) LIKE LOWER('%{search_term}%')
           OR LOWER(definition) LIKE LOWER('%{search_term}%')
           OR LOWER(ARRAY_TO_STRING(synonyms, ', ')) LIKE LOWER('%{search_term}%')
        ORDER BY term_name
        """
        
        try:
            df_search = session.sql(search_query).to_pandas()
            
            if not df_search.empty:
                st.success(f"Found {len(df_search)} matching terms")
                
                for _, result in df_search.iterrows():
                    with st.expander(f"📖 {result['TERM_NAME']} ({result['TERM_CATEGORY']})"):
                        st.write(f"**Definition:** {result['DEFINITION']}")
                        if pd.notna(result['SYNONYMS_TEXT']) and result['SYNONYMS_TEXT']:
                            st.write(f"**Synonyms:** {result['SYNONYMS_TEXT']}")
            else:
                st.warning("No matching terms found.")
        except Exception as e:
            st.error(f"Search error: {str(e)}")
            st.info("💡 Tip: Make sure you've run sql/08_business_vocabulary.sql to create the vocabulary tables.")

# ============================================
# PAGE: IMAGE SIMILARITY SEARCH
# ============================================
elif page == "🔍 Image Similarity":
    st.header("🔍 Image Similarity Search")
    st.markdown("### Find Similar Paranormal Images Using AI Embeddings")
    
    # Check if embeddings table exists
    try:
        embeddings_count = session.sql("SELECT COUNT(*) as cnt FROM GHOST_DETECTION.APP.GHOST_IMAGE_EMBEDDINGS").collect()[0]['CNT']
        
        if embeddings_count == 0:
            st.warning("⚠️ No image embeddings found yet.")
            st.info("Run the following to generate embeddings:")
            st.code("CALL GHOST_DETECTION.APP.BATCH_GENERATE_EMBEDDINGS();", language="sql")
        else:
            st.success(f"✅ {embeddings_count} image embeddings available for search")
            
    except Exception as e:
        st.error("❌ Image embeddings table not found. Please run: sql/14_image_embeddings_table.sql")
        st.stop()
    
    # Create tabs for different search methods
    tab1, tab2, tab3, tab4 = st.tabs(["🔎 Text Search", "🖼️ Image-to-Image", "📊 Statistics", "🎯 Generate Embeddings"])
    
    # TAB 1: Text-based similarity search
    with tab1:
        st.subheader("Search by Description")
        st.write("Enter a description to find similar paranormal images")
        
        # Search input
        search_query = st.text_area(
            "Search Query",
            value="translucent figure in white clothing",
            height=100,
            help="Describe the type of paranormal image you're looking for"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            top_k = st.slider("Number of results", 1, 20, 5)
        with col2:
            search_button = st.button("🔍 Search", type="primary", use_container_width=True)
        
        if search_button and search_query:
            with st.spinner("🔄 Searching for similar images..."):
                try:
                    # Use the FIND_SIMILAR_IMAGES procedure
                    search_sql = f"""
                    CALL GHOST_DETECTION.APP.FIND_SIMILAR_IMAGES(
                        '{search_query.replace("'", "''")}',
                        {top_k}
                    )
                    """
                    
                    results = session.sql(search_sql).to_pandas()
                    
                    if not results.empty:
                        st.success(f"Found {len(results)} similar images!")
                        
                        # Display results
                        for idx, row in results.iterrows():
                            with st.expander(
                                f"Match #{idx+1} - Similarity: {row['SIMILARITY_SCORE']:.3f} - {row['IMAGE_DESCRIPTION'][:80]}..."
                            ):
                                col1, col2 = st.columns([1, 2])
                                
                                with col1:
                                    st.metric("Similarity Score", f"{row['SIMILARITY_SCORE']:.3f}")
                                    st.write(f"**Evidence ID:** {row['EVIDENCE_ID']}")
                                    st.write(f"**Ghost ID:** {row['GHOST_ID']}")
                                    st.write(f"**Path:** `{row['IMAGE_PATH']}`")
                                
                                with col2:
                                    st.write("**Original Description:**")
                                    st.write(row['IMAGE_DESCRIPTION'])
                                    
                                    if pd.notna(row.get('AI_DESCRIPTION')):
                                        st.write("**AI Analysis:**")
                                        st.write(row['AI_DESCRIPTION'][:500] + "..." if len(str(row['AI_DESCRIPTION'])) > 500 else row['AI_DESCRIPTION'])
                    else:
                        st.warning("No similar images found. Try a different search query.")
                        
                except Exception as e:
                    st.error(f"Search error: {str(e)}")
                    st.info("💡 Make sure the FIND_SIMILAR_IMAGES function exists and embeddings are generated.")
    
    # TAB 2: Image-to-image similarity
    with tab2:
        st.subheader("Find Similar Images")
        st.write("Select an image to find others that are similar")
        
        # Get list of available embeddings
        try:
            embeddings_list = session.sql("""
                SELECT 
                    e.embedding_id,
                    e.evidence_id,
                    e.image_description,
                    g.ghost_name,
                    g.ghost_type
                FROM GHOST_DETECTION.APP.GHOST_IMAGE_EMBEDDINGS e
                LEFT JOIN GHOST_DETECTION.APP.GHOSTS g ON e.ghost_id = g.ghost_id
                ORDER BY e.created_at DESC
                LIMIT 100
            """).to_pandas()
            
            if not embeddings_list.empty:
                # Create selection dropdown
                embedding_options = {
                    f"{row['EMBEDDING_ID']} - {row['IMAGE_DESCRIPTION'][:60]}...": row['EMBEDDING_ID']
                    for _, row in embeddings_list.iterrows()
                }
                
                selected_display = st.selectbox(
                    "Select Source Image",
                    options=list(embedding_options.keys())
                )
                
                selected_embedding_id = embedding_options[selected_display]
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    top_k_img = st.slider("Number of similar images", 1, 20, 5, key="img_slider")
                with col2:
                    find_button = st.button("🔍 Find Similar", type="primary", use_container_width=True)
                
                if find_button:
                    with st.spinner("🔄 Finding similar images..."):
                        try:
                            similarity_sql = f"""
                            CALL GHOST_DETECTION.APP.FIND_SIMILAR_TO_IMAGE(
                                '{selected_embedding_id}',
                                {top_k_img}
                            )
                            """
                            
                            similar_results = session.sql(similarity_sql).to_pandas()
                            
                            if not similar_results.empty:
                                st.success(f"Found {len(similar_results)} similar images!")
                                
                                # Display in grid
                                cols = st.columns(2)
                                for idx, row in similar_results.iterrows():
                                    with cols[idx % 2]:
                                        with st.container():
                                            st.markdown(f"**Similarity: {row['SIMILARITY_SCORE']:.3f}**")
                                            st.write(f"📸 {row['IMAGE_DESCRIPTION'][:100]}...")
                                            st.caption(f"Evidence: {row['EVIDENCE_ID']} | Ghost: {row['GHOST_ID']}")
                                            st.caption(f"Path: `{row['IMAGE_PATH']}`")
                                            st.markdown("---")
                            else:
                                st.warning("No similar images found.")
                                
                        except Exception as e:
                            st.error(f"Similarity search error: {str(e)}")
            else:
                st.info("No embeddings available. Generate some first in the 'Generate Embeddings' tab.")
                
        except Exception as e:
            st.error(f"Error loading embeddings: {str(e)}")
    
    # TAB 3: Statistics
    with tab3:
        st.subheader("📊 Image Embedding Statistics")
        
        try:
            # Get statistics
            stats = session.sql("""
                SELECT * FROM GHOST_DETECTION.APP.VW_IMAGE_SIMILARITY_STATS
            """).to_pandas()
            
            if not stats.empty:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Embeddings", int(stats['TOTAL_EMBEDDINGS'].iloc[0]))
                with col2:
                    st.metric("Unique Ghosts", int(stats['UNIQUE_GHOSTS'].iloc[0]))
                with col3:
                    st.metric("Avg Confidence", f"{stats['AVG_CONFIDENCE'].iloc[0]:.3f}")
                with col4:
                    st.metric("Recent (7 days)", int(stats['RECENT_EMBEDDINGS'].iloc[0]))
                
                st.markdown("---")
                
                # Popular searches
                st.subheader("🔥 Most Searched Images")
                popular = session.sql("""
                    SELECT * FROM GHOST_DETECTION.APP.VW_POPULAR_IMAGE_SEARCHES
                    LIMIT 10
                """).to_pandas()
                
                if not popular.empty:
                    st.dataframe(
                        popular[['GHOST_NAME', 'GHOST_TYPE', 'IMAGE_DESCRIPTION', 'SEARCH_COUNT', 'CONFIDENCE_SCORE']],
                        use_container_width=True
                    )
                else:
                    st.info("No search history yet.")
                
                st.markdown("---")
                
                # Embedding performance
                st.subheader("⚡ Embedding Generation Performance")
                perf = session.sql("""
                    SELECT * FROM GHOST_DETECTION.APP.VW_EMBEDDING_PERFORMANCE
                    LIMIT 24
                """).to_pandas()
                
                if not perf.empty:
                    fig = px.line(
                        perf,
                        x='HOUR',
                        y='EMBEDDINGS_GENERATED',
                        title='Embeddings Generated (Last 24 Hours)',
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")
    
    # TAB 4: Generate Embeddings
    with tab4:
        st.subheader("🎯 Generate Image Embeddings")
        st.write("Create AI embeddings for images without them")
        
        # Check how many need embedding
        try:
            needs_embedding = session.sql("""
                SELECT COUNT(*) as cnt
                FROM GHOST_DETECTION.APP.GHOST_EVIDENCE e
                LEFT JOIN GHOST_DETECTION.APP.GHOST_IMAGE_EMBEDDINGS emb 
                    ON e.evidence_id = emb.evidence_id
                WHERE e.evidence_type IN ('Photograph', 'Video', 'Thermal Image', 'Image')
                  AND emb.embedding_id IS NULL
            """).collect()[0]['CNT']
            
            st.info(f"📊 {needs_embedding} images need embeddings")
            
            if needs_embedding > 0:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    if st.button("🚀 Generate All Embeddings", type="primary", use_container_width=True):
                        with st.spinner(f"⏳ Generating embeddings for {needs_embedding} images..."):
                            try:
                                result = session.call("GHOST_DETECTION.APP.BATCH_GENERATE_EMBEDDINGS")
                                st.success(f"✅ {result}")
                                st.balloons()
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                
                with col2:
                    st.metric("To Process", needs_embedding)
            else:
                st.success("✅ All images have embeddings!")
            
            st.markdown("---")
            
            # Manual single embedding generation
            st.subheader("➕ Generate Single Embedding")
            
            with st.form("single_embedding_form"):
                evidence_id = st.text_input("Evidence ID", placeholder="EV0001")
                description = st.text_area(
                    "Image Description",
                    placeholder="Describe the paranormal image...",
                    height=100
                )
                
                submit = st.form_submit_button("Generate Embedding")
                
                if submit and evidence_id and description:
                    try:
                        result = session.call(
                            "GHOST_DETECTION.APP.GENERATE_IMAGE_EMBEDDING",
                            evidence_id,
                            description
                        )
                        st.success(f"✅ {result}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        
        except Exception as e:
            st.error(f"Error checking embeddings: {str(e)}")

# ============================================
# PAGE: SNOWBREAKERS CHAT
# ============================================
elif page == "💬 SnowBreakers Chat":
    st.markdown("# 💬 SnowBreakers AI Chat")
    st.markdown("### *Ask me anything about ghosts, sightings, and paranormal activity!*")
    st.markdown("---")
    
    # Initialize chat history in session state
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "👻 Hello! I'm the SnowBreakers AI Assistant. I can help you analyze ghost data, find patterns in sightings, and answer questions about paranormal activity. What would you like to know?"}
        ]
    
    # Sidebar with quick suggestions
    with st.sidebar:
        st.markdown("---")
        st.subheader("💡 Quick Questions")
        
        suggestions = [
            "How many ghosts have we detected?",
            "What's the most common ghost type?",
            "Show me recent high-threat sightings",
            "Where are the paranormal hotspots?",
            "What ghost patterns have we observed?",
            "Analyze ghost activity by time of day",
            "Which ghosts are most dangerous?",
            "Show investigation success rates"
        ]
        
        st.markdown("Click to ask:")
        for suggestion in suggestions:
            if st.button(f"📝 {suggestion}", key=f"suggest_{suggestions.index(suggestion)}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": suggestion})
                st.rerun()
    
    # Display chat messages
    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about ghost data..."):
        # Add user message to chat
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Analyzing ghost data..."):
                try:
                    # Build context from database
                    context_parts = []
                    
                    # Get ghost statistics
                    try:
                        ghost_stats = session.sql("""
                            SELECT 
                                COUNT(*) as total_ghosts,
                                COUNT(DISTINCT ghost_type) as unique_types,
                                AVG(threat_level) as avg_threat
                            FROM GHOST_DETECTION.APP.GHOSTS
                        """).collect()[0]
                        
                        context_parts.append(f"""
Database Statistics:
- Total Ghosts: {ghost_stats['TOTAL_GHOSTS']}
- Unique Ghost Types: {ghost_stats['UNIQUE_TYPES']}
- Average Threat Level: {ghost_stats['AVG_THREAT']:.2f}
""")
                    except:
                        pass
                    
                    # Get recent sightings
                    try:
                        recent = session.sql("""
                            SELECT 
                                COUNT(*) as recent_count,
                                MAX(sighting_date) as latest_date
                            FROM GHOST_DETECTION.APP.GHOST_SIGHTINGS
                            WHERE sighting_date >= DATEADD(day, -7, CURRENT_DATE())
                        """).collect()[0]
                        
                        context_parts.append(f"""
Recent Activity:
- Sightings (Last 7 days): {recent['RECENT_COUNT']}
- Latest Sighting: {recent['LATEST_DATE']}
""")
                    except:
                        pass
                    
                    # Get top ghost types
                    try:
                        top_types = session.sql("""
                            SELECT ghost_type, COUNT(*) as count
                            FROM GHOST_DETECTION.APP.GHOSTS
                            GROUP BY ghost_type
                            ORDER BY count DESC
                            LIMIT 3
                        """).collect()
                        
                        types_str = ", ".join([f"{row['GHOST_TYPE']} ({row['COUNT']})" for row in top_types])
                        context_parts.append(f"Top Ghost Types: {types_str}")
                    except:
                        pass
                    
                    # Build comprehensive prompt
                    system_context = "\n".join(context_parts)
                    
                    full_prompt = f"""You are the SnowBreakers AI Assistant, an expert in paranormal activity and ghost detection. 
You have access to a comprehensive ghost detection database with information about ghosts, sightings, evidence, and investigations.

Current Database Context:
{system_context}

User Question: {prompt}

Instructions:
- Provide helpful, accurate responses based on the database context
- If the question requires specific data not in the context, suggest SQL queries or analysis
- Use emojis appropriately (👻 🔍 📊 ⚠️ 💡)
- Be conversational but professional
- If you don't have enough information, suggest what data would be helpful
- Format responses with bullet points and clear sections when appropriate

Response:"""
                    
                    # Use Cortex Complete for response
                    response = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE(
                            'mistral-large2',
                            '{full_prompt.replace("'", "''")}'
                        ) as response
                    """).collect()[0]['RESPONSE']
                    
                    # Display response
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.chat_messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"⚠️ I encountered an error accessing the ghost database: {str(e)}\n\nPlease try rephrasing your question or ask about:\n- Ghost statistics and counts\n- Recent sightings and patterns\n- Threat assessments\n- Investigation data"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
    
    # Chat controls
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_messages = [
                {"role": "assistant", "content": "👻 Chat cleared! What would you like to know?"}
            ]
            st.rerun()
    
    with col2:
        if st.button("💾 Export Chat", use_container_width=True):
            # Export chat as JSON
            chat_export = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.chat_messages
            }
            st.download_button(
                label="📥 Download JSON",
                data=json.dumps(chat_export, indent=2),
                file_name=f"snowbreakers_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    # Additional features
    with st.expander("🔧 Advanced Features"):
        st.markdown("### Direct Database Query")
        st.markdown("*For advanced users: Execute custom SQL queries*")
        
        custom_query = st.text_area(
            "SQL Query",
            placeholder="SELECT * FROM GHOST_DETECTION.APP.GHOSTS LIMIT 10;",
            height=100
        )
        
        if st.button("▶️ Execute Query"):
            if custom_query:
                try:
                    result = session.sql(custom_query).to_pandas()
                    st.success(f"✅ Query executed successfully! Returned {len(result)} rows.")
                    st.dataframe(result, use_container_width=True)
                    
                    # Add result summary to chat
                    summary = f"📊 Executed custom query: `{custom_query}`. Returned {len(result)} rows."
                    st.session_state.chat_messages.append({"role": "assistant", "content": summary})
                    
                except Exception as e:
                    st.error(f"❌ Query error: {str(e)}")
            else:
                st.warning("Please enter a SQL query")
    
    with st.expander("💡 Usage Tips"):
        st.markdown("""
        ### How to Use SnowBreakers Chat
        
        **Ask Natural Questions:**
        - "How many ghosts have we detected this month?"
        - "What's the average threat level of poltergeists?"
        - "Show me sightings in abandoned buildings"
        
        **Get Insights:**
        - "What patterns do you see in recent activity?"
        - "Which locations have the most sightings?"
        - "Analyze ghost behavior trends"
        
        **Request Analysis:**
        - "Compare ghost types by danger level"
        - "Find correlations between EMF readings and ghost types"
        - "Identify paranormal hotspots"
        
        **Explore Data:**
        - Use the quick questions in the sidebar
        - Ask follow-up questions for deeper analysis
        - Request specific charts or visualizations
        
        **Pro Tips:**
        - Be specific in your questions for better results
        - Ask for SQL queries if you want to see the data directly
        - Use the export feature to save important conversations
        """)

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Ghost Detection System v1.0 | Powered by Snowflake Cortex AI</p>
        <p>👻 Who you gonna call? SnowGhost Breakers! 🚫👻</p>
    </div>
    """,
    unsafe_allow_html=True
)

