-- ============================================
-- ADD SAMPLE COORDINATES TO SIGHTINGS
-- ============================================
-- Run this to add coordinates to existing sightings for map testing
-- This will make maps work immediately in your Streamlit app

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Check current coordinate status
SELECT 
    COUNT(*) as total_sightings,
    COUNT(latitude) as with_latitude,
    COUNT(longitude) as with_longitude,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_both_coordinates
FROM GHOST_SIGHTINGS;

-- ============================================
-- OPTION 1: Add Random US City Coordinates
-- ============================================
-- Updates first 10 sightings with coordinates from major US cities

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 40.7128,
    longitude = -74.0060
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 34.0522,
    longitude = -118.2437
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 41.8781,
    longitude = -87.6298
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 29.7604,
    longitude = -95.3698
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 39.7392,
    longitude = -104.9903
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 37.7749,
    longitude = -122.4194
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 47.6062,
    longitude = -122.3321
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 42.3601,
    longitude = -71.0589
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 33.4484,
    longitude = -112.0740
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

UPDATE GHOST_SIGHTINGS
SET 
    latitude = 32.7767,
    longitude = -96.7970
WHERE sighting_id IN (
    SELECT sighting_id FROM GHOST_SIGHTINGS 
    WHERE latitude IS NULL 
    LIMIT 1
);

-- ============================================
-- OPTION 2: Update Based on Location Name
-- ============================================
-- If your sightings have location names, update coordinates based on those

-- New York locations
UPDATE GHOST_SIGHTINGS
SET latitude = 40.7128, longitude = -74.0060
WHERE LOWER(location_name) LIKE '%new york%' 
  OR LOWER(location_name) LIKE '%manhattan%'
  OR LOWER(location_address) LIKE '%new york%';

-- London locations  
UPDATE GHOST_SIGHTINGS
SET latitude = 51.5074, longitude = -0.1278
WHERE LOWER(location_name) LIKE '%london%'
  OR LOWER(location_address) LIKE '%london%';

-- Tokyo locations
UPDATE GHOST_SIGHTINGS
SET latitude = 35.6762, longitude = 139.6503
WHERE LOWER(location_name) LIKE '%tokyo%'
  OR LOWER(location_address) LIKE '%tokyo%';

-- Paris locations
UPDATE GHOST_SIGHTINGS
SET latitude = 48.8566, longitude = 2.3522
WHERE LOWER(location_name) LIKE '%paris%'
  OR LOWER(location_address) LIKE '%paris%';

-- Los Angeles locations
UPDATE GHOST_SIGHTINGS
SET latitude = 34.0522, longitude = -118.2437
WHERE LOWER(location_name) LIKE '%los angeles%'
  OR LOWER(location_name) LIKE '%la %'
  OR LOWER(location_address) LIKE '%los angeles%';

-- ============================================
-- OPTION 3: Set ALL to one location (quick test)
-- ============================================
-- Uncomment to set all NULL coordinates to New York (for quick testing)

/*
UPDATE GHOST_SIGHTINGS
SET 
    latitude = 40.7128,
    longitude = -74.0060
WHERE latitude IS NULL OR longitude IS NULL;
*/

-- ============================================
-- VERIFY RESULTS
-- ============================================

-- Check updated coordinate count
SELECT 
    COUNT(*) as total_sightings,
    COUNT(latitude) as with_latitude,
    COUNT(longitude) as with_longitude,
    COUNT(CASE WHEN latitude IS NOT NULL AND longitude IS NOT NULL THEN 1 END) as with_both_coordinates
FROM GHOST_SIGHTINGS;

-- View sample with coordinates
SELECT 
    sighting_id,
    location_name,
    latitude,
    longitude,
    sighting_datetime
FROM GHOST_SIGHTINGS
WHERE latitude IS NOT NULL
  AND longitude IS NOT NULL
ORDER BY sighting_datetime DESC
LIMIT 20;

-- ============================================
-- CITY COORDINATE REFERENCE
-- ============================================
/*
Major US Cities:
- New York, NY: 40.7128, -74.0060
- Los Angeles, CA: 34.0522, -118.2437
- Chicago, IL: 41.8781, -87.6298
- Houston, TX: 29.7604, -95.3698
- Phoenix, AZ: 33.4484, -112.0740
- Philadelphia, PA: 39.9526, -75.1652
- San Antonio, TX: 29.4241, -98.4936
- San Diego, CA: 32.7157, -117.1611
- Dallas, TX: 32.7767, -96.7970
- San Francisco, CA: 37.7749, -122.4194
- Seattle, WA: 47.6062, -122.3321
- Boston, MA: 42.3601, -71.0589
- Denver, CO: 39.7392, -104.9903
- Miami, FL: 25.7617, -80.1918
- New Orleans, LA: 29.9511, -90.0715

International Cities:
- London, UK: 51.5074, -0.1278
- Paris, France: 48.8566, 2.3522
- Tokyo, Japan: 35.6762, 139.6503
- Sydney, Australia: -33.8688, 151.2093
- Toronto, Canada: 43.6532, -79.3832
- Berlin, Germany: 52.5200, 13.4050
- Rome, Italy: 41.9028, 12.4964
- Mexico City, Mexico: 19.4326, -99.1332
*/

-- ============================================
-- DONE!
-- ============================================
-- Now refresh your Streamlit app to see maps with data!

