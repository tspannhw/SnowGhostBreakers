"""
Pytest Configuration and Fixtures
Shared fixtures for all tests
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# ============================================================================
# Session-Level Fixtures
# ============================================================================

@pytest.fixture(scope='session')
def test_config():
    """Test configuration"""
    return {
        'database': 'GHOST_DETECTION',
        'schema': 'APP',
        'warehouse': 'GHOST_WAREHOUSE',
        'role': 'GHOSTBUSTER'
    }


@pytest.fixture(scope='session')
def snowflake_connection_params():
    """Snowflake connection parameters for testing"""
    return {
        'account': 'test_account',
        'user': 'test_user',
        'password': 'test_password',
        'warehouse': 'GHOST_WAREHOUSE',
        'database': 'GHOST_DETECTION',
        'schema': 'APP',
        'role': 'GHOSTBUSTER'
    }


# ============================================================================
# Mock Snowflake Session
# ============================================================================

@pytest.fixture
def mock_snowpark_session():
    """Mock Snowpark session"""
    session = Mock()
    session.get_current_database.return_value = "GHOST_DETECTION"
    session.get_current_schema.return_value = "APP"
    session.get_current_warehouse.return_value = "GHOST_WAREHOUSE"
    session.get_current_user.return_value = "test_user"
    session.get_current_role.return_value = "GHOSTBUSTER"
    
    # Mock SQL execution
    session.sql = Mock(return_value=Mock(collect=Mock(return_value=[])))
    session.table = Mock(return_value=Mock())
    session.call = Mock(return_value="Success")
    
    return session


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_ghost_data():
    """Sample ghost data for testing"""
    return {
        'ghost_id': 1,
        'ghost_name': 'Lady in White',
        'ghost_type': 'Apparition',
        'first_sighting_date': datetime(2024, 1, 1),
        'last_sighting_date': datetime(2024, 1, 15),
        'threat_level': 'High',
        'status': 'Active',
        'description': 'Translucent female figure in Victorian dress',
        'behavioral_pattern': 'Appears at midnight near old staircase'
    }


@pytest.fixture
def sample_sighting_data():
    """Sample sighting data for testing"""
    return {
        'sighting_id': 1,
        'ghost_id': 1,
        'sighting_datetime': datetime(2024, 1, 15, 23, 30),
        'location_name': 'Old Victorian Mansion',
        'location_coordinates': '40.7128,-74.0060',
        'witness_count': 3,
        'paranormal_activity_level': 8,
        'emf_reading': 6.5,
        'temperature': 52.0,
        'environmental_conditions': 'Clear night, no wind',
        'witness_description': 'White glowing figure on stairs'
    }


@pytest.fixture
def sample_evidence_data():
    """Sample evidence data for testing"""
    return {
        'evidence_id': 1,
        'sighting_id': 1,
        'ghost_id': 1,
        'evidence_type': 'Image',
        'file_path': '/evidence/ghost_001.jpg',
        'file_size_bytes': 1024000,
        'mime_type': 'image/jpeg',
        'capture_datetime': datetime(2024, 1, 15, 23, 35),
        'processing_status': 'Analyzed',
        'metadata': '{"camera": "Canon EOS", "iso": 800}'
    }


@pytest.fixture
def sample_ai_analysis_data():
    """Sample AI analysis data for testing"""
    return {
        'analysis_id': 1,
        'sighting_id': 1,
        'evidence_id': 1,
        'analysis_type': 'Image_Classification',
        'ai_model_used': 'mistral-large2',
        'analysis_result': 'Class A Apparition detected with 85% confidence',
        'confidence_score': 0.85,
        'analysis_datetime': datetime.now(),
        'processing_time_ms': 1250
    }


@pytest.fixture
def sample_investigation_data():
    """Sample investigation data for testing"""
    return {
        'investigation_id': 1,
        'investigation_name': 'Victorian Mansion Investigation',
        'lead_investigator': 'John Doe',
        'status': 'In_Progress',
        'start_date': datetime(2024, 1, 1),
        'priority_level': 'High',
        'description': 'Comprehensive investigation of recurring apparition'
    }


# ============================================================================
# DataFrame Fixtures
# ============================================================================

@pytest.fixture
def sample_ghosts_dataframe():
    """Sample ghosts DataFrame for testing"""
    return pd.DataFrame([
        {
            'GHOST_ID': 1,
            'GHOST_NAME': 'Lady in White',
            'GHOST_TYPE': 'Apparition',
            'THREAT_LEVEL': 'High',
            'STATUS': 'Active'
        },
        {
            'GHOST_ID': 2,
            'GHOST_NAME': 'Shadow Man',
            'GHOST_TYPE': 'Shadow Entity',
            'THREAT_LEVEL': 'Extreme',
            'STATUS': 'Active'
        },
        {
            'GHOST_ID': 3,
            'GHOST_NAME': 'Playful Spirit',
            'GHOST_TYPE': 'Poltergeist',
            'THREAT_LEVEL': 'Low',
            'STATUS': 'Contained'
        }
    ])


@pytest.fixture
def sample_sightings_dataframe():
    """Sample sightings DataFrame for testing"""
    return pd.DataFrame([
        {
            'SIGHTING_ID': 1,
            'GHOST_ID': 1,
            'SIGHTING_DATETIME': datetime(2024, 1, 15, 23, 30),
            'LOCATION_NAME': 'Old Mansion',
            'PARANORMAL_ACTIVITY_LEVEL': 8,
            'EMF_READING': 6.5,
            'TEMPERATURE': 52.0
        },
        {
            'SIGHTING_ID': 2,
            'GHOST_ID': 2,
            'SIGHTING_DATETIME': datetime(2024, 1, 16, 1, 15),
            'LOCATION_NAME': 'Abandoned Hospital',
            'PARANORMAL_ACTIVITY_LEVEL': 9,
            'EMF_READING': 8.2,
            'TEMPERATURE': 48.0
        }
    ])


@pytest.fixture
def sample_evidence_dataframe():
    """Sample evidence DataFrame for testing"""
    return pd.DataFrame([
        {
            'EVIDENCE_ID': 1,
            'GHOST_ID': 1,
            'EVIDENCE_TYPE': 'Image',
            'FILE_SIZE_BYTES': 1024000,
            'PROCESSING_STATUS': 'Analyzed'
        },
        {
            'EVIDENCE_ID': 2,
            'GHOST_ID': 1,
            'EVIDENCE_TYPE': 'Audio',
            'FILE_SIZE_BYTES': 512000,
            'PROCESSING_STATUS': 'Pending'
        }
    ])


# ============================================================================
# Business Vocabulary Fixtures
# ============================================================================

@pytest.fixture
def sample_vocabulary_data():
    """Sample business vocabulary data"""
    return [
        {
            'term': 'Apparition',
            'definition': 'A ghost that appears as a visible entity',
            'category': 'Ghost Type',
            'term_status': 'Active'
        },
        {
            'term': 'EMF',
            'definition': 'Electromagnetic Field measurement in milligauss',
            'category': 'Measurement',
            'term_status': 'Active'
        },
        {
            'term': 'Poltergeist',
            'definition': 'A ghost that interacts with physical objects',
            'category': 'Ghost Type',
            'term_status': 'Active'
        }
    ]


@pytest.fixture
def sample_ontology_data():
    """Sample ontology hierarchy data"""
    return pd.DataFrame([
        {
            'CLASSIFICATION_ID': 1,
            'CLASSIFICATION_LEVEL': 1,
            'CLASSIFICATION_NAME': 'Supernatural Entity',
            'PARENT_ID': None,
            'CLASSIFICATION_PATH': 'Supernatural Entity'
        },
        {
            'CLASSIFICATION_ID': 2,
            'CLASSIFICATION_LEVEL': 2,
            'CLASSIFICATION_NAME': 'Spectral Manifestation',
            'PARENT_ID': 1,
            'CLASSIFICATION_PATH': 'Supernatural Entity > Spectral Manifestation'
        },
        {
            'CLASSIFICATION_ID': 3,
            'CLASSIFICATION_LEVEL': 3,
            'CLASSIFICATION_NAME': 'Apparition',
            'PARENT_ID': 2,
            'CLASSIFICATION_PATH': 'Supernatural Entity > Spectral Manifestation > Apparition'
        }
    ])


# ============================================================================
# AI Agent Fixtures
# ============================================================================

@pytest.fixture
def sample_ai_agent_data():
    """Sample AI agent data"""
    return {
        'agent_id': 1,
        'agent_name': 'GhostAnalyzer',
        'agent_type': 'Analytical',
        'capabilities': '["data_analysis", "pattern_recognition", "threat_assessment"]',
        'ai_model': 'mistral-large2',
        'is_active': True,
        'max_query_cost': 1000
    }


@pytest.fixture
def sample_agent_policy_data():
    """Sample agent policy data"""
    return {
        'policy_id': 1,
        'policy_name': 'StandardAnalysisPolicy',
        'policy_type': 'Operational',
        'allowed_operations': 'SELECT,INSERT',
        'max_query_cost': 1000,
        'is_active': True
    }


# ============================================================================
# Mock Cortex AI Responses
# ============================================================================

@pytest.fixture
def mock_cortex_complete_response():
    """Mock Cortex Complete response"""
    return """
    GHOST ANALYSIS REPORT
    
    Entity: Lady in White
    Classification: Class A Apparition
    Threat Level: High
    
    Analysis:
    This entity exhibits classic apparition characteristics with consistent
    manifestation patterns at midnight hours. EMF readings of 6.5 mG confirm
    strong paranormal presence. Temperature anomalies support spectral activity.
    
    Recommendations:
    1. Implement containment protocols
    2. Monitor nightly between 11 PM - 1 AM
    3. Document all future manifestations
    4. Consider investigation escalation if activity increases
    """


@pytest.fixture
def mock_cortex_sentiment_response():
    """Mock Cortex Sentiment response"""
    return 0.75  # Positive sentiment


@pytest.fixture
def mock_cortex_embedding_response():
    """Mock Cortex Embedding response"""
    return [round(np.random.random(), 4) for _ in range(768)]


# ============================================================================
# Test Utilities
# ============================================================================

@pytest.fixture
def assert_dataframe_structure():
    """Utility to assert DataFrame structure"""
    def _assert_structure(df, required_columns):
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        for col in required_columns:
            assert col in df.columns
    return _assert_structure


@pytest.fixture
def assert_valid_timestamp():
    """Utility to assert valid timestamp"""
    def _assert_timestamp(timestamp_value):
        assert timestamp_value is not None
        if isinstance(timestamp_value, str):
            datetime.fromisoformat(timestamp_value.replace('Z', '+00:00'))
        elif isinstance(timestamp_value, datetime):
            assert timestamp_value <= datetime.now()
    return _assert_timestamp


@pytest.fixture
def assert_valid_threat_level():
    """Utility to assert valid threat level"""
    def _assert_threat(threat_level):
        valid_levels = ['Low', 'Medium', 'High', 'Extreme']
        assert threat_level in valid_levels
    return _assert_threat


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Pytest configuration"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "cortex: mark test as requiring Cortex AI"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test items during collection"""
    for item in items:
        # Add markers based on test name
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_cortex" in item.nodeid:
            item.add_marker(pytest.mark.cortex)
        else:
            item.add_marker(pytest.mark.unit)


# ============================================================================
# Test Reporting
# ============================================================================

@pytest.fixture(scope='session', autouse=True)
def test_session_info(request):
    """Print test session information"""
    print("\n" + "="*80)
    print("GHOST DETECTION SYSTEM - TEST SESSION")
    print("="*80)
    print(f"Test Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Working Directory: {os.getcwd()}")
    print("="*80 + "\n")
    
    yield
    
    print("\n" + "="*80)
    print(f"Test Session Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

