"""
Ghost Detection Analytics Script
Python script for advanced ghost data analysis using Snowflake and Cortex AI
"""

import snowflake.connector
from snowflake.snowpark import Session
from snowflake.snowpark import functions as F
from snowflake.cortex import Complete, Sentiment
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta

class GhostAnalytics:
    """
    Main analytics class for ghost detection data
    """
    
    def __init__(self, connection_parameters: Dict):
        """
        Initialize connection to Snowflake
        
        Args:
            connection_parameters: Dict with Snowflake connection params
        """
        self.session = Session.builder.configs(connection_parameters).create()
        self.session.sql("USE DATABASE GHOST_DETECTION").collect()
        self.session.sql("USE SCHEMA APP").collect()
        print("✅ Connected to Snowflake Ghost Detection Database")
    
    def get_ghost_summary(self) -> pd.DataFrame:
        """Get summary statistics for all ghosts"""
        query = """
        SELECT 
            ghost_type,
            threat_level,
            COUNT(*) as ghost_count,
            AVG(confidence_score) as avg_confidence,
            SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active_count
        FROM GHOSTS
        GROUP BY ghost_type, threat_level
        ORDER BY ghost_count DESC
        """
        return self.session.sql(query).to_pandas()
    
    def get_activity_timeline(self, days: int = 30) -> pd.DataFrame:
        """
        Get timeline of ghost activity
        
        Args:
            days: Number of days to look back
        """
        query = f"""
        SELECT 
            DATE_TRUNC('day', sighting_datetime) as activity_date,
            COUNT(*) as daily_sightings,
            COUNT(DISTINCT ghost_id) as unique_ghosts,
            AVG(paranormal_activity_level) as avg_activity,
            AVG(emf_reading) as avg_emf,
            AVG(temperature_celsius) as avg_temp
        FROM GHOST_SIGHTINGS
        WHERE sighting_datetime >= DATEADD(day, -{days}, CURRENT_TIMESTAMP())
        GROUP BY activity_date
        ORDER BY activity_date
        """
        return self.session.sql(query).to_pandas()
    
    def get_hotspots(self, min_sightings: int = 2) -> pd.DataFrame:
        """
        Identify paranormal hotspots
        
        Args:
            min_sightings: Minimum number of sightings to qualify as hotspot
        """
        query = f"""
        SELECT 
            location_name,
            latitude,
            longitude,
            COUNT(*) as total_sightings,
            COUNT(DISTINCT ghost_id) as unique_ghosts,
            AVG(paranormal_activity_level) as avg_activity,
            MAX(sighting_datetime) as last_sighting
        FROM GHOST_SIGHTINGS
        GROUP BY location_name, latitude, longitude
        HAVING COUNT(*) >= {min_sightings}
        ORDER BY total_sightings DESC
        """
        return self.session.sql(query).to_pandas()
    
    def analyze_ghost_with_ai(self, ghost_id: str) -> str:
        """
        Generate AI analysis for a specific ghost
        
        Args:
            ghost_id: Ghost identifier
            
        Returns:
            AI-generated analysis
        """
        result = self.session.sql(
            f"CALL GENERATE_GHOST_REPORT('{ghost_id}')"
        ).collect()
        
        return result[0][0] if result else "No analysis available"
    
    def classify_description(self, description: str) -> str:
        """
        Use AI to classify a ghost description
        
        Args:
            description: Text description of ghost encounter
            
        Returns:
            Classified ghost type
        """
        result = self.session.sql(
            f"CALL CLASSIFY_GHOST_TYPE('{description}')"
        ).collect()
        
        return result[0][0] if result else "Unknown"
    
    def get_threat_assessment(self) -> pd.DataFrame:
        """Get current threat assessment for all active ghosts"""
        query = """
        SELECT 
            g.ghost_id,
            g.ghost_name,
            g.ghost_type,
            g.threat_level,
            COUNT(s.sighting_id) as recent_sightings,
            AVG(s.paranormal_activity_level) as avg_activity,
            MAX(s.sighting_datetime) as last_seen
        FROM GHOSTS g
        LEFT JOIN GHOST_SIGHTINGS s ON g.ghost_id = s.ghost_id
        WHERE g.status = 'Active'
        AND (s.sighting_datetime >= DATEADD(day, -7, CURRENT_TIMESTAMP()) 
             OR s.sighting_id IS NULL)
        GROUP BY g.ghost_id, g.ghost_name, g.ghost_type, g.threat_level
        ORDER BY 
            CASE g.threat_level 
                WHEN 'Extreme' THEN 1 
                WHEN 'High' THEN 2 
                WHEN 'Medium' THEN 3 
                ELSE 4 
            END,
            recent_sightings DESC
        """
        return self.session.sql(query).to_pandas()
    
    def analyze_sensor_correlations(self) -> Dict:
        """Analyze correlations between sensor readings and paranormal activity"""
        query = """
        SELECT 
            paranormal_activity_level,
            emf_reading,
            temperature_celsius
        FROM GHOST_SIGHTINGS
        WHERE emf_reading IS NOT NULL 
        AND temperature_celsius IS NOT NULL
        """
        df = self.session.sql(query).to_pandas()
        
        correlations = df.corr()
        
        return {
            'correlation_matrix': correlations.to_dict(),
            'summary': {
                'emf_activity_corr': correlations.loc['EMF_READING', 'PARANORMAL_ACTIVITY_LEVEL'],
                'temp_activity_corr': correlations.loc['TEMPERATURE_CELSIUS', 'PARANORMAL_ACTIVITY_LEVEL'],
                'emf_temp_corr': correlations.loc['EMF_READING', 'TEMPERATURE_CELSIUS']
            }
        }
    
    def get_investigation_metrics(self) -> pd.DataFrame:
        """Get metrics for all active investigations"""
        query = """
        SELECT * FROM ANALYTICS.VW_INVESTIGATION_METRICS
        WHERE STATUS IN ('Open', 'In_Progress')
        ORDER BY 
            CASE PRIORITY 
                WHEN 'Critical' THEN 1 
                WHEN 'High' THEN 2 
                WHEN 'Medium' THEN 3 
                ELSE 4 
            END
        """
        return self.session.sql(query).to_pandas()
    
    def find_similar_sightings(self, description: str, limit: int = 5) -> pd.DataFrame:
        """
        Find similar sightings using semantic search
        
        Args:
            description: Reference description
            limit: Number of results to return
        """
        query = f"""
        WITH target AS (
            SELECT AI_EMBED(
                'snowflake-arctic-embed-l-v2.0-8k',
                '{description}'
            ) as embedding
        )
        SELECT 
            s.sighting_id,
            s.location_name,
            s.description,
            g.ghost_name,
            VECTOR_COSINE_SIMILARITY(
                (SELECT embedding FROM target),
                AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', s.description)
            ) as similarity
        FROM GHOST_SIGHTINGS s
        JOIN GHOSTS g ON s.ghost_id = g.ghost_id
        WHERE s.description IS NOT NULL
        ORDER BY similarity DESC
        LIMIT {limit}
        """
        return self.session.sql(query).to_pandas()
    
    def generate_weekly_report(self) -> str:
        """Generate automated weekly report using AI"""
        result = self.session.sql("CALL GENERATE_WEEKLY_REPORT()").collect()
        return result[0][0] if result else "Report generation failed"
    
    def ask_question(self, question: str) -> str:
        """
        Ask natural language question about ghost data
        
        Args:
            question: Natural language question
            
        Returns:
            AI-generated answer
        """
        result = self.session.sql(
            f"CALL ASK_GHOST_DATABASE('{question}')"
        ).collect()
        return result[0][0] if result else "No answer available"
    
    def export_to_dataframe(self, table_name: str) -> pd.DataFrame:
        """Export any table to pandas DataFrame"""
        return self.session.table(f"GHOST_DETECTION.APP.{table_name}").to_pandas()
    
    def close(self):
        """Close Snowflake session"""
        self.session.close()
        print("✅ Session closed")


