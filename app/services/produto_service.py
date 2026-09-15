# app/services/produto_service.py
"""Centraliza validação e operações de estoque compartilhadas pelas interfaces.

Somente o repository acessa SQLite; erros de domínio são convertidos em HTTP na API.
"""

import math

from app.repositories.produto_repository import ProdutoRepository, UniqueNameError


class ProdutoError(Exception):
    """Erro de domínio com código para apresentação coerente nas interfaces."""

    def __init__(self, code: str, message: str):
        """Registra categoria e mensagem segura para o usuário."""
        self.code = code
        super().__init__(message)


class ProdutoService:
    """Aplica as mesmas regras de produto para CLI, API e web."""

    def __init__(self, repository: ProdutoRepository):
        """Recebe repository para persistir produtos validados."""
        self.repository = repository

    def _validate(self, nome, preco, quantidade):
        """Normaliza nome e valida números; levanta ProdutoError em dados inválidos."""
        if not isinstance(nome, str) or not nome.strip():
            raise ProdutoError("invalid", "Nome é obrigatório")
        nome = " ".join(nome.split())
        try:
            preco = float(preco)
        except (TypeError, ValueError):
            raise ProdutoError("invalid", "Preço deve ser numérico") from None
        if not math.isfinite(preco) or preco < 0:
            raise ProdutoError("invalid", "Preço deve ser não negativo e finito")
        if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade < 0:
            raise ProdutoError("invalid", "Quantidade deve ser inteira e não negativa")
        return nome, preco, quantidade

    def create(self, nome, preco, quantidade):
        """Cria produto válido, rejeitando nome já usado mesmo com outra caixa."""
        nome, preco, quantidade = self._validate(nome, preco, quantidade)
        if self.repository.get_by_name(nome):
            raise ProdutoError("duplicate", "Produto com este nome já existe")
        try:
            return self.repository.create(nome, preco, quantidade)
        except UniqueNameError:
            raise ProdutoError("duplicate", "Produto com este nome já existe") from None

    def get(self, produto_id: int):
        """Retorna produto existente ou levanta erro de não encontrado."""
        produto = self.repository.get_by_id(produto_id)
        if produto is None:
            raise ProdutoError("not_found", "Produto não encontrado")
        return produto

    def list_all(self):
        """Retorna todos os produtos pela ordem definida no repository."""
        return self.repository.list_all()

    def update(self, produto_id, nome, preco, quantidade):
        """Atualiza produto existente após validar campos e unicidade lógica."""
        self.get(produto_id)
        nome, preco, quantidade = self._validate(nome, preco, quantidade)
        duplicate = self.repository.get_by_name(nome)
        if duplicate and duplicate.id != produto_id:
            raise ProdutoError("duplicate", "Produto com este nome já existe")
        try:
            return self.repository.update(produto_id, nome, preco, quantidade)
        except UniqueNameError:
            raise ProdutoError("duplicate", "Produto com este nome já existe") from None

    def delete(self, produto_id):
        """Exclui produto existente ou levanta erro de não encontrado."""
        if not self.repository.delete(produto_id):
            raise ProdutoError("not_found", "Produto não encontrado")
