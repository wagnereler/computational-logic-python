# API

Responsabilidade: contratos Pydantic, endpoints REST e autenticação bearer/OpenAPI. Pode converter erros de domínio em HTTP e declarar schemas de entrada/saída. Não deve executar SQL, abrir SQLite ou persistir diretamente. Depende de FastAPI, schemas e services disponibilizados por `app.state`. Correto: `POST /api/v1/produtos` chama `ProdutoService.create`. Incorreto: router executar `INSERT INTO produtos`.
