# Core

Responsabilidade: configuração externa e primitivas de segurança. Pode conter leitura de ambiente, hash Argon2 e JWT. Não deve conter SQL, páginas ou regras de estoque. Depende apenas de biblioteca padrão, PyJWT e pwdlib. Correto: `security.decode_token` valida assinatura e expiração. Incorreto: definir segredo JWT literal ou consultar `usuarios` aqui.
