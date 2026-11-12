"""Chatbot RAG com Function Calling (Gemini) integrado ao banco relacional."""
import json
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

import db
import rag_bridge

load_dotenv()
MODEL = os.getenv("MODEL", "gemini-3.5-flash-lite")
MAX_RODADAS = 6  # limite de chamadas de ferramenta por pergunta
_client = None


def get_client():
    """Cria o cliente uma vez só. A chave vem de GEMINI_API_KEY no .env."""
    global _client
    if _client is None:
                _client = genai.Client(http_options=types.HttpOptions(timeout=60000))
    return _client


SYSTEM = """Você é o SmartCampus, assistente acadêmico de uma instituição de ensino.
Regras:
- Para perguntas sobre conteúdo, provas, cronograma ou regras, use a ferramenta buscar_documentos
  e responda APENAS com base nos trechos retornados. Cite a fonte (nome do arquivo).
- Para notas, média ou boletim do aluno, use as ferramentas de banco de dados. Nunca invente notas.
- Se a informação não estiver nos documentos, diga que não encontrou.
- Perguntas compostas exigem usar mais de uma ferramenta.
- Responda em português, de forma clara e objetiva."""


def _texto(descricao):
    return types.Schema(type=types.Type.STRING, description=descricao)


# Descrição das ferramentas no formato do Gemini (mesmas ferramentas da versão anterior)
FERRAMENTAS = [
    types.FunctionDeclaration(
        name="buscar_documentos",
        description="Busca trechos em plano de ensino, materiais de aula e regulamento (RAG/ChromaDB).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"consulta": _texto("Texto da busca semântica")},
            required=["consulta"],
        ),
    ),
    types.FunctionDeclaration(
        name="consultar_media",
        description="Retorna a média e as notas do aluno logado em uma disciplina.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"nome_disciplina": _texto("Ex.: Banco de Dados, Inteligência Artificial")},
            required=["nome_disciplina"],
        ),
    ),
    types.FunctionDeclaration(
        name="gerar_boletim",
        description="Gera o boletim completo (todas as disciplinas) do aluno logado.",
    ),
    types.FunctionDeclaration(
        name="listar_alertas",
        description="Lista alertas de média baixa do aluno logado.",
    ),
    types.FunctionDeclaration(
        name="abrir_chamado",
        description="Registra uma dúvida/chamado para a secretaria ou professor em nome do aluno logado.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={"pergunta": _texto("Texto da dúvida ou solicitação")},
            required=["pergunta"],
        ),
    ),
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


def _para_json(valor):
    """Converte Decimal, datas etc. em tipos que o Gemini aceita."""
    return json.loads(json.dumps(valor, default=str, ensure_ascii=False))


def responder(historico, pergunta, ra, aluno_nome, on_tool=None):
    """Adiciona a pergunta ao histórico, roda o loop de function calling e devolve o texto final."""
    historico.append(types.Content(role="user", parts=[types.Part.from_text(text=pergunta)]))
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM + f"\nAluno logado: {aluno_nome} (RA {ra}).",
        tools=[types.Tool(function_declarations=FERRAMENTAS)],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )

    for _ in range(MAX_RODADAS):
        resp = get_client().models.generate_content(model=MODEL, contents=historico, config=config)
        # guarda a resposta do modelo como veio (inclui os pedidos de ferramenta)
        historico.append(resp.candidates[0].content)

        chamadas = resp.function_calls or []
        if not chamadas:
            return resp.text or "Não consegui gerar uma resposta. Tente reformular a pergunta."

        respostas = []
        for chamada in chamadas:
            args = dict(chamada.args or {})
            if on_tool:
                on_tool(chamada.name, args)
            resultado = executar_ferramenta(chamada.name, args, ra)
            respostas.append(types.Part.from_function_response(
                name=chamada.name,
                response={"resultado": _para_json(resultado)},
            ))
        historico.append(types.Content(role="user", parts=respostas))

    return "A pergunta precisou de ferramentas demais. Tente dividir em perguntas menores."


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
