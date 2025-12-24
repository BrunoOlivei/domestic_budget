from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.core import get_settings


settings = get_settings()

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    account_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    bank_name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="BRL", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(tz=settings.time_zone), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(tz=settings.time_zone), onupdate=datetime.now(tz=settings.time_zone), nullable=False
    )

    def __repr__(self) -> str:
        return f"<BankAccount(id={self.id}, name={self.name}, balance={self.balance})>"
