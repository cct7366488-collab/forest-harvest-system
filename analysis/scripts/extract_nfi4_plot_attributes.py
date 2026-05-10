from pathlib import Path
from collections import Counter, defaultdict
import json
import psycopg2
from psycopg2.extras import Json

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "forest_db",
    "user": "forest_user",
    "password": "forest_password",
}

NOTE = "Extracted from nfi4_subrecords staging table"


def clean(value):
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in ["none", "nan", "null"]:
        return ""
    return text


def safe_float(value):
    text = clean(value)
    if text == "":
        return None
    try:
        return float(text)
    except Exception:
        return None


def safe_int(value):
    text = clean(value)
    if text == "":
        return None
    try:
        return int(float(text))
    except Exception:
        return None


def first_existing(raw, names):
    for name in names:
        if name in raw:
            value = clean(raw.get(name))
            if value != "":
                return value
    return None


def most_common_non_empty(values):
    cleaned = [clean(v) for v in values]
    cleaned = [v for v in cleaned if v != ""]
    if not cleaned:
        return None
    return Counter(cleaned).most_common(1)[0][0]


def numeric_most_common(values):
    value = most_common_non_empty(values)
    return safe_float(value)


def integer_most_common(values):
    value = most_common_non_empty(values)
    return safe_int(value)


def collect_values(records, field_names):
    values = []

    for record in records:
        raw = record["raw_attributes"] or {}

        for field_name in field_names:
            if field_name in raw:
                values.append(raw.get(field_name))
                break

    return values


def summarize_raw(records):
    field_values = defaultdict(list)

    for record in records:
        raw = record["raw_attributes"] or {}

        for key, value in raw.items():
            text = clean(value)
            if text != "":
                field_values[key].append(text)

    summary = {
        "source_subrecord_count": len(records),
        "fields": {}
    }

    for key, values in field_values.items():
        counter = Counter(values)
        summary["fields"][key] = {
            "non_empty_count": len(values),
            "unique_count": len(counter),
            "top_values": counter.most_common(10)
        }

    return summary


FIELD_MAP = {
    "terrain": ["Terrain", "地被型態", "地形"],
    "elevation_m": ["Elevation", "Altitude", "海拔"],
    "slope_degree": ["Slope", "坡度"],
    "aspect_degree": ["Aspect", "方位角", "坡向"],
    "landuse": ["LANDUSE", "Landuse", "landuse", "土地利用"],
    "forest_type_major": ["林型大類"],
    "forest_type_middle": ["林型中類"],
    "forest_type_minor": ["林型小類"],
    "main_species_a": ["A木樹種"],
    "main_species_b": ["B木樹種"],
    "plot_area_ha": ["樣區面積", "PlotArea", "PLOTAREA"],
    "tree_count": ["樣木數"],
    "stand_age": ["AGE", "Age", "林齡"],
    "stand_density": ["DENSITY", "Density", "密度"],
    "plot_basal_area": ["樣區BA"],
    "plot_volume": ["樣區Vol"],
    "basal_area_ha": ["SBA_ha"],
    "volume_ha": ["Vol_ha"],
    "stem_ha": ["株_ha"],
    "co2_ha": ["CO2_ha"],
    "co2_ha_secondary": ["CO2_ha1"],
    "crown_density": ["樹冠密度", "Crown", "COVDENSITY"],
    "crown_height": ["COVHEIGHT", "CovHeight", "冠層高度"]
}


TEXT_FIELDS = [
    "terrain",
    "landuse",
    "forest_type_major",
    "forest_type_middle",
    "forest_type_minor",
    "main_species_a",
    "main_species_b"
]

INTEGER_FIELDS = [
    "tree_count"
]

NUMERIC_FIELDS = [
    "elevation_m",
    "slope_degree",
    "aspect_degree",
    "plot_area_ha",
    "stand_age",
    "stand_density",
    "plot_basal_area",
    "plot_volume",
    "basal_area_ha",
    "volume_ha",
    "stem_ha",
    "co2_ha",
    "co2_ha_secondary",
    "crown_density",
    "crown_height"
]


def load_subrecords():
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id,
                    plot_id,
                    plot_code,
                    sample_id,
                    group_key,
                    record_index,
                    x_coord,
                    y_coord,
                    source_file,
                    raw_attributes
                FROM nfi4_subrecords
                ORDER BY plot_code, record_index
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    records = []

    for row in rows:
        raw = row[9]

        if isinstance(raw, str):
            raw = json.loads(raw)

        records.append({
            "id": row[0],
            "plot_id": row[1],
            "plot_code": row[2],
            "sample_id": row[3],
            "group_key": row[4],
            "record_index": row[5],
            "x_coord": safe_float(row[6]),
            "y_coord": safe_float(row[7]),
            "source_file": row[8],
            "raw_attributes": raw or {}
        })

    return records


def build_attributes_for_group(plot_code, records):
    first = records[0]

    data = {
        "plot_id": first["plot_id"],
        "plot_code": plot_code,
        "inventory_cycle": "NFI4",
        "sample_id": first["sample_id"],
        "group_key": first["group_key"],
        "source_subrecord_count": len(records),
        "x_coord": first["x_coord"],
        "y_coord": first["y_coord"],
        "source_file": first["source_file"],
        "raw_summary": summarize_raw(records),
        "notes": NOTE
    }

    for field in TEXT_FIELDS:
        values = collect_values(records, FIELD_MAP[field])
        data[field] = most_common_non_empty(values)

    for field in INTEGER_FIELDS:
        values = collect_values(records, FIELD_MAP[field])
        data[field] = integer_most_common(values)

    for field in NUMERIC_FIELDS:
        values = collect_values(records, FIELD_MAP[field])
        data[field] = numeric_most_common(values)

    return data


