from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, Field


T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, description="Indica se a requesição foi processada com sucesso ou falha")
    message: str = Field(default="", description="Mensagem de contexto (sucesso ou erro)")
    data: Optional[T] = Field(default=None, description="Dados do retorno ou detalhes do erro")


class StandardListResponse(BaseModel, Generic[T]):
    success: bool = Field(default=True, description="Indica se a requesição foi processada com sucesso ou falha")
    message: str = Field(default="", description="Mensagem de contexto (sucesso ou erro)")
    data: List[T] = Field(default=[], description="Dados do retorno ou detalhes do erro")
