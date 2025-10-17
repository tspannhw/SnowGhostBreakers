#!/usr/bin/env python3
"""
Quick fix script for Cell 18 in notebook
Copy and paste this entire cell content into Cell 18
"""

FIXED_CELL_18 = '''# Image Similarity Search using AI embeddings
print("🔍 Image Similarity Search")
print("=" * 80)

# Create embeddings for image descriptions (metadata-based search)
# Using latest AI_EMBED with snowflake-arctic-embed-l-v2.0-8k model
image_search_query = """
WITH image_metadata AS (
    SELECT 
        e.evidence_id,
        g.ghost_name,
        g.ghost_type,
        e.file_path,
        CONCAT(
            'Ghost: ', g.ghost_name, ', ',
            'Type: ', g.ghost_type, ', ',
            'Description: ', COALESCE(e.description, 'No description')
        ) as search_text
    FROM GHOST_EVIDENCE e
    JOIN GHOSTS g ON e.ghost_id = g.ghost_id
    WHERE e.evidence_type = 'Image'
),
target_search AS (
    SELECT SNOWFLAKE.CORTEX.AI_EMBED(
        'snowflake-arctic-embed-l-v2.0-8k',
        'Shadow entity with electronic interference'
    ) as target_embedding
)
SELECT 
    im.evidence_id,
    im.ghost_name,
    im.ghost_type,
    im.file_path,
    VECTOR_COSINE_SIMILARITY(
        (SELECT target_embedding FROM target_search),
        SNOWFLAKE.CORTEX.AI_EMBED('snowflake-arctic-embed-l-v2.0-8k', im.search_text)
    ) as similarity_score
FROM image_metadata im
ORDER BY similarity_score DESC
LIMIT 5
"""

similar_images_df = session.sql(image_search_query).to_pandas()

print("\\n🎯 Most Similar Images to: 'Shadow entity with electronic interference'")
print("\\nSearch Results:")
print(similar_images_df.to_string())  # Fixed: Use print instead of display()

# Visualize similarity scores
if not similar_images_df.empty:
    fig = px.bar(
        similar_images_df,
        x='GHOST_NAME',
        y='SIMILARITY_SCORE',
        color='GHOST_TYPE',
        title='Image Similarity Scores (AI_EMBED with arctic-embed-l-v2.0-8k)',
        labels={'SIMILARITY_SCORE': 'Similarity Score', 'GHOST_NAME': 'Ghost'}
    )
    fig.update_layout(height=400)
    fig.show()
else:
    print("ℹ️ No similar images found.")

# Group similar images by ghost type
print("\\n📊 Image Evidence by Ghost Type:")
type_distribution = session.sql("""
SELECT 
    g.ghost_type,
    COUNT(e.evidence_id) as image_count,
    AVG(CASE 
        WHEN e.processing_status = 'Analyzed' THEN 1.0 
        ELSE 0.0 
    END) * 100 as analyzed_percentage
FROM GHOST_EVIDENCE e
JOIN GHOSTS g ON e.ghost_id = g.ghost_id
WHERE e.evidence_type = 'Image'
GROUP BY g.ghost_type
ORDER BY image_count DESC
""").to_pandas()

print(type_distribution.to_string())  # Fixed: Use print instead of display()

if not type_distribution.empty:
    fig = px.pie(
        type_distribution,
        values='IMAGE_COUNT',
        names='GHOST_TYPE',
        title='Image Evidence Distribution by Ghost Type'
    )
    fig.show()
else:
    print("ℹ️ No image evidence data available.")
'''

if __name__ == '__main__':
    print("=" * 80)
    print("FIXED CELL 18 CODE")
    print("=" * 80)
    print("\nCopy the code below and paste it into Cell 18 of your notebook:")
    print("=" * 80)
    print(FIXED_CELL_18)
    print("=" * 80)
    print("\n✅ Changes Made:")
    print("1. display(similar_images_df) → print(similar_images_df.to_string())")
    print("2. display(type_distribution) → print(type_distribution.to_string())")
    print("3. Added empty DataFrame checks")
    print("4. Updated chart title to show AI_EMBED model")
    print("5. Already using latest arctic-embed-l-v2.0-8k model ✅")

