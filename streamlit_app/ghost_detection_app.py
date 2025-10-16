"""
Ghost Detection and Analysis Application
Streamlit Application for Snowflake
"""

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
     "📋 Investigations", "🤖 AI Insights", "➕ New Sighting", "📈 Analytics", "📚 Vocabulary"]
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
    hotspots_df = session.table("GHOST_DETECTION.ANALYTICS.VW_PARANORMAL_HOTSPOTS").to_pandas()
    if not hotspots_df.empty and 'LATITUDE' in hotspots_df.columns:
        fig = px.scatter_mapbox(
            hotspots_df,
            lat='LATITUDE',
            lon='LONGITUDE',
            size='TOTAL_SIGHTINGS',
            color='HOTSPOT_CLASSIFICATION',
            hover_name='LOCATION_NAME',
            hover_data=['TOTAL_SIGHTINGS', 'UNIQUE_GHOSTS', 'AVG_ACTIVITY_LEVEL'],
            zoom=10,
            mapbox_style="carto-positron"
        )
        st.plotly_chart(fig, use_container_width=True)

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
    WHERE s.LATITUDE IS NOT NULL AND s.LONGITUDE IS NOT NULL
    ORDER BY s.SIGHTING_DATETIME DESC
    LIMIT 100
    """
    
    map_df = session.sql(map_query).to_pandas()
    
    if not map_df.empty:
        fig = px.scatter_mapbox(
            map_df,
            lat='LATITUDE',
            lon='LONGITUDE',
            size='PARANORMAL_ACTIVITY_LEVEL',
            color='GHOST_TYPE',
            hover_name='LOCATION_NAME',
            hover_data={'GHOST_NAME': True, 'GHOST_TYPE': True, 
                       'SIGHTING_DATETIME': True, 'PARANORMAL_ACTIVITY_LEVEL': True,
                       'LATITUDE': False, 'LONGITUDE': False},
            zoom=10,
            height=500,
            mapbox_style="carto-positron",
            title="Recent Ghost Sightings"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No sightings with location coordinates available. Add coordinates when reporting new sightings!")
    
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
    if uploaded_files:
        st.markdown("### 🔍 AI Image Analysis")
        cols = st.columns(min(len(uploaded_files), 3))
        
        for idx, uploaded_file in enumerate(uploaded_files):
            col = cols[idx % 3]
            with col:
                st.image(uploaded_file, caption=uploaded_file.name, use_column_width=True)
                
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
    
    with st.form("new_sighting_form"):
        st.subheader("📍 Location Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            location_name = st.text_input("Location Name*", help="e.g., 'Old Victorian Mansion'")
            location_address = st.text_area("Full Address", height=80)
            witness_name = st.text_input("Witness Name*")
            witness_contact = st.text_input("Witness Contact", help="Email or phone")
        
        with col2:
            st.markdown("**📍 Location Coordinates**")
            use_map = st.checkbox("📍 Show location on map", value=True)
            
            col_lat, col_lon = st.columns(2)
            with col_lat:
                latitude = st.number_input("Latitude", value=40.7128, format="%.6f")
            with col_lon:
                longitude = st.number_input("Longitude", value=-74.0060, format="%.6f")
            
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
                sighting_id = f"SIGHT_{str(uuid.uuid4())[:8].upper()}"
                sighting_datetime = datetime.combine(sighting_date, sighting_time)
                
                # Combine description with image analysis
                full_desc = description
                if image_analysis_results:
                    full_desc += "\n\n--- AI IMAGE ANALYSIS ---\n"
                    for img in image_analysis_results:
                        full_desc += f"\n{img['filename']}:\n{img['analysis']}\n"
                
                with st.spinner("🤖 Analyzing with AI..."):
                    try:
                        classification = Complete(
                            'mistral-large2',
                            f"Classify this paranormal sighting as: Apparition, Poltergeist, Shadow Figure, "
                            f"Orb, Residual Haunt, Intelligent Haunt, Demonic, or Unknown. "
                            f"Description: {full_desc}. Location: {location_name}. Activity: {paranormal_level}/10. "
                            f"Return classification and brief explanation."
                        )
                        
                        st.success("✅ Sighting reported successfully!")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Sighting ID", sighting_id)
                        with col2:
                            st.metric("Activity Level", f"{paranormal_level}/10")
                        with col3:
                            st.metric("Photos", len(image_analysis_results))
                        
                        st.info(f"🤖 **AI Classification:**\n\n{classification}")
                        if latitude != 0 or longitude != 0:
                            st.success(f"📍 Location: {latitude:.6f}, {longitude:.6f}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
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
        usage_context
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
                            
                            if pd.notna(term['USAGE_CONTEXT']):
                                st.info(f"**Usage:** {term['USAGE_CONTEXT']}")
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

