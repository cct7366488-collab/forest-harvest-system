from pathlib import Path
from collections import Counter, defaultdict
import json
import psycopg2

PROJECT_ROOT = Path(r"C:\Projects\forest-harvest-system")
DOCS_DATA = PROJECT_ROOT / "docs" / "data"
OBSIDIAN_NFI = Path(r"C:\ObsidianVaults\ForestHarvestSystem\database\nfi")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "forest_db",
    "user": "forest_user",
    "password": "forest_password",
}

TREE_CANDIDATE_KEYWORDS = {
    "tree_no": ["tree_no", "treeno", "treeid", "tree_id", "樣木號", "樣木編號", "立木號"],
    "species_code": ["species_code", "spcode", "sp_code", "樹種代碼", "樹種碼"],
    "species_name": ["species", "spname", "sp_name", "樹種", "樹種名稱"],
    "dbh_cm": ["dbh", "diameter", "diam", "胸徑", "胸高直徑"],
    "height_m": ["height", "樹高"],
    "clear_bole_height_m": ["clear", "bole", "枝下高"],
    "crown_class": ["crown", "樹冠", "冠"],
    "estimated_volume_m3": ["volumn", "volume", "材積"],
}


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def load_records():
    conn = psycopg2.connect(**DB_CONFIG)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, plot_id, plot_code, sample_id, record_index, raw_attributes
                FROM nfi4_subrecords
                ORDER BY id
                """
            )
            rows = cur.fetchall()
    finally:
        conn.close()

    records = []

    for row in rows:
        raw = row[5]

        if isinstance(raw, str):
            raw = json.loads(raw)

        records.append({
            "id": row[0],
            "plot_id": row[1],
            "plot_code": row[2],
            "sample_id": row[3],
            "record_index": row[4],
            "raw_attributes": raw or {},
        })

    return records


def is_numeric(value):
    try:
        if clean(value) == "":
            return False
        float(value)
        return True
    except Exception:
        return False


def analyze_fields(records):
    field_counter = Counter()
    non_empty_counter = Counter()
    numeric_counter = Counter()
    unique_values = defaultdict(set)
    sample_values = defaultdict(list)

    for record in records:
        raw = record["raw_attributes"]

        for key, value in raw.items():
            field_counter[key] += 1

            text = clean(value)

            if text != "":
                non_empty_counter[key] += 1
                unique_values[key].add(text)

                if is_numeric(text):
                    numeric_counter[key] += 1

                if len(sample_values[key]) < 10:
                    sample_values[key].append(text)

    reports = []

    for key in sorted(field_counter.keys()):
        reports.append({
            "field_name": key,
            "appears_in_records": field_counter[key],
            "non_empty_count": non_empty_counter[key],
            "unique_count": len(unique_values[key]),
            "numeric_count": numeric_counter[key],
            "sample_values": sample_values[key],
        })

    reports = sorted(
        reports,
        key=lambda item: (
            -item["non_empty_count"],
            -item["unique_count"],
            item["field_name"]
        )
    )

    return reports


def match_candidates(reports):
    available_fields = [item["field_name"] for item in reports]
    matches = {}

    for trees_field, keywords in TREE_CANDIDATE_KEYWORDS.items():
        found = []

        for field in available_fields:
            lower_field = field.lower()

            for keyword in keywords:
                if keyword.lower() in lower_field:
                    found.append(field)
                    break

        matches[trees_field] = found

    return matches


records = load_records()
reports = analyze_fields(records)
candidate_matches = match_candidates(reports)

plot_counts = Counter(record["plot_code"] for record in records)

decision = {
    "can_convert_directly_to_trees_now": False,
    "reason": [
        "目前 staging 樣本已擴大，但仍需確認是否存在 DBH / 胸徑、樹種代碼、樹種名稱、樣木號碼等核心欄位。",
        "若 DBH 與樹種欄位仍缺失，則不應直接轉入 trees。",
        "Height、Volumn、Crown 可作為候選欄位，但不足以單獨構成正式樣木資料。",
    ],
}

result = {
    "purpose": "Expanded NFI4 subrecords field completeness analysis",
    "source_table": "nfi4_subrecords",
    "sample_count": len(records),
    "plot_counts": dict(plot_counts),
    "field_reports": reports,
    "tree_candidate_matches": candidate_matches,
    "decision": decision,
}

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-subrecords-expanded-analysis.json"
md_path = DOCS_DATA / "nfi4-subrecords-expanded-analysis.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-subrecords-expanded-analysis.json").write_text(json_text, encoding="utf-8")

lines = []

lines.append("# NFI4 subrecords 擴大樣本與欄位完整性分析")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件分析已匯入 `nfi4_subrecords` staging table 的擴大樣本，用於判斷是否具備轉入 `trees` 的欄位條件。")
lines.append("")
lines.append("## 二、樣本狀態")
lines.append("")
lines.append(f"- nfi4_subrecords 樣本筆數：{len(records)}")
lines.append("")
lines.append("### 各 plot_code 子紀錄筆數")
lines.append("")
lines.append("| plot_code | 子紀錄筆數 |")
lines.append("|---|---:|")

for plot_code, count in sorted(plot_counts.items()):
    lines.append(f"| {plot_code} | {count} |")

lines.append("")
lines.append("## 三、疑似 trees 欄位候選")
lines.append("")
lines.append("| trees 欄位 | 找到的 raw_attributes 候選欄位 |")
lines.append("|---|---|")

for trees_field, found in candidate_matches.items():
    value = ", ".join(found) if found else "未找到"
    lines.append(f"| {trees_field} | {value} |")

lines.append("")
lines.append("## 四、raw_attributes 欄位完整性")
lines.append("")
lines.append("| 欄位 | 出現筆數 | 非空值 | 唯一值 | 數值型筆數 | 樣本值 |")
lines.append("|---|---:|---:|---:|---:|---|")

for report in reports:
    samples = ", ".join(report["sample_values"][:5])
    lines.append(
        f"| {report['field_name']} | {report['appears_in_records']} | "
        f"{report['non_empty_count']} | {report['unique_count']} | "
        f"{report['numeric_count']} | {samples} |"
    )

lines.append("")
lines.append("## 五、目前判斷")
lines.append("")
lines.append("目前仍不建議直接將 `nfi4_subrecords` 轉入 `trees`。")
lines.append("")
lines.append("原因：")
lines.append("")

for reason in decision["reason"]:
    lines.append("- " + reason)

lines.append("")
lines.append("## 六、下一步")
lines.append("")
lines.append("1. 若 DBH / 樹種 / 樹號欄位仍未出現，應考慮建立 `nfi4_plot_attributes` 或 `nfi4_inventory_details`。")
lines.append("2. 若後續確認有完整樣木欄位，再建立 `nfi4_subrecords_to_trees_sample.py`。")
lines.append("3. 不應在欄位不足時強行寫入 `trees`。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-subrecords-expanded-analysis.md").write_text(md_text, encoding="utf-8")

print("NFI4 subrecords expanded analysis completed")
print(f"Sample count: {len(records)}")
print()
print("Plot counts:")
for plot_code, count in sorted(plot_counts.items()):
    print(f"  {plot_code}: {count}")

print()
print("Candidate matches:")
for trees_field, found in candidate_matches.items():
    print(f"  {trees_field}: {found if found else 'NOT FOUND'}")

print()
print(json_path)
print(md_path)
