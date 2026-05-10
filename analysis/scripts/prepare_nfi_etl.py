"""
Prepare NFI3 / NFI4 shapefile ETL workflow for Forest Harvest System.

This script currently performs discovery and field preview only.
It supports common Taiwan DBF encodings: utf-8, cp950, big5, latin1.
Future version will transform NFI shapefile records into PostGIS plots/trees tables.
"""

from pathlib import Path
import shapefile

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"

ENCODINGS = ['utf-8', 'cp950', 'big5', 'latin1']


def open_shapefile_with_fallback(shp_path: Path):
    last_error = None

    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            # Force DBF header/field loading
            _ = reader.fields
            return reader, enc
        except UnicodeDecodeError as e:
            last_error = e
        except Exception as e:
            last_error = e

    raise RuntimeError(f'Unable to read shapefile with encodings {ENCODINGS}: {shp_path}. Last error: {last_error}')


def preview_dataset(name: str, folder: Path):
    print(f'=== {name} ===')
    shp_files = list(folder.rglob('*.shp'))
    print(f'Shapefile count: {len(shp_files)}')

    for shp in shp_files:
        print(f'File: {shp}')

        try:
            reader, encoding = open_shapefile_with_fallback(shp)
            print(f'Encoding used: {encoding}')
            print(f'Shape type: {reader.shapeTypeName}')
            print(f'Record count: {len(reader)}')

            fields = [f[0] for f in reader.fields[1:]]
            print('Fields:')
            for field in fields:
                print(f'  - {field}')

        except Exception as e:
            print(f'ERROR: {e}')

        print()


if __name__ == '__main__':
    preview_dataset('NFI3', NFI_ROOT / 'nfi3')
    preview_dataset('NFI4', NFI_ROOT / 'nfi4')
