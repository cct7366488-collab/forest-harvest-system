from pathlib import Path
from typing import Any
import shapefile
import psycopg2
from psycopg2.extras import Json

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI4_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi" / "nfi4"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "forest_db",
    "user": "forest_user",
    "password": "forest_password",
}

ENCODINGS = ["cp950", "big5", "utf-8", "latin1"]

PER_PLOT_LIMIT = 20
MAX_SCAN = 50000
SAMPLE_NOTE = "NFI4 expanded subrecord sample import"


def open_reader(shp_path: Path):
    last_error = None

    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(
                str(shp_path),
                encoding=enc,
                encodingErrors="replace",
            )
            _ = reader.fields

            for _record in reader.iterRecords():
                break

            return reader, enc
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Cannot open shapefile: {shp_path}. Last error: {last_error}")


def clean(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def safe_float(value: Any):
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def jsonable(value: Any):
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def normalize_record(record_dict: dict) -> dict:
    return {str(key): jsonable(value) for key, value in record_dict.items()}


def build_group_key(sample_id: str, x_coord, y_coord) -> str:
    return f"{sample_id}|{x_coord}|{y_coord}"


def build_plot_code(sample_id: str, x_coord, y_coord) -> str:
    return f"NFI4-{sample_id}-{x_coord}-{y_coord}"


def get_nfi4_shapefile() -> Path:
    shp_files = list(NFI4_ROOT.rglob("*.shp"))

    if not shp_files:
        raise FileNotFoundError(f"No NFI4 shapefile found under: {NFI4_ROOT}")

    return shp_files[0]


def load_existing_nfi4_plots(cur):
    cur.execute(
        """
        SELECT id, plot_code, original_plot_id, x_coord, y_coord
        FROM plots
        WHERE inventory_cycle = 'NFI4'
        ORDER BY id
        """
    )

    lookup = {}

    for plot_id, plot_code, original_plot_id, x_coord, y_coord in cur.fetchall():
        sample_id = clean(original_plot_id)
        x = safe_float(x_coord)
        y = safe_float(y_coord)

        group_key = build_group_key(sample_id, x, y)

        lookup[group_key] = {
            "plot_id": plot_id,
            "plot_code": plot_code,
            "sample_id": sample_id,
            "x_coord": x,
            "y_coord": y,
        }

    return lookup


def insert_subrecord(cur, payload: dict):
    cur.execute(
        """
        INSERT INTO nfi4_subrecords (
            plot_id,
            plot_code,
            inventory_cycle,
            sample_id,
            group_key,
            record_index,
            x_coord,
            y_coord,
            geom,
            source_file,
            raw_attributes,
            notes
        ) VALUES (
            %(plot_id)s,
            %(plot_code)s,
            'NFI4',
            %(sample_id)s,
            %(group_key)s,
            %(record_index)s,
            %(x_coord)s,
            %(y_coord)s,
            CASE
                WHEN %(x_coord)s IS NOT NULL AND %(y_coord)s IS NOT NULL
                THEN ST_SetSRID(ST_MakePoint(%(x_coord)s, %(y_coord)s), 3826)
                ELSE NULL
            END,
            %(source_file)s,
            %(raw_attributes)s,
            %(notes)s
        )
        RETURNING id
        """,
        payload,
    )

    return cur.fetchone()[0]


def main():
    shp_path = get_nfi4_shapefile()
    reader, encoding = open_reader(shp_path)

    print("NFI4 expanded subrecords import started")
    print(f"Shapefile: {shp_path}")
    print(f"Encoding used: {encoding}")
    print(f"Per plot limit: {PER_PLOT_LIMIT}")
    print(f"Max scan: {MAX_SCAN}")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    scanned = 0
    inserted = 0
    skipped_no_plot = 0
    per_plot_counts = {}

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM nfi4_subrecords WHERE notes IN (%s, %s)", (
                "NFI4 sample subrecord import",
                SAMPLE_NOTE,
            ))

            plot_lookup = load_existing_nfi4_plots(cur)

            print(f"Existing NFI4 plots in plots table: {len(plot_lookup)}")

            for group_key in plot_lookup.keys():
                per_plot_counts[group_key] = 0

            for record_index, shape_record in enumerate(reader.iterShapeRecords(), start=1):
                scanned += 1

                if scanned % 5000 == 0:
                    print(f"Scanned={scanned}, inserted={inserted}, skipped_no_plot={skipped_no_plot}")

                if scanned > MAX_SCAN:
                    print("Reached MAX_SCAN, stop scanning.")
                    break

                if plot_lookup and all(count >= PER_PLOT_LIMIT for count in per_plot_counts.values()):
                    print("All target plot groups reached PER_PLOT_LIMIT.")
                    break

                record = shape_record.record.as_dict()
                shape = shape_record.shape

                sample_id = clean(record.get("樣點編號")) or "NO_SAMPLE"
                x_coord = safe_float(record.get("X_Coord"))
                y_coord = safe_float(record.get("Y_Coord"))

                if (x_coord is None or y_coord is None) and getattr(shape, "points", None):
                    if len(shape.points) > 0:
                        x_coord = x_coord if x_coord is not None else safe_float(shape.points[0][0])
                        y_coord = y_coord if y_coord is not None else safe_float(shape.points[0][1])

                group_key = build_group_key(sample_id, x_coord, y_coord)

                plot_info = plot_lookup.get(group_key)

                if plot_info is None:
                    skipped_no_plot += 1
                    continue

                if per_plot_counts[group_key] >= PER_PLOT_LIMIT:
                    continue

                payload = {
                    "plot_id": plot_info["plot_id"],
                    "plot_code": plot_info["plot_code"],
                    "sample_id": sample_id,
                    "group_key": group_key,
                    "record_index": record_index,
                    "x_coord": x_coord,
                    "y_coord": y_coord,
                    "source_file": str(shp_path),
                    "raw_attributes": Json(normalize_record(record)),
                    "notes": SAMPLE_NOTE,
                }

                insert_subrecord(cur, payload)

                inserted += 1
                per_plot_counts[group_key] += 1

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    print("NFI4 expanded subrecords import completed")
    print(f"Scanned records: {scanned}")
    print(f"Inserted subrecords: {inserted}")
    print(f"Skipped because plot_code not found in plots: {skipped_no_plot}")
    print("Per plot counts:")

    for key, count in per_plot_counts.items():
        print(f"  {key}: {count}")


if __name__ == "__main__":
    main()
