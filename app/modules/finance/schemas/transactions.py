from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransactionBase(BaseModel):
    pass


class TransactionCreate(TransactionBase):
    account_id: int = Field(..., description="Id da conta associada à transação")
    category_id: int = Field(..., description="Id da categoria associada à transação")
    amount: Decimal = Field(..., description="Valor da transação")
    date: datetime = Field(..., description="Data da transação")
    description: Optional[str] = Field(
        default=None, max_length=255, description="Descrição da transação"
    )


class TransactionResponse(TransactionBase):
    id: int
    account_id: int
    category_id: int
    amount: Decimal
    date: datetime
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
