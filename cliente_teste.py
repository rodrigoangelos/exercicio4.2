"""Cliente de teste do servidor MCP.

Sobe o servidor_mcp.py via stdio, lista as ferramentas expostas, executa
criar_tarefa("tarefa via mcp") e listar_tarefas(), e imprime no stdout um
único envelope JSON com os resultados.

Atenção: apenas JSON é escrito no stdout (nada de logs), para que o
autograder consiga fazer o parse da saída.
"""

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _bloco_unico(resultado):
    """Faz o parse de um CallToolResult que devolve um único objeto JSON."""
    return json.loads(resultado.content[0].text)


def _lista_de_blocos(resultado):
    """Faz o parse de um CallToolResult que devolve uma lista.

    O servidor MCP serializa cada item da lista como um bloco de conteúdo
    separado; aqui juntamos todos os blocos de volta em um array. Blocos
    vazios (lista sem itens) são ignorados.
    """
    itens = []
    for bloco in resultado.content:
        texto = getattr(bloco, "text", "")
        if texto and texto.strip():
            itens.append(json.loads(texto))
    return itens


async def main() -> None:
    parametros = StdioServerParameters(
        command=sys.executable,
        args=["servidor_mcp.py"],
    )

    async with stdio_client(parametros) as (leitura, escrita):
        async with ClientSession(leitura, escrita) as sessao:
            await sessao.initialize()

            ferramentas = await sessao.list_tools()
            nomes_tools = [t.name for t in ferramentas.tools]

            criar = await sessao.call_tool(
                "criar_tarefa", {"titulo": "tarefa via mcp"}
            )
            criar_resultado = _bloco_unico(criar)

            listar = await sessao.call_tool("listar_tarefas", {})
            listar_resultado = _lista_de_blocos(listar)

    envelope = {
        "tools": nomes_tools,
        "criar_resultado": criar_resultado,
        "listar_resultado": listar_resultado,
    }
    print(json.dumps(envelope, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
