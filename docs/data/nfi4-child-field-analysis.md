# NFI4 子紀錄 / 樣木層級欄位分析

## 一、目的

本文件用於判斷 NFI4 原始 Shapefile 中，哪些欄位屬於樣區層級，哪些欄位可能屬於樣木或子紀錄層級。

分析方式：

- 先依 `樣點編號 + X_Coord + Y_Coord` 建立樣區群組。
- 若某欄位在同一樣區群組內會變動，表示它可能是子紀錄層級欄位。
- 若某欄位在同一樣區群組內固定不變，表示它較可能是樣區層級欄位。

## 二、資料摘要

- 資料集：NFI4
- 檔案：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp`
- 編碼：cp950
- 原始紀錄筆數：86306
- 樣區群組數：1556
- 群組欄位：樣點編號, X_Coord, Y_Coord

## 三、最可能屬於樣木 / 子紀錄層級的欄位

| 欄位 | 分類 | 非空值 | 唯一值 | 變動群組數 | 群組內變動比例 |
|---|---|---:|---:|---:|---:|
| Volume | likely_tree_or_child_record_field | 86306 | 27547 | 1556 | 1.000 |
| Tree_Numbe | likely_tree_or_child_record_field | 86306 | 25402 | 1556 | 1.000 |
| DBH | likely_tree_or_child_record_field | 86306 | 1190 | 1556 | 1.000 |
| Tree_Heigh | likely_tree_or_child_record_field | 86306 | 349 | 1556 | 1.000 |
| Tree_X | likely_tree_or_child_record_field | 86306 | 71700 | 1554 | 0.999 |
| Tree_Y | likely_tree_or_child_record_field | 86306 | 71689 | 1554 | 0.999 |
| Tree_Crown | likely_tree_or_child_record_field | 86306 | 16 | 1534 | 0.986 |
| Tree_En_Na | likely_tree_or_child_record_field | 86306 | 564 | 1521 | 0.978 |
| Tree_Chi_N | likely_tree_or_child_record_field | 86306 | 548 | 1521 | 0.978 |
| P_S_ | likely_child_record_field | 29473 | 3135 | 1555 | 0.999 |
| Branch_Hei | likely_child_record_field | 86306 | 214 | 1555 | 0.999 |
| X_asis | likely_child_record_field | 86306 | 807 | 1554 | 0.999 |
| Y_axis | likely_child_record_field | 86306 | 605 | 1554 | 0.999 |
| Record_Typ | likely_child_record_field | 86306 | 7 | 1549 | 0.996 |
| Scientific | likely_child_record_field | 86306 | 545 | 1521 | 0.978 |

## 四、可能屬於樣區層級的欄位

| 欄位 | 分類 | 非空值 | 唯一值 | 變動群組數 |
|---|---|---:|---:|---:|
| SampleID1 | constant_within_plot_group | 86306 | 1550 | 0 |
| FrameID_1 | constant_within_plot_group | 86306 | 1539 | 0 |
| FrameID | constant_within_plot_group | 86306 | 1471 | 0 |
| 海拔 | constant_within_plot_group | 86306 | 1206 | 0 |
| BlkID | constant_within_plot_group | 86306 | 1076 | 0 |
| BlkID_1 | constant_within_plot_group | 86306 | 1007 | 0 |
| DTIME | constant_within_plot_group | 86306 | 770 | 0 |
| DTIME_1 | constant_within_plot_group | 86306 | 719 | 0 |
| Height | constant_within_plot_group | 86306 | 550 | 0 |
| Crown | constant_within_plot_group | 86306 | 456 | 0 |
| BlockID | constant_within_plot_group | 86306 | 322 | 0 |
| BlockID_1 | constant_within_plot_group | 86306 | 322 | 0 |
| Y_Coord | plot_group_key | 86306 | 317 | 0 |
| 主要地被種 | constant_within_plot_group | 86306 | 273 | 0 |
| 次要地被種 | constant_within_plot_group | 86306 | 230 | 0 |
| X_Coord | plot_group_key | 86306 | 170 | 0 |
| VerifyHeig | constant_within_plot_group | 86306 | 109 | 0 |
| VerifyCrow | constant_within_plot_group | 86306 | 106 | 0 |
| 樣點編號 | plot_group_key | 86306 | 65 | 0 |
| 含石率（％ | constant_within_plot_group | 86306 | 52 | 0 |
| 腐植層型態 | constant_within_plot_group | 86306 | 38 | 0 |
| UserName | constant_within_plot_group | 86306 | 35 | 0 |
| UserName_1 | constant_within_plot_group | 86306 | 35 | 0 |
| 調查人員 | constant_within_plot_group | 86306 | 31 | 0 |
| 林型小類 | likely_plot_level_field | 86306 | 24 | 0 |
| SlaveTreeI | constant_within_plot_group | 86306 | 22 | 0 |
| MajorTreeI | constant_within_plot_group | 86306 | 21 | 0 |
| IPCCTypeID | constant_within_plot_group | 86306 | 18 | 0 |
| MajorTreeP | constant_within_plot_group | 86306 | 18 | 0 |
| SlaveTreeP | constant_within_plot_group | 86306 | 18 | 0 |
| 腐植層厚度 | constant_within_plot_group | 86306 | 16 | 0 |
| Closing | constant_within_plot_group | 86306 | 15 | 0 |
| VerifyClos | constant_within_plot_group | 86306 | 14 | 0 |
| DeptID_1 | likely_plot_level_field | 86306 | 11 | 0 |
| VerifyUs_1 | constant_within_plot_group | 86306 | 11 | 0 |
| DeptID | likely_plot_level_field | 86306 | 10 | 0 |
| DeptName | likely_plot_level_field | 86306 | 10 | 0 |
| DeptName_1 | likely_plot_level_field | 86306 | 10 | 0 |
| FunctionTy | constant_within_plot_group | 86306 | 8 | 0 |
| 地形 | constant_within_plot_group | 86306 | 8 | 0 |
| 地被高度 | constant_within_plot_group | 86306 | 8 | 0 |
| 林區 | constant_within_plot_group | 86306 | 8 | 0 |
| TypeName | constant_within_plot_group | 86306 | 6 | 0 |
| 地被密度 | constant_within_plot_group | 86306 | 6 | 0 |
| 林型中類 | likely_plot_level_field | 86306 | 6 | 0 |
| VerifyUs_2 | constant_within_plot_group | 86306 | 5 | 0 |
| VerifyUs_3 | constant_within_plot_group | 86306 | 5 | 0 |
| Area | constant_within_plot_group | 86306 | 3 | 0 |
| MergeOnly | constant_within_plot_group | 86306 | 3 | 0 |
| 林型大類 | likely_plot_level_field | 86306 | 3 | 0 |
| 樣區面積 | likely_plot_level_field | 86306 | 3 | 0 |
| Finished | constant_within_plot_group | 86306 | 2 | 0 |
| SType | constant_within_plot_group | 86306 | 2 | 0 |
| VerifyDe_2 | constant_within_plot_group | 86306 | 2 | 0 |
| VerifyDe_3 | constant_within_plot_group | 86306 | 2 | 0 |
| VerifyFini | constant_within_plot_group | 86306 | 2 | 0 |
| VerifyPass | constant_within_plot_group | 86306 | 2 | 0 |
| IPCCName | constant_within_plot_group | 86306 | 1 | 0 |
| VerifyVolu | constant_within_plot_group | 86306 | 1 | 0 |
| Volumn | constant_within_plot_group | 86306 | 1 | 0 |
| 備註 | constant_within_plot_group | 86306 | 1 | 0 |
| 備註_1 | constant_within_plot_group | 86306 | 1 | 0 |

## 五、全部欄位總表

| 欄位 | 分類 | 非空值 | 空值 | 唯一值 | 群組內變動數 |
|---|---|---:|---:|---:|---:|
| Volume | likely_tree_or_child_record_field | 86306 | 0 | 27547 | 1556 |
| Tree_Numbe | likely_tree_or_child_record_field | 86306 | 0 | 25402 | 1556 |
| DBH | likely_tree_or_child_record_field | 86306 | 0 | 1190 | 1556 |
| Tree_Heigh | likely_tree_or_child_record_field | 86306 | 0 | 349 | 1556 |
| Tree_X | likely_tree_or_child_record_field | 86306 | 0 | 71700 | 1554 |
| Tree_Y | likely_tree_or_child_record_field | 86306 | 0 | 71689 | 1554 |
| Tree_Crown | likely_tree_or_child_record_field | 86306 | 0 | 16 | 1534 |
| Tree_En_Na | likely_tree_or_child_record_field | 86306 | 0 | 564 | 1521 |
| Tree_Chi_N | likely_tree_or_child_record_field | 86306 | 0 | 548 | 1521 |
| P_S_ | likely_child_record_field | 29473 | 56833 | 3135 | 1555 |
| Branch_Hei | likely_child_record_field | 86306 | 0 | 214 | 1555 |
| X_asis | likely_child_record_field | 86306 | 0 | 807 | 1554 |
| Y_axis | likely_child_record_field | 86306 | 0 | 605 | 1554 |
| Record_Typ | likely_child_record_field | 86306 | 0 | 7 | 1549 |
| Scientific | likely_child_record_field | 86306 | 0 | 545 | 1521 |
| Plot_Y | mixed_or_need_review | 86306 | 0 | 1398 | 9 |
| Plot_X | mixed_or_need_review | 86306 | 0 | 1213 | 9 |
| Survey_Dat | mixed_or_need_review | 86306 | 0 | 747 | 9 |
| Aspect | mixed_or_need_review | 86306 | 0 | 344 | 9 |
| Slope | mixed_or_need_review | 86306 | 0 | 63 | 9 |
| Plot_Numbe | mixed_or_need_review | 86306 | 0 | 1564 | 8 |
| Elevation | mixed_or_need_review | 86306 | 0 | 1202 | 8 |
| Terrain | mixed_or_need_review | 86306 | 0 | 8 | 4 |
| District_O | mixed_or_need_review | 86306 | 0 | 8 | 2 |
| SampleID | mixed_or_need_review | 86306 | 0 | 1557 | 1 |
| 流水號 | mixed_or_need_review | 86306 | 0 | 1557 | 1 |
| CO2_ha1 | mixed_or_need_review | 86306 | 0 | 1545 | 1 |
| 基本圖圖號 | mixed_or_need_review | 86306 | 0 | 1543 | 1 |
| vol_ha | mixed_or_need_review | 86306 | 0 | 1536 | 1 |
| SBA_ha | mixed_or_need_review | 86306 | 0 | 1410 | 1 |
| 樣區座標Y | mixed_or_need_review | 86306 | 0 | 1406 | 1 |
| CO2_ha | mixed_or_need_review | 86306 | 0 | 1328 | 1 |
| 樣區Vol | mixed_or_need_review | 86306 | 0 | 1241 | 1 |
| 樣區座標X | mixed_or_need_review | 86306 | 0 | 1215 | 1 |
| 調查日期 | mixed_or_need_review | 86306 | 0 | 748 | 1 |
| 樣區BA | mixed_or_need_review | 86306 | 0 | 502 | 1 |
| 方位角 | mixed_or_need_review | 86306 | 0 | 344 | 1 |
| B木樹種 | mixed_or_need_review | 86306 | 0 | 328 | 1 |
| A木樹種 | mixed_or_need_review | 86306 | 0 | 324 | 1 |
| 系統座標Y | mixed_or_need_review | 86306 | 0 | 304 | 1 |
| 株_ha | mixed_or_need_review | 86306 | 0 | 159 | 1 |
| 樣木數 | mixed_or_need_review | 86306 | 0 | 157 | 1 |
| 系統座標X | mixed_or_need_review | 86306 | 0 | 146 | 1 |
| 坡度 | mixed_or_need_review | 86306 | 0 | 63 | 1 |
| 地被型態 | mixed_or_need_review | 86306 | 0 | 8 | 1 |
| 樹冠密度 | mixed_or_need_review | 86306 | 0 | 6 | 1 |
| SampleID1 | constant_within_plot_group | 86306 | 0 | 1550 | 0 |
| FrameID_1 | constant_within_plot_group | 86306 | 0 | 1539 | 0 |
| FrameID | constant_within_plot_group | 86306 | 0 | 1471 | 0 |
| 海拔 | constant_within_plot_group | 86306 | 0 | 1206 | 0 |
| BlkID | constant_within_plot_group | 86306 | 0 | 1076 | 0 |
| BlkID_1 | constant_within_plot_group | 86306 | 0 | 1007 | 0 |
| DTIME | constant_within_plot_group | 86306 | 0 | 770 | 0 |
| DTIME_1 | constant_within_plot_group | 86306 | 0 | 719 | 0 |
| Height | constant_within_plot_group | 86306 | 0 | 550 | 0 |
| Crown | constant_within_plot_group | 86306 | 0 | 456 | 0 |
| BlockID | constant_within_plot_group | 86306 | 0 | 322 | 0 |
| BlockID_1 | constant_within_plot_group | 86306 | 0 | 322 | 0 |
| Y_Coord | plot_group_key | 86306 | 0 | 317 | 0 |
| 主要地被種 | constant_within_plot_group | 86306 | 0 | 273 | 0 |
| 次要地被種 | constant_within_plot_group | 86306 | 0 | 230 | 0 |
| X_Coord | plot_group_key | 86306 | 0 | 170 | 0 |
| VerifyHeig | constant_within_plot_group | 86306 | 0 | 109 | 0 |
| VerifyCrow | constant_within_plot_group | 86306 | 0 | 106 | 0 |
| 樣點編號 | plot_group_key | 86306 | 0 | 65 | 0 |
| 含石率（％ | constant_within_plot_group | 86306 | 0 | 52 | 0 |
| 腐植層型態 | constant_within_plot_group | 86306 | 0 | 38 | 0 |
| UserName | constant_within_plot_group | 86306 | 0 | 35 | 0 |
| UserName_1 | constant_within_plot_group | 86306 | 0 | 35 | 0 |
| 調查人員 | constant_within_plot_group | 86306 | 0 | 31 | 0 |
| 林型小類 | likely_plot_level_field | 86306 | 0 | 24 | 0 |
| SlaveTreeI | constant_within_plot_group | 86306 | 0 | 22 | 0 |
| MajorTreeI | constant_within_plot_group | 86306 | 0 | 21 | 0 |
| IPCCTypeID | constant_within_plot_group | 86306 | 0 | 18 | 0 |
| MajorTreeP | constant_within_plot_group | 86306 | 0 | 18 | 0 |
| SlaveTreeP | constant_within_plot_group | 86306 | 0 | 18 | 0 |
| 腐植層厚度 | constant_within_plot_group | 86306 | 0 | 16 | 0 |
| Closing | constant_within_plot_group | 86306 | 0 | 15 | 0 |
| VerifyClos | constant_within_plot_group | 86306 | 0 | 14 | 0 |
| DeptID_1 | likely_plot_level_field | 86306 | 0 | 11 | 0 |
| VerifyUs_1 | constant_within_plot_group | 86306 | 0 | 11 | 0 |
| DeptID | likely_plot_level_field | 86306 | 0 | 10 | 0 |
| DeptName | likely_plot_level_field | 86306 | 0 | 10 | 0 |
| DeptName_1 | likely_plot_level_field | 86306 | 0 | 10 | 0 |
| FunctionTy | constant_within_plot_group | 86306 | 0 | 8 | 0 |
| 地形 | constant_within_plot_group | 86306 | 0 | 8 | 0 |
| 地被高度 | constant_within_plot_group | 86306 | 0 | 8 | 0 |
| 林區 | constant_within_plot_group | 86306 | 0 | 8 | 0 |
| TypeName | constant_within_plot_group | 86306 | 0 | 6 | 0 |
| 地被密度 | constant_within_plot_group | 86306 | 0 | 6 | 0 |
| 林型中類 | likely_plot_level_field | 86306 | 0 | 6 | 0 |
| VerifyUs_2 | constant_within_plot_group | 86306 | 0 | 5 | 0 |
| VerifyUs_3 | constant_within_plot_group | 86306 | 0 | 5 | 0 |
| Area | constant_within_plot_group | 86306 | 0 | 3 | 0 |
| MergeOnly | constant_within_plot_group | 86306 | 0 | 3 | 0 |
| 林型大類 | likely_plot_level_field | 86306 | 0 | 3 | 0 |
| 樣區面積 | likely_plot_level_field | 86306 | 0 | 3 | 0 |
| Finished | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| SType | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| VerifyDe_2 | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| VerifyDe_3 | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| VerifyFini | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| VerifyPass | constant_within_plot_group | 86306 | 0 | 2 | 0 |
| IPCCName | constant_within_plot_group | 86306 | 0 | 1 | 0 |
| VerifyVolu | constant_within_plot_group | 86306 | 0 | 1 | 0 |
| Volumn | constant_within_plot_group | 86306 | 0 | 1 | 0 |
| 備註 | constant_within_plot_group | 86306 | 0 | 1 | 0 |
| 備註_1 | constant_within_plot_group | 86306 | 0 | 1 | 0 |

## 六、初步判讀

若 `Height`、`Volumn`、`Crown`、`SlaveTreeI` 等欄位在同一樣區群組內變動，則可視為 trees 或子紀錄層級候選欄位。

下一步應根據本分析結果建立 `NFI4 → trees` 欄位對應表，並測試少量樣木資料匯入。