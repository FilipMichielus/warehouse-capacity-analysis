-- Create logistics_data database
-- Creates database to store warehouse data
CREATE DATABASE IF NOT EXISTS logistics_data;

-- Use logistics_data database to create tables inside
USE logistics_data;


-- Create Building table
-- Stores warehouse buildings
CREATE TABLE Building (
    address BIGINT PRIMARY KEY,
    long_name VARCHAR(25) NOT NULL,
    shortcut VARCHAR(2) NOT NULL
);

-- Create Areas table
-- Stores areas inside different buildings
CREATE TABLE Areas (
    address BIGINT PRIMARY KEY,
    long_name VARCHAR(25) NOT NULL,
    zone_address BIGINT,
    building_address BIGINT NOT NULL,

    FOREIGN KEY (zone_address) REFERENCES Areas(address),
    FOREIGN KEY (building_address) REFERENCES Building(address)
);

-- Create Locations table
-- Stores warehouse locations
CREATE TABLE Locations (
    address BIGINT PRIMARY KEY,
    packing_type VARCHAR(4) NOT NULL,
    location_category VARCHAR(6) NOT NULL,
    location_status VARCHAR(1) NOT NULL,
    
    FOREIGN KEY (address) REFERENCES Areas(address)
);

-- Create Storage_configuration table
-- Stores configuration for storages
CREATE TABLE Storage_configuration(
    area_address BIGINT PRIMARY KEY,
    racks INT NOT NULL,
    columns_count INT NOT NULL,
    shelves INT NOT NULL,
    
    FOREIGN KEY (area_address) REFERENCES Areas(address)
);
