# tests/test_fix001_config.py
"""Verifica CLI, fallback do .env e Settings explícito sem enfraquecer JWT."""

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

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
def test_api_settings_reject_missing_or_short_secret(monkeypatch, tmp_path, secret):
    """Mantém rejeição de segredo JWT ausente ou menor que 32 caracteres."""
    monkeypatch.setattr("app.core.config.ENV_FILE", tmp_path / ".env")
    if secret is None:
        monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
    else:
        monkeypatch.setenv("JWT_SECRET_KEY", secret)
    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings.from_env()


def test_settings_load_from_env_file(monkeypatch, tmp_path):
    """Lê dados do arquivo isolado sem exportá-los para o processo."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=Estoque do arquivo\n"
        "JWT_SECRET_KEY=secret-from-file-with-at-least-thirty-two-characters\n"
        "DATABASE_PATH=isolated.db\n"
        "ADMIN_USERNAME=professor\n"
        "ADMIN_PASSWORD=example-password\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.core.config.ENV_FILE", env_file)
    for name in ("APP_NAME", "JWT_SECRET_KEY", "DATABASE_PATH", "ADMIN_USERNAME", "ADMIN_PASSWORD"):
        monkeypatch.delenv(name, raising=False)

    configuration = Settings.from_env()
    assert configuration.app_name == "Estoque do arquivo"
    assert configuration.database_path == Path("isolated.db")
    assert configuration.admin_username == "professor"
    assert "JWT_SECRET_KEY" not in os.environ
    assert create_app().title == "Estoque do arquivo"


def test_process_environment_precedes_env_file(monkeypatch, tmp_path):
    """Prefere valores do processo para título, JWT e caminho SQLite."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "APP_NAME=Nome do arquivo\n"
        "JWT_SECRET_KEY=secret-from-file-with-at-least-thirty-two-characters\n"
        "DATABASE_PATH=file.db\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.core.config.ENV_FILE", env_file)
    monkeypatch.setenv("APP_NAME", "Nome do processo")
    monkeypatch.setenv("JWT_SECRET_KEY", "process-secret-with-at-least-thirty-two-characters")
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "process.db"))

    configuration = Settings.from_env()
    assert configuration.app_name == "Nome do processo"
    assert configuration.jwt_secret_key == "process-secret-with-at-least-thirty-two-characters"
    assert configuration.database_path == tmp_path / "process.db"
    assert create_app().title == "Nome do processo"


def test_short_process_secret_is_not_replaced_by_file(monkeypatch, tmp_path):
    """Rejeita segredo curto do processo mesmo com JWT válido no arquivo."""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "JWT_SECRET_KEY=secret-from-file-with-at-least-thirty-two-characters\n",
        encoding="utf-8",
    )
    monkeypatch.setattr("app.core.config.ENV_FILE", env_file)
    monkeypatch.setenv("JWT_SECRET_KEY", "short")
    with pytest.raises(ValueError, match="JWT_SECRET_KEY"):
        Settings.from_env()


def test_no_file_and_no_secret_still_fail(monkeypatch, tmp_path):
    """Rejeita JWT ausente quando .env também não existe."""
    monkeypatch.setattr("app.core.config.ENV_FILE", tmp_path / ".env")
    monkeypatch.delenv("JWT_SECRET_KEY", raising=False)
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
    """Usa Settings explícito e banco isolado mesmo com .env e ambiente divergentes."""
    monkeypatch.setattr("app.core.config.ENV_FILE", settings.database_path.parent / ".env")
    (settings.database_path.parent / ".env").write_text("JWT_SECRET_KEY=short\n", encoding="utf-8")
    monkeypatch.setenv("APP_NAME", "Outro título")
    application = create_app(settings)
    assert application.title == settings.app_name
    with TestClient(application) as client:
        assert client.get("/health").status_code == 200
        assert application.state.settings is settings
