from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.finance.services.accounts import AccountService
from app.modules.finance.schemas.accounts import AccountCreate, AccountResponse


router = APIRouter(
    prefix="/accounts",
)


@router.post(
    "/",
    response_model=AccountResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    account_data: AccountCreate,
    session: Session = Depends(get_db_session),
):
    account_service = AccountService(db_session=session)
    try:
        new_account = account_service.create_account(account_data)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ve),
        )

    return new_account
