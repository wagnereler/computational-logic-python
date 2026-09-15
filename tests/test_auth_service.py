# tests/test_auth_service.py
"""Verifica hash de senha, login, JWT válido e tokens rejeitados."""

from app.core.security import create_token


def test_hash_and_login(auth_service):
    """Garante hash sem senha literal e autenticação válida/inválida."""
    user = auth_service.repository.get_by_username("admin")
    assert user.password_hash != "temporary-test-password"
    assert user.password_hash.startswith("$argon2")
    token = auth_service.login("admin", "temporary-test-password")
    assert auth_service.user_from_token(token).username == "admin"
    assert auth_service.login("admin", "wrong") is None
    assert auth_service.login("missing", "temporary-test-password") is None


def test_bad_and_expired_token(auth_service, settings):
    """Rejeita assinatura inválida e JWT já expirado."""
    assert auth_service.user_from_token("invalid") is None
    expired = create_token("admin", settings.jwt_secret_key, -1)
    assert auth_service.user_from_token(expired) is None


def test_bootstrap_preserves_existing(auth_service):
    """Não sobrescreve hash da primeira conta em reinicialização."""
    old_hash = auth_service.repository.get_by_username("admin").password_hash
    auth_service.bootstrap_admin()
    assert auth_service.repository.get_by_username("admin").password_hash == old_hash
