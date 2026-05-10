# NFI4 plot_code 組合欄位分析

- 檔案：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp`
- 編碼：cp950
- 總筆數：86306

## 組合欄位唯一性分析

| 組合欄位 | 唯一值數 | 重複 key 數 | 最大重複次數 | 是否逐筆唯一 |
|---|---:|---:|---:|---|
| 樣點編號 | 65 | 65 | 2223 | False |
| X_Coord + Y_Coord | 1550 | 1550 | 288 | False |
| 樣點編號 + X_Coord + Y_Coord | 1556 | 1556 | 237 | False |
| DeptID + 樣點編號 | 516 | 516 | 762 | False |
| DeptID + 樣點編號 + X_Coord + Y_Coord | 1556 | 1556 | 237 | False |
| DeptName + 樣點編號 + X_Coord + Y_Coord | 1556 | 1556 | 237 | False |
| BlkID + 樣點編號 | 1495 | 1495 | 268 | False |
| BlkID_1 + 樣點編號 | 1489 | 1489 | 268 | False |
| SampleID1 + 樣點編號 | 1556 | 1556 | 237 | False |
| FrameID_1 + 樣點編號 | 1556 | 1556 | 237 | False |
| BlockID_1 + 樣點編號 | 1381 | 1381 | 341 | False |
| DeptID_1 + 樣點編號 + X_Coord + Y_Coord | 1556 | 1556 | 237 | False |

## 初步解讀

若某組合的唯一值數遠小於總筆數，表示 NFI4 可能為樣木或子紀錄層級，而非純樣區層級。

若 X_Coord + Y_Coord 的唯一值數接近樣區數，則可作為樣區位置分組依據。

下一步應依分析結果決定 NFI4 匯入 plots 時是否採用座標群組或組合欄位。