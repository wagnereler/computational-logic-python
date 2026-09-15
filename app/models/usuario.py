# app/models/usuario.py
"""Define usuário autenticável sem misturar SQL ou apresentação."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Usuario:
    """Representa conta persistida; o hash nunca é exposto por schemas HTTP."""

    id: int
    username: str
    password_hash: str
    ativo: bool
    criado_em: str
