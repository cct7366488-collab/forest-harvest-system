# NFI4 plot attributes 抽取結果

## 一、目的

本文件記錄從 nfi4_subrecords staging table 抽取 NFI4 樣區 / 林分層級屬性，並寫入 nfi4_plot_attributes 的流程。

## 二、資料來源

來源資料表：

nfi4_subrecords

目標資料表：

nfi4_plot_attributes

## 三、抽取腳本

analysis/scripts/extract_nfi4_plot_attributes.py

## 四、抽取邏輯

1. 依 plot_code 將 nfi4_subrecords 分組。
2. 每個 plot_code 原則上產生一筆 nfi4_plot_attributes。
3. 對於文字欄位，採用最常見非空值。
4. 對於數值欄位，採用最常見非空值並轉為數值。
5. raw_summary 保留來源 raw_attributes 的欄位摘要。
6. 使用 plot_code 作為 upsert key，避免重複寫入。

## 五、目前欄位對應

| nfi4_plot_attributes 欄位 | 來源 raw_attributes 欄位 |
|---|---|
| terrain | Terrain / 地被型態 / 地形 |
| elevation_m | Elevation / Altitude / 海拔 |
| slope_degree | Slope / 坡度 |
| aspect_degree | Aspect / 方位角 / 坡向 |
| landuse | LANDUSE / 土地利用 |
| forest_type_major | 林型大類 |
| forest_type_middle | 林型中類 |
| forest_type_minor | 林型小類 |
| main_species_a | A木樹種 |
| main_species_b | B木樹種 |
| plot_area_ha | 樣區面積 |
| tree_count | 樣木數 |
| stand_age | AGE / 林齡 |
| stand_density | DENSITY / 密度 |
| plot_basal_area | 樣區BA |
| plot_volume | 樣區Vol |
| basal_area_ha | SBA_ha |
| volume_ha | Vol_ha |
| stem_ha | 株_ha |
| co2_ha | CO2_ha |
| co2_ha_secondary | CO2_ha1 |
| crown_density | 樹冠密度 / Crown / COVDENSITY |
| crown_height | COVHEIGHT / 冠層高度 |

## 六、後續工作

1. 擴大 nfi4_subrecords 匯入範圍。
2. 重新抽取 nfi4_plot_attributes。
3. 驗證每個 NFI4 plot_code 是否有一筆 attributes。
4. 後續若確認樣木層級資料，再另行設計 trees 匯入流程。
