import sys
from pathlib import Path
import chromadb

RAIZ = Path(__file__).resolve().parent.parent
PASTA_CHROMA = RAIZ / "chroma_db"
NOME_COLECAO = "smartcampus"


def buscar(consulta: str, k: int = 4) -> list[dict]:
   
    cliente = chromadb.PersistentClient(path=str(PASTA_CHROMA))
    colecao = cliente.get_collection(NOME_COLECAO)
    resultado = colecao.query(query_texts=[consulta], n_results=k)

    trechos = []
    for texto, meta, distancia in zip(
        resultado["documents"][0], resultado["metadatas"][0], resultado["distances"][0]
    ):
        trechos.append({
            "fonte": meta["fonte"],
            "disciplina": meta.get("disciplina", "Geral"),
            "trecho": texto,
            "distancia": round(distancia, 3),
        })
    return trechos


if __name__ == "__main__":
    pergunta = " ".join(sys.argv[1:]) or "Qual é o conteúdo da P2 de Banco de Dados?"
    print(f"Pergunta: {pergunta}\n")
    for i, item in enumerate(buscar(pergunta), start=1):
        print(f"[{i}] {item['fonte']} ({item['disciplina']}, distância {item['distancia']})")
        print(f"    {item['trecho'][:300]}...\n")
