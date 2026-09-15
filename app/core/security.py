# app/core/security.py
"""Aplica hash Argon2 e tokens JWT usando bibliotecas consolidadas.

O serviço de autenticação usa estas funções sem conhecer detalhes criptográficos.
"""

from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

_password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Produz hash irreversível da senha recebida para persistência."""
    return _password_hash.hash(password)


def verify_password(password: str, stored_hash: str) -> bool:
    """Compara senha informada com hash persistido, retornando sucesso ou falha."""
    return _password_hash.verify(password, stored_hash)


def create_token(username: str, secret: str, minutes: int) -> str:
    """Emite JWT HS256 com sujeito e expiração; requer segredo externo."""
    expires = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    return jwt.encode({"sub": username, "exp": expires}, secret, algorithm="HS256")


def decode_token(token: str, secret: str) -> str:
    """Valida assinatura e expiração; rejeita JWT sem sujeito válido."""
    payload = jwt.decode(token, secret, algorithms=["HS256"])
    username = payload.get("sub")
    if not isinstance(username, str) or not username:
        raise jwt.InvalidTokenError("Sujeito inválido")
    return username
