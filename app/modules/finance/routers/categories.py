from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db_session
from app.modules.finance.schemas.categories import CategoryCreate, CategoryResponse
from app.modules.finance.services.categories import CategoryService


router = APIRouter(
    prefix="/categories",
)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    session: Session = Depends(get_db_session)
):
    category_service = CategoryService(db_session=session)
    try:
        new_category = category_service.create_category(category_data)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ve),
        )
    except KeyError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )
    return new_category

@router.get(
    "/",
    response_model=list[CategoryResponse],
    status_code=status.HTTP_200_OK,
)
def list_categories(
    session: Session = Depends(get_db_session)
):
    category_service = CategoryService(db_session=session)
    categories = category_service.get_categories()

    return categories
