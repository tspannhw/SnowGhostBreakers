-- ============================================
-- ALTERNATIVE APPROACH: Without ARRAY_CONSTRUCT in VALUES
-- ============================================
-- This version builds arrays using UNION ALL SELECT instead
-- Works on all Snowflake versions

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- BUSINESS VOCABULARY - Alternative Insert Method
-- ============================================

-- Domain: Ghost Types and Classifications
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples)
SELECT 'TERM_001', 'Apparition', 'Ontology', 
       'A visible spirit or ghost of a deceased person, typically appearing as a translucent or semi-transparent figure', 
       'Ghost Types', 
       ARRAY_CONSTRUCT('Specter', 'Phantom', 'Spirit', 'Wraith'), 
       'An apparition was observed in the library, appearing as an elderly woman in vintage clothing'
UNION ALL
SELECT 'TERM_002', 'Poltergeist', 'Ontology', 
       'A type of ghost or spirit responsible for physical disturbances, such as loud noises and objects being moved or destroyed', 
       'Ghost Types',
       ARRAY_CONSTRUCT('Noisy Ghost', 'Disruptive Spirit'), 
       'Poltergeist activity includes objects levitating and being thrown across rooms'
UNION ALL
SELECT 'TERM_003', 'Shadow Entity', 'Ontology', 
       'A dark, humanoid-shaped mass that appears as a living shadow, typically associated with negative energy', 
       'Ghost Types',
       ARRAY_CONSTRUCT('Shadow Person', 'Shadow Being', 'Dark Figure'), 
       'Shadow entities are often seen in peripheral vision and cause electronic malfunctions'
UNION ALL
SELECT 'TERM_004', 'Ectoplasm', 'Property', 
       'A supernatural viscous substance allegedly produced by spiritual mediums and associated with paranormal phenomena', 
       'Manifestation Properties',
       ARRAY_CONSTRUCT('Ghost Slime', 'Paranormal Residue', 'Spirit Matter'), 
       'Green ectoplasm was found at the scene, indicating recent ghost activity'
UNION ALL
SELECT 'TERM_005', 'EMF Reading', 'Measurement', 
       'Electromagnetic Field measurement in milligauss (mG), used to detect paranormal activity', 
       'Equipment & Sensors',
       ARRAY_CONSTRUCT('Electromagnetic Field', 'EM Reading', 'Field Strength'), 
       'EMF readings above 7.0 mG typically indicate paranormal presence'
UNION ALL
SELECT 'TERM_006', 'Manifestation', 'Taxonomy', 
       'The act or instance of a ghost or spirit becoming visible or otherwise detectable', 
       'Ghost Behavior',
       ARRAY_CONSTRUCT('Appearance', 'Materialization', 'Visitation'), 
       'Full-body manifestations are rare and indicate a strong spiritual presence'
UNION ALL
SELECT 'TERM_007', 'Residual Haunting', 'Ontology', 
       'A type of haunting involving a repetitive replay of past events, like a recording, with no intelligent interaction', 
       'Haunting Types',
       ARRAY_CONSTRUCT('Psychic Imprint', 'Energy Loop', 'Playback Haunting'), 
       'The ghost repeats the same actions every night at the same time - a classic residual haunting'
UNION ALL
SELECT 'TERM_008', 'Intelligent Haunting', 'Ontology', 
       'A haunting where the entity is aware of and can interact with the living', 
       'Haunting Types',
       ARRAY_CONSTRUCT('Active Haunting', 'Interactive Spirit', 'Conscious Entity'), 
       'The ghost responded to questions and moved objects on command - an intelligent haunting'
UNION ALL
SELECT 'TERM_009', 'Cold Spot', 'Property', 
       'A localized area of significantly reduced temperature, often associated with paranormal activity', 
       'Environmental Indicators',
       ARRAY_CONSTRUCT('Temperature Anomaly', 'Cold Zone', 'Thermal Drop'), 
       'A cold spot of 10°C drop was detected where the ghost manifested'
UNION ALL
SELECT 'TERM_010', 'EVP', 'Measurement', 
       'Electronic Voice Phenomenon - voices or sounds captured on recording devices that were not audible at the time', 
       'Evidence Types',
       ARRAY_CONSTRUCT('Spirit Voice', 'Paranormal Audio', 'Ghost Recording'), 
       'EVP analysis revealed a whispered message in the audio recording';

-- Domain: Threat Assessment
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples)
SELECT 'TERM_011', 'Threat Level', 'Taxonomy', 
       'Assessed danger level of a paranormal entity to living persons', 
       'Risk Assessment',
       ARRAY_CONSTRUCT('Danger Rating', 'Risk Level', 'Hazard Classification'), 
       'Threat levels range from Low (benign observation) to Extreme (immediate danger to life)'
UNION ALL
SELECT 'TERM_012', 'PKE Surge', 'Measurement', 
       'Psychokinetic Energy surge detected by specialized equipment, indicating paranormal activity intensity', 
       'Equipment & Sensors',
       ARRAY_CONSTRUCT('Psychokinetic Spike', 'Energy Burst', 'Paranormal Surge'), 
       'A PKE surge of over 100 units indicates multiple entities or extreme activity'
UNION ALL
SELECT 'TERM_013', 'Containment', 'Procedure', 
       'The process of capturing and securing a paranormal entity to prevent further manifestation', 
       'Ghost Management',
       ARRAY_CONSTRUCT('Capture', 'Trapping', 'Securing'), 
       'Successful containment requires proper equipment and adherence to safety protocols'
