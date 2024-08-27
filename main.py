from fastapi import FastAPI
from core.config import settings
from routes.courses import router as course_router

app = FastAPI(name=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
app.include_router(course_router)
