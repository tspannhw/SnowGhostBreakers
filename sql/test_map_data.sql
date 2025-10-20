-- ============================================
-- Test Map Data - Diagnostic Script
-- ============================================
-- Run this in Snowflake to diagnose map issues

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- ============================================
-- 1. Check if tables exist
-- ============================================
SELECT '=== TABLE CHECK ===' as info;

SHOW TABLES IN SCHEMA APP;

-- ============================================
-- 2. Count records
-- ============================================
SELECT '=== RECORD COUNTS ===' as info;

SELECT 
    'Ghosts' as table_name, 
    COUNT(*) as record_count 
FROM GHOSTS
UNION ALL
SELECT 
    'Ghost Sightings Total', 
    COUNT(*) 
FROM GHOST_SIGHTINGS
UNION ALL
SELECT 
    'Sightings WITH Coordinates', 
    COUNT(*) 
FROM GHOST_SIGHTINGS 
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL
UNION ALL
SELECT 
    'Sightings MISSING Coordinates', 
    COUNT(*) 
FROM GHOST_SIGHTINGS 
WHERE latitude IS NULL 
   OR longitude IS NULL;

-- ============================================
-- 3. View actual coordinates
-- ============================================
SELECT '=== COORDINATE DATA ===' as info;

SELECT 
    sighting_id,
    location_name,
    latitude,
    longitude,
    ghost_id,
    sighting_datetime,
    CASE 
        WHEN latitude IS NULL OR longitude IS NULL THEN '❌ MISSING'
        WHEN latitude < -90 OR latitude > 90 THEN '❌ INVALID LAT'
        WHEN longitude < -180 OR longitude > 180 THEN '❌ INVALID LON'
        ELSE '✅ VALID'
    END as coord_status
FROM GHOST_SIGHTINGS
ORDER BY sighting_datetime DESC
LIMIT 20;

-- ============================================
-- 4. Test the exact query Streamlit uses
-- ============================================
SELECT '=== STREAMLIT MAP QUERY ===' as info;

SELECT 
    s.LOCATION_NAME,
    s.LATITUDE,
    s.LONGITUDE,
    g.GHOST_NAME,
    g.GHOST_TYPE,
    s.SIGHTING_DATETIME,
    s.PARANORMAL_ACTIVITY_LEVEL
FROM GHOST_SIGHTINGS s
JOIN GHOSTS g ON s.GHOST_ID = g.GHOST_ID
WHERE s.LATITUDE IS NOT NULL 
  AND s.LONGITUDE IS NOT NULL
  AND s.LATITUDE BETWEEN -90 AND 90
  AND s.LONGITUDE BETWEEN -180 AND 180
ORDER BY s.SIGHTING_DATETIME DESC
LIMIT 10;

-- ============================================
-- 5. Coordinate statistics
-- ============================================
SELECT '=== COORDINATE STATISTICS ===' as info;

SELECT 
    COUNT(*) as total_with_coords,
    AVG(latitude) as avg_latitude,
    AVG(longitude) as avg_longitude,
    MIN(latitude) as min_lat,
    MAX(latitude) as max_lat,
    MIN(longitude) as min_lon,
    MAX(longitude) as max_lon
FROM GHOST_SIGHTINGS
WHERE latitude IS NOT NULL 
  AND longitude IS NOT NULL;

-- ============================================
-- 6. Breakdown by ghost type
-- ============================================
SELECT '=== COORDINATES BY GHOST TYPE ===' as info;

SELECT 
    g.ghost_type,
    COUNT(*) as sightings,
    COUNT(CASE WHEN s.latitude IS NOT NULL THEN 1 END) as with_coords,
    ROUND(COUNT(CASE WHEN s.latitude IS NOT NULL THEN 1 END) * 100.0 / COUNT(*), 1) as coord_percentage
FROM GHOST_SIGHTINGS s
JOIN GHOSTS g ON s.ghost_id = g.ghost_id
GROUP BY g.ghost_type
ORDER BY sightings DESC;

-- ============================================
-- 7. Expected output interpretation
-- ============================================
SELECT '=== INTERPRETATION GUIDE ===' as info
UNION ALL
SELECT '✅ If "Sightings WITH Coordinates" > 0: Map should work'
UNION ALL
SELECT '❌ If "Sightings WITH Coordinates" = 0: No data for map - run sql/03_sample_data.sql'
UNION ALL
SELECT '⚠️  If coordinates exist but map is blank: Check Streamlit errors'
UNION ALL
SELECT '💡 Sample data includes 6+ sightings with coordinates';

-- ============================================
-- 8. Quick fix if no coordinates
-- ============================================
-- Uncomment and run this if you need to add coordinates to existing sightings:
/*
UPDATE GHOST_SIGHTINGS
SET 
    latitude = 40.7580,   -- New York Public Library
    longitude = -73.9855
WHERE sighting_id = 'SIGHT001' AND latitude IS NULL;

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 51.5194,   -- British Library, London
    longitude = -0.1270
WHERE sighting_id = 'SIGHT002' AND latitude IS NULL;
*/

