-- ============================================
-- Ghost Detection Application - Sample Data
-- ============================================
-- Sample data for testing and demonstration

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Insert sample investigators
INSERT INTO INVESTIGATORS (investigator_id, investigator_name, email, specialization, experience_years, cases_solved)
VALUES
    ('INV001', 'Dr. Peter Venkman', 'pvenkman@ghostbusters.com', 'Lead Investigator', 15, 127),
    ('INV002', 'Dr. Raymond Stantz', 'rstantz@ghostbusters.com', 'EMF Expert', 18, 145),
    ('INV003', 'Dr. Egon Spengler', 'espengler@ghostbusters.com', 'Technician', 20, 156),
    ('INV004', 'Winston Zeddemore', 'wzeddemore@ghostbusters.com', 'Field Specialist', 12, 98),
    ('INV005', 'Dana Barrett', 'dbarrett@ghostbusters.com', 'Medium', 8, 45);

-- Insert sample ghosts
INSERT INTO GHOSTS (ghost_id, ghost_name, ghost_type, threat_level, description, manifestation_frequency, 
                    origin_story, first_detected_date, last_seen_date, status, confidence_score)
VALUES
    ('GH001', 'The Library Apparition', 'Apparition', 'Low', 'Elderly female ghost seen in the New York Public Library, appears to be reorganizing books', 
     'Occasional', 'Former librarian who passed away in 1952, still devoted to her work', 
     '2024-01-15 14:30:00', '2024-10-01 18:45:00', 'Active', 0.92),
    
    ('GH002', 'Slimer', 'Ectoplasmic Entity', 'Medium', 'Green, gluttonous ghost known for consuming food and leaving ectoplasm trails',
     'Frequent', 'Believed to be a hotel chef from the 1920s who died from overeating',
     '2024-02-20 22:15:00', '2024-10-10 03:30:00', 'Active', 0.98),
    
    ('GH003', 'Shadow Walker', 'Shadow Entity', 'High', 'Dark humanoid shadow that appears in corners and causes electronic malfunctions',
     'Frequent', 'Unknown origin, first reported in abandoned subway tunnels',
     '2024-03-05 01:20:00', '2024-10-12 23:15:00', 'Active', 0.85),
    
    ('GH004', 'The Collector', 'Poltergeist', 'Extreme', 'Aggressive entity that moves objects and causes property damage',
     'Constant', 'Wealthy art collector from 1800s who died protecting his collection',
     '2024-04-10 16:00:00', '2024-10-14 20:00:00', 'Active', 0.95),
    
    ('GH005', 'Orb Cluster Alpha', 'Orb', 'Low', 'Group of floating luminous orbs, usually blue-white in color',
     'Rare', 'Possibly natural phenomenon or residual energy from old construction site',
     '2024-05-12 11:30:00', '2024-09-28 14:00:00', 'Dormant', 0.67);

-- Insert sample sightings
INSERT INTO GHOST_SIGHTINGS (sighting_id, ghost_id, location_name, location_address, latitude, longitude,
                             sighting_datetime, witness_name, witness_contact, environmental_conditions,
                             temperature_celsius, emf_reading, description, evidence_type, 
                             paranormal_activity_level, verified)
VALUES
    ('SIGHT001', 'GH001', 'New York Public Library', '476 5th Ave, New York, NY 10018', 40.7532, -73.9822,
     '2024-10-01 18:45:00', 'Sarah Mitchell', 'sarah.m@email.com', 'Temperature drop of 10°C, EMF spike detected',
     12.5, 8.7, 'Witnessed books floating off shelves and reorganizing themselves in the reference section', 
     'Visual', 6, TRUE),
    
    ('SIGHT002', 'GH002', 'Sedgewick Hotel', '224 W 47th St, New York, NY', 40.7590, -73.9845,
     '2024-10-10 03:30:00', 'Hotel Security', 'security@sedgewick.com', 'Ectoplasm residue, food items missing',
     18.0, 5.2, 'Green ghost observed in hotel kitchen consuming entire buffet setup',
     'Multiple', 8, TRUE),
    
    ('SIGHT003', 'GH003', 'Abandoned Subway Station', '91st St Station, New York, NY', 40.7880, -73.9720,
     '2024-10-12 23:15:00', 'Transit Worker', 'worker@mta.com', 'All flashlights failed, extreme EMF readings',
     8.0, 15.3, 'Large shadow figure blocking tunnel, caused complete electronic failure',
     'EMF', 9, TRUE),
    
    ('SIGHT004', 'GH004', 'Metropolitan Museum', '1000 5th Ave, New York, NY 10028', 40.7794, -73.9632,
     '2024-10-14 20:00:00', 'Night Curator', 'curator@metmuseum.org', 'Multiple objects levitating, temperature fluctuations',
     10.0, 12.8, 'Witnessed multiple art pieces floating and rearranging in Egyptian wing',
     'Multiple', 10, TRUE),
    
    ('SIGHT005', 'GH001', 'New York Public Library', '476 5th Ave, New York, NY 10018', 40.7532, -73.9822,
     '2024-09-15 19:20:00', 'Library Patron', 'patron@email.com', 'Cold spot near fiction section',
     14.0, 6.5, 'Saw elderly woman in vintage clothing disappearing near card catalog',
     'Visual', 5, TRUE);

