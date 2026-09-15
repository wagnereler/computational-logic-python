# app/repositories/usuario_repository.py
"""Persiste usuários e consulta contas para o serviço de autenticação."""

from pathlib import Path

from app.database.connection import connect
from app.models.usuario import Usuario


def _usuario(row) -> Usuario | None:
    """Converte linha SQLite em usuário de domínio ou None."""
    return Usuario(row["id"], row["username"], row["password_hash"], bool(row["ativo"]), row["criado_em"]) if row else None


class UsuarioRepository:
    """Isola consultas e inserção de conta do serviço de autenticação."""

    def __init__(self, path: Path):
        """Recebe banco SQLite externo, evitando banco real nos testes."""
        self.path = path

    def count(self) -> int:
        """Retorna número de contas para decidir criação inicial no service."""
        with connect(self.path) as db:
            return db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]

    def get_by_username(self, username: str) -> Usuario | None:
        """Busca conta por nome de usuário e retorna None quando ausente."""
        with connect(self.path) as db:
            return _usuario(db.execute("SELECT * FROM usuarios WHERE username = ?", (username,)).fetchone())

    def create(self, username: str, password_hash: str) -> Usuario:
        """Persiste somente hash e retorna usuário recém-criado."""
        with connect(self.path) as db:
            db.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
        return self.get_by_username(username)
