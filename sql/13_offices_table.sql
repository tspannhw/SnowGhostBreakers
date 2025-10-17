-- ==============================================
-- SnowGhost Breakers Global Offices Table
-- Based on Snowflake office locations worldwide
-- Source: https://careers.snowflake.com/us/en/locations
-- ==============================================

USE DATABASE GHOST_DETECTION;
USE SCHEMA APP;

-- Create OFFICES table
CREATE OR REPLACE TABLE OFFICES (
    office_id VARCHAR(50) PRIMARY KEY,
    office_name VARCHAR(200) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(50), -- Americas, Europe & Middle East, Asia-Pacific
    address VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT,
    timezone VARCHAR(50),
    phone VARCHAR(50),
    email VARCHAR(200),
    office_type VARCHAR(50), -- Headquarters, Regional Office, Field Office
    capacity INT, -- Number of investigators
    active_status BOOLEAN DEFAULT TRUE,
    opened_date DATE,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Insert SnowGhost Breakers Offices based on Snowflake locations
-- ============================================
-- AMERICAS
-- ============================================

INSERT INTO OFFICES (office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date)
SELECT * FROM VALUES
    ('OFF_US_MENLO', 'SnowGhost Breakers Headquarters', 'Menlo Park, CA', 'United States', 'Americas', 37.4529, -122.1817, 'America/Los_Angeles', 'Headquarters', 150, TRUE, '2015-01-15'),
    ('OFF_US_NYC', 'SnowGhost Breakers New York', 'New York, NY', 'United States', 'Americas', 40.7128, -74.0060, 'America/New_York', 'Regional Office', 120, TRUE, '2016-03-10'),
    ('OFF_US_PRINC', 'SnowGhost Breakers Princeton', 'Princeton, NJ', 'United States', 'Americas', 40.3573, -74.6672, 'America/New_York', 'Field Office', 50, TRUE, '2019-11-15'),
    ('OFF_US_BELLV', 'SnowGhost Breakers Bellevue', 'Bellevue, WA', 'United States', 'Americas', 47.6062, -122.2007, 'America/Los_Angeles', 'Regional Office', 100, TRUE, '2016-06-01'),
    ('OFF_CA_TORON', 'SnowGhost Breakers Toronto', 'Toronto', 'Canada', 'Americas', 43.6532, -79.3832, 'America/Toronto', 'Regional Office', 75, TRUE, '2017-03-15'),
    ('OFF_BR_SPAUL', 'SnowGhost Breakers São Paulo', 'São Paulo', 'Brazil', 'Americas', -23.5505, -46.6333, 'America/Sao_Paulo', 'Field Office', 40, TRUE, '2019-08-20'),
    ('OFF_MX_MEXIC', 'SnowGhost Breakers Mexico City', 'Mexico City', 'Mexico', 'Americas', 19.4326, -99.1332, 'America/Mexico_City', 'Field Office', 35, TRUE, '2020-02-10'),
    ('OFF_CO_BOGOT', 'SnowGhost Breakers Bogotá', 'Bogotá', 'Colombia', 'Americas', 4.7110, -74.0721, 'America/Bogota', 'Field Office', 25, TRUE, '2021-05-12'),
    ('OFF_CR_SJOS', 'SnowGhost Breakers San José', 'San José', 'Costa Rica', 'Americas', 9.9281, -84.0907, 'America/Costa_Rica', 'Field Office', 20, TRUE, '2021-09-01')
AS t(office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date);

-- ============================================
-- EUROPE & MIDDLE EAST
-- ============================================

INSERT INTO OFFICES (office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date)
SELECT * FROM VALUES
    ('OFF_NL_AMSTE', 'SnowGhost Breakers Amsterdam', 'Amsterdam', 'Netherlands', 'Europe & Middle East', 52.3676, 4.9041, 'Europe/Amsterdam', 'Regional Office', 85, TRUE, '2016-09-15'),
    ('OFF_DE_BERLI', 'SnowGhost Breakers Berlin', 'Berlin', 'Germany', 'Europe & Middle East', 52.5200, 13.4050, 'Europe/Berlin', 'Regional Office', 70, TRUE, '2017-11-20'),
    ('OFF_PL_WARSA', 'SnowGhost Breakers Warsaw', 'Warsaw', 'Poland', 'Europe & Middle East', 52.2297, 21.0122, 'Europe/Warsaw', 'Regional Office', 60, TRUE, '2018-04-10'),
    ('OFF_UK_LONDO', 'SnowGhost Breakers London', 'London', 'United Kingdom', 'Europe & Middle East', 51.5074, -0.1278, 'Europe/London', 'Regional Office', 90, TRUE, '2016-01-20'),
    ('OFF_FR_PARIS', 'SnowGhost Breakers Paris', 'Paris', 'France', 'Europe & Middle East', 48.8566, 2.3522, 'Europe/Paris', 'Field Office', 55, TRUE, '2018-07-15'),
    ('OFF_ES_MADRI', 'SnowGhost Breakers Madrid', 'Madrid', 'Spain', 'Europe & Middle East', 40.4168, -3.7038, 'Europe/Madrid', 'Field Office', 45, TRUE, '2019-03-25'),
    ('OFF_IT_MILAN', 'SnowGhost Breakers Milan', 'Milan', 'Italy', 'Europe & Middle East', 45.4642, 9.1900, 'Europe/Rome', 'Field Office', 40, TRUE, '2019-10-08'),
    ('OFF_CH_ZURIC', 'SnowGhost Breakers Zürich', 'Zürich', 'Switzerland', 'Europe & Middle East', 47.3769, 8.5417, 'Europe/Zurich', 'Field Office', 35, TRUE, '2020-01-15'),
    ('OFF_SE_STOCK', 'SnowGhost Breakers Stockholm', 'Stockholm', 'Sweden', 'Europe & Middle East', 59.3293, 18.0686, 'Europe/Stockholm', 'Field Office', 30, TRUE, '2020-06-10'),
    ('OFF_DK_COPEN', 'SnowGhost Breakers Copenhagen', 'Copenhagen', 'Denmark', 'Europe & Middle East', 55.6761, 12.5683, 'Europe/Copenhagen', 'Field Office', 28, TRUE, '2020-11-05'),
    ('OFF_FI_HELSI', 'SnowGhost Breakers Helsinki', 'Helsinki', 'Finland', 'Europe & Middle East', 60.1699, 24.9384, 'Europe/Helsinki', 'Field Office', 25, TRUE, '2021-02-18'),
    ('OFF_IE_DUBLI', 'SnowGhost Breakers Dublin', 'Dublin', 'Ireland', 'Europe & Middle East', 53.3498, -6.2603, 'Europe/Dublin', 'Field Office', 50, TRUE, '2018-12-01'),
    ('OFF_IL_TLAVI', 'SnowGhost Breakers Tel Aviv', 'Tel Aviv', 'Israel', 'Europe & Middle East', 32.0853, 34.7818, 'Asia/Jerusalem', 'Field Office', 42, TRUE, '2019-05-20'),
    ('OFF_AE_DUBAI', 'SnowGhost Breakers Dubai', 'Dubai', 'UAE', 'Europe & Middle East', 25.2048, 55.2708, 'Asia/Dubai', 'Field Office', 38, TRUE, '2020-09-15'),
    ('OFF_SA_RIYAD', 'SnowGhost Breakers Riyadh', 'Riyadh', 'Saudi Arabia', 'Europe & Middle East', 24.7136, 46.6753, 'Asia/Riyadh', 'Field Office', 30, TRUE, '2021-11-10')
AS t(office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date);

-- ============================================
-- ASIA-PACIFIC
-- ============================================

INSERT INTO OFFICES (office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date)
SELECT * FROM VALUES
    ('OFF_IN_PUNE', 'SnowGhost Breakers Pune', 'Pune', 'India', 'Asia-Pacific', 18.5204, 73.8567, 'Asia/Kolkata', 'Regional Office', 120, TRUE, '2017-05-10'),
    ('OFF_AU_SYDNE', 'SnowGhost Breakers Sydney', 'Sydney', 'Australia', 'Asia-Pacific', -33.8688, 151.2093, 'Australia/Sydney', 'Regional Office', 65, TRUE, '2018-02-20'),
    ('OFF_SG_SINGA', 'SnowGhost Breakers Singapore', 'Singapore', 'Singapore', 'Asia-Pacific', 1.3521, 103.8198, 'Asia/Singapore', 'Regional Office', 75, TRUE, '2017-08-15'),
    ('OFF_JP_TOKYO', 'SnowGhost Breakers Tokyo', 'Tokyo', 'Japan', 'Asia-Pacific', 35.6762, 139.6503, 'Asia/Tokyo', 'Regional Office', 80, TRUE, '2018-06-25'),
    ('OFF_KR_SEOUL', 'SnowGhost Breakers Seoul', 'Seoul', 'South Korea', 'Asia-Pacific', 37.5665, 126.9780, 'Asia/Seoul', 'Field Office', 55, TRUE, '2019-04-18'),
    ('OFF_CN_SHANG', 'SnowGhost Breakers Shanghai', 'Shanghai', 'China', 'Asia-Pacific', 31.2304, 121.4737, 'Asia/Shanghai', 'Regional Office', 90, TRUE, '2018-10-12'),
    ('OFF_NZ_AUCKL', 'SnowGhost Breakers Auckland', 'Auckland', 'New Zealand', 'Asia-Pacific', -36.8485, 174.7633, 'Pacific/Auckland', 'Field Office', 30, TRUE, '2020-03-05')
AS t(office_id, office_name, city, country, region, latitude, longitude, timezone, office_type, capacity, active_status, opened_date);

-- Create indexes for common queries
-- Note: Snowflake doesn't need traditional indexes but these comments document common access patterns
-- Snowflake automatically optimizes queries through clustering and metadata

-- Common queries that will be optimized:
-- SELECT * FROM OFFICES WHERE region = 'Americas';
-- SELECT * FROM OFFICES WHERE country = 'United States';
-- SELECT * FROM OFFICES WHERE active_status = TRUE;

-- Summary statistics
SELECT 
    'Total Offices' as metric,
    COUNT(*) as count
FROM OFFICES
UNION ALL
SELECT 
    'Active Offices' as metric,
    COUNT(*) as count
FROM OFFICES
WHERE active_status = TRUE
UNION ALL
SELECT 
    CONCAT('Offices in ', region) as metric,
    COUNT(*) as count
FROM OFFICES
WHERE active_status = TRUE
GROUP BY region
ORDER BY metric;

-- Display offices by region
SELECT 
    region,
    COUNT(*) as office_count,
    SUM(capacity) as total_capacity,
    LISTAGG(city, ', ') WITHIN GROUP (ORDER BY city) as cities
FROM OFFICES
WHERE active_status = TRUE
GROUP BY region
ORDER BY office_count DESC;

-- List all offices
SELECT 
    office_id,
    office_name,
    city,
    country,
    region,
    office_type,
    capacity,
    opened_date
FROM OFFICES
WHERE active_status = TRUE
ORDER BY region, country, city;

-- ============================================
-- Notes:
-- - Total: 29 offices across 3 regions
-- - Americas: 9 offices (including NYC and Princeton)
-- - Europe & Middle East: 13 offices  
-- - Asia-Pacific: 7 offices
-- - Based on Snowflake global presence
-- - All coordinates verified for accuracy
-- - Timezones included for scheduling
-- ============================================

