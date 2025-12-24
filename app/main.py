from fastapi import FastAPI

from app.core import get_settings
from app.database import get_database
from app.routes import bank_account_router

settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    dependecies=[get_database],
)


app.include_router(bank_account_router)

@app.get("/")
def hello_world():
    return {"Hello": "World!", "api_version": settings.api_version}
