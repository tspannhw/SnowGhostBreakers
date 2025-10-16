-- ============================================
-- Ghost Detection Application - Business Vocabulary
-- Comprehensive Ontology and Taxonomy System
-- ============================================
-- This creates a formal business vocabulary for ghost classification,
-- terminology management, and semantic standardization

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- BUSINESS VOCABULARY TABLES
-- ============================================

-- Main vocabulary terms table
CREATE OR REPLACE TABLE BUSINESS_VOCABULARY (
    term_id VARCHAR(50) PRIMARY KEY,
    term_name VARCHAR(200) NOT NULL,
    term_category VARCHAR(100), -- Ontology, Taxonomy, Property, Relationship
    definition TEXT,
    domain VARCHAR(100), -- Ghost Types, Manifestations, Equipment, etc.
    parent_term_id VARCHAR(50), -- For hierarchical relationships
    synonyms ARRAY,
    related_terms ARRAY,
    usage_examples TEXT,
    data_steward VARCHAR(200),
    status VARCHAR(50) DEFAULT 'Active', -- Active, Deprecated, Under Review
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (parent_term_id) REFERENCES BUSINESS_VOCABULARY(term_id)
);

-- Ghost Ontology - Hierarchical classification
CREATE OR REPLACE TABLE GHOST_ONTOLOGY (
    ontology_id VARCHAR(50) PRIMARY KEY,
    classification_level INT, -- 1=Kingdom, 2=Class, 3=Order, 4=Family, 5=Species
    classification_name VARCHAR(200) NOT NULL,
    parent_classification_id VARCHAR(50),
    description TEXT,
    defining_characteristics TEXT,
    typical_behaviors TEXT,
    threat_indicators TEXT,
    containment_protocols TEXT,
    research_notes TEXT,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (parent_classification_id) REFERENCES GHOST_ONTOLOGY(ontology_id)
);

