# NFI4 plot / stand attributes 判讀

## 一、目的

本文件用於判斷 NFI4 原始 Shapefile 中，哪些欄位較適合歸類為樣區層級或林分層級屬性，而不是直接轉入 `trees`。

## 二、資料摘要

- 資料集：NFI4
- 檔案：`C:\Projects\forest-harvest-system\data\raw\nfi\nfi4\第四次森林資源調查Final_20250505\第四次森林資源調查Final_20250505\4th_Final_ForestryInventoryData.shp`
- 編碼：cp950
- 原始紀錄筆數：86306
- 樣區群組數：1556
- 群組欄位：樣點編號, X_Coord, Y_Coord

## 三、可能的 plot / stand attributes

| 欄位 | 分類 | 非空值 | 唯一值 | 群組內變動數 | 群組內變動比例 | 樣本值 |
|---|---|---:|---:|---:|---:|---|
| Area | constant_within_plot_group | 86306 | 3 | 0 | 0.000 | 0.05, 0.05, 0.05, 0.05, 0.05 |
| BlkID | constant_within_plot_group | 86306 | 1076 | 0 | 0.000 | 100115g_55~0093_rgb.sup/100115g_55~0092_rgb.sup, L1_A06_2009_02_11_03_22_RGBN00A.sup/L1_A06_2009_02_11_03_22_RGBB16A.sup, 081204g_59~0007_rgb.sup/081204g_59~0006_rgb.sup, 081204g_60~0106_rgb.sup/081204g_60~0105_rgb.sup, 071028g_54~0087_rgb.sup/071028g_54~0088_rgb.sup |
| BlkID_1 | constant_within_plot_group | 86306 | 1007 | 0 | 0.000 | 100115g_55~0093_rgb.sup/100115g_55~0092_rgb.sup, L1_A06_2009_02_11_03_22_RGBN00A.sup/L1_A06_2009_02_11_03_22_RGBB16A.sup, 081204g_59~0007_rgb.sup/081204g_59~0006_rgb.sup, 081204g_60~0106_rgb.sup/081204g_60~0105_rgb.sup, 071028g_54~0087_rgb.sup/071028g_54~0088_rgb.sup |
| BlockID | likely_plot_attribute | 86306 | 322 | 0 | 0.000 | 96211A03, 96211A03, 96211A05, 96211A05, 96211A02 |
| BlockID_1 | likely_plot_attribute | 86306 | 322 | 0 | 0.000 | 96211A03, 96211A03, 96211A05, 96211A05, 96211A02 |
| Closing | admin_or_qaqc_plot_level | 86306 | 15 | 0 | 0.000 | 5, 14, 8, 7, 5 |
| Crown | likely_stand_attribute | 86306 | 456 | 0 | 0.000 | 9.29, 0.0, 6.27, 5.18, 10.49 |
| DTIME | constant_within_plot_group | 86306 | 770 | 0 | 0.000 | 40955.0, 41030.0, 41375.0, 41493.0, 40865.0 |
| DTIME_1 | constant_within_plot_group | 86306 | 719 | 0 | 0.000 | 40956.0, 41036.0, 41439.0, 41446.0, 40855.0 |
| DeptID | admin_or_qaqc_plot_level | 86306 | 10 | 0 | 0.000 | 09, 01, 01, 01, 09 |
| DeptID_1 | admin_or_qaqc_plot_level | 86306 | 11 | 0 | 0.000 | 09, 01, 01, 01, 09 |
| DeptName | admin_or_qaqc_plot_level | 86306 | 10 | 0 | 0.000 | 農航所, 羅東林管處, 羅東林管處, 羅東林管處, 農航所 |
| DeptName_1 | admin_or_qaqc_plot_level | 86306 | 10 | 0 | 0.000 | 農航所, 羅東林管處, 羅東林管處, 羅東林管處, 農航所 |
| Finished | admin_or_qaqc_plot_level | 86306 | 2 | 0 | 0.000 | 1.0, 1.0, 1.0, 1.0, 1.0 |
| FrameID | likely_plot_attribute | 86306 | 1471 | 0 | 0.000 | 96211005, 96211006, 96211009, 96211010, 96211014 |
| FrameID_1 | likely_plot_attribute | 86306 | 1539 | 0 | 0.000 | 96211005, 96211006, 96211009, 96211010, 96211014 |
| FunctionTy | constant_within_plot_group | 86306 | 8 | 0 | 0.000 | 1100, 1100, 2211, 2211, 1100 |
| Height | likely_stand_attribute | 86306 | 550 | 0 | 0.000 | 24.47, 0.0, 24.37, 14.81, 26.25 |
| IPCCName | constant_within_plot_group | 86306 | 1 | 0 | 0.000 | 林地, 林地, 林地, 林地, 林地 |
| IPCCTypeID | constant_within_plot_group | 86306 | 18 | 0 | 0.000 | 1.0, 5.0, 1.0, 1.0, 1.0 |
| MajorTreeI | constant_within_plot_group | 86306 | 21 | 0 | 0.000 | A101, B600, A118, A118, A101 |
| MajorTreeP | constant_within_plot_group | 86306 | 18 | 0 | 0.000 | 80.0, 60.0, 95.0, 90.0, 90.0 |
| MergeOnly | admin_or_qaqc_plot_level | 86306 | 3 | 0 | 0.000 | -1, 1, -1, -1, -1 |
| SType | constant_within_plot_group | 86306 | 2 | 0 | 0.000 | 0.0, 0.0, 1.0, 0.0, 0.0 |
| SampleID1 | likely_plot_attribute | 86306 | 1550 | 0 | 0.000 | 96211005003, 96211006014, 96211009006, 96211010003, 96211014018 |
| SlaveTreeI | constant_within_plot_group | 86306 | 22 | 0 | 0.000 | B600, A101, B600, B600, B600 |
| SlaveTreeP | constant_within_plot_group | 86306 | 18 | 0 | 0.000 | 20.0, 40.0, 5.0, 10.0, 10.0 |
| TypeName | constant_within_plot_group | 86306 | 6 | 0 | 0.000 | 針葉樹林型, 針闊葉樹混淆林, 針葉樹林型, 針葉樹林型, 針葉樹林型 |
| UserName | admin_or_qaqc_plot_level | 86306 | 35 | 0 | 0.000 | 陳玉文, 陳淑姿, 林秀靜, 林秀靜, 陳玉文 |
| UserName_1 | admin_or_qaqc_plot_level | 86306 | 35 | 0 | 0.000 | 陳玉文, 陳淑姿, 林秀靜, 林秀靜, 陳玉文 |
| VerifyClos | admin_or_qaqc_plot_level | 86306 | 14 | 0 | 0.000 | 5.0, 0.0, 0.0, 0.0, 0.0 |
| VerifyCrow | admin_or_qaqc_plot_level | 86306 | 106 | 0 | 0.000 | 9.61, 0.0, 0.0, 0.0, 0.0 |
| VerifyDe_2 | admin_or_qaqc_plot_level | 86306 | 2 | 0 | 0.000 | 09, 0, 0, 0, 0 |
| VerifyDe_3 | admin_or_qaqc_plot_level | 86306 | 2 | 0 | 0.000 | 農航所, 0, 0, 0, 0 |
| VerifyFini | admin_or_qaqc_plot_level | 86306 | 2 | 0 | 0.000 | 1, 0, 0, 0, 0 |
| VerifyHeig | admin_or_qaqc_plot_level | 86306 | 109 | 0 | 0.000 | 24.25, 0.0, 0.0, 0.0, 0.0 |
| VerifyPass | admin_or_qaqc_plot_level | 86306 | 2 | 0 | 0.000 | 1, 1, 1, 1, 1 |
| VerifyUs_1 | admin_or_qaqc_plot_level | 86306 | 11 | 0 | 0.000 | 林雅苓, 蔡仲涵, 陳豐苙, 陳豐苙, 蔡家銘 |
| VerifyUs_2 | admin_or_qaqc_plot_level | 86306 | 5 | 0 | 0.000 | 138.0, 0.0, 0.0, 0.0, 0.0 |
| VerifyUs_3 | admin_or_qaqc_plot_level | 86306 | 5 | 0 | 0.000 | 陳玉文, 0, 0, 0, 0 |
| VerifyVolu | admin_or_qaqc_plot_level | 86306 | 1 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| Volumn | likely_stand_attribute | 86306 | 1 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| 主要地被種 | constant_within_plot_group | 86306 | 273 | 0 | 0.000 | 魚鱗蕨, 冷清草, 台灣瘤足蕨, 玉山箭竹, 玉山箭竹 |
| 備註 | constant_within_plot_group | 86306 | 1 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| 備註_1 | constant_within_plot_group | 86306 | 1 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| 含石率（％ | constant_within_plot_group | 86306 | 52 | 0 | 0.000 | 9.0, 10.0, 2.0, 2.0, 3.0 |
| 地形 | likely_plot_attribute | 86306 | 8 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| 地被密度 | constant_within_plot_group | 86306 | 6 | 0 | 0.000 | 0.0, 0.0, 0.0, 0.0, 0.0 |
| 地被高度 | constant_within_plot_group | 86306 | 8 | 0 | 0.000 | 3.0, 3.0, 3.0, 3.0, 4.0 |
| 林區 | constant_within_plot_group | 86306 | 8 | 0 | 0.000 | 1.0, 1.0, 1.0, 1.0, 1.0 |
| 林型中類 | likely_stand_attribute | 86306 | 6 | 0 | 0.000 | 針葉樹林型, 針闊葉樹混淆林, 針葉樹林型, 針葉樹林型, 針葉樹林型 |
| 林型大類 | likely_stand_attribute | 86306 | 3 | 0 | 0.000 | 天然林, 天然林, 人工林, 人工林, 天然林 |
| 林型小類 | likely_stand_attribute | 86306 | 24 | 0 | 0.000 | 天然檜木林, 針闊葉樹混淆林, 柳杉人工林, 柳杉人工林, 天然檜木林 |
| 樣區面積 | likely_plot_attribute | 86306 | 3 | 0 | 0.000 | 0.05, 0.05, 0.05, 0.05, 0.05 |
| 次要地被種 | constant_within_plot_group | 86306 | 230 | 0 | 0.000 | 台灣瘤足蕨, 闊葉樓梯草, 魚鱗蕨, 台灣瘤足蕨, 稀子蕨 |
| 海拔 | likely_plot_attribute | 86306 | 1206 | 0 | 0.000 | 2200.0, 989.0, 1695.0, 1799.0, 2165.0 |
| 腐植層厚度 | constant_within_plot_group | 86306 | 16 | 0 | 0.000 | 0.1, 0.1, 4.0, 0.3, 0.4 |
| 腐植層型態 | constant_within_plot_group | 86306 | 38 | 0 | 0.000 | 3 (地表為凋落物堆積,凋落物濕腐,下層呈腐泥狀), 3 (地表為凋落物堆積,凋落物濕腐,下層呈腐泥狀), 3 (地表為凋落物堆積,凋落物濕腐,下層呈腐泥狀), 3 (地表為凋落物堆積,凋落物濕腐,下層呈腐泥狀), 3（地表為凋落物堆積，凋落物濕腐，下層呈腐泥狀） |
| 調查人員 | constant_within_plot_group | 86306 | 31 | 0 | 0.000 | 何家名, 何家名, 葉清旺, 何家名, 葉清旺 |
| X_Coord | plot_group_key | 86306 | 170 | 0 | 0.000 | 287580, 290580, 296830, 300080, 285080 |
| Y_Coord | plot_group_key | 86306 | 317 | 0 | 0.000 | 2710045, 2709545, 2709795, 2710045, 2706545 |
| 樣點編號 | plot_group_key | 86306 | 65 | 0 | 0.000 | 003, 014, 006, 003, 018 |

