# app/core/config.py
"""Lê a configuração externa usada por autenticação e persistência.

Não fornece valores secretos embutidos; testes podem criar instâncias isoladas.
"""

import os
from dataclasses import dataclass
from pathlib import Path


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
        """Obtém parâmetros do ambiente e falha quando o segredo JWT está ausente."""
        secret = os.environ.get("JWT_SECRET_KEY", "")
        if len(secret) < 32:
            raise ValueError("JWT_SECRET_KEY deve conter pelo menos 32 caracteres")
        return cls(
            os.environ.get("APP_NAME", "Controle de Estoque"),
            os.environ.get("APP_ENV", "development"),
            secret,
            int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            Path(os.environ.get("DATABASE_PATH", "data/estoque.db")),
            os.environ.get("ADMIN_USERNAME"),
            os.environ.get("ADMIN_PASSWORD"),
        )


def cli_database_path() -> Path:
    """Lê somente o caminho SQLite da CLI, sem exigir configurações de autenticação."""
    return Path(os.environ.get("DATABASE_PATH", "data/estoque.db"))
