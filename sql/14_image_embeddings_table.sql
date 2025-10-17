-- ============================================
-- GHOST IMAGE EMBEDDINGS TABLE AND FUNCTIONS
-- ============================================
-- Purpose: Dedicated table for storing AI-generated image embeddings
--          and performing vector similarity searches
-- Model: snowflake-arctic-embed-l-v2.0-8k (1024 dimensions)
-- Uses manual cosine similarity for compatibility
-- ============================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- TABLE: GHOST_IMAGE_EMBEDDINGS
-- ============================================
-- Stores image embeddings for fast similarity search

CREATE TABLE IF NOT EXISTS GHOST_IMAGE_EMBEDDINGS (
    embedding_id VARCHAR(50) PRIMARY KEY,
    evidence_id VARCHAR(50) NOT NULL,
    sighting_id VARCHAR(50),
    ghost_id VARCHAR(50),
    
    -- Image information
    image_path VARCHAR(500),
    image_description TEXT,
    image_metadata VARIANT,
    
    -- Embedding data (1024 dimensions for snowflake-arctic-embed-l-v2.0-8k)
    embedding_vector ARRAY,
    embedding_model VARCHAR(100) DEFAULT 'snowflake-arctic-embed-l-v2.0-8k',
    vector_dimension INT DEFAULT 1024,
    
    -- AI analysis results
    ai_description TEXT,
    confidence_score FLOAT,
    detected_features ARRAY,
    ghost_characteristics VARIANT,
    
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_searched TIMESTAMP_NTZ,
    search_count INT DEFAULT 0,
    
    -- Foreign keys
    FOREIGN KEY (evidence_id) REFERENCES GHOST_EVIDENCE(evidence_id),
    FOREIGN KEY (sighting_id) REFERENCES GHOST_SIGHTINGS(sighting_id),
    FOREIGN KEY (ghost_id) REFERENCES GHOSTS(ghost_id)
);

-- ============================================
-- FUNCTION: COSINE_SIMILARITY (Manual Implementation)
-- ============================================
-- Calculate cosine similarity between two vectors
-- Compatible with all Snowflake editions

CREATE OR REPLACE FUNCTION COSINE_SIMILARITY(vec1 ARRAY, vec2 ARRAY)
RETURNS FLOAT
LANGUAGE JAVASCRIPT
AS
$$
    if (!VEC1 || !VEC2) return null;
    if (VEC1.length !== VEC2.length) return null;
    
    let dotProduct = 0;
    let magnitude1 = 0;
    let magnitude2 = 0;
    
    for (let i = 0; i < VEC1.length; i++) {
        const v1 = VEC1[i];
        const v2 = VEC2[i];
        dotProduct += v1 * v2;
        magnitude1 += v1 * v1;
        magnitude2 += v2 * v2;
    }
    
    magnitude1 = Math.sqrt(magnitude1);
    magnitude2 = Math.sqrt(magnitude2);
    
    if (magnitude1 === 0 || magnitude2 === 0) return 0;
    
    return dotProduct / (magnitude1 * magnitude2);
$$;

-- ============================================
-- STORED PROCEDURE: GENERATE_IMAGE_EMBEDDING
-- ============================================
-- Generates and stores embedding for an image

