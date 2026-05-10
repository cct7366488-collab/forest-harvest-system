# NFI3 / NFI4 欄位對應表

本文件為 NFI3 / NFI4 匯入 `plots` 資料表的初步欄位對應。

注意：本表為自動判讀初版，後續仍需人工確認欄位意義、單位與座標系統。

## NFI3

來源資料夾：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi3`

### 第三次森林調查樣區97.shp

- 檔案：C:\Projects\forest-harvest-system\data\raw\nfi\nfi3\第三次森林資源調查樣區\第三次森林調查樣區97.shp
- 編碼：utf-8
- 幾何型態：POINT
- 筆數：3996

| plots 欄位 | NFI 來源欄位 |
|---|---|
| plot_code | PLOT_ID |
| original_plot_id | ID |
| county | 待確認 |
| township | 待確認 |
| forest_district | 待確認 |
| working_circle | 待確認 |
| compartment | 待確認 |
| sub_compartment | 待確認 |
| elevation_m | ELEVATION |
| slope_degree | 待確認 |
| aspect_degree | ASPECT |
| forest_type | STAND |
| land_use_type | LANDUSE |
| plot_area_ha | AREA |
| x_coord | DINDEX |
| y_coord | SURVEYOR |
| longitude | 待確認 |
| latitude | 待確認 |
| notes | 待確認 |

## NFI4

來源資料夾：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4`

### 4th_Final_ForestryInventoryData.shp

- 檔案：C:\Projects\forest-harvest-system\data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp
- 編碼：cp950
- 幾何型態：POINT
- 筆數：86306

| plots 欄位 | NFI 來源欄位 |
|---|---|
| plot_code | SampleID |
| original_plot_id | SampleID |
| county | 待確認 |
| township | 待確認 |
| forest_district | DeptName |
| working_circle | 待確認 |
| compartment | 待確認 |
| sub_compartment | 待確認 |
| elevation_m | Elevation |
| slope_degree | Slope |
| aspect_degree | Aspect |
| forest_type | 林型小類 |
| land_use_type | 待確認 |
| plot_area_ha | Area |
| x_coord | X_Coord |
| y_coord | Y_Coord |
| longitude | 待確認 |
| latitude | 待確認 |
| notes | 待確認 |
