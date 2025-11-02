````

       SELECT GHOST_ID, EVIDENCE_TYPE, CAPTURE_DATETIME, SNOWFLAKE.CORTEX.COMPLETE('pixtral-large',    
       'Please fully describe this image and let me know if this is a ghost.  Respond in compact JSON format.',
    TO_FILE(FILE_PATH) ) as GHOST_AI 
    from ghost_evidence where  SIGHTING_ID = 'SIGHT_7A67693F';

````

 
 ```json
{
  "description": "The image depicts a Halloween decoration setup in front of a house at night. There are three large skeleton figures standing upright, each with glowing blue eyes. The skeletons are positioned in a yard with bushes and plants, and the scene is illuminated with red lighting, creating a spooky atmosphere. Additional smaller skeletons and decorative elements are visible on the ground and around the larger skeletons.",
  "is_ghost": false
}
```

![2025-10-09_19-35-33_224](https://github.com/user-attachments/assets/d1059804-3072-409f-917e-681e7475318d)



GHOST_ID	EVIDENCE_TYPE	CAPTURE_DATETIME	GHOST_AI
GHO006	Photograph	2025-10-31 23:30:00.000	" ```json
{
  "description": "The image depicts a Halloween decoration setup in front of a house at night. There are three large skeleton figures standing upright, each with glowing blue eyes. The skeletons are positioned in a yard with bushes and plants, and the scene is illuminated with red lighting, creating a spooky atmosphere. Additional smaller skeletons and decorative elements are visible on the ground and around the larger skeletons.",
  "is_ghost": false
}
```"<img width="336" height="132" alt="image" src="https://github.com/user-attachments/assets/56639acf-d23c-4ccc-8fdf-1f7e1696691e" />
