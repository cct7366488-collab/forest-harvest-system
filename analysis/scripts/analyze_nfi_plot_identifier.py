from pathlib import Path
from collections import Counter
import json
import shapefile

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

ENCODINGS = ["utf-8", "cp950", "big5", "latin1"]

def open_reader(shp_path):
    last_error = None
    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            return reader, enc
        except Exception as e:
            last_error = e
    raise RuntimeError("Cannot open shapefile: " + str(shp_path) + " / " + str(last_error))

def clean_value(value):
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in ["none", "nan", "null"]:
        return ""
    return text

def is_candidate_field(field_name):
    name = field_name.lower()
    keywords = [
        "id", "plot", "sample", "sampl", "block", "blk",
        "frame", "point", "coord", "x_", "y_", "xcoord", "ycoord",
        "county", "town", "dept", "林班", "樣", "號"
    ]
    return any(k in name for k in keywords)

def analyze_field(records, field_name):
    values = [clean_value(r.get(field_name)) for r in records]
    non_empty = [v for v in values if v != ""]
    counter = Counter(non_empty)
    duplicate_values = {k: v for k, v in counter.items() if v > 1}

    return {
        "field_name": field_name,
        "total_records": len(values),
        "non_empty_count": len(non_empty),
        "empty_count": len(values) - len(non_empty),
        "unique_count": len(counter),
        "duplicate_value_count": len(duplicate_values),
        "is_unique_if_non_empty": len(counter) == len(non_empty) and len(non_empty) > 0,
        "top_values": counter.most_common(10),
        "top_duplicates": sorted(duplicate_values.items(), key=lambda x: x[1], reverse=True)[:10],
    }

def analyze_shapefile(dataset_name, shp_path):
    reader, encoding = open_reader(shp_path)

    fields = [f[0] for f in reader.fields[1:]]
    records = [r.as_dict() for r in reader.iterRecords()]

    candidate_fields = [f for f in fields if is_candidate_field(f)]

    field_reports = []
    for field in candidate_fields:
        field_reports.append(analyze_field(records, field))

    field_reports = sorted(
        field_reports,
        key=lambda x: (
            not x["is_unique_if_non_empty"],
            -x["non_empty_count"],
            x["duplicate_value_count"],
            -x["unique_count"]
        )
    )

    return {
        "dataset": dataset_name,
        "file": str(shp_path),
        "encoding": encoding,
        "shape_type": reader.shapeTypeName,
        "record_count": len(records),
        "all_fields": fields,
        "candidate_fields": candidate_fields,
        "field_reports": field_reports
    }

result = {
    "purpose": "Analyze candidate unique plot identifiers for NFI3 / NFI4",
    "datasets": []
}

for folder_name in ["nfi3", "nfi4"]:
    dataset_name = folder_name.upper()
    folder = NFI_ROOT / folder_name

    for shp in folder.rglob("*.shp"):
        result["datasets"].append(analyze_shapefile(dataset_name, shp))

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi-plot-identifier-analysis.json"
md_path = DOCS_DATA / "nfi-plot-identifier-analysis.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi-plot-identifier-analysis.json").write_text(json_text, encoding="utf-8")

lines = []
lines.append("# NFI3 / NFI4 樣區唯一識別碼盤點")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件用於判斷 NFI3 / NFI4 Shapefile 中，哪些欄位適合作為 `plots.plot_code` 或 `plots.original_plot_id`。")
lines.append("")
lines.append("判斷重點包括：")
lines.append("")
lines.append("- 是否非空值")
lines.append("- 是否唯一")
lines.append("- 是否有重複值")
lines.append("- 是否可作為 NFI3 / NFI4 樣區重測比對基礎")
lines.append("")
lines.append("---")
lines.append("")

for dataset in result["datasets"]:
    lines.append(f"## {dataset['dataset']}")
    lines.append("")
    lines.append(f"- 檔案：`{dataset['file']}`")
    lines.append(f"- 編碼：{dataset['encoding']}")
    lines.append(f"- 幾何型態：{dataset['shape_type']}")
    lines.append(f"- 總筆數：{dataset['record_count']}")
    lines.append("")
    lines.append("### 候選欄位總覽")
    lines.append("")
    lines.append("| 欄位 | 非空值 | 空值 | 唯一值 | 重複值數 | 非空值是否唯一 |")
    lines.append("|---|---:|---:|---:|---:|---|")

    for report in dataset["field_reports"]:
        unique_text = "是" if report["is_unique_if_non_empty"] else "否"
        lines.append(
            f"| {report['field_name']} | {report['non_empty_count']} | {report['empty_count']} | "
            f"{report['unique_count']} | {report['duplicate_value_count']} | {unique_text} |"
        )

    lines.append("")
    lines.append("### 前 10 個候選欄位詳細樣本")
    lines.append("")

    for report in dataset["field_reports"][:10]:
        lines.append(f"#### {report['field_name']}")
        lines.append("")
        lines.append(f"- 非空值：{report['non_empty_count']}")
        lines.append(f"- 空值：{report['empty_count']}")
        lines.append(f"- 唯一值：{report['unique_count']}")
        lines.append(f"- 重複值數：{report['duplicate_value_count']}")
        lines.append(f"- 非空值是否唯一：{'是' if report['is_unique_if_non_empty'] else '否'}")
        lines.append("")
        lines.append("常見值：")
        lines.append("")
        for value, count in report["top_values"]:
            lines.append(f"- `{value}`：{count}")

        if report["top_duplicates"]:
            lines.append("")
            lines.append("重複值：")
            lines.append("")
            for value, count in report["top_duplicates"]:
                lines.append(f"- `{value}`：{count}")

        lines.append("")

    lines.append("---")
    lines.append("")

lines.append("## 二、後續判斷原則")
lines.append("")
lines.append("1. 若有非空且唯一的欄位，優先作為 `original_plot_id`。")
lines.append("2. `plot_code` 建議加上調查期別前綴，例如 `NFI4-xxxxx`。")
lines.append("3. 若單一欄位不唯一，應考慮組合欄位，例如 `SampleID + BlockID + X_Coord + Y_Coord`。")
lines.append("4. NFI3 / NFI4 是否可重測比對，需另行確認是否存在共同樣區識別碼或空間鄰近關係。")
lines.append("")
lines.append("## 三、下一步")
lines.append("")
lines.append("1. 依本報告選定 NFI3 / NFI4 的正式唯一識別欄位。")
lines.append("2. 修正 `nfi-field-mapping.json`。")
lines.append("3. 修正 `import_nfi_plots_sample.py`。")
lines.append("4. 清除前一次 NFI 測試匯入資料。")
lines.append("5. 重新匯入 NFI3 / NFI4 各 5 筆測試資料。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi-plot-identifier-analysis.md").write_text(md_text, encoding="utf-8")

print("NFI plot identifier analysis completed")
print(json_path)
print(md_path)
print(OBSIDIAN_NFI / "nfi-plot-identifier-analysis.md")
