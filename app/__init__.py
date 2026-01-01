from fastapi import FastAPI

from app.core.core import get_settings
from app.core.database import get_database
# from app.modules.finance import finance_routes

settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    dependecies=[get_database],
)

# app.include_router(*finance_routes)