-- Insert sample evidence
INSERT INTO GHOST_EVIDENCE (evidence_id, sighting_id, ghost_id, evidence_type, file_path, 
                            capture_datetime, metadata, processing_status)
SELECT * FROM VALUES
    ('EVID001', 'SIGHT001', 'GH001', 'Image', '@GHOST_IMAGES_STAGE/library_ghost_001.jpg',
     '2024-10-01 18:45:30'::TIMESTAMP_NTZ, PARSE_JSON('{"camera": "Full Spectrum", "exposure": "1/60s", "iso": 3200}'), 'Analyzed'),
    
    ('EVID002', 'SIGHT002', 'GH002', 'Image', '@GHOST_IMAGES_STAGE/slimer_sighting_001.jpg',
     '2024-10-10 03:30:15'::TIMESTAMP_NTZ, PARSE_JSON('{"camera": "Security Cam", "resolution": "1080p", "frame_rate": 30}'), 'Analyzed'),
    
    ('EVID003', 'SIGHT003', 'GH003', 'Audio', '@GHOST_IMAGES_STAGE/shadow_entity_audio_001.mp3',
     '2024-10-12 23:15:45'::TIMESTAMP_NTZ, PARSE_JSON('{"recorder": "EVP Recorder", "sample_rate": 44100, "duration_sec": 120}'), 'Analyzed'),
    
    ('EVID004', 'SIGHT004', 'GH004', 'Video', '@GHOST_IMAGES_STAGE/poltergeist_activity_001.mp4',
     '2024-10-14 20:00:00'::TIMESTAMP_NTZ, PARSE_JSON('{"camera": "Night Vision", "resolution": "4K", "duration_sec": 180}'), 'Analyzed'),
    
    ('EVID005', 'SIGHT001', 'GH001', 'Sensor_Data', '@GHOST_DATA_STAGE/emf_readings_001.json',
     '2024-10-01 18:45:00'::TIMESTAMP_NTZ, PARSE_JSON('{"device": "K2 EMF Meter", "readings_count": 150, "max_reading": 8.7}'), 'Analyzed')
AS t(evidence_id, sighting_id, ghost_id, evidence_type, file_path, capture_datetime, metadata, processing_status);

-- Insert sample AI analysis
INSERT INTO GHOST_AI_ANALYSIS (analysis_id, evidence_id, sighting_id, ghost_id, analysis_type, 
                               model_used, confidence_score, detected_entities, sentiment_score,
                               anomaly_detected, summary, recommendations)
