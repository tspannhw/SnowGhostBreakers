"""
Ghost Detection and Analysis Application
Streamlit Application for Snowflake
"""

import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import functions as F
from snowflake.cortex import Complete, Sentiment, Classify
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
     "📋 Investigations", "🤖 AI Insights", "➕ New Sighting", "📈 Analytics"]
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
    
    # Query sightings
    sightings_query = session.table("GHOST_DETECTION.APP.GHOST_SIGHTINGS").join(
        session.table("GHOST_DETECTION.APP.GHOSTS"),
        "GHOST_ID"
    )
    
    # Apply filters
    if selected_ghost_type != "All":
        sightings_query = sightings_query.filter(F.col("GHOST_TYPE") == selected_ghost_type)
    
    if selected_threat != "All":
        sightings_query = sightings_query.filter(F.col("THREAT_LEVEL") == selected_threat)
    
    sightings_df = sightings_query.select(
        "SIGHTING_ID", "GHOST_NAME", "GHOST_TYPE", "LOCATION_NAME", 
        "SIGHTING_DATETIME", "PARANORMAL_ACTIVITY_LEVEL", "EMF_READING",
        "TEMPERATURE_CELSIUS", "VERIFIED", "DESCRIPTION"
    ).order_by(F.col("SIGHTING_DATETIME").desc()).limit(100).to_pandas()
    
    st.write(f"**Showing {len(sightings_df)} recent sightings**")
    
    # Display sightings
    for idx, row in sightings_df.iterrows():
        with st.expander(
            f"📍 {row['LOCATION_NAME']} - {row['GHOST_NAME']} "
            f"({row['SIGHTING_DATETIME'].strftime('%Y-%m-%d %H:%M')})"
        ):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {row['DESCRIPTION']}")
                st.write(f"**Ghost:** {row['GHOST_NAME']} ({row['GHOST_TYPE']})")
            
            with col2:
                st.metric("Activity Level", f"{row['PARANORMAL_ACTIVITY_LEVEL']}/10")
                st.metric("EMF Reading", f"{row['EMF_READING']:.1f} mG")
                st.metric("Temperature", f"{row['TEMPERATURE_CELSIUS']:.1f}°C")
                
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
        evidence_type_counts = evidence_df['EVIDENCE_TYPE'].value_counts()
        fig = px.bar(x=evidence_type_counts.index, y=evidence_type_counts.values,
                     labels={'x': 'Evidence Type', 'y': 'Count'})
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
        st.subheader("Threat Level Predictions")
        st.info("Coming soon: Predictive analytics for ghost behavior patterns")

# ============================================
# PAGE: NEW SIGHTING
# ============================================
elif page == "➕ New Sighting":
    st.header("➕ Report New Ghost Sighting")
    
    with st.form("new_sighting_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            location_name = st.text_input("Location Name*")
            location_address = st.text_area("Address")
            latitude = st.number_input("Latitude", format="%.6f")
            longitude = st.number_input("Longitude", format="%.6f")
            
            witness_name = st.text_input("Witness Name*")
            witness_contact = st.text_input("Witness Contact")
        
        with col2:
            sighting_date = st.date_input("Sighting Date*")
            sighting_time = st.time_input("Sighting Time*")
            
            evidence_type = st.selectbox(
                "Evidence Type*",
                ["Visual", "Audio", "EMF", "Temperature", "Multiple"]
            )
            
            paranormal_level = st.slider("Paranormal Activity Level", 1, 10, 5)
            temperature = st.number_input("Temperature (°C)", value=20.0)
            emf_reading = st.number_input("EMF Reading (mG)", value=0.0)
        
        description = st.text_area("Description of Sighting*", height=150)
        environmental = st.text_area("Environmental Conditions", height=100)
        
        submitted = st.form_submit_button("📝 Submit Sighting Report")
        
        if submitted:
            if location_name and witness_name and description:
                # Generate IDs
                import uuid
                sighting_id = f"SIGHT{str(uuid.uuid4())[:8].upper()}"
                
                sighting_datetime = datetime.combine(sighting_date, sighting_time)
                
                # Use Cortex AI to classify ghost type
                with st.spinner("Analyzing description with AI..."):
                    ghost_type_result = session.call(
                        "GHOST_DETECTION.APP.CLASSIFY_GHOST_TYPE",
                        description
                    )
                    
                    st.success(f"✅ Sighting reported successfully!")
                    st.info(f"**AI Classification:** {ghost_type_result}")
                    st.write(f"**Sighting ID:** {sighting_id}")
                    
                    # Note: In production, insert into database here
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
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Ghost Detection System v1.0 | Powered by Snowflake Cortex AI</p>
        <p>👻 Who you gonna call? Ghostbusters! 🚫👻</p>
    </div>
    """,
    unsafe_allow_html=True
)