-- Taxonomy attributes and properties
CREATE OR REPLACE TABLE TAXONOMY_ATTRIBUTES (
    attribute_id VARCHAR(50) PRIMARY KEY,
    attribute_name VARCHAR(200) NOT NULL,
    attribute_category VARCHAR(100), -- Physical, Behavioral, Environmental, Temporal
    data_type VARCHAR(50), -- String, Numeric, Boolean, Enumeration
    valid_values ARRAY, -- For enumerations
    measurement_unit VARCHAR(50),
    description TEXT,
    mandatory BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Relationship types between entities
CREATE OR REPLACE TABLE ENTITY_RELATIONSHIPS (
    relationship_id VARCHAR(50) PRIMARY KEY,
    relationship_name VARCHAR(200) NOT NULL,
    source_entity_type VARCHAR(100),
    target_entity_type VARCHAR(100),
    relationship_type VARCHAR(100), -- Hierarchical, Associative, Causal
    cardinality VARCHAR(50), -- One-to-One, One-to-Many, Many-to-Many
    description TEXT,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Term mappings to data model
CREATE OR REPLACE TABLE VOCABULARY_DATA_MAPPING (
    mapping_id VARCHAR(50) PRIMARY KEY,
    term_id VARCHAR(50),
    table_name VARCHAR(200),
    column_name VARCHAR(200),
    mapping_type VARCHAR(50), -- Direct, Derived, Computed
    transformation_logic TEXT,
    created_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    FOREIGN KEY (term_id) REFERENCES BUSINESS_VOCABULARY(term_id)
);

-- ============================================
-- INSERT CORE BUSINESS VOCABULARY
-- ============================================

-- Domain: Ghost Types and Classifications
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples) VALUES
('TERM_001', 'Apparition', 'Ontology', 'A visible spirit or ghost of a deceased person, typically appearing as a translucent or semi-transparent figure', 'Ghost Types', 
 ARRAY_CONSTRUCT('Specter', 'Phantom', 'Spirit', 'Wraith'), 
 'An apparition was observed in the library, appearing as an elderly woman in vintage clothing'),

('TERM_002', 'Poltergeist', 'Ontology', 'A type of ghost or spirit responsible for physical disturbances, such as loud noises and objects being moved or destroyed', 'Ghost Types',
 ARRAY_CONSTRUCT('Noisy Ghost', 'Disruptive Spirit'), 
 'Poltergeist activity includes objects levitating and being thrown across rooms'),

('TERM_003', 'Shadow Entity', 'Ontology', 'A dark, humanoid-shaped mass that appears as a living shadow, typically associated with negative energy', 'Ghost Types',
 ARRAY_CONSTRUCT('Shadow Person', 'Shadow Being', 'Dark Figure'), 
 'Shadow entities are often seen in peripheral vision and cause electronic malfunctions'),

('TERM_004', 'Ectoplasm', 'Property', 'A supernatural viscous substance allegedly produced by spiritual mediums and associated with paranormal phenomena', 'Manifestation Properties',
 ARRAY_CONSTRUCT('Ghost Slime', 'Paranormal Residue', 'Spirit Matter'), 
 'Green ectoplasm was found at the scene, indicating recent ghost activity'),

('TERM_005', 'EMF Reading', 'Measurement', 'Electromagnetic Field measurement in milligauss (mG), used to detect paranormal activity', 'Equipment & Sensors',
 ARRAY_CONSTRUCT('Electromagnetic Field', 'EM Reading', 'Field Strength'), 
 'EMF readings above 7.0 mG typically indicate paranormal presence'),

('TERM_006', 'Manifestation', 'Taxonomy', 'The act or instance of a ghost or spirit becoming visible or otherwise detectable', 'Ghost Behavior',
 ARRAY_CONSTRUCT('Appearance', 'Materialization', 'Visitation'), 
 'Full-body manifestations are rare and indicate a strong spiritual presence'),

('TERM_007', 'Residual Haunting', 'Ontology', 'A type of haunting involving a repetitive replay of past events, like a recording, with no intelligent interaction', 'Haunting Types',
 ARRAY_CONSTRUCT('Psychic Imprint', 'Energy Loop', 'Playback Haunting'), 
 'The ghost repeats the same actions every night at the same time - a classic residual haunting'),

('TERM_008', 'Intelligent Haunting', 'Ontology', 'A haunting where the entity is aware of and can interact with the living', 'Haunting Types',
 ARRAY_CONSTRUCT('Active Haunting', 'Interactive Spirit', 'Conscious Entity'), 
 'The ghost responded to questions and moved objects on command - an intelligent haunting'),

('TERM_009', 'Cold Spot', 'Property', 'A localized area of significantly reduced temperature, often associated with paranormal activity', 'Environmental Indicators',
 ARRAY_CONSTRUCT('Temperature Anomaly', 'Cold Zone', 'Thermal Drop'), 
 'A cold spot of 10°C drop was detected where the ghost manifested'),

('TERM_010', 'EVP', 'Measurement', 'Electronic Voice Phenomenon - voices or sounds captured on recording devices that were not audible at the time', 'Evidence Types',
 ARRAY_CONSTRUCT('Spirit Voice', 'Paranormal Audio', 'Ghost Recording'), 
 'EVP analysis revealed a whispered message in the audio recording');

-- Domain: Threat Assessment
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples) VALUES
('TERM_011', 'Threat Level', 'Taxonomy', 'Assessed danger level of a paranormal entity to living persons', 'Risk Assessment',
 ARRAY_CONSTRUCT('Danger Rating', 'Risk Level', 'Hazard Classification'), 
 'Threat levels range from Low (benign observation) to Extreme (immediate danger to life)'),

('TERM_012', 'PKE Surge', 'Measurement', 'Psychokinetic Energy surge detected by specialized equipment, indicating paranormal activity intensity', 'Equipment & Sensors',
 ARRAY_CONSTRUCT('Psychokinetic Spike', 'Energy Burst', 'Paranormal Surge'), 
 'A PKE surge of over 100 units indicates multiple entities or extreme activity'),

