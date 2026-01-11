from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1 import api_router
from app.core.config import settings
from app.database.db import engine, Base
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(BASE_DIR, "frontend")

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))
#okay