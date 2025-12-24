from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db_session
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate

router = APIRouter(
    prefix="/api/v1/bank-accounts",
    tags=["bank-accounts"],
)


@router.post(
    "/",
    response_model=BankAccountCreate,
    status_code=status.HTTP_201_CREATED,
)
def create_bank_account(
    account_data: BankAccountCreate,
    session: Session = Depends(get_db_session),
) -> BankAccount:
    existing_account = (
        session.query(BankAccount)
        .filter(BankAccount.account_number == account_data.account_number)
        .first()
    )

    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account number already exists",
        )

    new_account = BankAccount(
        name=account_data.name,
        account_number=account_data.account_number,
        bank_name=account_data.bank_name,
        account_type=account_data.account_type,
        balance=account_data.balance,
    )

    session.add(new_account)
    session.commit()
    session.refresh(new_account)

    return new_account


@router.get("/")
def list_bank_accounts(session: Session = Depends(get_db_session)):
    """List all active bank accounts."""
    accounts = session.query(BankAccount).filter(BankAccount.is_active).all()
    return accounts


@router.get("/{account_id}")
def get_bank_account(
    account_id: int,
    session: Session = Depends(get_db_session),
):
    account = session.query(BankAccount).filter(BankAccount.account_id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found",
        )

    return account


@router.put("/{account_id}", response_model=BankAccountCreate)
def update_bank_account(
    account_id: int,
    account_data: BankAccountCreate,
    session: Session = Depends(get_db_session),
):
    account = session.query(BankAccount).filter(BankAccount.account_id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found",
        )

    account.name = account_data.name
    account.bank_name = account_data.bank_name
    account.account_type = account_data.account_type
    account.balance = account_data.balance

    session.commit()
    session.refresh(account)

    return account


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank_account(
    account_id: int,
    session: Session = Depends(get_db_session),
):
    account = session.query(BankAccount).filter(BankAccount.account_id == account_id).first()

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bank account not found",
        )

    account.is_active = False
    session.commit()
