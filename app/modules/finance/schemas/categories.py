from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

from app.modules.finance.models.categories import CategoryType


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome da categoria (Ex: Moradia, Salário)")
    parent_id: Optional[int] = Field(None, description="ID da categoria pai, se aplicável")


class CategoryCreate(CategoryBase):
    category_type: Optional[CategoryType] = Field(None, description="Tipo da categoria (Ex: income, expense)")


class CategoryResponse(CategoryBase):
    id: int
    category_type: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