## 四、在同一樣區群組內會變動的欄位

這類欄位不一定是 trees，但代表它們不是單純 plot-level constant attributes。

| 欄位 | 分類 | 非空值 | 唯一值 | 群組內變動數 | 群組內變動比例 |
|---|---|---:|---:|---:|---:|
| A木樹種 | possible_tree_field_need_review | 86306 | 324 | 1 | 0.001 |
| B木樹種 | possible_tree_field_need_review | 86306 | 328 | 1 | 0.001 |
| CO2_ha | varies_within_plot_group | 86306 | 1328 | 1 | 0.001 |
| CO2_ha1 | varies_within_plot_group | 86306 | 1545 | 1 | 0.001 |
| SBA_ha | varies_within_plot_group | 86306 | 1410 | 1 | 0.001 |
| SampleID | plot_attribute_mixed_or_subrecord | 86306 | 1557 | 1 | 0.001 |
| vol_ha | varies_within_plot_group | 86306 | 1536 | 1 | 0.001 |
| 地被型態 | varies_within_plot_group | 86306 | 8 | 1 | 0.001 |
| 坡度 | plot_attribute_mixed_or_subrecord | 86306 | 63 | 1 | 0.001 |
| 基本圖圖號 | varies_within_plot_group | 86306 | 1543 | 1 | 0.001 |
| 方位角 | varies_within_plot_group | 86306 | 344 | 1 | 0.001 |
| 株_ha | varies_within_plot_group | 86306 | 159 | 1 | 0.001 |
| 樣區BA | plot_attribute_mixed_or_subrecord | 86306 | 502 | 1 | 0.001 |
| 樣區Vol | plot_attribute_mixed_or_subrecord | 86306 | 1241 | 1 | 0.001 |
| 樣區座標X | plot_attribute_mixed_or_subrecord | 86306 | 1215 | 1 | 0.001 |
| 樣區座標Y | plot_attribute_mixed_or_subrecord | 86306 | 1406 | 1 | 0.001 |
| 樣木數 | stand_attribute_mixed_or_subrecord | 86306 | 157 | 1 | 0.001 |
| 樹冠密度 | stand_attribute_mixed_or_subrecord | 86306 | 6 | 1 | 0.001 |
| 流水號 | varies_within_plot_group | 86306 | 1557 | 1 | 0.001 |
| 系統座標X | varies_within_plot_group | 86306 | 146 | 1 | 0.001 |
| 系統座標Y | varies_within_plot_group | 86306 | 304 | 1 | 0.001 |
| 調查日期 | varies_within_plot_group | 86306 | 748 | 1 | 0.001 |
| District_O | varies_within_plot_group | 86306 | 8 | 2 | 0.001 |
| Terrain | stand_attribute_mixed_or_subrecord | 86306 | 8 | 4 | 0.003 |
| Elevation | varies_within_plot_group | 86306 | 1202 | 8 | 0.005 |
| Plot_Numbe | varies_within_plot_group | 86306 | 1564 | 8 | 0.005 |
| Aspect | varies_within_plot_group | 86306 | 344 | 9 | 0.006 |
| Plot_X | varies_within_plot_group | 86306 | 1213 | 9 | 0.006 |
| Plot_Y | varies_within_plot_group | 86306 | 1398 | 9 | 0.006 |
| Slope | varies_within_plot_group | 86306 | 63 | 9 | 0.006 |
| Survey_Dat | varies_within_plot_group | 86306 | 747 | 9 | 0.006 |
| Scientific | varies_within_plot_group | 86306 | 545 | 1521 | 0.978 |
| Tree_Chi_N | varies_within_plot_group | 86306 | 548 | 1521 | 0.978 |
| Tree_En_Na | varies_within_plot_group | 86306 | 564 | 1521 | 0.978 |
| Tree_Crown | stand_attribute_mixed_or_subrecord | 86306 | 16 | 1534 | 0.986 |
| Record_Typ | varies_within_plot_group | 86306 | 7 | 1549 | 0.996 |
| Tree_X | varies_within_plot_group | 86306 | 71700 | 1554 | 0.999 |
| Tree_Y | varies_within_plot_group | 86306 | 71689 | 1554 | 0.999 |
| X_asis | varies_within_plot_group | 86306 | 807 | 1554 | 0.999 |
| Y_axis | varies_within_plot_group | 86306 | 605 | 1554 | 0.999 |
| Branch_Hei | varies_within_plot_group | 86306 | 214 | 1555 | 0.999 |
| P_S_ | varies_within_plot_group | 29473 | 3135 | 1555 | 0.999 |
| DBH | possible_tree_field_need_review | 86306 | 1190 | 1556 | 1.000 |
| Tree_Heigh | varies_within_plot_group | 86306 | 349 | 1556 | 1.000 |
| Tree_Numbe | varies_within_plot_group | 86306 | 25402 | 1556 | 1.000 |
| Volume | stand_attribute_mixed_or_subrecord | 86306 | 27547 | 1556 | 1.000 |

## 五、初步資料工程判斷

目前不應直接將 NFI4 subrecords 轉入 `trees`。

較合理的方向是先建立正式的 plot / stand attribute table，例如：

```text
nfi4_plot_attributes
```

或：

```text
nfi4_stand_attributes
```

用於保存 Height、Volumn、Crown、林型、樣木數、樣區面積、覆蓋度等較像樣區或林分層級的資料。

## 六、下一步

1. 依本分析結果設計 `nfi4_plot_attributes` 資料表。
2. 從 `nfi4_subrecords` 聚合或抽取 plot / stand attributes。
3. 驗證每個 plot_code 是否可產生一筆或多筆 attributes。
4. trees 轉換暫停，直到確認 DBH、樹種、樣木號碼等欄位。