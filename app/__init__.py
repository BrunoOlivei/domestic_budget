from fastapi import FastAPI, Depends

from app.core.core import get_settings
from app.core.database import get_database
from app.utils.exception_handlers import configure_exception_handlers
from app.modules.finance import router as finance_routers

settings = get_settings()


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    dependencies=[Depends(get_database)],
)

configure_exception_handlers(app)


app.include_router(finance_routers)