UNION ALL
SELECT 'TERM_014', 'Spectral Classification', 'Taxonomy', 
       'The systematic categorization of ghosts based on observable characteristics and behavior patterns', 
       'Ghost Classification',
       ARRAY_CONSTRUCT('Ghost Typing', 'Entity Classification', 'Spirit Taxonomy'), 
       'Spectral classification helps predict behavior and determine appropriate response protocols'
UNION ALL
SELECT 'TERM_015', 'Paranormal Activity Level', 'Measurement', 
       'A numerical scale (1-10) indicating the intensity of supernatural phenomena', 
       'Activity Metrics',
       ARRAY_CONSTRUCT('Activity Rating', 'Intensity Score', 'Manifestation Strength'), 
       'Level 8-10 activity requires immediate investigation team deployment';

-- Domain: Equipment and Technology
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples)
SELECT 'TERM_016', 'Full Spectrum Camera', 'Equipment', 
       'A camera modified to capture light across the full electromagnetic spectrum, including infrared and ultraviolet', 
       'Detection Equipment',
       ARRAY_CONSTRUCT('FS Camera', 'Spectrum Imaging', 'Paranormal Camera'), 
       'Full spectrum cameras can capture entities invisible to the naked eye'
UNION ALL
SELECT 'TERM_017', 'Proton Pack', 'Equipment', 
       'Specialized equipment for ghost capture using controlled proton streams', 
       'Containment Equipment',
       ARRAY_CONSTRUCT('Neutrona Wand', 'Ghost Trap Gun', 'Particle Accelerator'), 
       'Proton packs must be properly calibrated to avoid crossing streams'
UNION ALL
SELECT 'TERM_018', 'Containment Unit', 'Equipment', 
       'A specially designed storage facility for captured paranormal entities', 
       'Storage Equipment',
       ARRAY_CONSTRUCT('Ghost Storage', 'Ecto Containment', 'Spirit Vault'), 
       'The containment unit maintains entities in a stable dimensional prison'
UNION ALL
SELECT 'TERM_019', 'K2 Meter', 'Equipment', 
       'EMF detector commonly used in paranormal investigations to measure electromagnetic field fluctuations', 
       'Detection Equipment',
       ARRAY_CONSTRUCT('EMF Detector', 'Field Meter', 'K2 EMF'), 
       'K2 meter lights indicate EMF spikes correlating with entity presence'
UNION ALL
SELECT 'TERM_020', 'Spirit Box', 'Equipment', 
       'Device that rapidly scans radio frequencies, theoretically allowing spirits to communicate', 
       'Communication Equipment',
       ARRAY_CONSTRUCT('Ghost Box', 'Radio Sweep Device', 'ITC Device'), 
       'Spirit box sessions captured direct responses to investigator questions';

-- ============================================
-- TAXONOMY ATTRIBUTES - Alternative Insert Method
-- ============================================

INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, attribute_category, data_type, valid_values, measurement_unit, description, mandatory)
SELECT 'ATTR_001', 'Opacity Level', 'Physical', 'Enumeration', 
       ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid'), 
       NULL, 'Degree of visual solidity of the entity', FALSE
UNION ALL
SELECT 'ATTR_002', 'Manifestation Frequency', 'Temporal', 'Enumeration',
       ARRAY_CONSTRUCT('Rare', 'Occasional', 'Frequent', 'Constant'), 
       NULL, 'How often the entity appears or manifests', TRUE
UNION ALL
SELECT 'ATTR_003', 'Intelligence Level', 'Behavioral', 'Enumeration',
       ARRAY_CONSTRUCT('None', 'Minimal', 'Moderate', 'High', 'Superior'), 
       NULL, 'Cognitive capability and awareness of the entity', TRUE
UNION ALL
SELECT 'ATTR_004', 'Aggression Index', 'Behavioral', 'Numeric', 
       NULL, 'Scale 1-10', 'Measure of hostile or aggressive behavior', TRUE
UNION ALL
SELECT 'ATTR_005', 'EMF Signature', 'Environmental', 'Numeric', 
       NULL, 'milligauss (mG)', 'Electromagnetic field strength associated with entity', TRUE
UNION ALL
SELECT 'ATTR_006', 'Temperature Effect', 'Environmental', 'Numeric', 
       NULL, 'Celsius', 'Temperature change caused by entity presence', FALSE
UNION ALL
SELECT 'ATTR_007', 'Communication Ability', 'Behavioral', 'Boolean', 
       NULL, NULL, 'Whether entity can communicate with investigators', FALSE
UNION ALL
SELECT 'ATTR_008', 'Physical Interaction', 'Physical', 'Boolean', 
       NULL, NULL, 'Capability to move or manipulate physical objects', TRUE
UNION ALL
SELECT 'ATTR_009', 'Energy Consumption', 'Physical', 'Enumeration',
       ARRAY_CONSTRUCT('Low', 'Medium', 'High', 'Extreme'), 
       NULL, 'Amount of ambient energy required for manifestation', FALSE
UNION ALL
SELECT 'ATTR_010', 'Mobility Range', 'Physical', 'Enumeration',
       ARRAY_CONSTRUCT('Location-Bound', 'Limited-Range', 'Free-Roaming', 'Dimensional'), 
       NULL, 'Geographic restriction of entity movement', TRUE;

-- Verify
SELECT 'Vocabulary terms inserted:' AS status, COUNT(*) AS count FROM BUSINESS_VOCABULARY;
SELECT 'Taxonomy attributes inserted:' AS status, COUNT(*) AS count FROM TAXONOMY_ATTRIBUTES;

SELECT '✅ Alternative insert method complete!' AS message;

