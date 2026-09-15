# app/web/routes.py
"""Renderiza Jinja2 e usa os mesmos services da API para operar estoque.

JWT fica em cookie HttpOnly; handlers não acessam SQL nem repositories.
"""

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.produto_service import ProdutoError

base = Path(__file__).parent
templates = Jinja2Templates(directory=str(base / "templates"))
router = APIRouter()


def _user(request: Request):
    """Obtém usuário ativo de cookie JWT; retorna None se ausente ou inválido."""
    token = request.cookies.get("access_token")
    return request.app.state.auth_service.user_from_token(token) if token else None


def _protected(request: Request):
    """Retorna redirecionamento ao login quando sessão web não é válida."""
    return None if _user(request) else RedirectResponse("/login", status_code=303)


def _money(value: float) -> str:
    """Formata preço apenas para apresentação em moeda brasileira."""
    text = f"{value:,.2f}"
    return "R$ " + text.replace(",", "#").replace(".", ",").replace("#", ".")


templates.env.filters["money"] = _money


@router.get("/")
def home(request: Request):
    """Encaminha sessão ativa ao estoque e visitante ao login."""
    return RedirectResponse("/produtos" if _user(request) else "/login", status_code=303)


@router.get("/login")
def login_page(request: Request):
    """Exibe formulário de login sem dados de autenticação sensíveis."""
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
def login(request: Request, username: str = Form(), password: str = Form()):
    """Autentica com AuthService e grava JWT em cookie HttpOnly."""
    token = request.app.state.auth_service.login(username, password)
    if token is None:
        return templates.TemplateResponse(request, "login.html", {"error": "Credenciais inválidas"}, status_code=401)
    response = RedirectResponse("/produtos", status_code=303)
    settings = request.app.state.settings
    response.set_cookie("access_token", token, httponly=True, samesite="lax", secure=settings.app_env == "production", max_age=settings.access_token_expire_minutes * 60)
    return response


@router.post("/logout")
def logout(request: Request):
    """Apaga cookie de sessão e encaminha ao login."""
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("access_token")
    return response


@router.get("/produtos")
def products_page(request: Request):
    """Exibe estoque para sessão válida usando ProdutoService."""
    redirect = _protected(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "produtos.html", {"produtos": request.app.state.produto_service.list_all(), "user": _user(request)})


@router.get("/produtos/novo")
def new_page(request: Request):
    """Exibe formulário de criação somente para usuário autenticado."""
    redirect = _protected(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "produto_form.html", {"produto": None, "error": None})


@router.post("/produtos/novo")
def new_product(request: Request, nome: str = Form(), preco: str = Form(), quantidade: str = Form()):
    """Cria produto pelo service, reapresentando erros legíveis no formulário."""
    redirect = _protected(request)
    if redirect:
        return redirect
    try:
        request.app.state.produto_service.create(nome, preco.replace(",", "."), int(quantidade))
    except (ProdutoError, ValueError) as error:
        return templates.TemplateResponse(request, "produto_form.html", {"produto": None, "error": str(error) if isinstance(error, ProdutoError) else "Quantidade deve ser inteira"}, status_code=400)
    return RedirectResponse("/produtos", status_code=303)


@router.get("/produtos/{produto_id}/editar")
def edit_page(request: Request, produto_id: int):
    """Exibe dados do produto para edição ou redireciona ID inválido."""
    redirect = _protected(request)
    if redirect:
        return redirect
    try:
        produto = request.app.state.produto_service.get(produto_id)
    except ProdutoError:
        return RedirectResponse("/produtos", status_code=303)
    return templates.TemplateResponse(request, "produto_form.html", {"produto": produto, "error": None})


@router.post("/produtos/{produto_id}/editar")
def edit_product(request: Request, produto_id: int, nome: str = Form(), preco: str = Form(), quantidade: str = Form()):
    """Atualiza produto via service e informa falhas de validação."""
    redirect = _protected(request)
    if redirect:
        return redirect
    try:
        request.app.state.produto_service.update(produto_id, nome, preco.replace(",", "."), int(quantidade))
    except (ProdutoError, ValueError) as error:
        try:
            produto = request.app.state.produto_service.get(produto_id)
        except ProdutoError:
            produto = None
        return templates.TemplateResponse(request, "produto_form.html", {"produto": produto, "error": str(error) if isinstance(error, ProdutoError) else "Quantidade deve ser inteira"}, status_code=400)
    return RedirectResponse("/produtos", status_code=303)


@router.post("/produtos/{produto_id}/excluir")
def delete_product(request: Request, produto_id: int):
    """Exclui produto pelo service e retorna à listagem."""
    redirect = _protected(request)
    if redirect:
        return redirect
    try:
        request.app.state.produto_service.delete(produto_id)
    except ProdutoError:
        pass
    return RedirectResponse("/produtos", status_code=303)
