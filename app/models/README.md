# Models

Responsabilidade: representar entidades Produto e Usuario. Pode conter dataclasses e tipos de domínio. Não deve executar SQL, chamar `input()` ou renderizar HTML. Depende só da biblioteca padrão. Correto: `Produto` guarda ID e campos persistidos. Incorreto: método `Produto.salvar()` abrir conexão SQLite.
