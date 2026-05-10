from fastapi import FastAPI
from app.api.plots import router as plots_router

app = FastAPI(
    title="Forest Harvest System API",
    description="森林收穫與森林資源調查資料平台 API",
    version="0.1.0"
)


@app.get('/')
def root():
    return {"message": "Forest Harvest System API Running"}


@app.get('/health')
def health():
    return {"status": "healthy"}


app.include_router(plots_router)
