-- NFI4 staging table for raw child/sub-records
-- Purpose: preserve NFI4 raw records before converting them into formal trees or other normalized tables.

CREATE TABLE IF NOT EXISTS nfi4_subrecords (
    id BIGSERIAL PRIMARY KEY,
    plot_id BIGINT REFERENCES plots(id) ON DELETE SET NULL,
    plot_code VARCHAR(150),
    inventory_cycle VARCHAR(20) DEFAULT 'NFI4',
    sample_id VARCHAR(100),
    group_key TEXT,
    record_index INTEGER,
    x_coord NUMERIC,
    y_coord NUMERIC,
    geom geometry(Point, 3826),
    source_file TEXT,
    raw_attributes JSONB NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_plot_id ON nfi4_subrecords(plot_id);
CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_plot_code ON nfi4_subrecords(plot_code);
CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_sample_id ON nfi4_subrecords(sample_id);
CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_group_key ON nfi4_subrecords(group_key);
CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_geom ON nfi4_subrecords USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_nfi4_subrecords_raw_attributes ON nfi4_subrecords USING GIN(raw_attributes);