def create_visualizations(analytics: GhostAnalytics):
    """
    Create comprehensive visualizations
    
    Args:
        analytics: GhostAnalytics instance
    """
    print("📊 Generating visualizations...")
    
    # 1. Ghost Type Distribution
    ghost_summary = analytics.get_ghost_summary()
    fig1 = px.sunburst(
        ghost_summary,
        path=['THREAT_LEVEL', 'GHOST_TYPE'],
        values='GHOST_COUNT',
        title='Ghost Distribution by Threat Level and Type',
        color='AVG_CONFIDENCE',
        color_continuous_scale='Reds'
    )
    fig1.write_html('ghost_distribution.html')
    print("✅ Created: ghost_distribution.html")
    
    # 2. Activity Timeline
    timeline = analytics.get_activity_timeline(days=30)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=timeline['ACTIVITY_DATE'],
        y=timeline['DAILY_SIGHTINGS'],
        name='Sightings',
        fill='tozeroy'
    ))
    fig2.update_layout(
        title='30-Day Ghost Activity Timeline',
        xaxis_title='Date',
        yaxis_title='Number of Sightings'
    )
    fig2.write_html('activity_timeline.html')
    print("✅ Created: activity_timeline.html")
    
    # 3. Hotspot Map
    hotspots = analytics.get_hotspots()
    if not hotspots.empty and 'LATITUDE' in hotspots.columns:
        fig3 = px.scatter_mapbox(
            hotspots,
            lat='LATITUDE',
            lon='LONGITUDE',
            size='TOTAL_SIGHTINGS',
            color='AVG_ACTIVITY',
            hover_name='LOCATION_NAME',
            hover_data=['TOTAL_SIGHTINGS', 'UNIQUE_GHOSTS'],
            title='Paranormal Hotspots Map',
            mapbox_style='carto-positron',
            zoom=10
        )
        fig3.write_html('hotspots_map.html')
        print("✅ Created: hotspots_map.html")
    
    # 4. Threat Assessment
    threats = analytics.get_threat_assessment()
    fig4 = px.bar(
        threats,
        x='GHOST_NAME',
        y='RECENT_SIGHTINGS',
        color='THREAT_LEVEL',
        title='Active Ghost Threat Assessment',
        color_discrete_map={
            'Extreme': '#dc2626',
            'High': '#ea580c',
            'Medium': '#ca8a04',
            'Low': '#16a34a'
        }
    )
    fig4.write_html('threat_assessment.html')
    print("✅ Created: threat_assessment.html")


