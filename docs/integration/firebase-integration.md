# Firebase 整合設定

## Firebase Project ID

forestry-rs-monitor

## 平台角色

Firebase 在 Forest Harvest System 中定位為應用層資料與使用者服務平台。

## 預計用途

- Authentication：使用者登入與權限管理
- Firestore：應用層資料、任務狀態、工作紀錄摘要
- Hosting：未來前端展示或管理介面部署
- 系統設定：平台狀態、功能旗標、操作紀錄

## 與 PostgreSQL / PostGIS 的分工

Firebase 不取代 PostgreSQL / PostGIS。

PostgreSQL / PostGIS 負責：

- GIS 空間資料
- 樣區資料
- 單木資料
- 林班小班資料
- 空間查詢與分析

Firebase 負責：

- 使用者
- 權限
- 即時狀態
- 前端互動資料
- 工作紀錄摘要

## 後續工作

1. 建立 Firebase 專案設定檔。
2. 設計 Firestore collections。
3. 建立 project_status collection。
4. 建立 work_logs collection。
5. 與 FastAPI 或前端進行整合。
