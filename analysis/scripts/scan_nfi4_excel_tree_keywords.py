import json
from pathlib import Path

path = Path("docs/data/nfi4-excel-structure-inventory.json")
data = json.loads(path.read_text(encoding="utf-8"))

keywords = [
    "DBH", "dbh", "胸徑", "胸高直徑",
    "樹種", "樹種代碼", "species", "Species",
    "樣木", "樣木號", "樣木編號",
    "立木", "單木", "tree", "Tree",
    "材積", "Volume", "Volumn",
    "樹高", "Height",
    "Crown", "樹冠"
]

print("=== NFI4 Excel keyword scan ===")
print()

for workbook in data.get("workbooks", []):
    print("Workbook:", workbook.get("name"))
    print("File:", workbook.get("file"))
    print()

    for sheet in workbook.get("sheets", []):
        headers = sheet.get("headers", [])
        matched = []

        for h in headers:
            if not h:
                continue
            for k in keywords:
                if k.lower() in str(h).lower():
                    matched.append(h)
                    break

        print("  Sheet:", sheet.get("sheet_name"))
        print("  rows:", sheet.get("max_row"), "cols:", sheet.get("max_column"))

        if matched:
            print("  matched tree-related fields:")
            for m in matched:
                print("   -", m)
        else:
            print("  matched tree-related fields: NOT FOUND")

        print()

print("=== done ===")
