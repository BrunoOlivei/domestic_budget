from sqlalchemy.orm import Session

from app.modules.finance.models.accounts import Accounts
from app.modules.finance.schemas.accounts import AccountCreate


class AccountService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def create_account(self, account_data: AccountCreate) -> Accounts:
        existing_account = (
            self.db_session.query(Accounts)
            .filter(Accounts.account_number == account_data.account_number)
            .first()
        )

        if existing_account:
            raise ValueError("Account with this account number already exists")

        new_account = Accounts(**account_data.model_dump())

        self.db_session.add(new_account)
        self.db_session.commit()
        self.db_session.refresh(new_account)

        return new_account
