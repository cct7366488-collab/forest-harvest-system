from fastapi import FastAPI
from app.api.plots import router as plots_router
from app.api.species import router as species_router
from app.api.trees import router as trees_router
from app.api.volume_models import router as volume_models_router
from app.api.height_models import router as height_models_router

app = FastAPI(
    title='Forest Harvest System API',
    description='森林收穫與森林資源調查資料平台 API',
    version='0.2.0'
)

@app.get('/')
def root():
    return {'message': 'Forest Harvest System API Running'}

@app.get('/health')
def health():
    return {'status': 'healthy'}

app.include_router(plots_router)
app.include_router(species_router)
app.include_router(trees_router)
app.include_router(volume_models_router)
app.include_router(height_models_router)
