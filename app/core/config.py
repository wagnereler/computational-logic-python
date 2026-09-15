# app/core/config.py
"""Lê a configuração externa usada por autenticação e persistência.

Combina ambiente do processo e .env da raiz sem modificar os.environ;
testes podem criar instâncias isoladas ou fornecer Settings explícito.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


def _env_values() -> dict[str, str | None]:
    """Lê .env da raiz quando existe; retorna vazio se o arquivo estiver ausente."""
    return dotenv_values(ENV_FILE) if ENV_FILE.is_file() else {}


def _setting(name: str, values: dict[str, str | None], default: str | None = None) -> str | None:
    """Devolve variável do processo antes do valor do arquivo e do padrão."""
    return os.environ.get(name, values.get(name) if values.get(name) is not None else default)


def app_name_from_env() -> str:
    """Obtém título da API sem exigir JWT durante a criação da aplicação."""
    return _setting("APP_NAME", _env_values(), "Controle de Estoque") or "Controle de Estoque"


@dataclass(frozen=True)
class Settings:
    """Agrupa parâmetros externos necessários à inicialização da aplicação."""

    app_name: str
    app_env: str
    jwt_secret_key: str
    access_token_expire_minutes: int
    database_path: Path
    admin_username: str | None
    admin_password: str | None

    @classmethod
    def from_env(cls) -> "Settings":
        """Combina processo e .env; valida JWT e não altera variáveis globais."""
        values = _env_values()
        secret = _setting("JWT_SECRET_KEY", values, "") or ""
        if len(secret) < 32:
            raise ValueError("JWT_SECRET_KEY deve conter pelo menos 32 caracteres")
        return cls(
            _setting("APP_NAME", values, "Controle de Estoque") or "Controle de Estoque",
            _setting("APP_ENV", values, "development") or "development",
            secret,
            int(_setting("ACCESS_TOKEN_EXPIRE_MINUTES", values, "30") or "30"),
            Path(_setting("DATABASE_PATH", values, "data/estoque.db") or "data/estoque.db"),
            _setting("ADMIN_USERNAME", values),
            _setting("ADMIN_PASSWORD", values),
        )


def cli_database_path() -> Path:
    """Lê somente o caminho SQLite da CLI, sem exigir configurações de autenticação."""
    return Path(os.environ.get("DATABASE_PATH", "data/estoque.db"))
