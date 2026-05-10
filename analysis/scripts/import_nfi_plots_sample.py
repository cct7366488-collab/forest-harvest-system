"""
Import sample NFI3 / NFI4 plot records into PostgreSQL plots table.
This is a controlled test import. Default limit is 5 records per dataset.
"""

from pathlib import Path
from decimal import Decimal
import json
import shapefile
import psycopg2

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
MAPPING_PATH = DOCS_DATA / "nfi-field-mapping.json"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "forest_db",
    "user": "forest_user",
    "password": "forest_password",
}

ENCODINGS = ['utf-8', 'cp950', 'big5', 'latin1']
SAMPLE_LIMIT = 5

def open_reader(shp_path: Path, preferred_encoding=None):
    encodings = [preferred_encoding] if preferred_encoding else []
    encodings += [e for e in ENCODINGS if e not in encodings]
    last_error = None
    for enc in encodings:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            return reader, enc
        except Exception as e:
            last_error = e
    raise RuntimeError(f'Cannot open {shp_path}. Last error: {last_error}')

def safe_float(value):
    if value is None:
        return None
    try:
        if value == '':
            return None
        return float(value)
    except Exception:
        return None

def safe_str(value):
    if value is None:
        return None
    text = str(value).strip()
    return text if text else None

def get_value(record_dict, field_name):
    if not field_name:
        return None
    return record_dict.get(field_name)

def insert_plot(cur, data):
    cur.execute(
        """
        SELECT id FROM plots
        WHERE plot_code = %s AND inventory_cycle = %s
        LIMIT 1
        """,
        (data['plot_code'], data['inventory_cycle'])
    )
    existing = cur.fetchone()
    if existing:
        return existing[0], False

    cur.execute(
        """
        INSERT INTO plots (
            plot_code, inventory_cycle, original_plot_id, county, township,
            forest_district, working_circle, compartment, sub_compartment,
            elevation_m, slope_degree, aspect_degree, forest_type, land_use_type,
            plot_area_ha, x_coord, y_coord, longitude, latitude, geom, source_file, notes
        ) VALUES (
            %(plot_code)s, %(inventory_cycle)s, %(original_plot_id)s, %(county)s, %(township)s,
            %(forest_district)s, %(working_circle)s, %(compartment)s, %(sub_compartment)s,
            %(elevation_m)s, %(slope_degree)s, %(aspect_degree)s, %(forest_type)s, %(land_use_type)s,
            %(plot_area_ha)s, %(x_coord)s, %(y_coord)s, %(longitude)s, %(latitude)s,
            CASE
                WHEN %(x_coord)s IS NOT NULL AND %(y_coord)s IS NOT NULL
                THEN ST_SetSRID(ST_MakePoint(%(x_coord)s, %(y_coord)s), 3826)
                ELSE NULL
            END,
            %(source_file)s, %(notes)s
        )
        RETURNING id
        """,
        data
    )
    return cur.fetchone()[0], True

def main():
    mapping = json.loads(MAPPING_PATH.read_text(encoding='utf-8'))
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    summary = []

    try:
        with conn.cursor() as cur:
            for dataset_name, dataset in mapping['datasets'].items():
                for shp_info in dataset['shapefiles']:
                    shp_path = Path(shp_info['file'])
                    reader, encoding = open_reader(shp_path, shp_info.get('encoding'))
                    field_map = shp_info['mapping_to_plots']
                    inserted = 0
                    skipped = 0

                    for index, sr in enumerate(reader.iterShapeRecords()):
                        if index >= SAMPLE_LIMIT:
                            break

                        record_dict = sr.record.as_dict()
                        shape = sr.shape

                        x = safe_float(get_value(record_dict, field_map.get('x_coord')))
                        y = safe_float(get_value(record_dict, field_map.get('y_coord')))

                        if (x is None or y is None) and getattr(shape, 'points', None):
                            if len(shape.points) > 0:
                                x = x if x is not None else safe_float(shape.points[0][0])
                                y = y if y is not None else safe_float(shape.points[0][1])

                        raw_plot_code = safe_str(get_value(record_dict, field_map.get('plot_code')))
                        if raw_plot_code:
                            plot_code = f'{dataset_name}-{raw_plot_code}'
                        else:
                            plot_code = f'{dataset_name}-{index+1:06d}'

                        data = {
                            'plot_code': plot_code,
                            'inventory_cycle': dataset_name,
                            'original_plot_id': safe_str(get_value(record_dict, field_map.get('original_plot_id'))),
                            'county': safe_str(get_value(record_dict, field_map.get('county'))),
                            'township': safe_str(get_value(record_dict, field_map.get('township'))),
                            'forest_district': safe_str(get_value(record_dict, field_map.get('forest_district'))),
                            'working_circle': safe_str(get_value(record_dict, field_map.get('working_circle'))),
                            'compartment': safe_str(get_value(record_dict, field_map.get('compartment'))),
                            'sub_compartment': safe_str(get_value(record_dict, field_map.get('sub_compartment'))),
                            'elevation_m': safe_float(get_value(record_dict, field_map.get('elevation_m'))),
                            'slope_degree': safe_float(get_value(record_dict, field_map.get('slope_degree'))),
                            'aspect_degree': safe_float(get_value(record_dict, field_map.get('aspect_degree'))),
                            'forest_type': safe_str(get_value(record_dict, field_map.get('forest_type'))),
                            'land_use_type': safe_str(get_value(record_dict, field_map.get('land_use_type'))),
                            'plot_area_ha': safe_float(get_value(record_dict, field_map.get('plot_area_ha'))),
                            'x_coord': x,
                            'y_coord': y,
                            'longitude': safe_float(get_value(record_dict, field_map.get('longitude'))),
                            'latitude': safe_float(get_value(record_dict, field_map.get('latitude'))),
                            'source_file': str(shp_path),
                            'notes': f'Sample import from {dataset_name}; encoding={encoding}'
                        }

                        _, was_inserted = insert_plot(cur, data)
                        if was_inserted:
                            inserted += 1
                        else:
                            skipped += 1

                    summary.append({
                        'dataset': dataset_name,
                        'file': str(shp_path),
                        'inserted': inserted,
                        'skipped_existing': skipped
                    })

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print('NFI sample plot import completed')
    for item in summary:
        print(item)

if __name__ == '__main__':
    main()
