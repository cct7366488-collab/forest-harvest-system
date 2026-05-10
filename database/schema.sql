-- Forest Harvest System Database Schema
-- Core tables: plots, trees, species, volume_models, height_models

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS species (
    id BIGSERIAL PRIMARY KEY,
    species_code VARCHAR(50) UNIQUE,
    chinese_name VARCHAR(100),
    scientific_name VARCHAR(255),
    family VARCHAR(100),
    genus VARCHAR(100),
    common_group VARCHAR(100),
    is_native BOOLEAN,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS volume_models (
    id BIGSERIAL PRIMARY KEY,
    species_code VARCHAR(50),
    species_name VARCHAR(100),
    model_name VARCHAR(150),
    formula_text TEXT NOT NULL,
    formula_expression TEXT,
    variables JSONB,
    coefficients JSONB,
    applicable_region VARCHAR(150),
    sample_size INTEGER,
    r_squared NUMERIC,
    author VARCHAR(150),
    publication_year INTEGER,
    source_reference TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS height_models (
    id BIGSERIAL PRIMARY KEY,
    species_code VARCHAR(50),
    species_name VARCHAR(100),
    model_name VARCHAR(150),
    formula_text TEXT NOT NULL,
    formula_expression TEXT,
    variables JSONB,
    coefficients JSONB,
    applicable_region VARCHAR(150),
    sample_size INTEGER,
    r_squared NUMERIC,
    author VARCHAR(150),
    publication_year INTEGER,
    source_reference TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plots (
    id BIGSERIAL PRIMARY KEY,
    plot_code VARCHAR(100),
    inventory_cycle VARCHAR(20),
    original_plot_id VARCHAR(100),
    county VARCHAR(100),
    township VARCHAR(100),
    forest_district VARCHAR(100),
    working_circle VARCHAR(100),
    compartment VARCHAR(100),
    sub_compartment VARCHAR(100),
    elevation_m NUMERIC,
    slope_degree NUMERIC,
    aspect_degree NUMERIC,
    forest_type VARCHAR(100),
    land_use_type VARCHAR(100),
    plot_area_ha NUMERIC,
    x_coord NUMERIC,
    y_coord NUMERIC,
    longitude NUMERIC,
    latitude NUMERIC,
    geom geometry(Point, 3826),
    source_file TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trees (
    id BIGSERIAL PRIMARY KEY,
    plot_id BIGINT REFERENCES plots(id) ON DELETE CASCADE,
    inventory_cycle VARCHAR(20),
    tree_no VARCHAR(50),
    tree_status VARCHAR(50),
    record_type VARCHAR(50),
    line_distance_m NUMERIC,
    plot_tree_distance_m NUMERIC,
    species_code VARCHAR(50),
    species_name VARCHAR(100),
    dbh_cm NUMERIC,
    height_m NUMERIC,
    clear_bole_height_m NUMERIC,
    crown_class VARCHAR(50),
    estimated_volume_m3 NUMERIC,
    volume_model_id BIGINT REFERENCES volume_models(id),
    height_model_id BIGINT REFERENCES height_models(id),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_plots_inventory_cycle ON plots(inventory_cycle);
CREATE INDEX IF NOT EXISTS idx_plots_plot_code ON plots(plot_code);
CREATE INDEX IF NOT EXISTS idx_plots_geom ON plots USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_trees_plot_id ON trees(plot_id);
CREATE INDEX IF NOT EXISTS idx_trees_species_code ON trees(species_code);
CREATE INDEX IF NOT EXISTS idx_trees_inventory_cycle ON trees(inventory_cycle);
CREATE INDEX IF NOT EXISTS idx_species_code ON species(species_code);
CREATE INDEX IF NOT EXISTS idx_volume_models_species_code ON volume_models(species_code);
CREATE INDEX IF NOT EXISTS idx_height_models_species_code ON height_models(species_code);
