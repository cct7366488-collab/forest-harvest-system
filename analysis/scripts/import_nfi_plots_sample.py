from pathlib import Path
import shapefile
import psycopg2

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "forest_db",
    "user": "forest_user",
    "password": "forest_password",
}

ENCODINGS = ["utf-8", "cp950", "big5", "latin1"]
SAMPLE_LIMIT = 5


def open_reader(shp_path):
    last_error = None
    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            return reader, enc
        except Exception as e:
            last_error = e
    raise RuntimeError(f"Cannot open shapefile: {shp_path} / {last_error}")


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def safe_float(value):
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def safe_str(value):
    text = clean(value)
    return text if text else None


def insert_plot(cur, data):
    cur.execute(
        """
        SELECT id FROM plots
        WHERE plot_code = %s AND inventory_cycle = %s
        LIMIT 1
        """,
        (data["plot_code"], data["inventory_cycle"]),
    )

    existing = cur.fetchone()
    if existing:
        return existing[0], False

    cur.execute(
        """
        INSERT INTO plots (
            plot_code, inventory_cycle, original_plot_id,
            county, township, forest_district,
            elevation_m, slope_degree, aspect_degree,
            forest_type, land_use_type,
            plot_area_ha, x_coord, y_coord,
            longitude, latitude, geom,
            source_file, notes
        ) VALUES (
            %(plot_code)s, %(inventory_cycle)s, %(original_plot_id)s,
            %(county)s, %(township)s, %(forest_district)s,
            %(elevation_m)s, %(slope_degree)s, %(aspect_degree)s,
            %(forest_type)s, %(land_use_type)s,
            %(plot_area_ha)s, %(x_coord)s, %(y_coord)s,
            %(longitude)s, %(latitude)s,
            CASE
                WHEN %(x_coord)s IS NOT NULL AND %(y_coord)s IS NOT NULL
                THEN ST_SetSRID(ST_MakePoint(%(x_coord)s, %(y_coord)s), 3826)
                ELSE NULL
            END,
            %(source_file)s, %(notes)s
        )
        RETURNING id
        """,
        data,
    )

    return cur.fetchone()[0], True


def import_nfi3(cur):
    folder = NFI_ROOT / "nfi3"
    shp = list(folder.rglob("*.shp"))[0]
    reader, enc = open_reader(shp)

    inserted = 0
    skipped = 0

    for idx, sr in enumerate(reader.iterShapeRecords()):
        if inserted >= SAMPLE_LIMIT:
            break

        record = sr.record.as_dict()
        shape = sr.shape

        plot_id = clean(record.get("PLOT_ID")) or clean(record.get("PLOT_")) or str(idx + 1)
        plot_code = "NFI3-" + plot_id

        x = None
        y = None
        if getattr(shape, "points", None) and len(shape.points) > 0:
            x = safe_float(shape.points[0][0])
            y = safe_float(shape.points[0][1])

        data = {
            "plot_code": plot_code,
            "inventory_cycle": "NFI3",
            "original_plot_id": plot_id,
            "county": None,
            "township": None,
            "forest_district": None,
            "elevation_m": safe_float(record.get("ELEVATION")) or safe_float(record.get("ELEV")),
            "slope_degree": safe_float(record.get("SLOPE")),
            "aspect_degree": safe_float(record.get("ASPECT")),
            "forest_type": safe_str(record.get("STAND")),
            "land_use_type": safe_str(record.get("LANDUSE")),
            "plot_area_ha": safe_float(record.get("PLOTAREA")),
            "x_coord": x,
            "y_coord": y,
            "longitude": None,
            "latitude": None,
            "source_file": str(shp),
            "notes": "NFI3 sample import; encoding=" + enc,
        }

        _, ok = insert_plot(cur, data)
        if ok:
            inserted += 1
        else:
            skipped += 1

    return {"dataset": "NFI3", "inserted": inserted, "skipped": skipped, "file": str(shp)}


def import_nfi4(cur):
    folder = NFI_ROOT / "nfi4"
    shp = list(folder.rglob("*.shp"))[0]
    reader, enc = open_reader(shp)

    groups = {}

    for sr in reader.iterShapeRecords():
        record = sr.record.as_dict()

        sample_id = clean(record.get("樣點編號"))
        x = clean(record.get("X_Coord"))
        y = clean(record.get("Y_Coord"))

        if not sample_id:
            sample_id = "NO_SAMPLE"

        group_key = sample_id + "|" + x + "|" + y

        if group_key not in groups:
            groups[group_key] = {
                "record": record,
                "shape": sr.shape,
            }

        if len(groups) >= SAMPLE_LIMIT:
            break

    inserted = 0
    skipped = 0

    for group_key, item in groups.items():
        record = item["record"]
        shape = item["shape"]

        sample_id = clean(record.get("樣點編號")) or "NO_SAMPLE"

        x = safe_float(record.get("X_Coord"))
        y = safe_float(record.get("Y_Coord"))

        if (x is None or y is None) and getattr(shape, "points", None) and len(shape.points) > 0:
            x = x if x is not None else safe_float(shape.points[0][0])
            y = y if y is not None else safe_float(shape.points[0][1])

        plot_code = f"NFI4-{sample_id}-{x}-{y}"

        data = {
            "plot_code": plot_code,
            "inventory_cycle": "NFI4",
            "original_plot_id": sample_id,
            "county": None,
            "township": None,
            "forest_district": safe_str(record.get("DeptName")),
            "elevation_m": safe_float(record.get("Altitude")),
            "slope_degree": safe_float(record.get("Slope")),
            "aspect_degree": safe_float(record.get("Aspect")),
            "forest_type": safe_str(record.get("林型小類")) or safe_str(record.get("林型中類")) or safe_str(record.get("林型大類")),
            "land_use_type": safe_str(record.get("LANDUSE")),
            "plot_area_ha": safe_float(record.get("樣區面積")),
            "x_coord": x,
            "y_coord": y,
            "longitude": None,
            "latitude": None,
            "source_file": str(shp),
            "notes": "NFI4 grouped sample import by 樣點編號 + X_Coord + Y_Coord; encoding=" + enc,
        }

        _, ok = insert_plot(cur, data)
        if ok:
            inserted += 1
        else:
            skipped += 1

    return {"dataset": "NFI4", "inserted": inserted, "skipped": skipped, "file": str(shp)}


def main():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM plots WHERE inventory_cycle IN ('NFI3', 'NFI4')")
            nfi3_result = import_nfi3(cur)
            nfi4_result = import_nfi4(cur)

        conn.commit()

        print("NFI sample plot import completed")
        print(nfi3_result)
        print(nfi4_result)

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()