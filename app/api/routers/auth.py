# app/api/routers/auth.py
"""Expõe login OAuth2 password para clientes API e botão Authorize."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import auth_service
from app.api.schemas.auth import TokenResponse

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticação"])


@router.post("/token", response_model=TokenResponse)
def token(form: OAuth2PasswordRequestForm = Depends(), service=Depends(auth_service)):
    """Autentica usuário/senha enviados em formulário e devolve JWT bearer."""
    access_token = service.login(form.username, form.password)
    if access_token is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciais inválidas")
    return TokenResponse(access_token=access_token)
