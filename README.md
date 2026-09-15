# Controle de Estoque de Eletrônicos

Projeto acadêmico de Computational Logic para controlar produtos com ID, nome, preço e quantidade. É possível adicionar, listar, consultar, atualizar e excluir produtos pela CLI, pela interface web ou pela API REST. As três interfaces compartilham o `ProdutoService`.

O fluxo é `CLI/Web/API → services → repositories → database → SQLite`. A API usa JWT; a web usa o token em cookie HttpOnly; a CLI mantém o menu interativo acadêmico sem login. Veja os READMEs em `app/` para as responsabilidades de cada camada.

Tecnologias: Python 3.13, FastAPI, Uvicorn, Pydantic, Jinja2, SQLite, PyJWT, Argon2 via pwdlib, pytest e Docker. Este é um projeto didático, sem configuração completa para produção.

## Pré-requisitos e clonagem

Use Python 3.13 como versão de referência, `pip` e Git. Docker e Docker Compose são opcionais para executar em contêineres: Linux pode usar Docker Engine com Compose Plugin; macOS e Windows podem usar Docker Desktop.

```text
git clone git@github.com:wagnereler/computational-logic-python.git
cd computational-logic-python
```

Se não usar SSH, clone por HTTPS: `git clone https://github.com/wagnereler/computational-logic-python.git`.

## Instalação local

Execute os comandos na raiz do projeto. Ative a `.venv` antes de instalar dependências e executar a aplicação.

### Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Dependendo da instalação, `python` também pode criar a `.venv`. Depois da ativação, use `python` nos demais comandos.

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se a política de execução bloquear a ativação, use o Prompt de Comando ou ajuste a política conforme as regras do seu ambiente.

### Windows CMD

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuração do ambiente

Copie `.env.example` para `.env` e edite `APP_NAME`, `APP_ENV`, `JWT_SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `DATABASE_PATH`, `ADMIN_USERNAME` e `ADMIN_PASSWORD` conforme o ambiente. `JWT_SECRET_KEY` precisa ter pelo menos 32 caracteres; escolha `ADMIN_PASSWORD` com pelo menos 5 caracteres. O exemplo deixa os segredos vazios: API, web e Docker Compose não iniciam sem eles. Não inclua `.env` no Git.

Linux e macOS:

```bash
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Windows CMD:

```bat
copy .env.example .env
```

Após editar `.env`, a aplicação carrega automaticamente o arquivo da raiz ao iniciar. Variáveis já definidas no terminal têm prioridade; as ausentes usam `.env` como fallback. Não é preciso exportar o arquivo manualmente em Linux, macOS ou Windows. Se `.env` não existir, a aplicação ainda aceita variáveis do ambiente, mas exige um segredo JWT válido para API/web.

## Executando a aplicação

Com a `.venv` ativa, escolha um comando na raiz do projeto. Em um novo terminal Linux ou macOS, por exemplo, basta executar `source .venv/bin/activate` e `fastapi run` após configurar `.env`:

```text
fastapi dev
```

`fastapi dev` é o modo de desenvolvimento local e recarrega a aplicação quando o código muda.

```text
fastapi run
```

`fastapi run` usa a CLI do FastAPI sem reload automático. Neste projeto, ambos detectam `app.main:app` a partir da raiz, sem `pyproject.toml`. O comando não configura, por si só, uma implantação completa de produção.

Como alternativa de desenvolvimento com Uvicorn diretamente:

```text
uvicorn app.main:app --reload
```

A CLI acadêmica usa o mesmo `ProdutoService` da API e da web e preserva o requisito de menu interativo. Em Linux, macOS, PowerShell ou CMD, execute:

```text
python cli.py
```

A CLI precisa apenas de `DATABASE_PATH`, cujo padrão é `data/estoque.db`; não exige as variáveis de JWT ou administrador. O menu usa `while`, `if/elif/else`, `for`, funções, tratamento de exceções e `break`.

## Endereços úteis e autenticação

Com `fastapi dev` ou Uvicorn, acesse:

| Página | Endereço |
| --- | --- |
| Web | <http://127.0.0.1:8000/> |
| Login | <http://127.0.0.1:8000/login> |
| Produtos | <http://127.0.0.1:8000/produtos> |
| Swagger/OpenAPI | <http://127.0.0.1:8000/docs> |
| ReDoc | <http://127.0.0.1:8000/redoc> |
| Saúde | <http://127.0.0.1:8000/health> |

`fastapi run` escuta em `0.0.0.0` por padrão; no próprio computador, use `localhost:8000` para acessar as mesmas rotas. Docker publica <http://localhost:8000>.

O primeiro administrador é criado a partir de `ADMIN_USERNAME` e `ADMIN_PASSWORD` quando a tabela de usuários está vazia. A senha é armazenada como hash Argon2, e a API autentica por JWT. No Swagger, use **Authorize** com as credenciais configuradas.

## Testes

Com a `.venv` ativa, execute em qualquer sistema:

```text
pytest -q
```

Para ver cada teste: `pytest -v`. A suíte usa SQLite isolado e não modifica `data/estoque.db`.

## Docker Compose

Após configurar `.env`, os comandos são os mesmos em Linux, macOS e Windows com Docker Compose disponível:

```text
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Confira <http://localhost:8000/health> no navegador e, ao terminar, execute `docker compose down`. O volume nomeado `estoque_data` preserva os dados SQLite entre reinícios. A imagem não incorpora `.env` nem o banco local; Compose passa a configuração ao contêiner e publica apenas a porta 8000.