def upsert_plot_attributes(cur, data):
    cur.execute(
        """
        INSERT INTO nfi4_plot_attributes (
            plot_id,
            plot_code,
            inventory_cycle,
            sample_id,
            group_key,
            source_subrecord_count,
            x_coord,
            y_coord,
            geom,
            terrain,
            elevation_m,
            slope_degree,
            aspect_degree,
            landuse,
            forest_type_major,
            forest_type_middle,
            forest_type_minor,
            main_species_a,
            main_species_b,
            plot_area_ha,
            tree_count,
            stand_age,
            stand_density,
            plot_basal_area,
            plot_volume,
            basal_area_ha,
            volume_ha,
            stem_ha,
            co2_ha,
            co2_ha_secondary,
            crown_density,
            crown_height,
            raw_summary,
            source_file,
            notes,
            updated_at
        ) VALUES (
            %(plot_id)s,
            %(plot_code)s,
            %(inventory_cycle)s,
            %(sample_id)s,
            %(group_key)s,
            %(source_subrecord_count)s,
            %(x_coord)s,
            %(y_coord)s,
            CASE
                WHEN %(x_coord)s IS NOT NULL AND %(y_coord)s IS NOT NULL
                THEN ST_SetSRID(ST_MakePoint(%(x_coord)s, %(y_coord)s), 3826)
                ELSE NULL
            END,
            %(terrain)s,
            %(elevation_m)s,
            %(slope_degree)s,
            %(aspect_degree)s,
            %(landuse)s,
            %(forest_type_major)s,
            %(forest_type_middle)s,
            %(forest_type_minor)s,
            %(main_species_a)s,
            %(main_species_b)s,
            %(plot_area_ha)s,
            %(tree_count)s,
            %(stand_age)s,
            %(stand_density)s,
            %(plot_basal_area)s,
            %(plot_volume)s,
            %(basal_area_ha)s,
            %(volume_ha)s,
            %(stem_ha)s,
            %(co2_ha)s,
            %(co2_ha_secondary)s,
            %(crown_density)s,
            %(crown_height)s,
            %(raw_summary)s,
            %(source_file)s,
            %(notes)s,
            CURRENT_TIMESTAMP
        )
        ON CONFLICT (plot_code)
        DO UPDATE SET
            plot_id = EXCLUDED.plot_id,
            sample_id = EXCLUDED.sample_id,
            group_key = EXCLUDED.group_key,
            source_subrecord_count = EXCLUDED.source_subrecord_count,
            x_coord = EXCLUDED.x_coord,
            y_coord = EXCLUDED.y_coord,
            geom = EXCLUDED.geom,
            terrain = EXCLUDED.terrain,
            elevation_m = EXCLUDED.elevation_m,
            slope_degree = EXCLUDED.slope_degree,
            aspect_degree = EXCLUDED.aspect_degree,
            landuse = EXCLUDED.landuse,
            forest_type_major = EXCLUDED.forest_type_major,
            forest_type_middle = EXCLUDED.forest_type_middle,
            forest_type_minor = EXCLUDED.forest_type_minor,
            main_species_a = EXCLUDED.main_species_a,
            main_species_b = EXCLUDED.main_species_b,
            plot_area_ha = EXCLUDED.plot_area_ha,
            tree_count = EXCLUDED.tree_count,
            stand_age = EXCLUDED.stand_age,
            stand_density = EXCLUDED.stand_density,
            plot_basal_area = EXCLUDED.plot_basal_area,
            plot_volume = EXCLUDED.plot_volume,
            basal_area_ha = EXCLUDED.basal_area_ha,
            volume_ha = EXCLUDED.volume_ha,
            stem_ha = EXCLUDED.stem_ha,
            co2_ha = EXCLUDED.co2_ha,
            co2_ha_secondary = EXCLUDED.co2_ha_secondary,
            crown_density = EXCLUDED.crown_density,
            crown_height = EXCLUDED.crown_height,
            raw_summary = EXCLUDED.raw_summary,
            source_file = EXCLUDED.source_file,
            notes = EXCLUDED.notes,
            updated_at = CURRENT_TIMESTAMP
        RETURNING id
        """,
        {
            **data,
            "raw_summary": Json(data["raw_summary"])
        }
    )

    return cur.fetchone()[0]


def main():
    records = load_subrecords()

    if not records:
        print("No nfi4_subrecords found. Nothing to extract.")
        return

    groups = defaultdict(list)

    for record in records:
        groups[record["plot_code"]].append(record)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    created_or_updated = 0

    try:
        with conn.cursor() as cur:
            for plot_code, group_records in sorted(groups.items()):
                data = build_attributes_for_group(plot_code, group_records)
                upsert_plot_attributes(cur, data)
                created_or_updated += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    print("NFI4 plot attributes extraction completed")
    print(f"Source nfi4_subrecords: {len(records)}")
    print(f"Plot attribute records created or updated: {created_or_updated}")

    print()
    print("Extracted plot_codes:")
    for plot_code, group_records in sorted(groups.items()):
        print(f"  {plot_code}: {len(group_records)} subrecords")


if __name__ == "__main__":
    main()
