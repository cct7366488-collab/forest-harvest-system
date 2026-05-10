from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

inventory_path = DOCS_DATA / "nfi-field-inventory.json"
dictionary_json_path = DOCS_DATA / "nfi-data-dictionary.json"
dictionary_md_path = DOCS_DATA / "nfi-data-dictionary.md"

if not inventory_path.exists():
    raise FileNotFoundError(f"找不到欄位盤點檔案：{inventory_path}")

with open(inventory_path, "r", encoding="utf-8") as f:
    inventory = json.load(f)

def infer_chinese_name(field_name: str) -> str:
    name = field_name.lower()

    mapping = {
        "plot": "樣區編號或樣區識別欄位",
        "id": "識別碼",
        "no": "編號",
        "code": "代碼",
        "x": "X 座標",
        "y": "Y 座標",
        "lon": "經度",
        "lng": "經度",
        "lat": "緯度",
        "elev": "海拔",
        "alt": "海拔",
        "slope": "坡度",
        "aspect": "坡向",
        "species": "樹種",
        "sp": "樹種或樣區起始點欄位",
        "dbh": "胸高直徑",
        "diam": "直徑",
        "height": "樹高",
        "h": "高度",
        "volume": "材積",
        "vol": "材積",
        "area": "面積",
        "forest": "森林或林型",
        "type": "類型",
        "date": "調查日期",
        "year": "年度",
        "cycle": "調查期別",
        "county": "縣市",
        "town": "鄉鎮",
        "comp": "林班或小班",
        "land": "土地利用或地類",
    }

    for key, value in mapping.items():
        if key in name:
            return value

    return "待判讀"

def infer_category(field_name: str) -> str:
    name = field_name.lower()

    if any(k in name for k in ["plot", "id", "no", "code"]):
        return "識別與編碼欄位"
    if any(k in name for k in ["x", "y", "lon", "lng", "lat", "coord", "twd", "tm2"]):
        return "空間定位欄位"
    if any(k in name for k in ["elev", "alt", "slope", "aspect", "land", "forest", "type"]):
        return "環境與林分欄位"
    if any(k in name for k in ["species", "sp", "dbh", "diam", "height", "tree", "vol", "volume"]):
        return "樣木與林木量測欄位"
    if any(k in name for k in ["date", "year", "cycle", "time"]):
        return "調查時間欄位"

    return "待分類欄位"

def infer_sql_type(field_type: str, size: int, decimal: int) -> str:
    if field_type == "C":
        return f"VARCHAR({size})"
    if field_type == "N":
        if decimal and decimal > 0:
            return "NUMERIC"
        if size <= 9:
            return "INTEGER"
        return "BIGINT"
    if field_type == "F":
        return "DOUBLE PRECISION"
    if field_type == "D":
        return "DATE"
    if field_type == "L":
        return "BOOLEAN"
    return "TEXT"

def infer_target_table(field_name: str) -> str:
    category = infer_category(field_name)

    if category == "識別與編碼欄位":
        return "plots / nfi_cycles / species"
    if category == "空間定位欄位":
        return "plots"
    if category == "環境與林分欄位":
        return "plots"
    if category == "樣木與林木量測欄位":
        return "trees / species / volume_models / height_models"
    if category == "調查時間欄位":
        return "nfi_cycles / plots"

    return "待判定"

field_index = {}

for dataset_name, dataset in inventory.get("datasets", {}).items():
    for shp in dataset.get("shapefiles", []):
        if "error" in shp:
            continue

        shp_name = Path(shp["file"]).name

        for field in shp.get("fields", []):
            field_name = field["name"]

            if field_name not in field_index:
                field_index[field_name] = {
                    "field_name": field_name,
                    "chinese_name": infer_chinese_name(field_name),
                    "category": infer_category(field_name),
                    "source_datasets": [],
                    "source_files": [],
                    "shapefile_type": shp.get("shape_type", ""),
                    "field_type": field["type"],
                    "field_size": field["size"],
                    "decimal": field["decimal"],
                    "suggested_sql_type": infer_sql_type(field["type"], field["size"], field["decimal"]),
                    "unit": "待確認",
                    "required": "待確認",
                    "target_table": infer_target_table(field_name),
                    "notes": "由欄位盤點自動產生，需依原始資料表與專業判讀進一步確認。"
                }

            if dataset_name not in field_index[field_name]["source_datasets"]:
                field_index[field_name]["source_datasets"].append(dataset_name)

            if shp_name not in field_index[field_name]["source_files"]:
                field_index[field_name]["source_files"].append(shp_name)