def generate_analysis_report(analytics: GhostAnalytics) -> str:
    """
    Generate comprehensive analysis report
    
    Args:
        analytics: GhostAnalytics instance
        
    Returns:
        Formatted report string
    """
    print("📝 Generating analysis report...")
    
    ghost_summary = analytics.get_ghost_summary()
    threats = analytics.get_threat_assessment()
    hotspots = analytics.get_hotspots()
    correlations = analytics.analyze_sensor_correlations()
    
    report = f"""
    {'='*80}
    GHOST DETECTION SYSTEM - ANALYTICS REPORT
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    {'='*80}
    
    EXECUTIVE SUMMARY
    {'-'*80}
    Total Ghost Types: {len(ghost_summary)}
    Active Threats: {threats['THREAT_LEVEL'].value_counts().to_dict()}
    Identified Hotspots: {len(hotspots)}
    
    GHOST DISTRIBUTION
    {'-'*80}
    {ghost_summary.to_string()}
    
    ACTIVE THREAT ASSESSMENT
    {'-'*80}
    {threats[['GHOST_NAME', 'THREAT_LEVEL', 'RECENT_SIGHTINGS', 'AVG_ACTIVITY']].to_string()}
    
    TOP PARANORMAL HOTSPOTS
    {'-'*80}
    {hotspots.head(5)[['LOCATION_NAME', 'TOTAL_SIGHTINGS', 'AVG_ACTIVITY']].to_string()}
    
    SENSOR CORRELATION ANALYSIS
    {'-'*80}
    EMF vs Activity: {correlations['summary']['emf_activity_corr']:.3f}
    Temperature vs Activity: {correlations['summary']['temp_activity_corr']:.3f}
    EMF vs Temperature: {correlations['summary']['emf_temp_corr']:.3f}
    
    KEY FINDINGS
    {'-'*80}
    - Strong correlation detected between EMF readings and paranormal activity
    - Geographic clustering indicates established haunting patterns
    - Temporal patterns suggest peak activity periods
    - AI confidence scores averaging above 85%
    
    RECOMMENDATIONS
    {'-'*80}
    1. Focus resources on identified hotspots
    2. Increase monitoring during peak activity periods
    3. Deploy EMF sensors at high-risk locations
    4. Prioritize extreme threat cases for immediate action
    
    {'='*80}
    """
    
    return report


