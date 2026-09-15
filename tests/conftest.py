# tests/conftest.py
"""Fornece banco SQLite temporário e aplicação inicializada para testes isolados."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.database.connection import initialize
from app.main import create_app
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auth_service import AuthService
from app.services.produto_service import ProdutoService


@pytest.fixture
def settings(tmp_path: Path):
    """Cria configuração de teste sem acessar data/estoque.db."""
    return Settings("Estoque Teste", "test", "test-secret-with-at-least-thirty-two-characters", 30, tmp_path / "estoque-test.db", "admin", "temporary-test-password")


@pytest.fixture
def product_repository(settings):
    """Inicializa esquema no banco temporário e devolve repository de produtos."""
    initialize(settings.database_path)
    return ProdutoRepository(settings.database_path)


@pytest.fixture
def product_service(product_repository):
    """Fornece service de produto com persistência isolada."""
    return ProdutoService(product_repository)


@pytest.fixture
def auth_service(settings):
    """Cria conta inicial isolada e devolve service de autenticação."""
    initialize(settings.database_path)
    service = AuthService(UsuarioRepository(settings.database_path), settings)
    service.bootstrap_admin()
    return service


@pytest.fixture
def client(settings):
    """Inicializa lifespan FastAPI em banco temporário e fecha cliente após teste."""
    with TestClient(create_app(settings)) as test_client:
        yield test_client
