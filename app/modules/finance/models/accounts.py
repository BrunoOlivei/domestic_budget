from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Boolean, DateTime, Numeric, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.base import Base


class AccountTypeEnum(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    INVESTMENT = "investment"
    CASH = "cash"


class Accounts(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[AccountTypeEnum] = mapped_column(String(20), nullable=False)
    account_number: Mapped[str] = mapped_column(String(20), nullable=True)
    agency_number: Mapped[str] = mapped_column(String(20), nullable=True)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(18, 2), default=0.00, nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), default="BRL", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<BankAccount(id={self.account_id}, name={self.name}, balance={self.balance}), currency={self.currency}>"
