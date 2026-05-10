# NFI4 staging table 設計文件

## 一、設計目的

NFI4 原始資料共有 86,306 筆，但經前階段分析後確認，它不是單純一列一個樣區。

NFI4 比較可能是：

樣區群組
  ↓
多筆子紀錄 / 樣木 / 林分 / 驗證 / 狀態資料

因此本階段不直接將 NFI4 原始每一列匯入 trees，而是先建立 staging table：

nfi4_subrecords

用來保存 NFI4 每一筆原始子紀錄。

## 二、為何不直接匯入 trees

原因如下：

1. NFI4 原始資料不是一列一樣區。
2. NFI4 原始資料也尚未確認是否一列一棵樹。
3. 許多欄位可能是林型、驗證、狀態、樣區資訊或子紀錄資訊。
4. 若太早正規化進 trees，可能造成資料誤判。

## 三、正式資料工程策略

NFI4 raw shapefile
  ↓
nfi4_subrecords
  ↓
欄位判讀與清理
  ↓
trees / plots / other normalized tables

## 四、nfi4_subrecords 主要欄位

| 欄位 | 說明 |
|---|---|
| id | 系統主鍵 |
| plot_id | 對應 plots.id，可為 NULL |
| plot_code | 對應樣區代碼 |
| inventory_cycle | 固定為 NFI4 |
| sample_id | NFI4 樣點編號 |
| group_key | 樣點編號 + X_Coord + Y_Coord 組合鍵 |
| record_index | 原始紀錄順序 |
| x_coord | X 座標 |
| y_coord | Y 座標 |
| geom | PostGIS 點位 |
| source_file | 原始 Shapefile 路徑 |
| raw_attributes | 原始屬性資料 JSONB |
| notes | 備註 |
| created_at | 建立時間 |

## 五、目前狀態

- nfi4_subrecords 資料表已建立。
- 目前筆數為 0。
- 下一階段才會建立 NFI4 子紀錄匯入腳本。

## 六、下一步

1. 建立 NFI4 raw subrecords 匯入腳本。
2. 先匯入少量 NFI4 子紀錄測試。
3. 確認 nfi4_subrecords 與 plots 的 plot_id 關聯。
4. 再判斷哪些 raw_attributes 欄位可以轉入 trees。
5. 最後才建立正式 NFI4 trees 匯入流程。
