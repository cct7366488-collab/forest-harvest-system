# NFI4 subrecords 少量匯入測試

## 一、目的

本文件記錄 NFI4 原始子紀錄匯入 nfi4_subrecords staging table 的少量測試結果。

## 二、資料工程策略

NFI4 原始資料不直接匯入 trees，而是先保存到 staging table：

nfi4_subrecords

原因是 NFI4 原始資料並非單純一列一樣區，也尚未確認一列是否等於一棵樣木。

## 三、匯入腳本

analysis/scripts/import_nfi4_subrecords_sample.py

## 四、匯入邏輯

1. 讀取 NFI4 Shapefile。
2. 使用 cp950 / big5 / utf-8 / latin1 編碼 fallback。
3. 取得 樣點編號、X_Coord、Y_Coord。
4. 組成 plot_code：

NFI4-{樣點編號}-{X_Coord}-{Y_Coord}

5. 以 plot_code 對應 plots.id。
6. 將每筆 NFI4 原始屬性完整存入 raw_attributes JSONB。
7. 寫入 nfi4_subrecords。

## 五、測試結果

本次少量匯入結果：

- nfi4_subrecords 匯入筆數：20
- 對應 plot_code：NFI4-003-287580.0-2710045.0
- 對應 plot_id：13
- sample_id：003
- x_coord：287580.0
- y_coord：2710045.0

## 六、目前判讀

本階段已確認 NFI4 子紀錄可以成功保存到 nfi4_subrecords，且可以與 plots 資料表建立 plot_id 關聯。

但目前尚不能直接判定每一筆 nfi4_subrecords 都等於一棵樣木。

後續需要再分析 raw_attributes 中哪些欄位真正屬於 trees 樣木層級。

## 七、下一步

1. 分析 nfi4_subrecords.raw_attributes 中可轉入 trees 的欄位。
2. 建立 NFI4 subrecords → trees 欄位對應表。
3. 建立 trees 轉換腳本。
4. 測試產生少量 trees 紀錄。
5. 驗證 trees.plot_id 與 plots.id 關聯。
