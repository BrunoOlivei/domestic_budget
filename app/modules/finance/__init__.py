from fastapi import APIRouter

from app.modules.finance.routers.accounts import router as accounts_router
from app.modules.finance.routers.categories import router as category_router

router = APIRouter(
    prefix="/api/v1/finance",
    tags=["finance"],
)


router.include_router(accounts_router)
router.include_router(category_router)
