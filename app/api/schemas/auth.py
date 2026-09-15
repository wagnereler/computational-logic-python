# app/api/schemas/auth.py
"""Contrato de resposta do fluxo OAuth2 password com JWT."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Retorna access token e tipo bearer para clientes autorizados."""

    access_token: str
    token_type: str = "bearer"
