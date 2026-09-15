# tests/test_produto_service.py
"""Confirma regras de negócio usadas igualmente por CLI, API e web."""

import pytest

from app.services.produto_service import ProdutoError


def test_valid_product_and_normalization(product_service):
    """Aceita item válido e remove espaços redundantes do nome."""
    product = product_service.create("  Fone   sem fio  ", "19.90", 4)
    assert product.nome == "Fone sem fio"
    assert product_service.get(product.id).preco == 19.9


@pytest.mark.parametrize("fields", [(" ", 1, 1), ("Fone", -1, 1), ("Fone", 1, -1), ("Fone", "abc", 1), ("Fone", 1, 1.5)])
def test_invalid_fields(product_service, fields):
    """Rejeita nome vazio, preço inválido e quantidade não inteira ou negativa."""
    with pytest.raises(ProdutoError) as caught:
        product_service.create(*fields)
    assert caught.value.code == "invalid"


def test_duplicate_and_missing(product_service):
    """Rejeita duplicidade lógica e IDs inexistentes em update/delete."""
    product_service.create("Mouse", 20, 1)
    with pytest.raises(ProdutoError) as duplicate:
        product_service.create("mouse", 30, 2)
    assert duplicate.value.code == "duplicate"
    with pytest.raises(ProdutoError) as missing_update:
        product_service.update(999, "Mouse", 20, 1)
    assert missing_update.value.code == "not_found"
    with pytest.raises(ProdutoError) as missing_delete:
        product_service.delete(999)
    assert missing_delete.value.code == "not_found"
