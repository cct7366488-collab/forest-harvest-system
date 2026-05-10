from pathlib import Path
from collections import defaultdict, Counter
import json
import shapefile

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
NFI_ROOT = PROJECT_ROOT / "data" / "raw" / "nfi"
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

ENCODINGS = ["cp950", "big5", "utf-8", "latin1"]

GROUP_FIELDS = ["樣點編號", "X_Coord", "Y_Coord"]

PLOT_ATTRIBUTE_KEYWORDS = [
    "dept", "user", "county", "town", "sample", "frame", "block",
    "x_coord", "y_coord", "coord", "樣點", "樣區", "樣區面積",
    "地形", "坡", "海拔", "土地", "林班", "小班"
]

STAND_ATTRIBUTE_KEYWORDS = [
    "stand", "forest", "landuse", "terrain", "age", "density",
    "maincover", "secondcov", "covdensity", "covheight",
    "height", "volumn", "volume", "crown", "林型", "林分",
    "覆蓋", "蓄積", "材積", "樹冠", "樣木數"
]

ADMIN_ATTRIBUTE_KEYWORDS = [
    "dept", "deptid", "deptname", "username", "user", "verify",
    "finished", "closing", "merge", "管理", "驗證", "檢核"
]

TREE_REQUIRED_KEYWORDS = [
    "dbh", "diameter", "胸徑", "胸高直徑", "樹種", "species",
    "tree_no", "treeno", "樣木號", "樣木編號"
]


def open_reader(shp_path: Path):
    last_error = None

    for enc in ENCODINGS:
        try:
            reader = shapefile.Reader(
                str(shp_path),
                encoding=enc,
                encodingErrors="replace"
            )
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


def contains_keyword(field_name, keywords):
    lower = field_name.lower()
    return any(keyword.lower() in lower for keyword in keywords)


def classify_field(field_name, group_vary_count, total_groups, non_empty_count, unique_count):
    if field_name in GROUP_FIELDS:
        return "plot_group_key"

    vary_ratio = group_vary_count / total_groups if total_groups else 0

    if contains_keyword(field_name, TREE_REQUIRED_KEYWORDS):
        if vary_ratio > 0:
            return "possible_tree_field_need_review"
        return "tree_keyword_but_constant_need_review"

    if contains_keyword(field_name, ADMIN_ATTRIBUTE_KEYWORDS):
        if group_vary_count == 0:
            return "admin_or_qaqc_plot_level"
        return "admin_or_qaqc_mixed"

    if contains_keyword(field_name, STAND_ATTRIBUTE_KEYWORDS):
        if group_vary_count == 0:
            return "likely_stand_attribute"
        return "stand_attribute_mixed_or_subrecord"

    if contains_keyword(field_name, PLOT_ATTRIBUTE_KEYWORDS):
        if group_vary_count == 0:
            return "likely_plot_attribute"
        return "plot_attribute_mixed_or_subrecord"

    if group_vary_count == 0 and non_empty_count > 0:
        return "constant_within_plot_group"

    if vary_ratio > 0:
        return "varies_within_plot_group"

    return "need_review"


def analyze():
    folder = NFI_ROOT / "nfi4"
    shp_files = list(folder.rglob("*.shp"))

    if not shp_files:
        raise FileNotFoundError("No NFI4 shapefile found")

    shp_path = shp_files[0]
    reader, encoding = open_reader(shp_path)

    fields = [field[0] for field in reader.fields[1:]]
    records = [record.as_dict() for record in reader.iterRecords()]

    groups = defaultdict(list)

    for record in records:
        groups[group_key(record)].append(record)

    total_records = len(records)
    total_groups = len(groups)

    reports = []

    for field in fields:
        all_values = [clean(record.get(field)) for record in records]
        non_empty_values = [value for value in all_values if value != ""]
        global_counter = Counter(non_empty_values)

        group_vary_count = 0
        group_non_empty_count = 0
        group_constant_values = Counter()
        example_values = []

        for key, group_records in groups.items():
            values = [clean(record.get(field)) for record in group_records]
            values = [value for value in values if value != ""]

            distinct_values = sorted(set(values))

            if values:
                group_non_empty_count += 1

            if len(distinct_values) == 1:
                group_constant_values[distinct_values[0]] += 1

            if len(distinct_values) > 1:
                group_vary_count += 1

            if len(example_values) < 8 and distinct_values:
                example_values.append(distinct_values[0])

        classification = classify_field(
            field,
            group_vary_count,
            total_groups,
            len(non_empty_values),
            len(global_counter)
        )

        reports.append({
            "field_name": field,
            "classification": classification,
            "total_records": total_records,
            "non_empty_count": len(non_empty_values),
            "empty_count": total_records - len(non_empty_values),
            "unique_count": len(global_counter),
            "group_non_empty_count": group_non_empty_count,
            "group_vary_count": group_vary_count,
            "group_vary_ratio": group_vary_count / total_groups if total_groups else 0,
            "top_values": global_counter.most_common(10),
            "top_group_constant_values": group_constant_values.most_common(10),
            "example_values": example_values[:8],
        })

    reports = sorted(
        reports,
        key=lambda item: (
            0 if item["classification"] in [
                "likely_stand_attribute",
                "likely_plot_attribute",
                "constant_within_plot_group",
                "admin_or_qaqc_plot_level"
            ] else 1,
            item["group_vary_count"],
            -item["non_empty_count"],
            item["field_name"]
        )
    )

    return {
        "purpose": "NFI4 plot / stand attributes analysis",
        "dataset": "NFI4",
        "file": str(shp_path),
        "encoding": encoding,
        "record_count": total_records,
        "plot_group_count": total_groups,
        "group_fields": GROUP_FIELDS,
        "field_reports": reports,
    }


