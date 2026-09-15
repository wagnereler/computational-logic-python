# app/models/produto.py
"""Define a entidade Produto consumida pelo service e pelas interfaces."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Produto:
    """Representa um item persistido de estoque com identificador e datas."""

    id: int
    nome: str
    preco: float
    quantidade: int
    criado_em: str
    atualizado_em: str
