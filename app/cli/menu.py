# app/cli/menu.py
"""Menu interativo acadêmico com fluxo explícito e ProdutoService compartilhado.

Entrada e mensagens ficam aqui; validação e persistência permanecem nas camadas próprias.
"""

from app.core.config import cli_database_path
from app.database.connection import initialize
from app.repositories.produto_repository import ProdutoRepository
from app.services.produto_service import ProdutoError, ProdutoService


def _money(value: float) -> str:
    """Apresenta preço em reais sem mudar o valor persistido."""
    text = f"{value:,.2f}"
    return "R$ " + text.replace(",", "#").replace(".", ",").replace("#", ".")


def _fields():
    """Lê campos do terminal; aceita vírgula no preço e inteiro na quantidade."""
    nome = input("Nome: ")
    preco = input("Preço: ").replace(",", ".")
    quantidade = int(input("Quantidade: "))
    return nome, preco, quantidade


def _add(service: ProdutoService):
    """Recebe dados do usuário e adiciona produto pelo service."""
    produto = service.create(*_fields())
    print(f"Produto {produto.id} adicionado.")


def _update(service: ProdutoService):
    """Lê identificador e novos campos, delegando atualização ao service."""
    produto_id = int(input("ID do produto: "))
    produto = service.update(produto_id, *_fields())
    print(f"Produto {produto.id} atualizado.")


def _delete(service: ProdutoService):
    """Lê identificador e solicita exclusão ao service."""
    produto_id = int(input("ID do produto: "))
    service.delete(produto_id)
    print("Produto excluído.")


def _list(service: ProdutoService):
    """Itera o estoque e mostra produtos em formato legível."""
    produtos = service.list_all()
    if not produtos:
        print("Estoque vazio.")
    for produto in produtos:
        print(f"{produto.id} - {produto.nome} - {_money(produto.preco)} - {produto.quantidade} unidade(s)")


def run():
    """Inicializa banco e executa menu while/if/elif/else até opção de saída."""
    database_path = cli_database_path()
    initialize(database_path)
    service = ProdutoService(ProdutoRepository(database_path))
    while True:
        print("\n==================================\n   SISTEMA DE CONTROLE DE ESTOQUE\n==================================")
        print("1 - Adicionar produto\n2 - Atualizar produto\n3 - Excluir produto\n4 - Visualizar estoque\n5 - Sair")
        try:
            choice = input("Opção: ").strip()
            if choice == "1":
                _add(service)
            elif choice == "2":
                _update(service)
            elif choice == "3":
                _delete(service)
            elif choice == "4":
                _list(service)
            elif choice == "5":
                print("Até logo!")
                break
            else:
                print("Opção inválida.")
        except (ProdutoError, ValueError) as error:
            print(f"Erro: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nAté logo!")
            break