result = analyze()

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-plot-stand-attributes-analysis.json"
md_path = DOCS_DATA / "nfi4-plot-stand-attributes-analysis.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-plot-stand-attributes-analysis.json").write_text(json_text, encoding="utf-8")

lines = []

lines.append("# NFI4 plot / stand attributes 判讀")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件用於判斷 NFI4 原始 Shapefile 中，哪些欄位較適合歸類為樣區層級或林分層級屬性，而不是直接轉入 `trees`。")
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
lines.append("## 三、可能的 plot / stand attributes")
lines.append("")
lines.append("| 欄位 | 分類 | 非空值 | 唯一值 | 群組內變動數 | 群組內變動比例 | 樣本值 |")
lines.append("|---|---|---:|---:|---:|---:|---|")

for report in result["field_reports"]:
    if report["classification"] in [
        "likely_stand_attribute",
        "likely_plot_attribute",
        "constant_within_plot_group",
        "admin_or_qaqc_plot_level",
        "plot_group_key"
    ]:
        samples = ", ".join(report["example_values"][:5])
        lines.append(
            f"| {report['field_name']} | {report['classification']} | "
            f"{report['non_empty_count']} | {report['unique_count']} | "
            f"{report['group_vary_count']} | {report['group_vary_ratio']:.3f} | {samples} |"
        )

lines.append("")
lines.append("## 四、在同一樣區群組內會變動的欄位")
lines.append("")
lines.append("這類欄位不一定是 trees，但代表它們不是單純 plot-level constant attributes。")
lines.append("")
lines.append("| 欄位 | 分類 | 非空值 | 唯一值 | 群組內變動數 | 群組內變動比例 |")
lines.append("|---|---|---:|---:|---:|---:|")

for report in result["field_reports"]:
    if report["group_vary_count"] > 0:
        lines.append(
            f"| {report['field_name']} | {report['classification']} | "
            f"{report['non_empty_count']} | {report['unique_count']} | "
            f"{report['group_vary_count']} | {report['group_vary_ratio']:.3f} |"
        )

lines.append("")
lines.append("## 五、初步資料工程判斷")
lines.append("")
lines.append("目前不應直接將 NFI4 subrecords 轉入 `trees`。")
lines.append("")
lines.append("較合理的方向是先建立正式的 plot / stand attribute table，例如：")
lines.append("")
lines.append("```text")
lines.append("nfi4_plot_attributes")
lines.append("```")
lines.append("")
lines.append("或：")
lines.append("")
lines.append("```text")
lines.append("nfi4_stand_attributes")
lines.append("```")
lines.append("")
lines.append("用於保存 Height、Volumn、Crown、林型、樣木數、樣區面積、覆蓋度等較像樣區或林分層級的資料。")
lines.append("")
lines.append("## 六、下一步")
lines.append("")
lines.append("1. 依本分析結果設計 `nfi4_plot_attributes` 資料表。")
lines.append("2. 從 `nfi4_subrecords` 聚合或抽取 plot / stand attributes。")
lines.append("3. 驗證每個 plot_code 是否可產生一筆或多筆 attributes。")
lines.append("4. trees 轉換暫停，直到確認 DBH、樹種、樣木號碼等欄位。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-plot-stand-attributes-analysis.md").write_text(md_text, encoding="utf-8")

print("NFI4 plot / stand attributes analysis completed")
print(f"Record count: {result['record_count']}")
print(f"Plot group count: {result['plot_group_count']}")
print()
print("Top likely plot / stand attributes:")
count = 0

for report in result["field_reports"]:
    if report["classification"] in [
        "likely_stand_attribute",
        "likely_plot_attribute",
        "constant_within_plot_group",
        "admin_or_qaqc_plot_level",
        "plot_group_key"
    ]:
        print(
            report["field_name"],
            "| class=", report["classification"],
            "| non_empty=", report["non_empty_count"],
            "| unique=", report["unique_count"],
            "| group_vary=", report["group_vary_count"],
            "| ratio=", round(report["group_vary_ratio"], 3)
        )
        count += 1
        if count >= 25:
            break

print()
print(json_path)
print(md_path)
