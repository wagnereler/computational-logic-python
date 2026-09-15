# Services

Responsabilidade: regras compartilhadas por CLI, API e web. Pode validar produto, verificar duplicidade e autenticar contas. Não deve executar SQL, usar SQLite, HTML ou `input()`. Depende de repositories, models, core e funções de segurança. Correto: `ProdutoService.create` valida e delega inserção. Incorreto: cada interface implementar sua própria regra de preço.