CREATE OR REPLACE PROCEDURE GENERATE_IMAGE_EMBEDDING(
    evidence_id_param VARCHAR,
    image_description_param TEXT
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    embedding_id VARCHAR;
    sighting_id VARCHAR;
    ghost_id VARCHAR;
    image_path VARCHAR;
    embedding_vector_result ARRAY;
    ai_desc TEXT;
BEGIN
    -- Generate unique embedding ID
    embedding_id := 'EMB_' || SUBSTR(UUID_STRING(), 1, 8);
    
    -- Get evidence details
    SELECT 
        e.sighting_id,
        e.ghost_id,
        e.file_path
    INTO 
        :sighting_id,
        :ghost_id,
        :image_path
    FROM GHOST_EVIDENCE e
    WHERE e.evidence_id = :evidence_id_param;
    
    -- Generate embedding using Cortex AI
    SELECT 
        AI_EMBED(
            'snowflake-arctic-embed-l-v2.0-8k',
            :image_description_param
        ) INTO :embedding_vector_result;
    
    -- Generate AI description using Cortex Complete
    SELECT 
        SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large2',
            CONCAT(
                'Analyze this paranormal image description and provide detailed ghost characteristics: ',
                :image_description_param
            )
        ) INTO :ai_desc;
    
    -- Insert embedding record
    INSERT INTO GHOST_IMAGE_EMBEDDINGS (
        embedding_id,
        evidence_id,
        sighting_id,
        ghost_id,
        image_path,
        image_description,
        embedding_vector,
        ai_description,
        confidence_score
    ) VALUES (
        :embedding_id,
        :evidence_id_param,
        :sighting_id,
        :ghost_id,
        :image_path,
        :image_description_param,
        :embedding_vector_result,
        :ai_desc,
        0.85
    );
    
    RETURN 'Embedding generated: ' || :embedding_id;
END;
$$;

-- ============================================
-- PROCEDURE: FIND_SIMILAR_IMAGES
-- ============================================
-- Finds images similar to a given query using vector similarity

CREATE OR REPLACE PROCEDURE FIND_SIMILAR_IMAGES(
    query_text VARCHAR,
    top_k INT
)
RETURNS TABLE (
    embedding_id VARCHAR,
    evidence_id VARCHAR,
    ghost_id VARCHAR,
    image_description TEXT,
    similarity_score FLOAT,
    image_path VARCHAR,
    ai_description TEXT
)
LANGUAGE SQL
AS
$$
DECLARE
    result RESULTSET;
BEGIN
    LET query_sql := '
        SELECT 
            e.embedding_id,
            e.evidence_id,
            e.ghost_id,
            e.image_description,
            COSINE_SIMILARITY(
                e.embedding_vector,
                AI_EMBED(''snowflake-arctic-embed-l-v2.0-8k'', ?)
            ) AS similarity_score,
            e.image_path,
            e.ai_description
        FROM GHOST_IMAGE_EMBEDDINGS e
        WHERE e.embedding_vector IS NOT NULL
          AND COSINE_SIMILARITY(
                e.embedding_vector,
                AI_EMBED(''snowflake-arctic-embed-l-v2.0-8k'', ?)
              ) > 0.5
        ORDER BY similarity_score DESC
        LIMIT ?
    ';
    
    result := (EXECUTE IMMEDIATE :query_sql USING (query_text, query_text, top_k));
    
    RETURN TABLE(result);
END;
$$;

-- ============================================
-- PROCEDURE: FIND_SIMILAR_TO_IMAGE
-- ============================================
-- Finds images similar to a specific image by embedding_id

CREATE OR REPLACE PROCEDURE FIND_SIMILAR_TO_IMAGE(
    source_embedding_id VARCHAR,
    top_k INT
)
RETURNS TABLE (
    embedding_id VARCHAR,
    evidence_id VARCHAR,
    ghost_id VARCHAR,
    image_description TEXT,
    similarity_score FLOAT,
    image_path VARCHAR
)
LANGUAGE SQL
AS
$$
DECLARE
    result RESULTSET;
BEGIN
    LET query_sql := '
        SELECT 
            e.embedding_id,
            e.evidence_id,
            e.ghost_id,
            e.image_description,
            COSINE_SIMILARITY(
                e.embedding_vector,
                (SELECT embedding_vector FROM GHOST_IMAGE_EMBEDDINGS WHERE embedding_id = ?)
            ) AS similarity_score,
            e.image_path
        FROM GHOST_IMAGE_EMBEDDINGS e
        WHERE e.embedding_id != ?
          AND e.embedding_vector IS NOT NULL
          AND COSINE_SIMILARITY(
                e.embedding_vector,
                (SELECT embedding_vector FROM GHOST_IMAGE_EMBEDDINGS WHERE embedding_id = ?)
              ) > 0.5
        ORDER BY similarity_score DESC
        LIMIT ?
    ';
    
    result := (EXECUTE IMMEDIATE :query_sql USING (source_embedding_id, source_embedding_id, source_embedding_id, top_k));
    
    RETURN TABLE(result);
