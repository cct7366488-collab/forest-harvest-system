# Forest Harvest System 資料表設計初版

## 一、設計目的

本文件設計 Forest Harvest System 第一階段核心資料表：

1. plots：森林樣區資料表
2. trees：樣木 / 單木資料表
3. species：樹種代碼表
4. volume_models：立木材積式資料表
5. height_models：樹高曲線式資料表

## 二、設計原則

- 原始資料放在 data/raw/nfi，不直接修改。
- 正式資料進入 PostgreSQL / PostGIS。
- plots 使用 PostGIS geometry(Point, 3826) 儲存樣區位置。
- NFI3 與 NFI4 透過 inventory_cycle 欄位區分。
- 材積式與樹高曲線式獨立成資料表，不寫死在程式內。

## 三、plots 樣區資料表

用途：儲存樣區基本資料、空間位置、地形環境與林分資訊。

主要欄位：

- id：系統主鍵
- plot_code：樣區編號
- inventory_cycle：調查期別，NFI3 或 NFI4
- county：縣市
- township：鄉鎮
- forest_district：林區或管理單位
- working_circle：事業區
- compartment：林班
- sub_compartment：小班
- elevation_m：海拔
- slope_degree：坡度
- aspect_degree：坡向
- forest_type：林型
- land_use_type：土地利用型
- plot_area_ha：樣區面積
- x_coord / y_coord：平面座標
- longitude / latitude：經緯度
- geom：PostGIS 幾何欄位

## 四、trees 樣木資料表

用途：儲存樣區內樣木或單木調查資料。

主要欄位：

- id：系統主鍵
- plot_id：對應 plots.id
- inventory_cycle：調查期別
- tree_no：樣木號碼
- tree_status：樣木狀態
- record_type：記錄類型
- species_code：樹種代碼
- species_name：樹種中文名
- dbh_cm：胸高直徑
- height_m：樹高
- clear_bole_height_m：枝下高
- crown_class：樹冠級
- estimated_volume_m3：估算材積
- volume_model_id：使用之材積模式
- height_model_id：使用之樹高模式

## 五、species 樹種資料表

用途：儲存樹種代碼、中文名、學名與分類資訊。

主要欄位：

- id
- species_code
- chinese_name
- scientific_name
- family
- genus
- common_group
- is_native
- notes

## 六、volume_models 立木材積式資料表

用途：儲存不同樹種、地區、作者與年代的立木材積推估公式。

主要欄位：

- id
- species_code
- species_name
- model_name
- formula_text
- formula_expression
- variables
- coefficients
- applicable_region
- sample_size
- r_squared
- author
- publication_year
- source_reference
- notes

## 七、height_models 樹高曲線式資料表

用途：儲存由胸徑推估樹高或建立 DBH-H 關係的樹高曲線式。

主要欄位與 volume_models 類似，但其公式用途為 height estimation。

## 八、資料表關聯

plots 1 --- * trees
species 1 --- * trees
species 1 --- * volume_models
species 1 --- * height_models
volume_models 1 --- * trees
height_models 1 --- * trees

## 九、下一步

1. 檢查 NFI3 / NFI4 欄位與本資料表欄位之對應。
2. 匯入 schema.sql 到 PostgreSQL。
3. 建立 SQLAlchemy ORM models。
4. 建立 plots / trees CRUD API。
5. 建立材積式與樹高曲線式資料匯入流程。
