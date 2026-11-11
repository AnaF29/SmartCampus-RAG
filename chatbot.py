"""Chatbot RAG com Function Calling (Claude) integrado ao banco relacional."""
import json
import os
import sys
import anthropic
from dotenv import load_dotenv

import db
import rag_bridge

load_dotenv()
MODEL = os.getenv("MODEL", "claude-sonnet-5-5")
_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic()
    return _client

SYSTEM = """Você é o SmartCampus, assistente acadêmico de uma instituição de ensino.
Regras:
- Para perguntas sobre conteúdo, provas, cronograma ou regras, use a ferramenta buscar_documentos
  e responda APENAS com base nos trechos retornados. Cite a fonte (nome do arquivo).
- Para notas, média ou boletim do aluno, use as ferramentas de banco de dados. Nunca invente notas.
- Se a informação não estiver nos documentos, diga que não encontrou.
- Perguntas compostas exigem usar mais de uma ferramenta.
- Responda em português, de forma clara e objetiva."""

TOOLS = [
    {
        "name": "buscar_documentos",
        "description": "Busca trechos em plano de ensino, materiais de aula e regulamento (RAG/ChromaDB).",
        "input_schema": {
            "type": "object",
            "properties": {"consulta": {"type": "string", "description": "Texto da busca semântica"}},
            "required": ["consulta"],
        },
    },
    {
        "name": "consultar_media",
        "description": "Retorna a média e as notas do aluno logado em uma disciplina.",
        "input_schema": {
            "type": "object",
            "properties": {"nome_disciplina": {"type": "string", "description": "Ex.: Banco de Dados, Inteligência Artificial"}},
            "required": ["nome_disciplina"],
        },
    },
    {
        "name": "gerar_boletim",
        "description": "Gera o boletim completo (todas as disciplinas) do aluno logado.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "listar_alertas",
        "description": "Lista alertas de média baixa do aluno logado.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "abrir_chamado",
        "description": "Registra uma dúvida/chamado para a secretaria ou professor em nome do aluno logado.",
        "input_schema": {
            "type": "object",
            "properties": {"pergunta": {"type": "string", "description": "Texto da dúvida ou solicitação"}},
            "required": ["pergunta"],
        },
    },
]


def executar_ferramenta(nome, args, ra):
    """O RA vem da sessão (nunca do modelo), evitando acesso a dados de outro aluno."""
    try:
        if nome == "buscar_documentos":
            return rag_bridge.buscar(args["consulta"])
        if nome == "consultar_media":
            return db.consultar_media(ra, args["nome_disciplina"])
        if nome == "gerar_boletim":
            return db.gerar_boletim(ra)
        if nome == "listar_alertas":
            return db.listar_alertas(ra)
        if nome == "abrir_chamado":
            return db.abrir_chamado(ra, args["pergunta"])
        return {"erro": f"Ferramenta desconhecida: {nome}"}
    except Exception as e:  # devolve o erro ao modelo em vez de quebrar o chat
        return {"erro": str(e)}


def responder(historico, pergunta, ra, aluno_nome, on_tool=None):
    """Adiciona a pergunta ao histórico, roda o loop de tool use e devolve o texto final."""
    historico.append({"role": "user", "content": pergunta})
    system = SYSTEM + f"\nAluno logado: {aluno_nome} (RA {ra})."
    while True:
        resp = get_client().messages.create(
            model=MODEL, max_tokens=1500, system=system, tools=TOOLS, messages=historico
        )
        historico.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":
            return "".join(b.text for b in resp.content if b.type == "text")
        resultados = []
        for b in resp.content:
            if b.type == "tool_use":
                if on_tool:
                    on_tool(b.name, b.input)
                out = executar_ferramenta(b.name, b.input, ra)
                resultados.append({
                    "type": "tool_result",
                    "tool_use_id": b.id,
                    "content": json.dumps(out, default=str, ensure_ascii=False),
                })
        historico.append({"role": "user", "content": resultados})


if __name__ == "__main__":
    ra = sys.argv[1] if len(sys.argv) > 1 else "2026001"
    nome = next((a["nome"] for a in db.listar_alunos() if a["ra"] == ra), ra)
    print(f"SmartCampus — logado como {nome} ({ra}). Digite 'sair' para encerrar.\n")
    hist = []
    while True:
        p = input("Você: ").strip()
        if p.lower() in {"sair", "exit"}:
            break
        print("\nSmartCampus:", responder(hist, p, ra, nome, lambda n, a: print(f"  [ferramenta] {n} {a}")), "\n")
