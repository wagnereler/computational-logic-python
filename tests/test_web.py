# tests/test_web.py
"""Cobre páginas essenciais e proteção por cookie JWT na interface web."""


def test_web_login_and_protection(client):
    """Exibe login, redireciona anônimo e abre estoque com sessão HttpOnly."""
    assert client.get("/login").status_code == 200
    assert client.get("/produtos", follow_redirects=False).headers["location"] == "/login"
    response = client.post("/login", data={"username": "admin", "password": "temporary-test-password"}, follow_redirects=False)
    assert response.status_code == 303
    assert "httponly" in response.headers["set-cookie"].lower()
    assert client.get("/produtos").status_code == 200
    assert client.get("/produtos/novo").status_code == 200
    assert client.get("/static/css/app.css").status_code == 200
