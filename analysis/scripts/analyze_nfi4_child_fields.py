from pathlib import Path
from collections import defaultdict, Counter
import json
import shapefile

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

ENCODINGS = ["utf-8", "cp950", "big5", "latin1"]

GROUP_FIELDS = ["樣點編號", "X_Coord", "Y_Coord"]

TREE_KEYWORDS = [
    "tree", "slave", "height", "vol", "volumn", "volume", "crown",
    "dbh", "diam", "stype", "type", "closing",
    "樣木", "樹", "胸", "徑", "高", "材積", "冠", "枝"
]

PLOT_KEYWORDS = [
    "dept", "x_coord", "y_coord", "樣點", "林型", "樣區", "landuse",
    "altitude", "slope", "aspect", "county", "town"
]


def open_reader(shp_path):
    last_error = None

    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(str(shp_path), encoding=enc)
            _ = reader.fields
            return reader, enc
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Cannot open shapefile: {shp_path}. Last error: {last_error}")


def clean(value):
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in ["none", "nan", "null"]:
        return ""
    return text


def group_key(record):
    return "|".join(clean(record.get(field)) for field in GROUP_FIELDS)


def has_keyword(field_name, keywords):
    name = field_name.lower()
    return any(keyword.lower() in name for keyword in keywords)


def classify_field(field_name, group_vary_ratio, non_empty_count, unique_count):
    if field_name in GROUP_FIELDS:
        return "plot_group_key"

    tree_keyword = has_keyword(field_name, TREE_KEYWORDS)
    plot_keyword = has_keyword(field_name, PLOT_KEYWORDS)

    if group_vary_ratio >= 0.20 and tree_keyword:
        return "likely_tree_or_child_record_field"

    if group_vary_ratio >= 0.20:
        return "likely_child_record_field"

    if group_vary_ratio == 0 and plot_keyword:
        return "likely_plot_level_field"

    if group_vary_ratio == 0:
        return "constant_within_plot_group"

    return "mixed_or_need_review"


def analyze_nfi4():
    nfi4_folder = NFI_ROOT / "nfi4"
    shp_files = list(nfi4_folder.rglob("*.shp"))

    if not shp_files:
        raise FileNotFoundError("找不到 NFI4 Shapefile")

    shp_path = shp_files[0]
    reader, encoding = open_reader(shp_path)

    fields = [f[0] for f in reader.fields[1:]]
    records = [record.as_dict() for record in reader.iterRecords()]

    groups = defaultdict(list)

    for record in records:
        key = group_key(record)
        groups[key].append(record)

    total_records = len(records)
    total_groups = len(groups)

    field_reports = []

    for field in fields:
        values = [clean(record.get(field)) for record in records]
        non_empty_values = [value for value in values if value != ""]
        global_counter = Counter(non_empty_values)

        group_vary_count = 0
        group_non_empty_count = 0
        group_distinct_examples = []

        for key, group_records in groups.items():
            group_values = [clean(record.get(field)) for record in group_records]
            group_values = [value for value in group_values if value != ""]

            if group_values:
                group_non_empty_count += 1

            distinct_values = sorted(set(group_values))

            if len(distinct_values) > 1:
                group_vary_count += 1

                if len(group_distinct_examples) < 5:
                    group_distinct_examples.append({
                        "group_key": key,
                        "distinct_values": distinct_values[:10],
                        "distinct_count": len(distinct_values)
                    })

        group_vary_ratio = group_vary_count / total_groups if total_groups > 0 else 0

        report = {
            "field_name": field,
            "total_records": total_records,
            "non_empty_count": len(non_empty_values),
            "empty_count": total_records - len(non_empty_values),
            "unique_count": len(global_counter),
            "group_non_empty_count": group_non_empty_count,
            "group_vary_count": group_vary_count,
            "group_vary_ratio": group_vary_ratio,
            "top_values": global_counter.most_common(10),
            "group_distinct_examples": group_distinct_examples,
            "classification": classify_field(field, group_vary_ratio, len(non_empty_values), len(global_counter))
        }

        field_reports.append(report)

    field_reports = sorted(
        field_reports,
        key=lambda item: (
            0 if item["classification"] == "likely_tree_or_child_record_field" else 1,
            -item["group_vary_count"],
            -item["unique_count"],
            item["field_name"]
        )
    )

    return {
        "dataset": "NFI4",
        "file": str(shp_path),
        "encoding": encoding,
        "record_count": total_records,
        "plot_group_count": total_groups,
        "group_fields": GROUP_FIELDS,
        "field_reports": field_reports
    }


