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

# NFI4 是台灣資料，優先使用 cp950 / big5
ENCODINGS = ["cp950", "big5", "utf-8", "latin1"]

SAMPLE_LIMIT = 20
MAX_SCAN = 5000
SAMPLE_NOTE = "NFI4 sample subrecord import"


def open_reader(shp_path: Path):
    last_error = None

    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            # 強制讀一筆，確認欄位與 DBF 編碼真的可用
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
        SELECT id, plot_code
        FROM plots
        WHERE inventory_cycle = 'NFI4'
        """
    )
    return {plot_code: plot_id for plot_id, plot_code in cur.fetchall()}


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

    print("NFI4 subrecords sample import started")
    print(f"Shapefile: {shp_path}")
    print(f"Encoding used: {encoding}")
    print(f"Sample limit: {SAMPLE_LIMIT}")
    print(f"Max scan: {MAX_SCAN}")

    inserted = 0
    skipped_no_plot = 0
    scanned = 0

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM nfi4_subrecords WHERE notes = %s", (SAMPLE_NOTE,))

            plot_lookup = load_existing_nfi4_plots(cur)

            print(f"Existing NFI4 plots in plots table: {len(plot_lookup)}")

            for record_index, shape_record in enumerate(reader.iterShapeRecords(), start=1):
                scanned += 1

                if scanned % 500 == 0:
                    print(f"Scanned={scanned}, inserted={inserted}, skipped_no_plot={skipped_no_plot}")

                if scanned > MAX_SCAN:
                    print("Reached MAX_SCAN, stop scanning.")
                    break

                if inserted >= SAMPLE_LIMIT:
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

                plot_code = build_plot_code(sample_id, x_coord, y_coord)
                group_key = f"{sample_id}|{x_coord}|{y_coord}"

                plot_id = plot_lookup.get(plot_code)

                if plot_id is None:
                    skipped_no_plot += 1
                    continue

                payload = {
                    "plot_id": plot_id,
                    "plot_code": plot_code,
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

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    print("NFI4 subrecords sample import completed")
    print(f"Scanned records: {scanned}")
    print(f"Inserted subrecords: {inserted}")
    print(f"Skipped because plot_code not found in plots: {skipped_no_plot}")


if __name__ == "__main__":
    main()