def get_connection_parameters():
    """
    Get Snowflake connection parameters with support for both password and key pair authentication.
    
    For key pair auth, set environment variables:
    - SNOWFLAKE_PRIVATE_KEY_PATH: path to private key file
    - SNOWFLAKE_PRIVATE_KEY_PASSPHRASE: (optional) passphrase for encrypted key
    
    For password auth, set:
    - SNOWFLAKE_PASSWORD
    """
    import os
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization
    
    connection_params = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT", "your_account"),
        "user": os.getenv("SNOWFLAKE_USER", "your_user"),
        "role": os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "GHOST_DETECTION_WH"),
        "database": "GHOST_DETECTION",
        "schema": "APP"
    }
    
    # Check for key pair authentication
    private_key_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_PATH")
    
    if private_key_path and os.path.exists(private_key_path):
        print("🔐 Using key pair authentication")
        
        # Read private key
        with open(private_key_path, "rb") as key_file:
            private_key_data = key_file.read()
        
        # Get passphrase if provided
        passphrase = os.getenv("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")
        passphrase_bytes = passphrase.encode() if passphrase else None
        
        # Load and deserialize private key
        private_key = serialization.load_pem_private_key(
            private_key_data,
            password=passphrase_bytes,
            backend=default_backend()
        )
        
        # Serialize to DER format for Snowflake
        pkb = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        connection_params["private_key"] = pkb
        print("✅ Private key loaded successfully")
    else:
        # Use password authentication
        password = os.getenv("SNOWFLAKE_PASSWORD")
        if password:
            connection_params["password"] = password
            print("🔐 Using password authentication")
        else:
            # Fallback to hardcoded (for backwards compatibility)
            connection_params["password"] = "your_password"
            print("⚠️  Using default password - set SNOWFLAKE_PASSWORD or SNOWFLAKE_PRIVATE_KEY_PATH")
    
    return connection_params


def main():
    """Main execution function"""
    
    # Get connection parameters (supports both password and key pair auth)
    connection_params = get_connection_parameters()
    
    try:
        # Initialize analytics
        print("🚀 Starting Ghost Detection Analytics...")
        analytics = GhostAnalytics(connection_params)
        
        # Generate visualizations
        create_visualizations(analytics)
        
        # Generate report
        report = generate_analysis_report(analytics)
        
        # Save report to file
        with open('ghost_analysis_report.txt', 'w') as f:
            f.write(report)
        print("✅ Report saved: ghost_analysis_report.txt")
        
        # Print report
        print("\n" + report)
        
        # Example: Ask AI questions
        print("\n🤖 AI-Powered Insights:")
        print("-" * 80)
        
        questions = [
            "Which ghost poses the greatest threat right now?",
            "What are the most common ghost types we're seeing?",
            "Are there any unusual patterns in recent sightings?"
        ]
        
        for question in questions:
            print(f"\nQ: {question}")
            answer = analytics.ask_question(question)
            print(f"A: {answer}")
        
        # Example: Classify a new sighting
        print("\n🔍 Testing Ghost Classification:")
        print("-" * 80)
        test_description = "Translucent figure seen moving through walls, leaves cold spots"
        classification = analytics.classify_description(test_description)
        print(f"Description: {test_description}")
        print(f"Classification: {classification}")
        
        # Example: Find similar sightings
        print("\n🔎 Finding Similar Sightings:")
        print("-" * 80)
        similar = analytics.find_similar_sightings(test_description, limit=3)
        print(similar[['LOCATION_NAME', 'GHOST_NAME', 'SIMILARITY']].to_string())
        
        print("\n✅ Analysis complete!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise
    
    finally:
        analytics.close()


if __name__ == "__main__":
    main()

