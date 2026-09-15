# AGENTS.md

## Objetivo do projeto

Este repositório contém o trabalho acadêmico da disciplina Computational Logic.

O sistema deve implementar um controle de estoque para uma loja de eletrônicos utilizando Python.

Além dos requisitos acadêmicos obrigatórios, o projeto utilizará:

- FastAPI;
- API REST;
- documentação OpenAPI/Swagger;
- autenticação JWT;
- interface web com templates;
- SQLite;
- Docker;
- Docker Compose;
- interface CLI para preservar o requisito de menu interativo do trabalho.

A solução deve continuar simples, didática e explicável pelo aluno.

---

## Git

Nunca execute automaticamente:

- `git commit`;
- `git push`;
- `git merge`;
- `git rebase`;
- `git tag`;
- criação de release;
- alteração de branch.

Um pedido para implementar uma funcionalidade NÃO constitui autorização para commit.

Após qualquer implementação:

1. execute os testes;
2. execute as validações;
3. mostre `git status`;
4. apresente resumo do diff;
5. sugira título e corpo para o commit;
6. pare e aguarde autorização explícita do usuário.

Somente execute `git commit` quando o usuário autorizar explicitamente o commit após revisar o resultado.

Push, merge, tag e release também exigem autorização explícita separada.

---

## Padrão documental dos arquivos Python

Todo arquivo `.py` deve possuir na primeira linha seu caminho relativo ao repositório.

Exemplo:

    # app/services/produto_service.py

Logo após essa linha deve existir uma docstring de módulo detalhando:

- finalidade do arquivo;
- responsabilidade dentro da arquitetura;
- interação com outras camadas, quando aplicável.

Exemplo:

    # app/services/produto_service.py
    """
    Serviço responsável pelas regras de negócio relacionadas aos produtos.

    Este módulo valida os dados recebidos pelas interfaces e coordena
    operações executadas pelo repository.
    """

Toda função ou método deve possuir docstring específica informando, conforme aplicável:

- finalidade;
- parâmetros;
- retorno;
- exceções relevantes;
- efeitos colaterais importantes.

Evitar docstrings genéricas.

---

## README por camada

Cada camada deve possuir seu próprio `README.md`.

O README da camada deve informar:

1. responsabilidade da camada;
2. o que pode existir nela;
3. o que não deve existir nela;
4. dependências permitidas;
5. exemplos corretos;
6. exemplos incorretos.

Os documentos devem refletir a implementação real.

---

## Arquitetura

A separação de responsabilidades deve ser preservada.

Fluxo principal:

    Interfaces
       |
       v
    Services
       |
       v
    Repositories
       |
       v
    Database
       |
       v
    SQLite

Interfaces previstas:

- CLI;
- API REST;
- interface Web.

### Database

Responsável por:

- conexão SQLite;
- inicialização do banco;
- configuração técnica da persistência.

Não deve conter:

- regras de negócio;
- entrada do usuário;
- lógica de apresentação.

### Models

Responsável pelas entidades do domínio.

Não deve:

- acessar banco diretamente;
- executar SQL;
- interagir com o usuário.

### Repositories

Responsável exclusivamente pelo acesso aos dados.

Deve:

- utilizar SQL parametrizado;
- encapsular CRUD;
- converter dados persistidos em objetos do domínio quando aplicável.

Não deve:

- utilizar `input()`;
- imprimir mensagens de interface;
- implementar regras de negócio.

### Services

Responsável pelas regras de negócio.

Exemplos:

- validação de nome;
- validação de preço;
- validação de quantidade;
- duplicidade;
- autenticação;
- autorização.

Não deve:

- executar SQL diretamente;
- acessar SQLite diretamente;
- implementar HTML;
- utilizar `input()`.

### API

Responsável por:

- endpoints REST;
- schemas de entrada e saída;
- status HTTP;
- dependências de autenticação;
- integração com os services.

A API não deve acessar repositories ou banco diretamente quando houver service correspondente.

### Web

Responsável pela interface HTML.

Utilizar templates simples.

Não deve conter regras de negócio ou SQL.

### CLI

Responsável pelo menu interativo exigido no trabalho acadêmico.

Deve utilizar:

- `while`;
- `if / elif / else`;
- `for`, quando aplicável;
- funções;
- tratamento de exceções;
- `break`.

A CLI deve delegar regras de negócio aos services.

---

## API e Swagger

Utilizar FastAPI.

A aplicação deve expor documentação automática em:

    /docs

e:

    /redoc

Utilizar schemas explícitos para entrada e saída da API.

Não expor informações sensíveis na documentação.

---

## Autenticação

Utilizar JWT.

Requisitos mínimos:

- endpoint de login;
- geração de access token;
- validação do token;
- proteção dos endpoints privados;
- senha nunca armazenada em texto puro.

Não implementar criptografia ou algoritmo JWT manualmente se existir biblioteca consolidada e adequada.

Segredos devem vir de configuração externa.

---

## Segurança

Nunca versionar:

- senhas;
- tokens;
- chaves JWT;
- secrets;
- arquivos `.env`;
- banco SQLite real;
- credenciais;
- certificados privados.

Nunca imprimir segredos em logs ou saídas de diagnóstico.

Criar `.env.example` contendo somente nomes de variáveis e valores seguros de exemplo.

---

## SQLite

O banco de desenvolvimento deve ficar em:

    data/estoque.db

O arquivo `.db` não deve ser versionado.

Os testes não devem utilizar o banco real.

Preferir SQLite temporário ou isolado nos testes.

---

## Docker

O projeto deve possuir:

- `Dockerfile`;
- `docker-compose.yml`;
- `.dockerignore`.

Regras:

- utilizar imagem oficial Python;
- não copiar `.env`;
- não copiar banco local;
- não copiar caches;
- não incorporar segredos na imagem;
- persistir `data/` usando volume;
- expor somente as portas necessárias;
- manter a imagem simples.

Validar:

    docker compose config

e, quando possível:

    docker compose build

Não publicar imagens em registry sem autorização explícita.

---

## Dependências

Manter `requirements.txt`.

Adicionar somente dependências realmente utilizadas.

Não adicionar bibliotecas apenas por conveniência quando a biblioteca padrão resolver adequadamente.

Dependências devem ser justificáveis pela arquitetura.

---

## Testes

O projeto deve possuir testes automatizados para as partes relevantes.

Cobrir, no mínimo:

- repositories;
- services;
- autenticação;
- endpoints principais da API.

Os testes não devem depender do banco SQLite de produção/desenvolvimento.

Antes de considerar uma tarefa concluída, executar a suíte de testes.

---

## Qualidade

Priorizar:

- simplicidade;
- legibilidade;
- separação de responsabilidades;
- nomes coerentes;
- funções pequenas;
- baixo acoplamento;
- código explicável no contexto acadêmico.

Evitar:

- abstrações artificiais;
- complexidade sem necessidade;
- arquitetura excessiva;
- duplicação de lógica;
- regras de negócio nas interfaces.

---

## Finalização de tarefas

Antes de encerrar qualquer implementação:

1. executar testes;
2. executar validações sintáticas;
3. executar `git diff --check`;
4. executar `git status --short`;
5. confirmar que nenhum segredo foi incluído;
6. confirmar que nenhum `.db` foi versionado;
7. apresentar resumo dos arquivos alterados;
8. sugerir título e corpo do commit;
9. parar sem criar commit.
