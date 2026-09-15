# app/repositories/produto_repository.py
"""Encapsula CRUD SQL parametrizado e converte linhas em Produto.

O service decide validações; este módulo apenas persiste e consulta dados.
"""

import sqlite3
from pathlib import Path

from app.database.connection import connect
from app.models.produto import Produto


def _produto(row) -> Produto | None:
    """Converte linha SQLite em entidade ou retorna None quando ausente."""
    return Produto(row["id"], row["nome"], row["preco"], row["quantidade"], row["criado_em"], row["atualizado_em"]) if row else None


class UniqueNameError(Exception):
    """Informa violação técnica do índice único ao service, sem mensagem de interface."""


class ProdutoRepository:
    """Executa operações de produtos em banco indicado, sem regras de interface."""

    def __init__(self, path: Path):
        """Recebe caminho SQLite, permitindo banco isolado em testes."""
        self.path = path

    def create(self, nome: str, preco: float, quantidade: int) -> Produto:
        """Insere produto e devolve entidade persistida; pode propagar erro de unicidade."""
        try:
            with connect(self.path) as db:
                cursor = db.execute("INSERT INTO produtos (nome, nome_normalizado, preco, quantidade) VALUES (?, ?, ?, ?)", (nome, nome.casefold(), preco, quantidade))
                produto_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            raise UniqueNameError from None
        return self.get_by_id(produto_id)

    def get_by_id(self, produto_id: int) -> Produto | None:
        """Consulta produto por identificador e retorna None se inexistente."""
        with connect(self.path) as db:
            return _produto(db.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone())

    def get_by_name(self, nome: str) -> Produto | None:
        """Consulta nome sem diferenciar caixa, retornando entidade ou None."""
        with connect(self.path) as db:
            return _produto(db.execute("SELECT * FROM produtos WHERE nome_normalizado = ?", (nome.casefold(),)).fetchone())

    def list_all(self) -> list[Produto]:
        """Lista estoque em ordem de identificador crescente."""
        with connect(self.path) as db:
            return [_produto(row) for row in db.execute("SELECT * FROM produtos ORDER BY id")]

    def update(self, produto_id: int, nome: str, preco: float, quantidade: int) -> Produto | None:
        """Atualiza campos e data; devolve None quando ID não existe."""
        try:
            with connect(self.path) as db:
                cursor = db.execute("UPDATE produtos SET nome = ?, nome_normalizado = ?, preco = ?, quantidade = ?, atualizado_em = CURRENT_TIMESTAMP WHERE id = ?", (nome, nome.casefold(), preco, quantidade, produto_id))
                if cursor.rowcount == 0:
                    return None
        except sqlite3.IntegrityError:
            raise UniqueNameError from None
        return self.get_by_id(produto_id)

    def delete(self, produto_id: int) -> bool:
        """Remove produto por ID e informa se alguma linha foi excluída."""
        with connect(self.path) as db:
            return db.execute("DELETE FROM produtos WHERE id = ?", (produto_id,)).rowcount > 0
