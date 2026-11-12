import re
from pathlib import Path

import chromadb

RAIZ = Path(__file__).resolve().parent.parent
PASTA_DOCUMENTOS = RAIZ / "documentos"
PASTA_CHROMA = RAIZ / "chroma_db"
NOME_COLECAO = "smartcampus"

EXTENSOES_ACEITAS = {".pdf", ".txt", ".md"}
TAMANHO_CHUNK = 800  
SOBREPOSICAO = 150


def ler_arquivo(caminho: Path) -> list[tuple[str, int]]:
   
    if caminho.suffix.lower() == ".pdf":
        from pypdf import PdfReader  

        leitor = PdfReader(caminho)
        return [
            (pagina.extract_text() or "", numero)
            for numero, pagina in enumerate(leitor.pages, start=1)
        ]
    return [(caminho.read_text(encoding="utf-8"), 0)]


def dividir_em_chunks(texto: str) -> list[str]:
    
    texto = " ".join(texto.split())  
    chunks = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + TAMANHO_CHUNK
        if fim < len(texto):
            ponto = texto.rfind(". ", inicio, fim)
            if ponto > inicio + TAMANHO_CHUNK // 2:
                fim = ponto + 1
        chunks.append(texto[inicio:fim].strip())
        if fim >= len(texto):
            break
        inicio = fim - SOBREPOSICAO
    return [c for c in chunks if c]


def dividir_em_secoes(texto: str) -> list[str]:
    """Divide o Markdown pelas seções (##) e põe o título na frente de cada trecho."""
    linhas = texto.splitlines()
    titulo = next((l.lstrip("# ").strip() for l in linhas if l.startswith("# ")), "")

    trechos = []
    for secao in re.split(r"(?m)^(?=## )", texto):
        if not secao.strip():
            continue
        primeira_linha = secao.strip().splitlines()[0]
        cabecalho = primeira_linha.lstrip("#").strip()
        if primeira_linha.startswith("## "):
            prefixo = f"{titulo} — {cabecalho}: "
        else:
            prefixo = f"{titulo}: "
        for parte in dividir_em_chunks(secao):
            trechos.append(prefixo + parte)
    return trechos


def descobrir_disciplina(nome_arquivo: str) -> str:
   
    nome = nome_arquivo.lower()
    if "banco_de_dados" in nome:
        return "Banco de Dados"
    if "inteligencia_artificial" in nome:
        return "Inteligência Artificial"
    return "Geral"


def main():
    arquivos = sorted(
        p for p in PASTA_DOCUMENTOS.iterdir() if p.suffix.lower() in EXTENSOES_ACEITAS
    )
    if not arquivos:
        print(f"Nenhum documento encontrado em {PASTA_DOCUMENTOS}")
        return

    cliente = chromadb.PersistentClient(path=str(PASTA_CHROMA))
    try:
        cliente.delete_collection(NOME_COLECAO)  # recria do zero
    except Exception:
        pass  
    colecao = cliente.create_collection(NOME_COLECAO)

    ids, textos, metadados = [], [], []
    for arquivo in arquivos:
        total = 0
        for texto, pagina in ler_arquivo(arquivo):
            dividir = dividir_em_secoes if arquivo.suffix.lower() == ".md" else dividir_em_chunks
            for i, chunk in enumerate(dividir(texto)):
                ids.append(f"{arquivo.stem}-p{pagina}-c{i}")
                textos.append(chunk)
                metadados.append({
                    "fonte": arquivo.name,
                    "pagina": pagina,
                    "disciplina": descobrir_disciplina(arquivo.name),
                })
                total += 1
        print(f"{arquivo.name}: {total} trechos")

    colecao.add(ids=ids, documents=textos, metadatas=metadados)
    print(f"\nPronto! {len(ids)} trechos salvos na coleção '{NOME_COLECAO}'.")


if __name__ == "__main__":
    main()