('TERM_013', 'Containment', 'Procedure', 'The process of capturing and securing a paranormal entity to prevent further manifestation', 'Ghost Management',
 ARRAY_CONSTRUCT('Capture', 'Trapping', 'Securing'), 
 'Successful containment requires proper equipment and adherence to safety protocols'),

('TERM_014', 'Spectral Classification', 'Taxonomy', 'The systematic categorization of ghosts based on observable characteristics and behavior patterns', 'Ghost Classification',
 ARRAY_CONSTRUCT('Ghost Typing', 'Entity Classification', 'Spirit Taxonomy'), 
 'Spectral classification helps predict behavior and determine appropriate response protocols'),

('TERM_015', 'Paranormal Activity Level', 'Measurement', 'A numerical scale (1-10) indicating the intensity of supernatural phenomena', 'Activity Metrics',
 ARRAY_CONSTRUCT('Activity Rating', 'Intensity Score', 'Manifestation Strength'), 
 'Level 8-10 activity requires immediate investigation team deployment');

-- Domain: Equipment and Technology
INSERT INTO BUSINESS_VOCABULARY (term_id, term_name, term_category, definition, domain, synonyms, usage_examples) VALUES
('TERM_016', 'Full Spectrum Camera', 'Equipment', 'A camera modified to capture light across the full electromagnetic spectrum, including infrared and ultraviolet', 'Detection Equipment',
 ARRAY_CONSTRUCT('FS Camera', 'Spectrum Imaging', 'Paranormal Camera'), 
 'Full spectrum cameras can capture entities invisible to the naked eye'),

('TERM_017', 'Proton Pack', 'Equipment', 'Specialized equipment for ghost capture using controlled proton streams', 'Containment Equipment',
 ARRAY_CONSTRUCT('Neutrona Wand', 'Ghost Trap Gun', 'Particle Accelerator'), 
 'Proton packs must be properly calibrated to avoid crossing streams'),

('TERM_018', 'Containment Unit', 'Equipment', 'A specially designed storage facility for captured paranormal entities', 'Storage Equipment',
 ARRAY_CONSTRUCT('Ghost Storage', 'Ecto Containment', 'Spirit Vault'), 
 'The containment unit maintains entities in a stable dimensional prison'),

('TERM_019', 'K2 Meter', 'Equipment', 'EMF detector commonly used in paranormal investigations to measure electromagnetic field fluctuations', 'Detection Equipment',
 ARRAY_CONSTRUCT('EMF Detector', 'Field Meter', 'K2 EMF'), 
 'K2 meter lights indicate EMF spikes correlating with entity presence'),

('TERM_020', 'Spirit Box', 'Equipment', 'Device that rapidly scans radio frequencies, theoretically allowing spirits to communicate', 'Communication Equipment',
 ARRAY_CONSTRUCT('Ghost Box', 'Radio Sweep Device', 'ITC Device'), 
 'Spirit box sessions captured direct responses to investigator questions');

-- ============================================
-- INSERT GHOST ONTOLOGY (Hierarchical Classification)
-- ============================================

-- Level 1: Kingdom
INSERT INTO GHOST_ONTOLOGY (ontology_id, classification_level, classification_name, description, defining_characteristics) VALUES
('ONT_L1_001', 1, 'Paranormal Entities', 
 'All supernatural beings and phenomena that exist outside normal physical laws',
 'Non-corporeal existence, ability to manifest, interaction with physical world, energy-based existence');

-- Level 2: Class
INSERT INTO GHOST_ONTOLOGY (ontology_id, classification_level, classification_name, parent_classification_id, description, defining_characteristics) VALUES
('ONT_L2_001', 2, 'Spectral Entities', 'ONT_L1_001',
 'Ghosts and spirits of deceased humans or animals',
 'Once-living origin, human-like intelligence, emotional responses, attachment to locations or objects'),

('ONT_L2_002', 2, 'Non-Human Entities', 'ONT_L1_001',
 'Paranormal beings that never had physical form',
 'Never living, alien intelligence patterns, undefined motivations, unpredictable behavior'),