dictionary = {
    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source": str(inventory_path),
    "description": "NFI3 / NFI4 欄位資料字典初版，依 Shapefile 欄位結構自動產生，供 Forest Harvest System 資料庫設計使用。",
    "fields": list(field_index.values())
}

with open(dictionary_json_path, "w", encoding="utf-8") as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)

lines = []
lines.append("# NFI3 / NFI4 資料字典")
lines.append("")
lines.append(f"產生時間：{dictionary['generated_at']}")
lines.append("")
lines.append("## 一、文件目的")
lines.append("")
lines.append("本文件依據 NFI3 與 NFI4 森林資源調查樣區 Shapefile 欄位結構，自動建立資料字典初版。")
lines.append("")
lines.append("本資料字典將作為 Forest Harvest System 後續資料庫設計、資料匯入、欄位對應與模型建構之基礎。")
lines.append("")
lines.append("## 二、資料表設計用途")
lines.append("")
lines.append("本資料字典將支援下列資料表設計：")
lines.append("")
lines.append("- `plots`：樣區基本資料表")
lines.append("- `trees`：樣木資料表")
lines.append("- `species`：樹種代碼表")
lines.append("- `volume_models`：立木材積式資料表")
lines.append("- `height_models`：樹高曲線式資料表")
lines.append("- `nfi_cycles`：森林資源調查期別表")
lines.append("- `nfi_plot_remeasurement`：樣區重測關聯表")
lines.append("")
lines.append("## 三、欄位資料字典")
lines.append("")
lines.append("| 欄位名稱 | 中文意義 | 分類 | 來源資料 | Shapefile 型態 | SQL 建議型態 | 單位 | 對應資料表 | 備註 |")
lines.append("|---|---|---|---|---|---|---|---|---|")

for item in dictionary["fields"]:
    source = ", ".join(item["source_datasets"])
    lines.append(
        f"| {item['field_name']} | {item['chinese_name']} | {item['category']} | {source} | "
        f"{item['field_type']}({item['field_size']},{item['decimal']}) | {item['suggested_sql_type']} | "
        f"{item['unit']} | {item['target_table']} | {item['notes']} |"
    )

lines.append("")
lines.append("## 四、欄位分類說明")
lines.append("")
lines.append("### 1. 識別與編碼欄位")
lines.append("")
lines.append("包含樣區代碼、調查期別代碼、樹種代碼、資料識別碼等。")
lines.append("")
lines.append("### 2. 空間定位欄位")
lines.append("")
lines.append("包含座標、經緯度、TWD97 / TM2 座標、幾何資訊等。")
lines.append("")
lines.append("### 3. 環境與林分欄位")
lines.append("")
lines.append("包含海拔、坡度、坡向、土地利用、林型、林分狀態等。")
lines.append("")
lines.append("### 4. 樣木與林木量測欄位")
lines.append("")
lines.append("包含樹種、胸徑、樹高、枝下高、材積、生長量等。")
lines.append("")
lines.append("### 5. 調查時間欄位")
lines.append("")
lines.append("包含調查日期、年度、調查期別等。")
lines.append("")
lines.append("## 五、下一步")
lines.append("")
lines.append("1. 人工檢核欄位中文意義。")
lines.append("2. 比對 NFI3 與 NFI4 欄位是否可建立重測關聯。")
lines.append("3. 設計正式 PostgreSQL / PostGIS 資料表。")
lines.append("4. 建立資料匯入 ETL 腳本。")
lines.append("5. 建立立木材積式與樹高曲線式資料表。")

with open(dictionary_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

with open(OBSIDIAN_NFI / "nfi-data-dictionary.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open(OBSIDIAN_NFI / "nfi-data-dictionary.json", "w", encoding="utf-8") as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=2)

print("NFI 資料字典建立完成")
print(f"Markdown: {dictionary_md_path}")
print(f"JSON: {dictionary_json_path}")
print(f"Obsidian: {OBSIDIAN_NFI}")
print(f"欄位數量：{len(dictionary['fields'])}")