result = analyze_nfi4()

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-child-field-analysis.json"
md_path = DOCS_DATA / "nfi4-child-field-analysis.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-child-field-analysis.json").write_text(json_text, encoding="utf-8")

lines = []

lines.append("# NFI4 子紀錄 / 樣木層級欄位分析")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件用於判斷 NFI4 原始 Shapefile 中，哪些欄位屬於樣區層級，哪些欄位可能屬於樣木或子紀錄層級。")
lines.append("")
lines.append("分析方式：")
lines.append("")
lines.append("- 先依 `樣點編號 + X_Coord + Y_Coord` 建立樣區群組。")
lines.append("- 若某欄位在同一樣區群組內會變動，表示它可能是子紀錄層級欄位。")
lines.append("- 若某欄位在同一樣區群組內固定不變，表示它較可能是樣區層級欄位。")
lines.append("")
lines.append("## 二、資料摘要")
lines.append("")
lines.append(f"- 資料集：{result['dataset']}")
lines.append(f"- 檔案：`{result['file']}`")
lines.append(f"- 編碼：{result['encoding']}")
lines.append(f"- 原始紀錄筆數：{result['record_count']}")
lines.append(f"- 樣區群組數：{result['plot_group_count']}")
lines.append(f"- 群組欄位：{', '.join(result['group_fields'])}")
lines.append("")
lines.append("## 三、最可能屬於樣木 / 子紀錄層級的欄位")
lines.append("")
lines.append("| 欄位 | 分類 | 非空值 | 唯一值 | 變動群組數 | 群組內變動比例 |")
lines.append("|---|---|---:|---:|---:|---:|")

for report in result["field_reports"]:
    if report["classification"] in ["likely_tree_or_child_record_field", "likely_child_record_field"]:
        lines.append(
            f"| {report['field_name']} | {report['classification']} | "
            f"{report['non_empty_count']} | {report['unique_count']} | "
            f"{report['group_vary_count']} | {report['group_vary_ratio']:.3f} |"
        )

lines.append("")
lines.append("## 四、可能屬於樣區層級的欄位")
lines.append("")
lines.append("| 欄位 | 分類 | 非空值 | 唯一值 | 變動群組數 |")
lines.append("|---|---|---:|---:|---:|")

for report in result["field_reports"]:
    if report["classification"] in ["likely_plot_level_field", "constant_within_plot_group", "plot_group_key"]:
        lines.append(
            f"| {report['field_name']} | {report['classification']} | "
            f"{report['non_empty_count']} | {report['unique_count']} | "
            f"{report['group_vary_count']} |"
        )

lines.append("")
lines.append("## 五、全部欄位總表")
lines.append("")
lines.append("| 欄位 | 分類 | 非空值 | 空值 | 唯一值 | 群組內變動數 |")
lines.append("|---|---|---:|---:|---:|---:|")

for report in result["field_reports"]:
    lines.append(
        f"| {report['field_name']} | {report['classification']} | "
        f"{report['non_empty_count']} | {report['empty_count']} | "
        f"{report['unique_count']} | {report['group_vary_count']} |"
    )

lines.append("")
lines.append("## 六、初步判讀")
lines.append("")
lines.append("若 `Height`、`Volumn`、`Crown`、`SlaveTreeI` 等欄位在同一樣區群組內變動，則可視為 trees 或子紀錄層級候選欄位。")
lines.append("")
lines.append("下一步應根據本分析結果建立 `NFI4 → trees` 欄位對應表，並測試少量樣木資料匯入。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-child-field-analysis.md").write_text(md_text, encoding="utf-8")

print("NFI4 child field analysis completed")
print(json_path)
print(md_path)
print(OBSIDIAN_NFI / "nfi4-child-field-analysis.md")
print()
print("Summary")
print("records:", result["record_count"])
print("plot groups:", result["plot_group_count"])
print()
print("Top likely child/tree fields:")

count = 0
for report in result["field_reports"]:
    if report["classification"] in ["likely_tree_or_child_record_field", "likely_child_record_field"]:
        print(
            report["field_name"],
            "class=", report["classification"],
            "non_empty=", report["non_empty_count"],
            "unique=", report["unique_count"],
            "group_vary=", report["group_vary_count"],
            "ratio=", round(report["group_vary_ratio"], 3)
        )
        count += 1
        if count >= 20:
            break
