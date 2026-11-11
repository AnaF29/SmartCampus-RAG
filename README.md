# SmartCampus RAG

Assistente acadêmico que responde perguntas sobre as disciplinas usando **RAG** (busca em documentos com ChromaDB) e consulta notas e boletim em um **banco MySQL** com procedures e triggers, por meio de **Function Calling**.

Exemplo: *"Qual é o conteúdo da P2 e qual é minha média atual em Banco de Dados?"*. O sistema busca o conteúdo da prova nos documentos e consulta a média no banco.

## Tecnologias

- **Python 3.10+**
- **MySQL 8** (via Docker): tabelas, procedures e triggers
- **ChromaDB**: base vetorial com os documentos das disciplinas
- **Claude (API da Anthropic)**: modelo de linguagem com Function Calling
- **Streamlit**: interface web

## Estrutura

```
sql/Smart.sql        script do banco (tabelas, inserts, procedures e triggers)
documentos/          documentos da base vetorial (planos de ensino, materiais, regulamento, calendário)
rag/ingestao.py      lê os documentos, divide em trechos e salva no ChromaDB
rag/busca.py         busca os trechos mais relevantes para uma pergunta
rag_bridge.py        liga o chatbot à busca do ChromaDB
db.py                funções que chamam as procedures e consultam o banco
chatbot.py           chatbot com Function Calling (terminal)
interface.py         interface web em Streamlit
```

## Como executar

### 1. Clonar o projeto
```
git clone https://github.com/AnaF29/SmartCampus-RAG.git
cd SmartCampus-RAG
```

### 2. Configurar o `.env`
Copie o `.env.example` para um arquivo `.env` e preencha:
- `DB_PASSWORD`: uma senha para o MySQL
- `ANTHROPIC_API_KEY`: sua chave da API da Anthropic

### 3. Subir o banco de dados
Com o Docker instalado:
```
docker compose up -d
```
Na primeira vez, o script `sql/Smart.sql` é executado automaticamente e cria o banco `Smart` com tabelas, dados de exemplo, procedures e triggers.

Para recriar o banco do zero (por exemplo, depois de alterar o script):
```
docker compose down -v
docker compose up -d
```

### 4. Instalar as dependências
```
python -m venv venv
venv\Scripts\activate        (Windows)
source venv/bin/activate     (Linux/Mac)
python -m pip install -r requirements.txt
```

### 5. Gerar a base vetorial
```
python rag/ingestao.py
```
Lê os arquivos da pasta `documentos/` e cria a base na pasta `chroma_db/`. Rode de novo sempre que alterar algum documento. Na primeira execução, o ChromaDB baixa um modelo de embeddings.

Para testar só a busca:
```
python rag/busca.py "Qual é o conteúdo da P2 de Banco de Dados?"
```

### 6. Iniciar o assistente
Interface web:
```
streamlit run interface.py
```
Ou pelo terminal, informando o RA do aluno:
```
python chatbot.py 2026001
```

## Perguntas de exemplo

- Qual é o conteúdo da P2 e qual é minha média em Banco de Dados?
- Mostre meu boletim.
- Tenho algum alerta de média baixa?
- Quantas faltas posso ter?
- Como peço revisão de nota?

Alunos cadastrados para teste: Ana Souza (RA 2026001), Bruno Lima (RA 2026002) e Carla Mendes (RA 2026003).

## Observação para Windows 11

Se aparecer o erro `DLL load failed while importing cygrpc: Uma política de Controle de Aplicativo bloqueou este arquivo`, o **Controle Inteligente de Aplicativos** do Windows está bloqueando uma biblioteca usada pelo ChromaDB. Ele pode ser desativado em *Segurança do Windows → Controle de aplicativos e navegador*. Atenção: no Windows 11, essa desativação é permanente.

## Divisão de tarefas

- **Letícia**: estrutura do banco e lógica do banco 
- **Ana Flávia**: repositório, documentos e base vetorial (ChromaDB)
- **Fernanda e Kauane**: chatbot, Function Calling e interface

## Uso de IA

O grupo usou ferramentas de IA como apoio no desenvolvimento, conforme permitido pelo professor.