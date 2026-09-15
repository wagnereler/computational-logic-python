# tests/test_fix001_config.py
"""Verifica configuração mínima da CLI e título FastAPI sem enfraquecer JWT."""

from pathlib import Path

import pytest

from app.cli.menu import run
from app.core.config import Settings, cli_database_path
from app.main import create_app


def test_cli_uses_only_database_path(monkeypatch, tmp_path, capsys):
    """Executa menu até sair sem JWT ou administrador, usando banco temporário."""
    path = tmp_path / "cli.db"
    monkeypatch.setenv("DATABASE_PATH", str(path))
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("ADMIN_USERNAME", raising=False)
    monkeypatch.delenv("ADMIN_PASSWORD", raising=False)
    monkeypatch.setattr("builtins.input", lambda prompt: "5")
    run()
    assert path.exists()
    assert "Até logo!" in capsys.readouterr().out


def test_cli_default_database_path(monkeypatch):
    """Retorna caminho padrão sem consultar variáveis de autenticação."""
    monkeypatch.delenv("DATABASE_PATH", raising=False)
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    assert cli_database_path() == Path("data/estoque.db")


@pytest.mark.parametrize("secret", [None, "short"])
def test_api_settings_reject_missing_or_short_secret(monkeypatch, secret):
    """Mantém rejeição de segredo JWT ausente ou menor que 32 caracteres."""
    if secret is None:
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    else:
        monkeypatch.setenv("JWT_SECRET_KEY", secret)
    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings.from_env()


def test_app_name_from_environment_without_jwt(monkeypatch):
    """Reflete APP_NAME no FastAPI e OpenAPI sem validar JWT na importação/factory."""
    monkeypatch.setenv("APP_NAME", "Estoque da Faculdade")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    application = create_app()
    assert application.title == "Estoque da Faculdade"
    assert application.openapi()["info"]["title"] == "Estoque da Faculdade"


def test_explicit_settings_keep_title(settings, monkeypatch):
    """Preserva título do factory de testes mesmo com APP_NAME externo diferente."""
    monkeypatch.setenv("APP_NAME", "Outro título")
    assert create_app(settings).title == settings.app_name