END;
$$;

-- ============================================
-- STORED PROCEDURE: BATCH_GENERATE_EMBEDDINGS
-- ============================================
-- Generates embeddings for all evidence without embeddings

CREATE OR REPLACE PROCEDURE BATCH_GENERATE_EMBEDDINGS(
    batch_size INT
)
RETURNS VARCHAR
LANGUAGE SQL
AS
$$
DECLARE
    processed_count INT DEFAULT 0;
    total_count INT;
    result_cursor CURSOR FOR 
        SELECT 
            e.evidence_id,
            COALESCE(e.description, 'Ghost evidence captured') AS description
        FROM GHOST_EVIDENCE e
        LEFT JOIN GHOST_IMAGE_EMBEDDINGS emb ON e.evidence_id = emb.evidence_id
        WHERE emb.embedding_id IS NULL
          AND e.evidence_type IN ('Photo', 'Video', 'Thermal Image')
        LIMIT :batch_size;
    current_evidence_id VARCHAR;
    current_description TEXT;
    embed_result VARCHAR;
BEGIN
    -- Get total count
    SELECT COUNT(*) INTO :total_count
    FROM GHOST_EVIDENCE e
    LEFT JOIN GHOST_IMAGE_EMBEDDINGS emb ON e.evidence_id = emb.evidence_id
    WHERE emb.embedding_id IS NULL
      AND e.evidence_type IN ('Photo', 'Video', 'Thermal Image');
    
    -- Process each record
    OPEN result_cursor;
    FOR record IN result_cursor DO
        current_evidence_id := record.evidence_id;
        current_description := record.description;
        
        -- Generate embedding for this evidence
        CALL GENERATE_IMAGE_EMBEDDING(:current_evidence_id, :current_description);
        
        processed_count := :processed_count + 1;
    END FOR;
    CLOSE result_cursor;
    
    RETURN CONCAT('Processed ', :processed_count, ' of ', :total_count, ' image embeddings');
END;
$$;

-- ============================================
-- PROCEDURE: GET_IMAGE_CLUSTERS
-- ============================================
-- Groups similar images into clusters by ghost type

CREATE OR REPLACE PROCEDURE GET_IMAGE_CLUSTERS(
    similarity_threshold FLOAT
)
RETURNS TABLE (
    cluster_id INT,
    embedding_id VARCHAR,
    ghost_id VARCHAR,
    image_description TEXT,
    cluster_size INT
)
LANGUAGE SQL
AS
$$
DECLARE
    result RESULTSET;
BEGIN
    result := (
        SELECT 
            ROW_NUMBER() OVER (ORDER BY e.ghost_id, e.created_at) AS cluster_id,
            e.embedding_id,
            e.ghost_id,
            e.image_description,
            COUNT(*) OVER (PARTITION BY e.ghost_id) AS cluster_size
        FROM GHOST_IMAGE_EMBEDDINGS e
        WHERE e.embedding_vector IS NOT NULL
        ORDER BY cluster_id, e.embedding_id
    );
    
    RETURN TABLE(result);
END;
$$;

-- ============================================
-- VIEW: VW_IMAGE_SIMILARITY_STATS
-- ============================================
-- Statistics about image embeddings and similarity

CREATE OR REPLACE VIEW VW_IMAGE_SIMILARITY_STATS AS
SELECT 
    COUNT(*) AS total_embeddings,
    COUNT(DISTINCT ghost_id) AS unique_ghosts,
    COUNT(DISTINCT sighting_id) AS unique_sightings,
    AVG(confidence_score) AS avg_confidence,
    AVG(search_count) AS avg_searches,
    MAX(created_at) AS latest_embedding,
    SUM(CASE WHEN created_at >= DATEADD(day, -7, CURRENT_DATE()) THEN 1 ELSE 0 END) AS recent_embeddings,
    AVG(vector_dimension) AS avg_vector_dimension
