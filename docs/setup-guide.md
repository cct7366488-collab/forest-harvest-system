\# 後端環境平台建構懶人包



\## 系統用途



本平台適用於：



\* 森林收穫系統

\* 森林監測平台

\* GIS 空間資料平台

\* 森林碳匯 MRV 系統

\* 樣區管理系統

\* 森林調查平台



\---



\# 一、開發環境需求



需先安裝：



1\. Python

2\. Docker Desktop

3\. Git

4\. VS Code



檢查方式：



```powershell

python --version

git --version

docker --version

docker compose version

```



\---



\# 二、專案位置



不要放在：



```text

Google Drive

OneDrive

Dropbox

```



建議：



```text

C:\\Projects

```



\---



\# 三、建立專案



```powershell

cd C:\\



mkdir Projects



cd Projects



mkdir forest-harvest-system



cd forest-harvest-system

```



\---



\# 四、建立目錄



```powershell

mkdir backend

mkdir frontend

mkdir database

mkdir gis

mkdir data

mkdir analysis

mkdir reports

mkdir docs

```



\---



\# 五、Git 初始化



```powershell

git init

```



\---



\# 六、建立 PostgreSQL + PostGIS



建立：



```text

docker-compose.yml

```



內容：



```yaml

version: '3.9'



services:

&#x20; postgres:

&#x20;   image: postgis/postgis:16-3.4



&#x20;   container\_name: forest\_postgis



&#x20;   restart: always



&#x20;   environment:

&#x20;     POSTGRES\_DB: forest\_db

&#x20;     POSTGRES\_USER: forest\_user

&#x20;     POSTGRES\_PASSWORD: forest\_password



&#x20;   ports:

&#x20;     - "5432:5432"



&#x20;   volumes:

&#x20;     - postgres\_data:/var/lib/postgresql/data



volumes:

&#x20; postgres\_data:

```



\---



\# 七、啟動 PostgreSQL



```powershell

docker compose up -d

```



檢查：



```powershell

docker ps

```



\---



\# 八、建立 FastAPI



建立 backend/app：



```powershell

mkdir backend\\app

mkdir backend\\app\\api

mkdir backend\\app\\models

mkdir backend\\app\\services

```



\---



\# 九、安裝 FastAPI



```powershell

pip install fastapi uvicorn sqlalchemy psycopg2-binary

```



\---



\# 十、啟動 FastAPI



```powershell

uvicorn app.main:app --reload

```



\---



\# 十一、測試 API



```text

http://127.0.0.1:8000

```



健康檢查：



```text

http://127.0.0.1:8000/health

```



\---



\# 十二、正式平台架構



```text

Browser

↓

FastAPI

↓

PostgreSQL

↓

PostGIS

↓

GIS Data

```



\---



\# 十三、未來擴充



後續可加入：



\* Leaflet GIS 地圖

\* GeoJSON

\* Shapefile 上傳

\* 碳匯估算

\* 材積模式

\* 單木資料管理

\* Dashboard

\* React 前端



