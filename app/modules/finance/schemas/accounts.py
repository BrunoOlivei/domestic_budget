from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.modules.finance.models.accounts import AccountTypeEnum


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome da conta (Ex: NuBank Principal)")
    bank_name: str = Field(..., min_length=1, max_length=100, description="Nome da instituição financeira (Ex: Nubank)")
    account_type: AccountTypeEnum = Field(..., description="Tipo da conta (Ex: checking, savings, credit, investment, cash)")


class AccountCreate(AccountBase):
    account_number: Optional[str] = Field(default=None, max_length=20, description="Número da conta (Ex: 12345-6)")
    agency_number: Optional[str] = Field(default=None, max_length=20, description="Número da agência (Ex: 0001)")
    balance: Decimal = Field(default=Decimal("0.00"), description="Saldo atual da conta")
    currency: str = Field(default="BRL", min_length=3, max_length=3, description="Moeda da conta (Ex: BRL, USD)")


class AccountResponse(AccountBase):
    id: int
    account_number: Optional[str]
    agency_number: Optional[str]
    balance: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
