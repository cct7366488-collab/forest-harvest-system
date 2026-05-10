from pathlib import Path
from collections import Counter
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

TREE_FIELDS = [
    {
        "trees_field": "plot_id",
        "source": "nfi4_subrecords.plot_id",
        "rule": "直接使用 staging table 中已對應的 plot_id。",
        "status": "confirmed"
    },
    {
        "trees_field": "inventory_cycle",
        "source": "constant",
        "rule": "固定填入 NFI4。",
        "status": "confirmed"
    },
    {
        "trees_field": "tree_no",
        "source": "record_index",
        "rule": "目前 NFI4 未確認有正式樣木號碼欄位，初版以 nfi4_subrecords.record_index 作為暫時 tree_no。",
        "status": "temporary"
    },
    {
        "trees_field": "tree_status",
        "source": None,
        "rule": "目前未確認直接對應欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "record_type",
        "source_candidates": ["SType", "IPCCTypeID"],
        "rule": "若 raw_attributes 中存在 SType，優先使用 SType；否則可參考 IPCCTypeID。",
        "status": "candidate"
    },
    {
        "trees_field": "line_distance_m",
        "source": None,
        "rule": "目前未確認直接對應欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "plot_tree_distance_m",
        "source": None,
        "rule": "目前未確認直接對應欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "species_code",
        "source": None,
        "rule": "目前 staging sample 尚未確認樹種代碼欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "species_name",
        "source": None,
        "rule": "目前 staging sample 尚未確認樹種中文名欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "dbh_cm",
        "source_candidates": ["DBH", "dbh", "Diameter", "diameter", "胸徑", "胸高直徑"],
        "rule": "目前 staging sample 尚未確認胸徑欄位；若後續 raw_attributes 出現 DBH 或胸徑類欄位，再正式對應。",
        "status": "missing"
    },
    {
        "trees_field": "height_m",
        "source_candidates": ["Height", "height", "樹高"],
        "rule": "目前可候選對應 raw_attributes.Height。",
        "status": "candidate"
    },
    {
        "trees_field": "clear_bole_height_m",
        "source_candidates": ["ClearBoleHeight", "clear_bole_height", "枝下高"],
        "rule": "目前未確認直接對應欄位，先保留 NULL。",
        "status": "missing"
    },
    {
        "trees_field": "crown_class",
        "source_candidates": ["Crown", "crown", "樹冠級"],
        "rule": "目前可候選對應 raw_attributes.Crown，但需確認此欄位是樹冠級、冠幅或其他冠層指標。",
        "status": "candidate_need_review"
    },
    {
        "trees_field": "estimated_volume_m3",
        "source_candidates": ["Volumn", "Volume", "volume", "材積"],
        "rule": "目前可候選對應 raw_attributes.Volumn。注意 NFI4 欄位使用 Volumn 拼法。",
        "status": "candidate"
    },
    {
        "trees_field": "notes",
        "source": "generated",
        "rule": "寫入 converted from nfi4_subrecords staging table，並保留來源 subrecord id。",
        "status": "confirmed"
    }
]


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def load_subrecords():
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
            "raw_attributes": raw or {}
        })

    return records


def analyze_raw_attributes(records):
    key_counter = Counter()
    non_empty_counter = Counter()
    unique_values = {}
    samples = {}

    for record in records:
        raw = record["raw_attributes"]

        for key, value in raw.items():
            key_counter[key] += 1

            text = clean(value)

            if text != "":
                non_empty_counter[key] += 1
                unique_values.setdefault(key, set()).add(text)

                if key not in samples:
                    samples[key] = []

                if len(samples[key]) < 8:
                    samples[key].append(text)

    reports = []

    for key in sorted(key_counter.keys()):
        reports.append({
            "field_name": key,
            "appears_in_records": key_counter[key],
            "non_empty_count": non_empty_counter[key],
            "unique_count": len(unique_values.get(key, set())),
            "sample_values": samples.get(key, [])
        })

    reports = sorted(
        reports,
        key=lambda x: (
            -x["non_empty_count"],
            -x["unique_count"],
            x["field_name"]
        )
    )

    return reports


def field_exists(raw_reports, candidates):
    available = {item["field_name"] for item in raw_reports}
    for candidate in candidates:
        if candidate in available:
            return candidate
    return None


def build_effective_mapping(raw_reports):
    effective = []

    for item in TREE_FIELDS:
        row = dict(item)

        if "source_candidates" in item:
            selected = field_exists(raw_reports, item["source_candidates"])
            row["selected_source"] = selected
            if selected is None and item["status"].startswith("candidate"):
                row["status"] = "candidate_not_found_in_current_sample"
            elif selected is not None and item["status"] == "missing":
                row["status"] = "candidate_found_need_review"

        effective.append(row)

    return effective


