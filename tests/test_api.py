# tests/test_api.py
"""Exercita saúde, documentação, login e CRUD REST protegido."""


def _headers(client):
    """Obtém token de teste por fluxo OAuth2 e devolve header bearer."""
    response = client.post("/api/v1/auth/token", data={"username": "admin", "password": "temporary-test-password"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_health_and_docs(client):
    """Confirma endpoint público e documentação Swagger/ReDoc/OpenAPI."""
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/docs").status_code == 200
    assert client.get("/redoc").status_code == 200
    assert client.get("/openapi.json").status_code == 200


def test_api_auth_and_crud(client):
    """Bloqueia anônimo e percorre criação, lista, consulta, update e delete."""
    assert client.get("/api/v1/produtos").status_code == 401
    assert client.post("/api/v1/auth/token", data={"username": "admin", "password": "wrong"}).status_code == 401
    headers = _headers(client)
    created = client.post("/api/v1/produtos", json={"nome": "Teclado", "preco": 89, "quantidade": 2}, headers=headers)
    assert created.status_code == 201
    product_id = created.json()["id"]
    assert len(client.get("/api/v1/produtos", headers=headers).json()) == 1
    assert client.get(f"/api/v1/produtos/{product_id}", headers=headers).status_code == 200
    assert client.put(f"/api/v1/produtos/{product_id}", json={"nome": "Teclado", "preco": 99, "quantidade": 3}, headers=headers).json()["preco"] == 99
    assert client.delete(f"/api/v1/produtos/{product_id}", headers=headers).status_code == 204
    assert client.get(f"/api/v1/produtos/{product_id}", headers=headers).status_code == 404


def test_api_errors(client):
    """Confirma 400, 409 e 422 sem expor stack trace."""
    headers = _headers(client)
    assert client.post("/api/v1/produtos", json={"nome": " ", "preco": 1, "quantidade": 1}, headers=headers).status_code == 400
    assert client.post("/api/v1/produtos", json={"nome": "Mouse", "preco": 1, "quantidade": 1}, headers=headers).status_code == 201
    assert client.post("/api/v1/produtos", json={"nome": "mouse", "preco": 1, "quantidade": 1}, headers=headers).status_code == 409
    assert client.post("/api/v1/produtos", json={"nome": "Outro", "preco": 1, "quantidade": "x"}, headers=headers).status_code == 422