('ONT_L2_003', 2, 'Energy Phenomena', 'ONT_L1_001',
 'Pure energy manifestations without consciousness',
 'No intelligence, environmental reactions, temporal patterns, residual energy signatures');

-- Level 3: Order (under Spectral Entities)
INSERT INTO GHOST_ONTOLOGY (ontology_id, classification_level, classification_name, parent_classification_id, description, defining_characteristics, typical_behaviors) VALUES
('ONT_L3_001', 3, 'Interactive Spirits', 'ONT_L2_001',
 'Conscious entities capable of communication and intelligent interaction',
 'Self-awareness, communication ability, learning capacity, goal-oriented behavior',
 'Responds to questions, manipulates objects with purpose, seeks attention or assistance'),

('ONT_L3_002', 3, 'Residual Imprints', 'ONT_L2_001',
 'Non-interactive recordings of past events',
 'Repetitive behavior, no awareness of observers, temporal consistency, environmental triggers',
 'Repeats same actions, ignores living persons, appears at consistent times/locations'),

('ONT_L3_003', 3, 'Malevolent Entities', 'ONT_L2_001',
 'Harmful or aggressive spirits with negative intent',
 'Hostile behavior, threat to living, negative energy emission, territorial aggression',
 'Physical attacks, psychological harm, property damage, feeding on fear');

-- Level 4: Family (under Interactive Spirits)
INSERT INTO GHOST_ONTOLOGY (ontology_id, classification_level, classification_name, parent_classification_id, description, defining_characteristics, threat_indicators, containment_protocols) VALUES
('ONT_L4_001', 4, 'Apparitions', 'ONT_L3_001',
 'Visible manifestations of human spirits',
 'Visual appearance, human form retention, variable opacity, conscious awareness',
 'Generally low threat unless distressed or territorial',
 'Communication-based resolution, peaceful transition assistance, minimal containment needed'),

('ONT_L4_002', 4, 'Poltergeists', 'ONT_L3_003',
 'Physically interactive and often violent entities',
 'Object manipulation, noise generation, physical force application, focused aggression',
 'Medium to high threat, property damage, potential physical harm',
 'Active containment required, proton stream capture, secure storage in containment unit'),

('ONT_L4_003', 4, 'Shadow Entities', 'ONT_L3_003',
 'Dark, shapeless manifestations of negative energy',
 'Shadowy appearance, electronic disruption, fear induction, light absorption',
 'High threat, psychological impact, technology interference',
 'Specialized equipment needed, light-based deterrents, immediate containment recommended');

-- Level 5: Species (specific classifications)
INSERT INTO GHOST_ONTOLOGY (ontology_id, classification_level, classification_name, parent_classification_id, description, defining_characteristics, typical_behaviors, containment_protocols) VALUES
('ONT_L5_001', 5, 'Class I Spectral Presence', 'ONT_L4_001',
 'Minimal manifestation, barely detectable',
 'Weak energy signature, occasional cold spots, minimal EMF readings (< 3 mG)',
 'Passive observation only, no interaction capability',
 'No containment needed, monitoring sufficient'),

('ONT_L5_002', 5, 'Class II Ectoplasmic Manifestation', 'ONT_L4_001',
 'Visible ghost with ectoplasmic properties',
 'Partial visibility, ectoplasm production, moderate EMF (3-7 mG), interactive capability',
 'Limited object interaction, communication possible, emotional responses',
 'Optional containment, depends on threat assessment and entity cooperation'),

('ONT_L5_003', 5, 'Class III Full Roaming Vapor', 'ONT_L4_001',
 'Fully visible, highly interactive entity',
 'Complete visual manifestation, strong EMF (7-12 mG), high energy signature',
 'Full physical interaction, sustained communication, complex behaviors',
 'Containment recommended if uncooperative or threat identified'),

('ONT_L5_004', 5, 'Class IV Aggressive Poltergeist', 'ONT_L4_002',
 'Violent entity with significant physical capabilities',
 'Extreme object manipulation, strong force application, very high EMF (12+ mG)',
 'Aggressive property damage, potential physical attacks, territory defense',
 'Immediate containment required, full team deployment, proton pack necessary'),