records = load_subrecords()
raw_reports = analyze_raw_attributes(records)
effective_mapping = build_effective_mapping(raw_reports)

result = {
    "purpose": "NFI4 subrecords to trees field mapping and conversion rules",
    "source_table": "nfi4_subrecords",
    "target_table": "trees",
    "sample_subrecord_count": len(records),
    "raw_attribute_reports": raw_reports,
    "trees_mapping": effective_mapping,
    "decision": {
        "can_convert_directly_to_trees_now": False,
        "reason": [
            "目前可確認 Height、Volumn、Crown 為候選欄位。",
            "目前尚未確認 DBH / 胸徑欄位。",
            "目前尚未確認 species_code / species_name 欄位。",
            "目前尚未確認每一筆 nfi4_subrecords 是否等同一棵樣木。",
            "因此現階段先建立轉換規則，不直接寫入 trees。"
        ],
        "recommended_next_step": "擴大 nfi4_subrecords 匯入樣本，並確認是否存在胸徑與樹種欄位。"
    }
}

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi4-subrecords-to-trees-mapping.json"
md_path = DOCS_DATA / "nfi4-subrecords-to-trees-mapping.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-subrecords-to-trees-mapping.json").write_text(json_text, encoding="utf-8")

lines = []

lines.append("# NFI4 subrecords → trees 欄位判讀與轉換規則")
lines.append("")
lines.append("## 一、目的")
lines.append("")
lines.append("本文件根據目前已匯入 `nfi4_subrecords` staging table 的樣本資料，建立 NFI4 子紀錄轉換至 `trees` 資料表的初步欄位判讀與轉換規則。")
lines.append("")
lines.append("本階段不直接寫入 `trees`，而是先建立正式轉換規則。")
lines.append("")
lines.append("## 二、目前樣本狀態")
lines.append("")
lines.append(f"- 來源資料表：`nfi4_subrecords`")
lines.append(f"- 目標資料表：`trees`")
lines.append(f"- 目前 staging sample 筆數：{len(records)}")
lines.append("")
lines.append("## 三、raw_attributes 欄位摘要")
lines.append("")
lines.append("| raw_attributes 欄位 | 出現筆數 | 非空值筆數 | 唯一值數 | 樣本值 |")
lines.append("|---|---:|---:|---:|---|")

for report in raw_reports:
    sample_text = ", ".join(report["sample_values"][:5])
    lines.append(
        f"| {report['field_name']} | {report['appears_in_records']} | "
        f"{report['non_empty_count']} | {report['unique_count']} | {sample_text} |"
    )

lines.append("")
lines.append("## 四、trees 欄位對應初版")
lines.append("")
lines.append("| trees 欄位 | 來源 | 狀態 | 規則 |")
lines.append("|---|---|---|---|")

for row in effective_mapping:
    if "selected_source" in row:
        source = row["selected_source"] if row["selected_source"] else "未在目前樣本中找到"
    else:
        source = row.get("source") if row.get("source") else "無直接來源"

    lines.append(
        f"| {row['trees_field']} | {source} | {row['status']} | {row['rule']} |"
    )

lines.append("")
lines.append("## 五、目前判斷")
lines.append("")
lines.append("目前不建議直接將 `nfi4_subrecords` 轉入 `trees`。")
lines.append("")
lines.append("原因：")
lines.append("")
for reason in result["decision"]["reason"]:
    lines.append("- " + reason)

lines.append("")
lines.append("## 六、建議後續流程")
lines.append("")
lines.append("1. 擴大 `nfi4_subrecords` 匯入樣本，不只匯入單一 plot_code。")
lines.append("2. 重新分析 raw_attributes 是否存在胸徑、樹種、樣木號碼等欄位。")
lines.append("3. 若確認存在樣木核心欄位，再建立 `nfi4_subrecords_to_trees_sample.py`。")
lines.append("4. 若 NFI4 子紀錄不等同樣木，則應另設正式明細表，而不是直接寫入 `trees`。")
lines.append("5. 最後再建立正式 `trees` ETL。")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi4-subrecords-to-trees-mapping.md").write_text(md_text, encoding="utf-8")

print("NFI4 subrecords to trees mapping completed")
print(f"Sample subrecords: {len(records)}")
print(json_path)
print(md_path)
print()
print("Selected tree mapping:")
for row in effective_mapping:
    if "selected_source" in row and row["selected_source"]:
        print(row["trees_field"], "<=", row["selected_source"], "|", row["status"])
