from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.modules.finance.schemas.accounts import (
    AccountCreate,
    AccountResponse,
    AccountUpdate,
)
from app.modules.finance.services.accounts import AccountService

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
        account_created = account_service.create_account(account_data)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(ve),
        )

    return account_created


@router.get(
    "/",
    response_model=List[AccountResponse],
    status_code=status.HTTP_200_OK,
)
def get_accounts(
    session: Session = Depends(get_db_session),
):
    account_service = AccountService(db_session=session)
    accounts = account_service.get_accounts()

    return accounts


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
)
def get_account_by_id(
    account_id: int,
    session: Session = Depends(get_db_session),
):
    account_service = AccountService(db_session=session)
    try:
        account = account_service.get_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )

    return account


@router.patch(
    "/{account_id}",
    response_model=AccountResponse,
    status_code=status.HTTP_200_OK,
)
def update_account(
    account_id: int,
    account_data: AccountUpdate,
    session: Session = Depends(get_db_session),
):
    account_service = AccountService(db_session=session)
    try:
        account_updated = account_service.update_account(account_id, account_data)
        if not account_updated:
            raise ValueError("Account not found")
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )

    return account_updated


@router.delete(
    "/{account_id}",
    status_code=status.HTTP_200_OK,
    response_model=AccountResponse,
)
def delete_account(
    account_id: int,
    session: Session = Depends(get_db_session),
):
    account_service = AccountService(db_session=session)
    try:
        account_deactivated = account_service.deactivate_account(account_id)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve),
        )

    return account_deactivated
