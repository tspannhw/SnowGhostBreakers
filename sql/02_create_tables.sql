-- ============================================
-- Ghost Detection Application - Table Definitions
-- ============================================
-- Core tables for storing ghost detection data, sightings, images, and analysis

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Main Ghost Registry Table
CREATE OR REPLACE TABLE GHOSTS (
    ghost_id VARCHAR(50) PRIMARY KEY,
    ghost_name VARCHAR(200),
    ghost_type VARCHAR(100), -- Type: Poltergeist, Apparition, Shadow, Orb, etc.
    threat_level VARCHAR(20), -- Low, Medium, High, Extreme
    description TEXT,
    manifestation_frequency VARCHAR(50), -- Rare, Occasional, Frequent, Constant
    origin_story TEXT,
    first_detected_date TIMESTAMP_NTZ,
    last_seen_date TIMESTAMP_NTZ,
    status VARCHAR(50), -- Active, Dormant, Captured, Neutralized
    confidence_score FLOAT, -- AI confidence in detection (0-1)
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Ghost Sightings/Encounters Table
CREATE OR REPLACE TABLE GHOST_SIGHTINGS (
    sighting_id VARCHAR(50) PRIMARY KEY,
    ghost_id VARCHAR(50),
    location_name VARCHAR(200),
    location_address TEXT,
    location_coordinates GEOGRAPHY, -- Geospatial data
    latitude FLOAT,
    longitude FLOAT,
    sighting_datetime TIMESTAMP_NTZ,
    witness_name VARCHAR(200),
    witness_contact VARCHAR(200),
    environmental_conditions TEXT, -- Temperature, EMF readings, etc.
    temperature_celsius FLOAT,
    emf_reading FLOAT, -- Electromagnetic field reading
    description TEXT,
    evidence_type VARCHAR(100), -- Visual, Audio, EMF, Temperature, Multiple
    paranormal_activity_level INT, -- 1-10 scale
    investigation_notes TEXT,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);

-- Ghost Images and Multimedia Evidence
CREATE OR REPLACE TABLE GHOST_EVIDENCE (
    evidence_id VARCHAR(50) PRIMARY KEY,
    sighting_id VARCHAR(50),
    ghost_id VARCHAR(50),
    evidence_type VARCHAR(50), -- Image, Video, Audio, Sensor_Data
    file_path VARCHAR(500), -- Path in Snowflake stage
    file_url VARCHAR(1000), -- External URL if applicable
    file_size_bytes INT,
    mime_type VARCHAR(100),
    capture_datetime TIMESTAMP_NTZ,
    image_data VARCHAR, -- Base64 encoded image for Cortex Vision
    thumbnail_data VARCHAR, -- Thumbnail for quick display
    metadata VARIANT, -- JSON metadata (EXIF, sensor data, etc.)
    processing_status VARCHAR(50) DEFAULT 'Pending', -- Pending, Processing, Analyzed, Failed
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (sighting_id) REFERENCES GHOST_SIGHTINGS(sighting_id),
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);

-- AI Analysis Results
CREATE OR REPLACE TABLE GHOST_AI_ANALYSIS (
    analysis_id VARCHAR(50) PRIMARY KEY,
    evidence_id VARCHAR(50),
    sighting_id VARCHAR(50),
    ghost_id VARCHAR(50),
    analysis_type VARCHAR(100), -- Image_Classification, Sentiment, Anomaly_Detection, Pattern_Recognition
    model_used VARCHAR(100), -- Cortex model name
    analysis_datetime TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    results VARIANT, -- JSON results from Cortex AI
    confidence_score FLOAT,
    detected_entities ARRAY, -- Entities detected in image/text
    sentiment_score FLOAT, -- For text analysis
    anomaly_detected BOOLEAN,
    summary TEXT, -- Generated summary from Cortex Complete
    recommendations TEXT,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (evidence_id) REFERENCES GHOST_EVIDENCE(evidence_id),
    FOREIGN KEY (sighting_id) REFERENCES GHOST_SIGHTINGS(sighting_id),
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);

-- Equipment and Sensor Readings
CREATE OR REPLACE TABLE SENSOR_READINGS (
    reading_id VARCHAR(50) PRIMARY KEY,
    sighting_id VARCHAR(50),
    sensor_type VARCHAR(100), -- EMF, Temperature, Motion, Audio, Camera
    reading_datetime TIMESTAMP_NTZ,
    reading_value FLOAT,
    reading_unit VARCHAR(50),
    anomaly_detected BOOLEAN DEFAULT FALSE,
    raw_data VARIANT, -- JSON with detailed sensor data
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (sighting_id) REFERENCES GHOST_SIGHTINGS(sighting_id)
);

-- Investigation Teams and Ghostbusters
CREATE OR REPLACE TABLE INVESTIGATORS (
    investigator_id VARCHAR(50) PRIMARY KEY,
    investigator_name VARCHAR(200),
    email VARCHAR(200),
    phone VARCHAR(50),
    specialization VARCHAR(100), -- EMF Expert, Medium, Technician, Lead Investigator
    experience_years INT,
    cases_solved INT DEFAULT 0,
    active_status BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Investigation Case Management
CREATE OR REPLACE TABLE INVESTIGATIONS (
    investigation_id VARCHAR(50) PRIMARY KEY,
    case_name VARCHAR(300),
    ghost_id VARCHAR(50),
    lead_investigator_id VARCHAR(50),
    start_date DATE,
    end_date DATE,
    status VARCHAR(50), -- Open, In_Progress, Closed, Archived
    priority VARCHAR(20), -- Low, Medium, High, Critical
    case_summary TEXT,
    outcome TEXT,
    evidence_count INT DEFAULT 0,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id),
    FOREIGN KEY (lead_investigator_id) REFERENCES INVESTIGATORS(investigator_id)
);

-- Audit Log for tracking changes
CREATE OR REPLACE TABLE AUDIT_LOG (
    log_id VARCHAR(50) PRIMARY KEY,
    table_name VARCHAR(100),
    record_id VARCHAR(50),
    action VARCHAR(50), -- INSERT, UPDATE, DELETE
    user_name VARCHAR(200),
    action_datetime TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    old_values VARIANT,
    new_values VARIANT
);

-- Note: Snowflake regular tables don't use indexes
-- Snowflake automatically optimizes queries through micro-partitions and metadata
-- For additional optimization, you can use clustering keys:
-- ALTER TABLE GHOSTS CLUSTER BY (ghost_type, status);
-- ALTER TABLE GHOST_SIGHTINGS CLUSTER BY (sighting_datetime, location_name);
-- ALTER TABLE GHOST_EVIDENCE CLUSTER BY (evidence_type, capture_datetime);

COMMENT ON TABLE GHOSTS IS 'Master registry of detected ghosts and paranormal entities';
COMMENT ON TABLE GHOST_SIGHTINGS IS 'Individual sighting events and encounters';
COMMENT ON TABLE GHOST_EVIDENCE IS 'Multimedia evidence including images, videos, and audio recordings';
COMMENT ON TABLE GHOST_AI_ANALYSIS IS 'AI-powered analysis results using Snowflake Cortex';
COMMENT ON TABLE SENSOR_READINGS IS 'Equipment sensor data from paranormal detection devices';
COMMENT ON TABLE INVESTIGATORS IS 'Ghostbuster team members and investigators';
COMMENT ON TABLE INVESTIGATIONS IS 'Case management for ghost investigations';

