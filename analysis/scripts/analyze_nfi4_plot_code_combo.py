from pathlib import Path
from collections import Counter
import shapefile
import json

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

ENCODINGS = ["utf-8", "cp950", "big5", "latin1"]

def open_reader(shp_path):
    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            return reader, enc
        except Exception:
            pass
    raise RuntimeError("Cannot open shapefile")

def clean(v):
    if v is None:
        return ""
    return str(v).strip()

def combo_key(record, fields):
    return "|".join(clean(record.get(f)) for f in fields)

def analyze_combo(records, fields):
    keys = [combo_key(r, fields) for r in records]
    counter = Counter(keys)
    duplicates = {k: v for k, v in counter.items() if v > 1}
    return {
        "fields": fields,
        "total_records": len(keys),
        "unique_count": len(counter),
        "duplicate_key_count": len(duplicates),
        "max_duplicate_count": max(duplicates.values()) if duplicates else 0,
        "is_unique": len(counter) == len(keys),
        "top_duplicates": sorted(duplicates.items(), key=lambda x: x[1], reverse=True)[:10],
    }

nfi4_folder = NFI_ROOT / "nfi4"
shp_files = list(nfi4_folder.rglob("*.shp"))

if not shp_files:
    raise FileNotFoundError("找不到 NFI4 shp")

shp = shp_files[0]
reader, encoding = open_reader(shp)

fields = [f[0] for f in reader.fields[1:]]
records = [r.as_dict() for r in reader.iterRecords()]

candidate_combos = [
    ["樣點編號"],
    ["X_Coord", "Y_Coord"],
    ["樣點編號", "X_Coord", "Y_Coord"],
    ["DeptID", "樣點編號"],
    ["DeptID", "樣點編號", "X_Coord", "Y_Coord"],
    ["DeptName", "樣點編號", "X_Coord", "Y_Coord"],
    ["BlkID", "樣點編號"],
    ["BlkID_1", "樣點編號"],
    ["SampleID1", "樣點編號"],
    ["SampleID01", "樣點編號"],
    ["FrameID_1", "樣點編號"],
    ["BlockID_1", "樣點編號"],
    ["DeptID_1", "樣點編號", "X_Coord", "Y_Coord"],
]

existing_combos = []
for combo in candidate_combos:
    if all(f in fields for f in combo):
        existing_combos.append(combo)

reports = [analyze_combo(records, combo) for combo in existing_combos]

result = {
    "dataset": "NFI4",
    "file": str(shp),
    "encoding": encoding,
    "record_count": len(records),
    "available_fields": fields,
    "combo_reports": reports
}

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-plot-code-combo-analysis.json"
md_path = DOCS_DATA / "nfi4-plot-code-combo-analysis.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-plot-code-combo-analysis.json").write_text(json_text, encoding="utf-8")

lines = []
lines.append("# NFI4 plot_code 組合欄位分析")
lines.append("")
lines.append(f"- 檔案：`{shp}`")
lines.append(f"- 編碼：{encoding}")
lines.append(f"- 總筆數：{len(records)}")
lines.append("")
lines.append("## 組合欄位唯一性分析")
lines.append("")
lines.append("| 組合欄位 | 唯一值數 | 重複 key 數 | 最大重複次數 | 是否逐筆唯一 |")
lines.append("|---|---:|---:|---:|---|")

for r in reports:
    lines.append(
        "| " + " + ".join(r["fields"]) +
        f" | {r['unique_count']} | {r['duplicate_key_count']} | {r['max_duplicate_count']} | {r['is_unique']} |"
    )

lines.append("")
lines.append("## 初步解讀")
lines.append("")
lines.append("若某組合的唯一值數遠小於總筆數，表示 NFI4 可能為樣木或子紀錄層級，而非純樣區層級。")
lines.append("")
lines.append("若 X_Coord + Y_Coord 的唯一值數接近樣區數，則可作為樣區位置分組依據。")
lines.append("")
lines.append("下一步應依分析結果決定 NFI4 匯入 plots 時是否採用座標群組或組合欄位。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-plot-code-combo-analysis.md").write_text(md_text, encoding="utf-8")

print("NFI4 combo analysis completed")
print(json_path)
print(md_path)
print()
print("Summary:")
for r in reports:
    print(
        " + ".join(r["fields"]),
        "unique=", r["unique_count"],
        "dup_keys=", r["duplicate_key_count"],
        "max_dup=", r["max_duplicate_count"],
        "is_unique=", r["is_unique"]
    )
