# Forest Harvest System 平台整合架構

## 一、平台定位

Forest Harvest System 是森林收穫、森林監測、GIS 空間資料與後續碳匯 MRV 分析的整合型平台。

本平台目前採用四層整合架構：

1. 本機開發環境
2. GitHub
3. Firebase
4. Obsidian

---

## 二、本機開發環境

正式本機專案位置：

C:\Projects\forest-harvest-system

用途：

- FastAPI 後端開發
- Docker Compose 管理
- PostgreSQL / PostGIS 本機資料庫
- Python 分析模組
- GIS 處理腳本
- Markdown 文件管理

---

## 三、GitHub

GitHub Repository：

https://github.com/cct7366488-collab/forest-harvest-system

用途：

- 程式碼版本控制
- 文件版本控制
- 雲端備份
- 團隊協作
- 未來 GitHub Pages 文件展示

---

## 四、Firebase

Firebase Project ID：

forestry-rs-monitor

用途規劃：

- 使用者登入驗證
- Firestore 應用資料
- 工作狀態資料
- 前端平台狀態
- 系統通知資料

注意：

Firebase 不取代 PostgreSQL / PostGIS。

Firebase 主要管理應用層資料；PostgreSQL / PostGIS 管理正式 GIS 空間資料。

---

## 五、Obsidian

Obsidian Vault Path：

C:\ObsidianVaults\ForestHarvestSystem

用途：

- 開工 / 收工紀錄
- 專案筆記
- 教學筆記
- 架構設計
- 資料庫設計
- Markdown 知識庫

下一次開工時，優先讀取：

C:\ObsidianVaults\ForestHarvestSystem\readme.md

---

## 六、正式分工

| 平台 | 角色 |
|---|---|
| C:\Projects | 正式本機開發區 |
| GitHub | 程式碼與文件版本控制 |
| Firebase | 應用資料與使用者服務 |
| Obsidian | 專案知識庫與工作紀錄 |
| PostgreSQL / PostGIS | GIS 空間資料核心 |

---

## 七、收工流程

當使用者輸入「收工」時，應完成：

1. 更新本機 Markdown 文件
2. 更新 Obsidian readme.md 與 worklog
3. 更新 Firebase 專案狀態資料
4. git add / commit / push 到 GitHub

---

## 八、開工流程

當使用者輸入「開工」時，應完成：

1. 優先讀取 Obsidian readme.md
2. 確認本機專案狀態
3. 確認 GitHub 同步狀態
4. 確認 Firebase Project ID
5. 接續上次未完成工作
