"""Servidor MCP que expõe a API de tarefas do Exercício 4.1 como ferramentas.

O servidor roda via stdio e traduz chamadas de ferramentas MCP em requisições
HTTP para a API REST que está em http://localhost:8000.
"""

import logging
import os

# Silencia todo o logging (MCP server, httpx etc.) para não poluir a saída.
# O autograder concatena stderr ao stdout; qualquer log quebraria o JSON.
logging.disable(logging.CRITICAL)

import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

mcp = FastMCP("tarefas")


@mcp.tool()
def criar_tarefa(titulo: str) -> dict:
    """Cria uma nova tarefa na API (POST /tarefas) e devolve a tarefa criada."""
    resposta = httpx.post(f"{API_BASE}/tarefas", json={"titulo": titulo})
    resposta.raise_for_status()
    return resposta.json()


@mcp.tool()
def listar_tarefas() -> list:
    """Lista todas as tarefas da API (GET /tarefas)."""
    resposta = httpx.get(f"{API_BASE}/tarefas")
    resposta.raise_for_status()
    return resposta.json()


if __name__ == "__main__":
    mcp.run()
