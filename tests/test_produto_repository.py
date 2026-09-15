# tests/test_produto_repository.py
"""Verifica CRUD parametrizado e conversão de produtos do repository."""


def test_repository_crud(product_repository):
    """Cria, busca, lista, atualiza e exclui sem tocar banco de desenvolvimento."""
    product = product_repository.create("Notebook", 3500, 2)
    assert product.id > 0
    assert product_repository.get_by_id(product.id).nome == "Notebook"
    assert product_repository.get_by_name("notebook").id == product.id
    assert len(product_repository.list_all()) == 1
    updated = product_repository.update(product.id, "Mouse", 45, 3)
    assert (updated.nome, updated.preco, updated.quantidade) == ("Mouse", 45, 3)
    assert product_repository.delete(product.id)
    assert product_repository.get_by_id(product.id) is None
    assert not product_repository.delete(product.id)
