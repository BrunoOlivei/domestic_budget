from typing import Optional
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


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
