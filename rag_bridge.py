"""Ponte entre o chatbot e a base vetorial (ChromaDB).

O chatbot chama buscar(consulta). Quem fez a parte do Chroma só precisa
ligar esta função à sua função de busca (veja o ponto marcado com AJUSTAR).

Formato esperado do retorno: lista de dicts, por exemplo
    [{"fonte": "plano_de_ensino.pdf", "trecho": "A P1 cobre ..."}, ...]
"""
import sys
from pathlib import Path

# permite importar a pasta rag/ da raiz do repositório
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def buscar(consulta: str, k: int = 8):
    try:
        # >>> AJUSTAR: troque pelo módulo/função de busca que a colega criou em rag/
        # Exemplo: se existe rag/busca.py com def buscar(pergunta, k): ...
        from rag.busca import buscar as buscar_chroma
    except ImportError:
        return {
            "aviso": "A base vetorial ainda não está conectada. "
                     "Ajuste app/rag_bridge.py para importar a função de busca do ChromaDB."
        }

    resultados = buscar_chroma(consulta, k)
    # >>> AJUSTAR (se necessário): converta para [{"fonte": ..., "trecho": ...}]
    return resultados
