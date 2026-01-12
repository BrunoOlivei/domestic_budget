from sqlalchemy.orm import Session

from app.modules.finance.models.transactions import Transactions
from app.modules.finance.schemas.transactions import TransactionCreate
from app.modules.finance.services.categories import CategoryService
from app.modules.finance.services.accounts import AccountService

class TransactionService:
    def __init__(self, db_session: Session) -> None:
        self.db_session = db_session
        self.category_service = CategoryService(db_session)
        self.account_service = AccountService(db_session)

    def create_transaction(self, transaction_data: TransactionCreate) -> Transactions:
        """
        Create a new transaction in the database.

        Args:
            transaction_data (TransactionCreate): The data for the new transaction.

        Returns:
            Transactions: The newly created transaction record.
        """
        if transaction_data.amount <= 0:
            raise ValueError("Transaction amount must be positive")

        if transaction_data.account_id is None or transaction_data.category_id is None:
            raise ValueError("Account ID and Category ID must be provided")

        account = self.account_service.get_account_by_id(transaction_data.account_id)

        if category := self.category_service.get_category_by_id(transaction_data.category_id):
            if category.category_type == "EXPENSE":
                account.balance -= transaction_data.amount
            elif category.category_type == "INCOME":
                account.balance += transaction_data.amount
            else:
                raise ValueError("Invalid category type")
        else:
            raise KeyError("Category not found")


        new_transaction = Transactions(**transaction_data.model_dump())
        self.db_session.add(new_transaction)
        self.db_session.add(account)
        self.db_session.commit()
        self.db_session.refresh(new_transaction)
        return new_transaction
