# app/database/connection.py
"""Abre conexões SQLite e cria o esquema técnico da aplicação.

Repositories usam a conexão; interfaces e services não executam SQL.
"""

import sqlite3
from pathlib import Path


def connect(path: Path) -> sqlite3.Connection:
    """Abre conexão com chaves de linha e integridade referencial habilitadas."""
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize(path: Path) -> None:
    """Cria tabelas e índice, sem alterar dados existentes."""
    with connect(path) as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nome_normalizado TEXT NOT NULL UNIQUE,
                preco REAL NOT NULL CHECK(preco >= 0),
                quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
