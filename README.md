# Forest Harvest System

森林收穫與 GIS 平台

## 技術架構

- FastAPI
- PostgreSQL
- PostGIS
- Docker

## 啟動 PostgreSQL

`powershell
docker compose up -d
uvicorn app.main:app --reload
@"