FROM GHOST_IMAGE_EMBEDDINGS;

-- ============================================
-- VIEW: VW_POPULAR_IMAGE_SEARCHES
-- ============================================
-- Most searched/referenced image embeddings

CREATE OR REPLACE VIEW VW_POPULAR_IMAGE_SEARCHES AS
SELECT 
    e.embedding_id,
    e.evidence_id,
    e.ghost_id,
    g.ghost_name,
    g.ghost_type,
    e.image_description,
    e.search_count,
    e.confidence_score,
    e.created_at,
    e.last_searched
FROM GHOST_IMAGE_EMBEDDINGS e
JOIN GHOSTS g ON e.ghost_id = g.ghost_id
WHERE e.search_count > 0
ORDER BY e.search_count DESC, e.last_searched DESC;

-- ============================================
-- VIEW: VW_EMBEDDING_PERFORMANCE
-- ============================================
-- Embedding generation performance over time

CREATE OR REPLACE VIEW VW_EMBEDDING_PERFORMANCE AS
SELECT 
    DATE_TRUNC('hour', created_at) AS hour,
    COUNT(*) AS embeddings_generated,
    AVG(confidence_score) AS avg_confidence,
    COUNT(DISTINCT ghost_id) AS unique_ghosts,
    AVG(vector_dimension) AS avg_dimension
FROM GHOST_IMAGE_EMBEDDINGS
WHERE created_at >= DATEADD(day, -7, CURRENT_DATE())
GROUP BY DATE_TRUNC('hour', created_at)
ORDER BY hour DESC;

-- ============================================
-- EXAMPLE QUERIES
-- ============================================

-- Example 1: Test cosine similarity function
-- SELECT COSINE_SIMILARITY(
--     ARRAY_CONSTRUCT(1, 2, 3),
--     ARRAY_CONSTRUCT(4, 5, 6)
-- ) AS test_similarity;

-- Example 2: Generate embedding for an evidence item
-- CALL GENERATE_IMAGE_EMBEDDING('EV_001', 'Bright orb of light captured in the hallway');

-- Example 3: Find similar images by text query
-- CALL FIND_SIMILAR_IMAGES('glowing orb', 10);

-- Example 4: Find similar images to a specific image
-- CALL FIND_SIMILAR_TO_IMAGE('EMB_12345678', 5);

-- Example 5: Batch generate embeddings
-- CALL BATCH_GENERATE_EMBEDDINGS(50);

-- Example 6: Get image clusters
-- CALL GET_IMAGE_CLUSTERS(0.7);

-- Example 7: View embedding statistics
-- SELECT * FROM VW_IMAGE_SIMILARITY_STATS;

-- Example 8: View popular searches
-- SELECT * FROM VW_POPULAR_IMAGE_SEARCHES LIMIT 10;

-- Example 9: View embedding performance
-- SELECT * FROM VW_EMBEDDING_PERFORMANCE LIMIT 24;

-- Example 10: Manual similarity search (if you want to test without procedures)
-- SELECT 
--     e1.embedding_id AS source,
--     e2.embedding_id AS match,
--     e2.image_description,
--     COSINE_SIMILARITY(e1.embedding_vector, e2.embedding_vector) AS similarity
-- FROM GHOST_IMAGE_EMBEDDINGS e1
-- CROSS JOIN GHOST_IMAGE_EMBEDDINGS e2
-- WHERE e1.embedding_id = 'EMB_12345678'
--   AND e2.embedding_id != 'EMB_12345678'
--   AND COSINE_SIMILARITY(e1.embedding_vector, e2.embedding_vector) > 0.7
-- ORDER BY similarity DESC
-- LIMIT 10;

-- ============================================
-- SETUP COMPLETE
-- ============================================
-- All image embedding functions and views created successfully!
-- Next steps:
--   1. Run: CALL BATCH_GENERATE_EMBEDDINGS(100);
--   2. Test: CALL FIND_SIMILAR_IMAGES('ghost orb', 5);
--   3. Check: SELECT * FROM VW_IMAGE_SIMILARITY_STATS;
