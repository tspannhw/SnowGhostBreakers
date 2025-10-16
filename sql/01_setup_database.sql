-- ============================================
-- Ghost Detection Application - Database Setup
-- ============================================
-- This script sets up the database, schemas, and initial configuration
-- for the Ghost Detection and Analysis application

-- Create database and schemas
CREATE DATABASE IF NOT EXISTS GHOST_DETECTION;
USE DATABASE GHOST_DETECTION;

-- Main application schema
CREATE SCHEMA IF NOT EXISTS APP;

-- Analytics and ML schema
CREATE SCHEMA IF NOT EXISTS ANALYTICS;

-- Staging area for raw data
CREATE SCHEMA IF NOT EXISTS STAGING;

-- Cortex AI and ML models
CREATE SCHEMA IF NOT EXISTS CORTEX_AI;

-- Set default schema
USE SCHEMA APP;

-- Enable Cortex Search and AI features
-- Note: Ensure your Snowflake account has Cortex features enabled

-- Create file formats for data loading
CREATE OR REPLACE FILE FORMAT JSON_FORMAT
  TYPE = 'JSON'
  STRIP_OUTER_ARRAY = TRUE
  COMPRESSION = 'AUTO';

CREATE OR REPLACE FILE FORMAT CSV_FORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = ','
  SKIP_HEADER = 1
  NULL_IF = ('NULL', 'null', '')
  EMPTY_FIELD_AS_NULL = TRUE
  COMPRESSION = 'AUTO';

-- Create stages for image and data uploads
CREATE OR REPLACE STAGE GHOST_IMAGES_STAGE
  FILE_FORMAT = (TYPE = 'CSV')
  COMMENT = 'Stage for ghost images and multimedia content';

CREATE OR REPLACE STAGE GHOST_DATA_STAGE
  FILE_FORMAT = JSON_FORMAT
  COMMENT = 'Stage for ghost detection data in JSON format';

-- Create notification integration (optional, for real-time processing)
-- CREATE NOTIFICATION INTEGRATION IF NOT EXISTS ghost_detection_notification
--   TYPE = QUEUE
--   ENABLED = TRUE;

COMMENT ON DATABASE GHOST_DETECTION IS 'Ghost Detection and Analysis System - Capturing and analyzing paranormal activity using Snowflake Cortex AI';

