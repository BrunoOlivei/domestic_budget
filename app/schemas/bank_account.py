from pydantic import BaseModel, Field


class BankAccountCreate(BaseModel):
    id: int | None = None
    name: str = Field(..., min_length=1, max_length=100)
    bank_name: str = Field(..., min_length=1, max_length=100)
    account_number: str = Field(..., min_length=1, max_length=20)
    agency_number: str = Field(..., min_length=1, max_length=10)
    account_type: str = Field(..., min_length=1, max_length=50)
    balance: float = Field(default=0.0, ge=0)
    created_at: str | None = None
    updated_at: str | None = None

    class Config:
        from_attributes = True
