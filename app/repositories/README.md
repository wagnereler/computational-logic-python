# Repositories

Responsabilidade: consultas e CRUD parametrizados, convertendo linhas em entidades. Pode conter SQL e mapeamento de `sqlite3.Row`. Não deve validar formulários, imprimir mensagens ou decidir status HTTP. Depende de database e models. Correto: `get_by_id` usa `WHERE id = ?`. Incorreto: montar SQL por interpolação ou chamar `input()`.
