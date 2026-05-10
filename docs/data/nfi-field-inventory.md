# NFI3 / NFI4 欄位結構盤點

產生時間：2026-05-10 14:51:51

## 一、資料定位

本文件盤點第三次與第四次森林資源調查樣區 Shapefile 欄位結構，作為 Forest Harvest System 後續資料字典、資料表設計與資料匯入流程之依據。

## 二、資料集摘要

### NFI3

- 來源資料夾：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi3`
- Shapefile 數量：1

#### 第三次森林調查樣區97.shp

- 完整路徑：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi3\第三次森林資源調查樣區\第三次森林調查樣區97.shp`
- 幾何型態：POINT
- 筆數：3996
- 邊界範圍 bbox：(152000.0, 2425000.0, 350000.0, 2797000.0)

| 欄位名稱 | 型態 | 長度 | 小數位 |
|---|---:|---:|---:|
| FID_ | N | 9 | 0 |
| AREA | N | 13 | 6 |
| PERIMETER | N | 13 | 6 |
| PLOT_ | N | 10 | 0 |
| PLOT_ID | N | 10 | 0 |
| MAPNO | N | 7 | 0 |
| PLOTNO | N | 2 | 0 |
| RECORDER | N | 1 | 0 |
| SURVEYOR | N | 1 | 0 |
| DATE_ | N | 5 | 0 |
| ABSCISSA | N | 5 | 0 |
| ORDINATE | N | 6 | 0 |
| PLOTAREA | N | 2 | 0 |
| ELEVATION | N | 3 | 0 |
| SLOP | N | 1 | 0 |
| ASPECT | N | 4 | 0 |
| LANDUSE | N | 2 | 0 |
| TERRAINS | N | 4 | 0 |
| AGE | N | 1 | 0 |
| DENSITY | N | 4 | 0 |
| STAND | N | 4 | 0 |
| MAINCOVER | N | 4 | 0 |
| SECONDCOV | N | 4 | 0 |
| COVDENSITY | N | 4 | 0 |
| COVHEIGHT | N | 4 | 0 |
| VOL | N | 11 | 0 |
| ID | N | 15 | 0 |
| S | N | 10 | 0 |
| N | N | 10 | 0 |
| SUMVOL | N | 16 | 4 |
| DINDEX | N | 16 | 4 |
| SIMPSON | N | 16 | 4 |
| SHANNON | N | 16 | 4 |
| E | N | 16 | 4 |

### NFI4

- 來源資料夾：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4`
- Shapefile 數量：1

#### 4th_Final_ForestryInventoryData.shp

- 完整路徑：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp`
- 讀取錯誤：'utf-8' codec can't decode byte 0xac in position 0: invalid start byte

## 三、初步判讀原則

後續資料字典應依欄位用途分類為：

1. 樣區基本資料欄位
2. 空間定位欄位
3. 林分與環境因子欄位
4. 樹種與樣木欄位
5. 材積、生長量與模式建構欄位
6. 調查期別與重測關聯欄位

## 四、下一步

1. 比對 NFI3 與 NFI4 欄位差異。
2. 建立 `nfi-data-dictionary.md`。
3. 設計 `plots`、`trees`、`species`、`volume_models`、`height_models` 資料表。
4. 建立 PostgreSQL / PostGIS 匯入流程。