# NFI4 檔案結構總盤點

產生時間：2026-05-10 19:25:30

## 一、目的

本文件盤點第四次森林資源調查 NFI4 原始資料夾中的所有檔案，用於判斷是否存在獨立的樣木資料表、樣區資料表、屬性資料表或模型資料。

目前已知 NFI4 Shapefile 比較像樣區 / 林分屬性資料，尚未確認真正樣木層級資料是否存在於其他檔案。

## 二、資料夾位置

`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4`

## 三、副檔名統計

| 副檔名 | 檔案數 | 總大小 MB |
|---|---:|---:|
| .dbf | 1 | 1063.009 |
| .prj | 1 | 0.0 |
| .qmd | 1 | 0.002 |
| .sbn | 1 | 0.791 |
| .sbx | 1 | 0.008 |
| .shp | 1 | 2.305 |
| .shx | 1 | 0.659 |
| .xlsx | 3 | 76.118 |

## 四、檔案清單

| 檔名 | 副檔名 | 大小 MB | 類型判斷 | 可能角色 | 相對路徑 |
|---|---|---:|---|---|---|
| 4th_Final_ForestryInventoryData.dbf | .dbf | 1063.009 | Shapefile attribute table / DBF table | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.dbf` |
| 4th_Final_ForestryInventoryData.prj | .prj | 0.0 | Shapefile support file | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.prj` |
| 4th_Final_ForestryInventoryData250505.qmd | .qmd | 0.002 | Other | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData250505.qmd` |
| 4th_Final_ForestryInventoryData.sbn | .sbn | 0.791 | Other | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.sbn` |
| 4th_Final_ForestryInventoryData.sbx | .sbx | 0.008 | Other | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.sbx` |
| 4th_Final_ForestryInventoryData.shp | .shp | 2.305 | GIS Shapefile geometry | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp` |
| 4th_Final_ForestryInventoryData.shx | .shx | 0.659 | Shapefile support file | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shx` |
| 4th_Final_ForestryInventoryData.xlsx | .xlsx | 40.394 | Excel table | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.xlsx` |
| 4th_Final_ForestryInventoryData250505.xlsx | .xlsx | 35.724 | Excel table | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData250505.xlsx` |
| ~$4th_Final_ForestryInventoryData250505.xlsx | .xlsx | 0.0 | Excel table | 可能是樣區 / 林分資料 | `data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\~$4th_Final_ForestryInventoryData250505.xlsx` |

## 五、初步判讀原則

1. 若只存在一組 Shapefile，則目前 NFI4 原始檔可能只提供樣區 / 林分層級資料。
2. 若存在 Excel、CSV、MDB、Access 等表格，需優先檢查是否為樣木層級資料。
3. 若存在多個 DBF，需判斷 DBF 是否只屬於 Shapefile 附屬檔，或是獨立屬性表。
4. 若找不到 DBH、樹種、樣木號等欄位，則不應直接建立 NFI4 trees ETL。

## 六、下一步

1. 檢視本盤點結果。
2. 若發現疑似樣木表，進一步做欄位盤點。
3. 若沒有疑似樣木表，則正式將 NFI4 定位為樣區 / 林分屬性資料來源。
4. 依結果決定是否建立 nfi4_inventory_details 或 nfi4_stand_attributes。