from fastapi import FastAPI

from app.core import get_settings
from app.database import Base, get_database
from app.routes import bank_account_router

settings = get_settings()
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Include routers
app.include_router(bank_account_router)


@app.on_event("startup")
async def startup():
    """Initialize database on application startup."""
    db = get_database()
    # Create all tables defined in models
    Base.metadata.create_all(bind=db.engine)


@app.on_event("shutdown")
async def shutdown():
    """Close database connections on application shutdown."""
    db = get_database()
    db.close()


@app.get("/")
def hello_world():
    return {"Hello": "World!", "api_version": settings.api_version}
