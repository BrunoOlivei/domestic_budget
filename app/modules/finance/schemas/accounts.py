from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class AccountBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome da conta (Ex: NuBank Principal)")
    bank_name: str = Field(..., min_length=1, max_length=100, description="Nome da instituição financeira (Ex: Nubank)")
    account_type: str = Field(..., min_length=1, max_length=100, description="Tipo da conta (Ex: Conta Corrente, Poupança)")


class AccountCreate(AccountBase):
    account_number: str | None = Field(default=None, max_length=20, description="Número da conta (Ex: 12345-6)")
    agency_number: str | None = Field(default=None, max_length=20, description="Número da agência (Ex: 0001)")
    balance: Decimal = Field(default=Decimal("0.00"), description="Saldo atual da conta")
    currency: str = Field(default="BRL", min_length=3, max_length=3, description="Moeda da conta (Ex: BRL, USD)")


class AccountResponse(AccountBase):
    account_id: int
    account_number: str | None
    agency_number: str | None
    balance: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
