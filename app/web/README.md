# Web

Responsabilidade: páginas Jinja2, CSS e fluxo de sessão com cookie JWT. Pode renderizar formulários e traduzir erros do service para texto. Não deve executar SQL, usar repository diretamente ou duplicar validação de preço. Depende de FastAPI/Jinja2 e services em `app.state`. Correto: rota `/produtos/novo` chama `ProdutoService.create`. Incorreto: template conter segredo JWT ou `INSERT`.
