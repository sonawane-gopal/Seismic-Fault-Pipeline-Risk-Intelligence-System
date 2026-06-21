-- SFPRIS - Seismic-Fault Pipeline Risk Intelligence System
--  Database Setup
CREATE DATABASE sfpris_db;

--  Enable PostGIS spatial extension
CREATE EXTENSION postgis;
CREATE EXTENSION IF NOT EXISTS postgis;

-- Enable PostGIS topology extension
CREATE EXTENSION postgis_topology;

--  Verify PostGIS is active
SELECT PostGIS_Version();


--  Schema Creation
-- TABLE 1: PHMSA Hazardous Liquid Incidents
-- ============================================================
DROP TABLE IF EXISTS phmsa_hl_incidents;
    CREATE TABLE phmsa_hl_incidents (
    id SERIAL PRIMARY KEY,
    report_number VARCHAR(50),
    iyear INTEGER,
    significant VARCHAR(10),
    cause VARCHAR(100),
    location_latitude DOUBLE PRECISION,
    location_longitude DOUBLE PRECISION,
    onshore_state_abbreviation VARCHAR(10),
    name VARCHAR(200),
    total_cost DOUBLE PRECISION,
    pipe_diameter DOUBLE PRECISION,
    material_involved VARCHAR(100),
    installation_year DOUBLE PRECISION,
    system_part_involved VARCHAR(200),
    source VARCHAR(50),
    geom GEOMETRY(Point, 4326)
);

-- ============================================================
-- TABLE 2: PHMSA Gas Transmission & Gathering Incidents
-- ============================================================
DROP TABLE IF EXISTS phmsa_gas_incidents;
   CREATE TABLE phmsa_gas_incidents (
    id SERIAL PRIMARY KEY,
    report_number VARCHAR(50),
    iyear INTEGER,
    significant VARCHAR(10),
    cause VARCHAR(100),
    location_latitude DOUBLE PRECISION,
    location_longitude DOUBLE PRECISION,
    onshore_state_abbreviation VARCHAR(10),
    name VARCHAR(200),
    total_cost DOUBLE PRECISION,
    pipe_diameter DOUBLE PRECISION,
    material_involved VARCHAR(100),
    installation_year DOUBLE PRECISION,
    system_part_involved VARCHAR(200),
    source VARCHAR(50),
    geom GEOMETRY(Point, 4326)
);
-- ============================================================
-- TABLE 3: USGS Quaternary Fault Lines
-- ============================================================
CREATE TABLE usgs_faults (
    id SERIAL PRIMARY KEY,
    fault_id VARCHAR(50),                 -- USGS fault ID
    fault_name VARCHAR(200),              -- Name of fault
    fault_class VARCHAR(10),              -- Class A, B, C, D
    slip_rate VARCHAR(50),                -- Slip rate category
    dip_direction VARCHAR(50),            -- Fault dip direction
    geom GEOMETRY(MultiLineString, 4326)  -- Fault line geometry
);

-- ============================================================
-- TABLE 4: HIFLD Natural Gas Pipelines
-- ============================================================
CREATE TABLE hifld_gas_pipelines (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(50),              -- Pipeline identifier
    operator_name VARCHAR(200),           -- Operator name
    pipe_type VARCHAR(100),               -- Type of pipeline
    diameter DOUBLE PRECISION,            -- Pipe diameter (inches)
    material VARCHAR(100),                -- Pipe material
    install_year INTEGER,                 -- Year installed
    state VARCHAR(50),                    -- State
    geom GEOMETRY(MultiLineString, 4326)  -- Pipeline geometry
);

-- ============================================================
-- TABLE 5: HIFLD Hazardous Liquid Pipelines
-- ============================================================
CREATE TABLE hifld_hl_pipelines (
    id SERIAL PRIMARY KEY,
    pipeline_id VARCHAR(50),              -- Pipeline identifier
    operator_name VARCHAR(200),           -- Operator name
    pipe_type VARCHAR(100),               -- Type of pipeline
    diameter DOUBLE PRECISION,            -- Pipe diameter (inches)
    material VARCHAR(100),                -- Pipe material
    install_year INTEGER,                 -- Year installed
    state VARCHAR(50),                    -- State
    geom GEOMETRY(MultiLineString, 4326)  -- Pipeline geometry
);

-- ============================================================
-- TABLE 6: USGS Earthquake Events
-- ============================================================
CREATE TABLE usgs_earthquakes (
    id SERIAL PRIMARY KEY,
    eq_id VARCHAR(50),                    -- USGS earthquake ID
    magnitude DOUBLE PRECISION,           -- Earthquake magnitude
    depth DOUBLE PRECISION,               -- Depth in km
    eq_time TIMESTAMP,                    -- Time of earthquake
    place VARCHAR(200),                   -- Location description
    latitude DOUBLE PRECISION,            -- Earthquake latitude
    longitude DOUBLE PRECISION,           -- Earthquake longitude
    geom GEOMETRY(Point, 4326)            -- Spatial point geometry
);

-- ============================================================
-- SPATIAL INDEXES: Speed up spatial queries
-- ============================================================
CREATE INDEX idx_phmsa_hl_geom ON phmsa_hl_incidents USING GIST(geom);
CREATE INDEX idx_phmsa_gas_geom ON phmsa_gas_incidents USING GIST(geom);
CREATE INDEX idx_usgs_faults_geom ON usgs_faults USING GIST(geom);
CREATE INDEX idx_hifld_gas_geom ON hifld_gas_pipelines USING GIST(geom);
CREATE INDEX idx_hifld_hl_geom ON hifld_hl_pipelines USING GIST(geom);
CREATE INDEX idx_usgs_eq_geom ON usgs_earthquakes USING GIST(geom);

-- ============================================================
-- VERIFY: List all created tables
-- ============================================================
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

SELECT current_database();
CREATE EXTENSION IF NOT EXISTS postgis;
SELECT PostGIS_Version();
