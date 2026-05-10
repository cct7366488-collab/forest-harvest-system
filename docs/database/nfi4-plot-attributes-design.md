# NFI4 plot attributes 資料表設計

## 一、設計目的

NFI4 原始資料經判讀後，暫時不適合直接轉入 trees。

目前較合理的資料工程策略是：

NFI4 raw shapefile
↓
nfi4_subrecords
↓
nfi4_plot_attributes
↓
後續再判斷是否可轉入 trees 或其他正式資料表

nfi4_plot_attributes 用來保存 NFI4 中屬於樣區層級或林分層級的屬性。

## 二、為何建立 nfi4_plot_attributes

目前 NFI4 subrecords 中可觀察到許多欄位較像樣區或林分層級資料，例如：

- Height
- Volumn
- Crown
- CO2_ha
- CO2_ha1
- SBA_ha
- Vol_ha
- 樣區BA
- 樣區Vol
- 樣木數
- 樹冠密度
- A木樹種
- B木樹種
- 林型大類
- 林型中類
- 林型小類
- Terrain
- Elevation
- Slope
- Aspect

這些欄位目前不應直接放入 trees。

## 三、資料表定位

nfi4_plot_attributes 是 NFI4 樣區 / 林分層級屬性表。

它不是 staging table。staging table 是：

nfi4_subrecords

它也不是單木資料表。單木資料表仍然是：

trees

## 四、主要欄位設計

| 欄位 | 說明 |
|---|---|
| id | 系統主鍵 |
| plot_id | 對應 plots.id |
| plot_code | NFI4 plot_code |
| inventory_cycle | 固定為 NFI4 |
| sample_id | 樣點編號 |
| group_key | 樣點編號 + X_Coord + Y_Coord |
| source_subrecord_count | 來源 subrecords 筆數 |
| x_coord / y_coord | 坐標 |
| geom | PostGIS 點位 |
| terrain | 地形 |
| elevation_m | 海拔 |
| slope_degree | 坡度 |
| aspect_degree | 坡向 |
| landuse | 土地利用 |
| forest_type_major | 林型大類 |
| forest_type_middle | 林型中類 |
| forest_type_minor | 林型小類 |
| main_species_a | A木樹種 |
| main_species_b | B木樹種 |
| plot_area_ha | 樣區面積 |
| tree_count | 樣木數 |
| plot_basal_area | 樣區BA |
| plot_volume | 樣區Vol |
| basal_area_ha | SBA_ha |
| volume_ha | Vol_ha |
| stem_ha | 株_ha |
| co2_ha | CO2_ha |
| co2_ha_secondary | CO2_ha1 |
| crown_density | 樹冠密度 |
| crown_height | 冠層高度或相關欄位 |
| raw_summary | 原始欄位摘要 JSONB |
| source_file | 來源檔案 |
| notes | 備註 |

## 五、設計原則

1. 每一個 plot_code 原則上對應一筆 nfi4_plot_attributes。
2. 若後續發現一個 plot_code 有多個林分類型，才考慮拆成 stand-level table。
3. raw_summary 保留原始欄位摘要，避免欄位判讀過早造成資訊遺失。
4. trees 轉換暫停，直到確認 DBH、樹種、樣木號碼等單木欄位。

## 六、下一步

1. 建立 nfi4_plot_attributes 抽取腳本。
2. 從 nfi4_subrecords 聚合或抽取每個 plot_code 的屬性。
3. 測試匯入少量 nfi4_plot_attributes。
4. 驗證每個 plot_code 對應一筆 attributes。
5. 後續再判斷是否需要 nfi4_stand_attributes。