('ONT_L5_005', 5, 'Class V Shadow Walker', 'ONT_L4_003',
 'Advanced shadow entity with electronic disruption capabilities',
 'Complete light absorption, tech failure induction, psychological impact',
 'Stalking behavior, fear feeding, electronic sabotage, dimensional shifting',
 'Priority containment, hardened equipment required, analog backup systems essential');

-- ============================================
-- INSERT TAXONOMY ATTRIBUTES
-- ============================================

INSERT INTO TAXONOMY_ATTRIBUTES (attribute_id, attribute_name, attribute_category, data_type, valid_values, measurement_unit, description, mandatory) VALUES
('ATTR_001', 'Opacity Level', 'Physical', 'Enumeration', 
 ARRAY_CONSTRUCT('Transparent', 'Translucent', 'Semi-Solid', 'Solid'), NULL,
 'Degree of visual solidity of the entity', FALSE),

('ATTR_002', 'Manifestation Frequency', 'Temporal', 'Enumeration',
 ARRAY_CONSTRUCT('Rare', 'Occasional', 'Frequent', 'Constant'), NULL,
 'How often the entity appears or manifests', TRUE),

('ATTR_003', 'Intelligence Level', 'Behavioral', 'Enumeration',
 ARRAY_CONSTRUCT('None', 'Minimal', 'Moderate', 'High', 'Superior'), NULL,
 'Cognitive capability and awareness of the entity', TRUE),

('ATTR_004', 'Aggression Index', 'Behavioral', 'Numeric', NULL, 'Scale 1-10',
 'Measure of hostile or aggressive behavior', TRUE),

('ATTR_005', 'EMF Signature', 'Environmental', 'Numeric', NULL, 'milligauss (mG)',
 'Electromagnetic field strength associated with entity', TRUE),

('ATTR_006', 'Temperature Effect', 'Environmental', 'Numeric', NULL, 'Celsius',
 'Temperature change caused by entity presence', FALSE),

('ATTR_007', 'Communication Ability', 'Behavioral', 'Boolean', NULL, NULL,
 'Whether entity can communicate with investigators', FALSE),

('ATTR_008', 'Physical Interaction', 'Physical', 'Boolean', NULL, NULL,
 'Capability to move or manipulate physical objects', TRUE),

('ATTR_009', 'Energy Consumption', 'Physical', 'Enumeration',
 ARRAY_CONSTRUCT('Low', 'Medium', 'High', 'Extreme'), NULL,
 'Amount of ambient energy required for manifestation', FALSE),

('ATTR_010', 'Mobility Range', 'Physical', 'Enumeration',
 ARRAY_CONSTRUCT('Location-Bound', 'Limited-Range', 'Free-Roaming', 'Dimensional'), NULL,
 'Geographic restriction of entity movement', TRUE);

-- ============================================
-- VIEWS FOR VOCABULARY NAVIGATION
-- ============================================

-- Complete vocabulary with hierarchy
CREATE OR REPLACE VIEW VW_VOCABULARY_HIERARCHY AS
WITH RECURSIVE vocab_tree AS (
    SELECT 
        term_id,
        term_name,
        term_category,
        definition,
        domain,
        parent_term_id,
        1 as level,
        CAST(term_name AS VARCHAR(1000)) as path
    FROM BUSINESS_VOCABULARY
    WHERE parent_term_id IS NULL
    
    UNION ALL
    
    SELECT 
        bv.term_id,
        bv.term_name,
        bv.term_category,
        bv.definition,
        bv.domain,
        bv.parent_term_id,
        vt.level + 1,
        CAST(vt.path || ' > ' || bv.term_name AS VARCHAR(1000))
    FROM BUSINESS_VOCABULARY bv
    INNER JOIN vocab_tree vt ON bv.parent_term_id = vt.term_id
)
SELECT * FROM vocab_tree ORDER BY path;

