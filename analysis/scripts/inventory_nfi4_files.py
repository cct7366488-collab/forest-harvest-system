from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI4_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi" / "nfi4"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

TARGET_EXTENSIONS = [
    ".shp", ".shx", ".dbf", ".prj", ".cpg",
    ".csv", ".txt", ".xlsx", ".xls",
    ".mdb", ".accdb",
    ".gpkg", ".geojson", ".json",
    ".zip", ".7z"
]

def classify_file(path: Path):
    suffix = path.suffix.lower()
    name = path.name.lower()

    if suffix == ".shp":
        return "GIS Shapefile geometry"
    if suffix == ".dbf":
        return "Shapefile attribute table / DBF table"
    if suffix in [".xlsx", ".xls"]:
        return "Excel table"
    if suffix in [".csv", ".txt"]:
        return "Delimited text table"
    if suffix in [".mdb", ".accdb"]:
        return "Access database"
    if suffix == ".gpkg":
        return "GeoPackage"
    if suffix in [".geojson", ".json"]:
        return "JSON / GeoJSON"
    if suffix in [".zip", ".7z"]:
        return "Compressed archive"
    if suffix in [".shx", ".prj", ".cpg"]:
        return "Shapefile support file"

    return "Other"

def possible_role(path: Path):
    text = path.name.lower()

    tree_keywords = [
        "tree", "trees", "sampletree", "stem", "dbh",
        "樣木", "立木", "單木", "樹木", "胸徑"
    ]

    plot_keywords = [
        "plot", "sample", "inventory", "forest", "stand",
        "樣區", "樣點", "林分", "森林"
    ]

    model_keywords = [
        "volume", "height", "model", "材積", "樹高", "模式"
    ]

    if any(k in text for k in tree_keywords):
        return "可能是樣木 / 單木資料"
    if any(k in text for k in model_keywords):
        return "可能是材積式 / 樹高式 / 模型資料"
    if any(k in text for k in plot_keywords):
        return "可能是樣區 / 林分資料"

    return "待判讀"

files = []

for path in NFI4_ROOT.rglob("*"):
    if path.is_file():
        suffix = path.suffix.lower()

        item = {
            "name": path.name,
            "relative_path": str(path.relative_to(PROJECT_ROOT)),
            "full_path": str(path),
            "extension": suffix,
            "size_bytes": path.stat().st_size,
            "size_mb": round(path.stat().st_size / 1024 / 1024, 3),
            "modified_time": datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "file_type": classify_file(path),
            "possible_role": possible_role(path),
            "is_target_extension": suffix in TARGET_EXTENSIONS
        }

        files.append(item)

files = sorted(files, key=lambda x: (x["extension"], x["relative_path"]))

summary_by_extension = {}

for item in files:
    ext = item["extension"] if item["extension"] else "(no extension)"
    summary_by_extension.setdefault(ext, {"count": 0, "total_size_mb": 0})
    summary_by_extension[ext]["count"] += 1
    summary_by_extension[ext]["total_size_mb"] += item["size_mb"]

for ext in summary_by_extension:
    summary_by_extension[ext]["total_size_mb"] = round(summary_by_extension[ext]["total_size_mb"], 3)

result = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "nfi4_root": str(NFI4_ROOT),
    "file_count": len(files),
    "summary_by_extension": summary_by_extension,
    "files": files
}

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-file-structure-inventory.json"
md_path = DOCS_DATA / "nfi4-file-structure-inventory.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-file-structure-inventory.json").write_text(json_text, encoding="utf-8")

lines = []
lines.append("# NFI4 檔案結構總盤點")
lines.append("")
lines.append(f"產生時間：{result['generated_at']}")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件盤點第四次森林資源調查 NFI4 原始資料夾中的所有檔案，用於判斷是否存在獨立的樣木資料表、樣區資料表、屬性資料表或模型資料。")
lines.append("")
lines.append("目前已知 NFI4 Shapefile 比較像樣區 / 林分屬性資料，尚未確認真正樣木層級資料是否存在於其他檔案。")
lines.append("")
lines.append("## 二、資料夾位置")
lines.append("")
lines.append(f"`{result['nfi4_root']}`")
lines.append("")
lines.append("## 三、副檔名統計")
lines.append("")
lines.append("| 副檔名 | 檔案數 | 總大小 MB |")
lines.append("|---|---:|---:|")

for ext, stat in sorted(summary_by_extension.items()):
    lines.append(f"| {ext} | {stat['count']} | {stat['total_size_mb']} |")

lines.append("")
lines.append("## 四、檔案清單")
lines.append("")
lines.append("| 檔名 | 副檔名 | 大小 MB | 類型判斷 | 可能角色 | 相對路徑 |")
lines.append("|---|---|---:|---|---|---|")

for item in files:
    lines.append(
        f"| {item['name']} | {item['extension']} | {item['size_mb']} | "
        f"{item['file_type']} | {item['possible_role']} | `{item['relative_path']}` |"
    )

lines.append("")
lines.append("## 五、初步判讀原則")
lines.append("")
lines.append("1. 若只存在一組 Shapefile，則目前 NFI4 原始檔可能只提供樣區 / 林分層級資料。")
lines.append("2. 若存在 Excel、CSV、MDB、Access 等表格，需優先檢查是否為樣木層級資料。")
lines.append("3. 若存在多個 DBF，需判斷 DBF 是否只屬於 Shapefile 附屬檔，或是獨立屬性表。")
lines.append("4. 若找不到 DBH、樹種、樣木號等欄位，則不應直接建立 NFI4 trees ETL。")
lines.append("")
lines.append("## 六、下一步")
lines.append("")
lines.append("1. 檢視本盤點結果。")
lines.append("2. 若發現疑似樣木表，進一步做欄位盤點。")
lines.append("3. 若沒有疑似樣木表，則正式將 NFI4 定位為樣區 / 林分屬性資料來源。")
lines.append("4. 依結果決定是否建立 nfi4_inventory_details 或 nfi4_stand_attributes。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-file-structure-inventory.md").write_text(md_text, encoding="utf-8")

print("NFI4 file structure inventory completed")
print("File count:", len(files))
print()
print("Summary by extension:")
for ext, stat in sorted(summary_by_extension.items()):
    print(f"  {ext}: count={stat['count']}, size_mb={stat['total_size_mb']}")
print()
print("Files:")
for item in files:
    print(f"  {item['extension']:8s} {item['size_mb']:10.3f} MB  {item['possible_role']}  {item['relative_path']}")

print()
print(json_path)
print(md_path)
