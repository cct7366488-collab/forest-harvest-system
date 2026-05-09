from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Forest Harvest System API Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