-- Complete ontology hierarchy
CREATE OR REPLACE VIEW VW_ONTOLOGY_HIERARCHY AS
WITH RECURSIVE onto_tree AS (
    SELECT 
        ontology_id,
        classification_level,
        classification_name,
        parent_classification_id,
        description,
        defining_characteristics,
        1 as depth,
        CAST(classification_name AS VARCHAR(1000)) as classification_path
    FROM GHOST_ONTOLOGY
    WHERE parent_classification_id IS NULL
    
    UNION ALL
    
    SELECT 
        go.ontology_id,
        go.classification_level,
        go.classification_name,
        go.parent_classification_id,
        go.description,
        go.defining_characteristics,
        ot.depth + 1,
        CAST(ot.classification_path || ' → ' || go.classification_name AS VARCHAR(1000))
    FROM GHOST_ONTOLOGY go
    INNER JOIN onto_tree ot ON go.parent_classification_id = ot.ontology_id
)
SELECT 
    ontology_id,
    classification_level,
    classification_name,
    classification_path,
    description,
    defining_characteristics,
    depth
FROM onto_tree 
ORDER BY classification_path;

-- Taxonomy attribute catalog
CREATE OR REPLACE VIEW VW_TAXONOMY_CATALOG AS
SELECT 
    attribute_category,
    COUNT(*) as attribute_count,
    LISTAGG(attribute_name, ', ') as attributes
FROM TAXONOMY_ATTRIBUTES
GROUP BY attribute_category
ORDER BY attribute_count DESC;

-- ============================================
-- VOCABULARY SEARCH FUNCTIONS
-- ============================================

-- Search vocabulary with AI
CREATE OR REPLACE FUNCTION SEARCH_VOCABULARY(search_term STRING)
RETURNS TABLE (
    term_id STRING,
    term_name STRING,
    definition STRING,
    relevance_score FLOAT
)
AS
$$
    SELECT 
        term_id,
        term_name,
        definition,
        VECTOR_COSINE_SIMILARITY(
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-l', search_term),
            SNOWFLAKE.CORTEX.EMBED_TEXT_768('snowflake-arctic-embed-l', term_name || ' ' || definition)
        ) as relevance_score
    FROM BUSINESS_VOCABULARY
    WHERE relevance_score > 0.6
    ORDER BY relevance_score DESC
$$;

-- Get term relationships
CREATE OR REPLACE FUNCTION GET_TERM_RELATIONSHIPS(term_id_param STRING)
RETURNS TABLE (
    related_term_id STRING,
    related_term_name STRING,
    relationship_type STRING
)
AS
$$
    SELECT 
        bv2.term_id,
        bv2.term_name,
        CASE 
            WHEN bv2.parent_term_id = term_id_param THEN 'Child Term'
            WHEN bv2.term_id = bv1.parent_term_id THEN 'Parent Term'
            WHEN value IN (SELECT value FROM TABLE(FLATTEN(bv1.related_terms))) THEN 'Related Term'
            ELSE 'Associated Term'
        END as relationship_type
    FROM BUSINESS_VOCABULARY bv1
    CROSS JOIN BUSINESS_VOCABULARY bv2
    WHERE bv1.term_id = term_id_param
    AND (bv2.parent_term_id = term_id_param 
         OR bv2.term_id = bv1.parent_term_id
         OR bv2.term_id IN (SELECT value FROM TABLE(FLATTEN(bv1.related_terms))))
$$;

COMMENT ON TABLE BUSINESS_VOCABULARY IS 'Master business vocabulary and terminology management';
COMMENT ON TABLE GHOST_ONTOLOGY IS 'Hierarchical ghost classification system (ontology)';
COMMENT ON TABLE TAXONOMY_ATTRIBUTES IS 'Standardized attributes for ghost taxonomy';
COMMENT ON VIEW VW_VOCABULARY_HIERARCHY IS 'Complete vocabulary with hierarchical relationships';
COMMENT ON VIEW VW_ONTOLOGY_HIERARCHY IS 'Complete ghost ontology hierarchy visualization';

