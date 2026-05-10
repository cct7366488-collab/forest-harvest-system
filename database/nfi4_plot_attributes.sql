-- NFI4 plot / stand attributes table
-- Purpose: store NFI4 plot-level and stand-level attributes extracted from nfi4_subrecords.

CREATE TABLE IF NOT EXISTS nfi4_plot_attributes (
    id BIGSERIAL PRIMARY KEY,
    plot_id BIGINT REFERENCES plots(id) ON DELETE CASCADE,
    plot_code VARCHAR(150) NOT NULL,
    inventory_cycle VARCHAR(20) DEFAULT 'NFI4',
    sample_id VARCHAR(100),
    group_key TEXT,

    source_subrecord_count INTEGER,

    x_coord NUMERIC,
    y_coord NUMERIC,
    geom geometry(Point, 3826),

    terrain VARCHAR(100),
    elevation_m NUMERIC,
    slope_degree NUMERIC,
    aspect_degree NUMERIC,
    landuse VARCHAR(100),

    forest_type_major VARCHAR(100),
    forest_type_middle VARCHAR(100),
    forest_type_minor VARCHAR(100),

    main_species_a VARCHAR(150),
    main_species_b VARCHAR(150),

    plot_area_ha NUMERIC,
    tree_count INTEGER,

    stand_age NUMERIC,
    stand_density NUMERIC,

    plot_basal_area NUMERIC,
    plot_volume NUMERIC,
    basal_area_ha NUMERIC,
    volume_ha NUMERIC,
    stem_ha NUMERIC,
    co2_ha NUMERIC,
    co2_ha_secondary NUMERIC,

    crown_density NUMERIC,
    crown_height NUMERIC,

    raw_summary JSONB,
    source_file TEXT,
    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_nfi4_plot_attributes_plot_code UNIQUE (plot_code)
);

CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_plot_id ON nfi4_plot_attributes(plot_id);
CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_plot_code ON nfi4_plot_attributes(plot_code);
CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_sample_id ON nfi4_plot_attributes(sample_id);
CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_group_key ON nfi4_plot_attributes(group_key);
CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_geom ON nfi4_plot_attributes USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_nfi4_plot_attributes_raw_summary ON nfi4_plot_attributes USING GIN(raw_summary);
