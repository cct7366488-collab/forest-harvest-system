# Obsidian 整合設定

## Vault Path

C:\ObsidianVaults\ForestHarvestSystem

## 開工讀取檔案

C:\ObsidianVaults\ForestHarvestSystem\readme.md

## 平台角色

Obsidian 在 Forest Harvest System 中定位為專案知識庫與工作筆記本。

## 用途

- 開工紀錄
- 收工紀錄
- 工作日誌
- 教學筆記
- 平台架構
- 資料庫設計
- AI 協作開發紀錄

## 目錄結構

ForestHarvestSystem
├── readme.md
├── worklog
├── integration
├── database
└── teaching

## 開工流程

當使用者輸入「開工」時，優先讀取：

C:\ObsidianVaults\ForestHarvestSystem\readme.md

並據此恢復上次工作進度。

## 收工流程

當使用者輸入「收工」時，需更新：

1. readme.md
2. worklog
3. integration 文件
4. 下一次待辦事項
