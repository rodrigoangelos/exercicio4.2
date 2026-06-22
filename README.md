# Exercício 4.2 — Servidor MCP local para a aplicação de TODO list

Servidor [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) local que
expõe a API REST de tarefas do **Exercício 4.1** como ferramentas para um agente de IA.

O servidor roda via **stdio** e traduz chamadas de ferramentas MCP em requisições
HTTP para a API que está em `http://localhost:8000`.

## Arquitetura

```
Agente / cliente  ──MCP (stdio)──►  servidor_mcp.py  ──HTTP──►  API 4.1 (localhost:8000)
```

## Ferramentas expostas

| Ferramenta | Ação | Chamada na API 4.1 |
|------------|------|--------------------|
| `criar_tarefa(titulo)` | Cria uma nova tarefa | `POST /tarefas` |
| `listar_tarefas()` | Lista todas as tarefas | `GET /tarefas` |

## Pré-requisitos

A API do Exercício 4.1 **precisa estar rodando** em `http://localhost:8000`, pois as
ferramentas do MCP chamam essa API diretamente:

```bash
# no diretório do exercício 4.1
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Como executar

```bash
# 1. Criar e ativar o ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Rodar o cliente de teste (sobe o servidor via stdio automaticamente)
python cliente_teste.py
```

## Saída do cliente de teste

O `cliente_teste.py` sobe o `servidor_mcp.py`, lista as ferramentas, executa
`criar_tarefa("tarefa via mcp")` e `listar_tarefas()`, e imprime **apenas** um
envelope JSON no stdout:

```json
{
  "tools": ["criar_tarefa", "listar_tarefas"],
  "criar_resultado": {"id": 1, "titulo": "tarefa via mcp", "concluida": false},
  "listar_resultado": [{"id": 1, "titulo": "tarefa via mcp", "concluida": false}]
}
```

## Configuração

A URL da API pode ser ajustada pela variável de ambiente `API_BASE`
(padrão: `http://localhost:8000`).

## Estrutura do projeto

```
.
├── servidor_mcp.py      # servidor MCP (tools criar_tarefa e listar_tarefas)
├── cliente_teste.py     # sobe o servidor via stdio e imprime o envelope JSON
├── requirements.txt
├── README.md
└── .autograde-exercise
```
