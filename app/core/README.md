# Core

Responsabilidade: configuração externa e primitivas de segurança. Pode conter leitura do ambiente com `.env` como fallback, hash Argon2 e JWT. Não deve conter SQL, páginas ou regras de estoque. Depende da biblioteca padrão, python-dotenv, PyJWT e pwdlib. Correto: `config.Settings.from_env` prioriza variáveis do processo e `security.decode_token` valida assinatura e expiração. Incorreto: definir segredo JWT literal ou consultar `usuarios` aqui.