VALUES
    ('ANALYSIS001', 'EVID001', 'SIGHT001', 'GH001', 'Image_Classification', 'snowflake-arctic-embed-l',
     0.92, ARRAY_CONSTRUCT('humanoid_figure', 'translucent_appearance', 'vintage_clothing'), NULL, TRUE,
     'Analysis confirms presence of anomalous translucent figure matching historical description of former librarian. High confidence in paranormal classification.',
     'Continue monitoring location. Deploy full spectrum cameras. Document any interaction with library materials.'),
    
    ('ANALYSIS002', 'EVID002', 'SIGHT002', 'GH002', 'Image_Classification', 'snowflake-arctic-embed-l',
     0.98, ARRAY_CONSTRUCT('ectoplasmic_entity', 'green_coloration', 'motion_blur'), NULL, TRUE,
     'Highly confident identification of Class 5 free-roaming vapor. Ectoplasm samples show high PKE levels. Entity demonstrates consistent behavior patterns.',
     'Recommend containment using proton pack. Entity shows food attraction - can be lured with bait. Exercise caution due to slime hazard.'),
    
    ('ANALYSIS003', 'EVID003', 'SIGHT003', 'GH003', 'Anomaly_Detection', 'cortex-anomaly-detector',
     0.85, ARRAY_CONSTRUCT('shadow_manifestation', 'emf_interference', 'electronic_disruption'), NULL, TRUE,
     'Audio analysis reveals EVP (Electronic Voice Phenomena) at 1:23 mark. Shadow entity classification confirmed. Threat level elevated due to electronic disruption capabilities.',
     'Immediate containment recommended. Use hardened equipment. Avoid digital devices. Deploy analog backup systems.'),
    
    ('ANALYSIS004', 'EVID004', 'SIGHT004', 'GH004', 'Pattern_Recognition', 'cortex-pattern-analyzer',
     0.95, ARRAY_CONSTRUCT('poltergeist_activity', 'object_manipulation', 'intelligent_behavior'), NULL, TRUE,
     'Video analysis shows 47 distinct object movements with clear intentional patterns. Entity demonstrates high intelligence and possessive behavior over art collection.',
     'URGENT: Extreme threat level. Entity shows aggressive territorial behavior. Recommend full team deployment with containment equipment. Coordinate with museum security.'),
    
    ('ANALYSIS005', 'EVID005', 'SIGHT001', 'GH001', 'Sentiment', 'cortex-sentiment',
     0.88, ARRAY_CONSTRUCT('calm', 'purposeful', 'non-threatening'), 0.65, FALSE,
     'EMF pattern analysis suggests benign entity. Behavioral patterns indicate continuation of life routine. No hostile intent detected.',
     'Low priority monitoring. Entity appears harmless. May be beneficial to library organization. Consider peaceful coexistence protocol.');

-- Insert sample sensor readings
INSERT INTO SENSOR_READINGS (reading_id, sighting_id, sensor_type, reading_datetime, 
                             reading_value, reading_unit, anomaly_detected, raw_data)
SELECT * FROM VALUES
    ('READ001', 'SIGHT001', 'EMF', '2024-10-01 18:45:00'::TIMESTAMP_NTZ, 8.7, 'mG', TRUE, 
     PARSE_JSON('{"baseline": 2.1, "peak": 8.7, "duration_seconds": 45, "fluctuation_pattern": "rapid_spike"}')),
    
    ('READ002', 'SIGHT001', 'Temperature', '2024-10-01 18:45:00'::TIMESTAMP_NTZ, 12.5, 'Celsius', TRUE,
     PARSE_JSON('{"baseline": 22.0, "minimum": 12.5, "drop_rate": "rapid", "recovery_time_seconds": 120}')),
    
    ('READ003', 'SIGHT003', 'EMF', '2024-10-12 23:15:00'::TIMESTAMP_NTZ, 15.3, 'mG', TRUE,
     PARSE_JSON('{"baseline": 1.8, "peak": 15.3, "duration_seconds": 180, "pattern": "sustained_high"}'))
AS t(reading_id, sighting_id, sensor_type, reading_datetime, reading_value, reading_unit, anomaly_detected, raw_data);

-- Insert sample investigations
INSERT INTO INVESTIGATIONS (investigation_id, case_name, ghost_id, lead_investigator_id, 
                           start_date, status, priority, case_summary, evidence_count)
VALUES
    ('CASE001', 'Library Haunting Investigation', 'GH001', 'INV001', '2024-01-16', 'Open', 'Low',
     'Ongoing investigation of benign apparition at NYPL. Entity appears non-threatening.', 3),
    
    ('CASE002', 'Sedgewick Hotel Infestation', 'GH002', 'INV002', '2024-02-21', 'In_Progress', 'Medium',
     'Active containment operation for ectoplasmic entity. Multiple sightings reported.', 5),
    
    ('CASE003', 'Shadow Entity Containment', 'GH003', 'INV003', '2024-03-06', 'In_Progress', 'High',
     'High-priority case. Entity demonstrates dangerous capabilities. Team deployment required.', 8),
    
    ('CASE004', 'Museum Poltergeist Crisis', 'GH004', 'INV001', '2024-04-11', 'In_Progress', 'Critical',
     'URGENT: Aggressive poltergeist causing significant property damage. Immediate action required.', 12);

COMMIT;

