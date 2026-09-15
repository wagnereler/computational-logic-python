# app/api/routers/produtos.py
"""Traduz operações do ProdutoService em respostas REST protegidas."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.api.dependencies import current_user, produto_service
from app.api.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services.produto_service import ProdutoError

router = APIRouter(prefix="/api/v1/produtos", tags=["Produtos"], dependencies=[Depends(current_user)])


def _http_error(error: ProdutoError) -> HTTPException:
    """Mapeia erro de domínio para 400, 404 ou 409 sem stack trace."""
    code = {"invalid": 400, "not_found": 404, "duplicate": 409}[error.code]
    return HTTPException(code, str(error))


@router.get("", response_model=list[ProdutoResponse])
def list_products(service=Depends(produto_service)):
    """Lista produtos para usuário autenticado."""
    return service.list_all()


@router.get("/{produto_id}", response_model=ProdutoResponse)
def get_product(produto_id: int, service=Depends(produto_service)):
    """Consulta ID e devolve 404 quando produto não existe."""
    try:
        return service.get(produto_id)
    except ProdutoError as error:
        raise _http_error(error) from None


@router.post("", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProdutoCreate, service=Depends(produto_service)):
    """Cria produto validado pelo service e devolve 201 ou erro de domínio."""
    try:
        return service.create(data.nome, data.preco, data.quantidade)
    except ProdutoError as error:
        raise _http_error(error) from None


@router.put("/{produto_id}", response_model=ProdutoResponse)
def update_product(produto_id: int, data: ProdutoUpdate, service=Depends(produto_service)):
    """Atualiza produto integralmente e devolve entidade ou erro adequado."""
    try:
        return service.update(produto_id, data.nome, data.preco, data.quantidade)
    except ProdutoError as error:
        raise _http_error(error) from None


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(produto_id: int, service=Depends(produto_service)):
    """Exclui produto e devolve 204 quando operação foi concluída."""
    try:
        service.delete(produto_id)
    except ProdutoError as error:
        raise _http_error(error) from None
    return Response(status_code=status.HTTP_204_NO_CONTENT)
