# app/api/dependencies.py
"""Fornece services e aplica autenticação bearer às rotas privadas.

O esquema OAuth2 aponta para o endpoint real e habilita Authorize no Swagger.
"""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def produto_service(request: Request):
    """Retorna service de estoque associado à aplicação atual."""
    return request.app.state.produto_service


def auth_service(request: Request):
    """Retorna service de autenticação associado à aplicação atual."""
    return request.app.state.auth_service


def current_user(token: str = Depends(oauth2_scheme), service=Depends(auth_service)):
    """Exige JWT válido e conta ativa; devolve 401 em qualquer falha."""
    user = service.user_from_token(token)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas", headers={"WWW-Authenticate": "Bearer"})
    return user
