import json
from pathlib import Path

path = Path("docs/data/nfi-plot-identifier-analysis.json")
data = json.loads(path.read_text(encoding="utf-8"))

for dataset in data["datasets"]:
    print()
    print("===", dataset["dataset"], "===")
    print("File:", dataset["file"])
    print("Record count:", dataset["record_count"])
    print()
    print("Top candidate fields:")
    for r in dataset["field_reports"][:10]:
        print(
            f"{r['field_name']:20s} "
            f"non_empty={r['non_empty_count']:6d} "
            f"unique={r['unique_count']:6d} "
            f"dup={r['duplicate_value_count']:6d} "
            f"unique_if_non_empty={r['is_unique_if_non_empty']}"
        )
