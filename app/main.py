# app/main.py
"""Monta FastAPI, inicializa SQLite e liga interfaces aos mesmos services.

O factory permite banco temporário em testes sem tocar data/estoque.db.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routers import auth, produtos
from app.core.config import Settings, app_name_from_env
from app.database.connection import initialize
from app.repositories.produto_repository import ProdutoRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auth_service import AuthService
from app.services.produto_service import ProdutoService
from app.web.routes import router as web_router


def create_app(settings: Settings | None = None) -> FastAPI:
    """Cria aplicação configurável, inicializando banco e administrador no lifespan."""
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        """Cria esquema e primeira conta antes de atender requisições."""
        configuration = settings or Settings.from_env()
        initialize(configuration.database_path)
        application.state.settings = configuration
        application.state.produto_service = ProdutoService(ProdutoRepository(configuration.database_path))
        application.state.auth_service = AuthService(UsuarioRepository(configuration.database_path), configuration)
        application.state.auth_service.bootstrap_admin()
        yield

    application = FastAPI(title=settings.app_name if settings else app_name_from_env(), lifespan=lifespan)
    application.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "web" / "static")), name="static")
    application.include_router(auth.router)
    application.include_router(produtos.router)
    application.include_router(web_router)

    @application.get("/health", tags=["Saúde"])
    def health():
        """Informa disponibilidade HTTP local para Docker e monitoramento simples."""
        return {"status": "ok"}

    return application


app = create_app()
