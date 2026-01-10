from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.modules.finance.models.category import CategoryType


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nome da categoria (Ex: Moradia, Salário)")
    category_type: Optional[CategoryType] = Field(None, description="Tipo da categoria (Ex: income, expense)")
    parent_id: Optional[int] = Field(None, description="ID da categoria pai, se aplicável")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
