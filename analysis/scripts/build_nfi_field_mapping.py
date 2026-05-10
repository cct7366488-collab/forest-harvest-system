from pathlib import Path
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

def choose_field(fields, candidates):
    lower_map = {f.lower(): f for f in fields}
    for c in candidates:
        if c.lower() in lower_map:
            return lower_map[c.lower()]
    for f in fields:
        fl = f.lower()
        for c in candidates:
            if c.lower() in fl:
                return f
    return None

def build_mapping(fields):
    return {
        "plot_code": choose_field(fields, ["plotid", "plot_id", "sampleid", "sampleid1", "sampleid01", "blockid", "blkid", "id"]),
        "original_plot_id": choose_field(fields, ["plotid", "sampleid", "sampleid1", "sampleid01", "blockid", "blkid", "id"]),
        "county": choose_field(fields, ["county", "countyname", "縣市"]),
        "township": choose_field(fields, ["township", "town", "鄉鎮"]),
        "forest_district": choose_field(fields, ["deptname", "dept", "林區", "管理處"]),
        "working_circle": choose_field(fields, ["working_circle", "workcircle", "事業區"]),
        "compartment": choose_field(fields, ["compartment", "林班"]),
        "sub_compartment": choose_field(fields, ["sub_compartment", "subcomp", "小班"]),
        "elevation_m": choose_field(fields, ["elevation", "elev", "altitude", "alt", "海拔"]),
        "slope_degree": choose_field(fields, ["slope", "坡度"]),
        "aspect_degree": choose_field(fields, ["aspect", "坡向"]),
        "forest_type": choose_field(fields, ["forest_type", "stand", "林型小類", "林型中類", "林型大類"]),
        "land_use_type": choose_field(fields, ["landuse", "land_use", "土地利用"]),
        "plot_area_ha": choose_field(fields, ["area", "plot_area", "面積"]),
        "x_coord": choose_field(fields, ["x_coord", "xcoord", "x", "tm2_x", "twd97_x"]),
        "y_coord": choose_field(fields, ["y_coord", "ycoord", "y", "tm2_y", "twd97_y"]),
        "longitude": choose_field(fields, ["longitude", "lon", "lng"]),
        "latitude": choose_field(fields, ["latitude", "lat"]),
        "notes": None
    }

result = {
    "purpose": "NFI3 / NFI4 fields mapping to plots table",
    "datasets": {}
}

for folder_name in ["nfi3", "nfi4"]:
    dataset_name = folder_name.upper()
    folder = NFI_ROOT / folder_name
    result["datasets"][dataset_name] = {
        "folder": str(folder),
        "shapefiles": []
    }

    for shp in folder.rglob("*.shp"):
        reader, encoding = open_reader(shp)
        fields = [f[0] for f in reader.fields[1:]]
        result["datasets"][dataset_name]["shapefiles"].append({
            "file": str(shp),
            "encoding": encoding,
            "shape_type": reader.shapeTypeName,
            "record_count": len(reader),
            "fields": fields,
            "mapping_to_plots": build_mapping(fields)
        })

DOCS_DATA.mkdir(parents=True, exist_ok=True)
OBSIDIAN_NFI.mkdir(parents=True, exist_ok=True)

json_path = DOCS_DATA / "nfi-field-mapping.json"
md_path = DOCS_DATA / "nfi-field-mapping.md"

json_text = json.dumps(result, ensure_ascii=False, indent=2)
json_path.write_text(json_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi-field-mapping.json").write_text(json_text, encoding="utf-8")

lines = []
lines.append("# NFI3 / NFI4 欄位對應表")
lines.append("")
lines.append("本文件為 NFI3 / NFI4 匯入 `plots` 資料表的初步欄位對應。")
lines.append("")
lines.append("注意：本表為自動判讀初版，後續仍需人工確認欄位意義、單位與座標系統。")
lines.append("")

for dataset_name, dataset in result["datasets"].items():
    lines.append("## " + dataset_name)
    lines.append("")
    lines.append("來源資料夾：`" + dataset["folder"] + "`")
    lines.append("")
    for item in dataset["shapefiles"]:
        lines.append("### " + Path(item["file"]).name)
        lines.append("")
        lines.append("- 檔案：" + item["file"])
        lines.append("- 編碼：" + item["encoding"])
        lines.append("- 幾何型態：" + item["shape_type"])
        lines.append("- 筆數：" + str(item["record_count"]))
        lines.append("")
        lines.append("| plots 欄位 | NFI 來源欄位 |")
        lines.append("|---|---|")
        for target, source in item["mapping_to_plots"].items():
            lines.append("| " + target + " | " + (source if source else "待確認") + " |")
        lines.append("")

md_text = "\n".join(lines)
md_path.write_text(md_text, encoding="utf-8")
(OBSIDIAN_NFI / "nfi-field-mapping.md").write_text(md_text, encoding="utf-8")

print("NFI field mapping created")
print(json_path)
print(md_path)
print(OBSIDIAN_NFI / "nfi-field-mapping.json")
print(OBSIDIAN_NFI / "nfi-field-mapping.md")
