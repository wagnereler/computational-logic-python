# app/services/auth_service.py
"""Autentica contas ativas e inicializa administrador usando configuração externa.

Repositories acessam usuários; funções de segurança cuidam do hash e do JWT.
"""

import jwt

from app.core.config import Settings
from app.core.security import create_token, decode_token, hash_password, verify_password
from app.repositories.usuario_repository import UsuarioRepository


class AuthService:
    """Compartilha autenticação JWT entre API e interface web."""

    def __init__(self, repository: UsuarioRepository, settings: Settings):
        """Recebe persistência e configuração sem embutir credenciais."""
        self.repository = repository
        self.settings = settings

    def bootstrap_admin(self) -> None:
        """Cria primeira conta somente quando banco vazio e credenciais fornecidas."""
        if self.repository.count():
            return
        if not self.settings.admin_username or not self.settings.admin_password:
            raise ValueError("Defina ADMIN_USERNAME e ADMIN_PASSWORD para o primeiro uso")
        if len(self.settings.admin_password) < 5:
            raise ValueError("ADMIN_PASSWORD deve ter pelo menos 5 caracteres")
        self.repository.create(self.settings.admin_username, hash_password(self.settings.admin_password))

    def login(self, username: str, password: str) -> str | None:
        """Emite JWT para credenciais válidas de conta ativa; retorna None caso contrário."""
        user = self.repository.get_by_username(username)
        if not user or not user.ativo or not verify_password(password, user.password_hash):
            return None
        return create_token(user.username, self.settings.jwt_secret_key, self.settings.access_token_expire_minutes)

    def user_from_token(self, token: str):
        """Valida JWT e conta ativa; retorna usuário ou None em falha."""
        try:
            username = decode_token(token, self.settings.jwt_secret_key)
        except jwt.InvalidTokenError:
            return None
        user = self.repository.get_by_username(username)
        return user if user and user.ativo else None
