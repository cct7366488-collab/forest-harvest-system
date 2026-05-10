from pathlib import Path
import json
import shapefile
from datetime import datetime

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

targets = {
    "NFI3": NFI_ROOT / "nfi3",
    "NFI4": NFI_ROOT / "nfi4",
}

def inspect_shapefile(shp_path: Path):
    reader = shapefile.Reader(str(shp_path))
    fields = []

    for field in reader.fields[1:]:
        name, field_type, size, decimal = field
        fields.append({
            "name": name,
            "type": field_type,
            "size": size,
            "decimal": decimal
        })

    return {
        "file": str(shp_path),
        "shape_type": reader.shapeTypeName,
        "record_count": len(reader),
        "bbox": reader.bbox,
        "fields": fields
    }

inventory = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "datasets": {}
}

for dataset_name, folder in targets.items():
    shp_files = list(folder.rglob("*.shp"))

    inventory["datasets"][dataset_name] = {
        "folder": str(folder),
        "shapefile_count": len(shp_files),
        "shapefiles": []
    }

    for shp in shp_files:
        try:
            inventory["datasets"][dataset_name]["shapefiles"].append(inspect_shapefile(shp))
        except Exception as e:
            inventory["datasets"][dataset_name]["shapefiles"].append({
                "file": str(shp),
                "error": str(e)
            })

json_path = DOCS_DATA / "nfi-field-inventory.json"
md_path = DOCS_DATA / "nfi-field-inventory.md"

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)

lines = []
lines.append("# NFI3 / NFI4 欄位結構盤點")
lines.append("")
lines.append(f"產生時間：{inventory['generated_at']}")
lines.append("")
lines.append("## 一、資料定位")
lines.append("")
lines.append("本文件盤點第三次與第四次森林資源調查樣區 Shapefile 欄位結構，作為 Forest Harvest System 後續資料字典、資料表設計與資料匯入流程之依據。")
lines.append("")
lines.append("## 二、資料集摘要")
lines.append("")

for dataset_name, dataset in inventory["datasets"].items():
    lines.append(f"### {dataset_name}")
    lines.append("")
    lines.append(f"- 來源資料夾：`{dataset['folder']}`")
    lines.append(f"- Shapefile 數量：{dataset['shapefile_count']}")
    lines.append("")

    for shp in dataset["shapefiles"]:
        lines.append(f"#### {Path(shp['file']).name}")
        lines.append("")
        lines.append(f"- 完整路徑：`{shp['file']}`")

        if "error" in shp:
            lines.append(f"- 讀取錯誤：{shp['error']}")
            lines.append("")
            continue

        lines.append(f"- 幾何型態：{shp['shape_type']}")
        lines.append(f"- 筆數：{shp['record_count']}")
        lines.append(f"- 邊界範圍 bbox：{shp['bbox']}")
        lines.append("")
        lines.append("| 欄位名稱 | 型態 | 長度 | 小數位 |")
        lines.append("|---|---:|---:|---:|")

        for field in shp["fields"]:
            lines.append(f"| {field['name']} | {field['type']} | {field['size']} | {field['decimal']} |")

        lines.append("")

lines.append("## 三、初步判讀原則")
lines.append("")
lines.append("後續資料字典應依欄位用途分類為：")
lines.append("")
lines.append("1. 樣區基本資料欄位")
lines.append("2. 空間定位欄位")
lines.append("3. 林分與環境因子欄位")
lines.append("4. 樹種與樣木欄位")
lines.append("5. 材積、生長量與模式建構欄位")
lines.append("6. 調查期別與重測關聯欄位")
lines.append("")
lines.append("## 四、下一步")
lines.append("")
lines.append("1. 比對 NFI3 與 NFI4 欄位差異。")
lines.append("2. 建立 `nfi-data-dictionary.md`。")
lines.append("3. 設計 `plots`、`trees`、`species`、`volume_models`、`height_models` 資料表。")
lines.append("4. 建立 PostgreSQL / PostGIS 匯入流程。")

with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

with open(OBSIDIAN_NFI / "nfi-field-inventory.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(OBSIDIAN_NFI / "nfi-field-inventory.json", "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)

print("NFI 欄位盤點完成")
print(f"Markdown: {md_path}")
print(f"JSON: {json_path}")
print(f"Obsidian: {OBSIDIAN_NFI}")
