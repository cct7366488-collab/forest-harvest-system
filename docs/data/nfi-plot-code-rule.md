# NFI3 / NFI4 plot_code 正式判定規則

## 一、NFI3

經唯一性分析，NFI3 的 PLOT_ID 與 PLOT_ 皆具唯一性。

正式規則：

- original_plot_id = PLOT_ID
- plot_code = NFI3-{PLOT_ID}

## 二、NFI4

NFI4 原始資料共有 86,306 筆，並非單純一列一樣區，而是樣區或樣點群組下包含多筆子紀錄。

經組合欄位分析，建議以：

樣點編號 + X_Coord + Y_Coord

作為樣區層級分組依據。

正式規則：

- original_plot_id = 樣點編號
- plot_code = NFI4-{樣點編號}-{X_Coord}-{Y_Coord}

## 三、匯入原則

1. NFI3：一筆原始資料視為一個樣區。
2. NFI4：需先依 樣點編號 + X_Coord + Y_Coord 分組後再匯入 plots。
3. plots 只儲存樣區層級資料。
4. NFI4 的多筆子紀錄未來應進一步判斷是否匯入 trees 或其他調查明細表。
5. 本規則已用少量樣區資料測試，NFI3 匯入 5 筆，NFI4 匯入 5 筆。
