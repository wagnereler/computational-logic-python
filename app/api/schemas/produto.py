# app/api/schemas/produto.py
"""Contratos explícitos de entrada e saída dos endpoints de produto."""

from pydantic import BaseModel, Field


class ProdutoCreate(BaseModel):
    """Recebe campos necessários para criar produto via API."""

    nome: str
    preco: float
    quantidade: int = Field(strict=True)


class ProdutoUpdate(ProdutoCreate):
    """Recebe todos os campos para atualização integral via PUT."""


class ProdutoResponse(BaseModel):
    """Expõe dados públicos do produto, sem informação de autenticação."""

    id: int
    nome: str
    preco: float
    quantidade: int
    criado_em: str
    atualizado_em: str
