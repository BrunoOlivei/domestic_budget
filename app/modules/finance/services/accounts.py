from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.modules.finance.models.accounts import Accounts
from app.modules.finance.schemas.accounts import AccountCreate, AccountUpdate


class AccountService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session

    def get_accounts(self) -> List[Accounts]:
        """
        Retrieve all accounts from the database.

        Returns:
            List[Accounts]: A list of all account records.
        """
        return self.db_session.query(Accounts).all()

    def get_account_by_id(self, account_id: int) -> Accounts:
        """
        Retrieve a single account by its ID.

        Args:
            account_id (int): The ID of the account to retrieve.

        Returns:
            Accounts: The account record with the specified ID.
        """
        try:
            account = (
                self.db_session.query(Accounts)
                .filter(Accounts.id == account_id)
                .first()
            )
            if not account:
                raise ValueError("Account not found")
            return account
        except Exception as e:
            raise e

    def get_account_by_number(self, account_number: str) -> Optional[Accounts]:
        """
        Retrieve a single account by its account number.

        Args:
            account_number (str): The account number of the account to retrieve.

        Returns:
            Accounts: The account record with the specified account number.
        """
        try:
            account = (
                self.db_session.query(Accounts)
                .filter(Accounts.account_number == account_number)
                .first()
            )
            if not account:
                return None
            return account
        except Exception as e:
            raise e

    def create_account(self, account_data: AccountCreate) -> Accounts:
        """
        Create a new account in the database, ensuring no duplicate account numbers exist.

        Args:
            account_data (AccountCreate): The data for the new account.

        Returns:
            Accounts: The newly created account record.
        """
        if account_data.account_number:
            existing_account = self.get_account_by_number(account_data.account_number)

            if existing_account and existing_account.is_active:
                raise ValueError("Account with this account number already exists")

            if existing_account and not existing_account.is_active:
                existing_account.is_active = True
                existing_account.deleted_at = None
                for field, value in account_data.model_dump(exclude_unset=True).items():
                    setattr(existing_account, field, value)

                self.db_session.commit()
                self.db_session.refresh(existing_account)

                return existing_account

        new_account = Accounts(**account_data.model_dump())

        self.db_session.add(new_account)
        self.db_session.commit()
        self.db_session.refresh(new_account)

        return new_account

    def update_account(self, account_id: int, account_data: AccountUpdate) -> Accounts:
        """
        Update an existing account's details.

        Args:
            account_id (int): The ID of the account to update.
            account_data (AccountCreate): The updated data for the account.

        Returns:
            Accounts: The updated account record.
        """
        account = self.get_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        if account_data.account_number:
            account_by_account_number = self.get_account_by_number(account_data.account_number)
            if account_by_account_number and account_by_account_number.id != account_id:
                raise ValueError("Another account with this account number already exists")

        for field, value in account_data.model_dump(exclude_unset=True).items():
            setattr(account, field, value)

        self.db_session.commit()
        self.db_session.refresh(account)

        return account

    def deactivate_account(self, account_id: int) -> Accounts:
        """
        Deactivate an account by setting its is_active flag to False and updating the deleted_at timestamp.

        Args:
            account_id (int): The ID of the account to delete.
        """
        account = self.get_account_by_id(account_id)
        if not account:
            raise ValueError("Account not found")

        account.is_active = False
        account.deleted_at = datetime.now()
        self.db_session.commit()
        self.db_session.refresh(account)

        return account
