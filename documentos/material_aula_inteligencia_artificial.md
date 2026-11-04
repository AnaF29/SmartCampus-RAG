# Material de Aula — Inteligência Artificial

**Disciplina:** Inteligência Artificial (SC-IA01) — Prof. Luiz
**Faculdade Smart Campus** (material fictício para fins acadêmicos)
**Assuntos:** Avaliação de modelos, embeddings, RAG e function calling

---

## Aula 5 — Avaliação de modelos de classificação

Para saber se um modelo de aprendizado de máquina funciona, os dados são divididos em um conjunto de **treino**, usado para o modelo aprender, e um conjunto de **teste**, usado para avaliar o modelo com dados que ele nunca viu. Uma divisão comum é 80% para treino e 20% para teste.

A **matriz de confusão** mostra os acertos e erros do modelo:
- verdadeiro positivo (VP): o modelo disse "sim" e era "sim";
- falso positivo (FP): o modelo disse "sim" e era "não";
- verdadeiro negativo (VN): o modelo disse "não" e era "não";
- falso negativo (FN): o modelo disse "não" e era "sim".

Métricas principais:
- **Acurácia** = (VP + VN) / total. Mede o percentual de acertos geral, mas engana quando as classes são desbalanceadas.
- **Precisão** = VP / (VP + FP). Das vezes que o modelo disse "sim", quantas estavam certas.
- **Revocação (recall)** = VP / (VP + FN). Dos casos que eram "sim", quantos o modelo encontrou.

Exemplo: em um modelo que prevê alunos com risco de reprovação, a revocação é mais importante, porque deixar de identificar um aluno em risco (falso negativo) é pior do que alertar um aluno que não estava em risco.

---

## Aula 10 — Embeddings e similaridade

Um **embedding** é uma representação de um texto (palavra, frase ou documento) como um vetor de números. Textos com significado parecido geram vetores próximos no espaço vetorial, mesmo que usem palavras diferentes. Por exemplo, "quando é a prova?" e "qual a data da avaliação?" geram embeddings próximos.

A proximidade entre dois vetores costuma ser medida pela **similaridade de cosseno**, que vai de -1 a 1. Quanto mais perto de 1, mais parecidos os textos. Alguns bancos vetoriais trabalham com **distância** em vez de similaridade: nesse caso, quanto menor a distância, mais parecidos.

Embeddings são gerados por modelos treinados especificamente para isso. Modelos multilíngues funcionam melhor para textos em português.

---

## Aula 12 — RAG (Retrieval-Augmented Generation)

LLMs só sabem o que aprenderam no treinamento. Eles não conhecem documentos internos de uma instituição e podem **alucinar**, ou seja, inventar respostas que parecem corretas. O **RAG** resolve isso buscando trechos relevantes em uma base de documentos e entregando esses trechos ao modelo junto com a pergunta.

Etapas de um sistema RAG:

1. **Ingestão:** os documentos (PDFs, textos) são carregados e o texto é extraído.
2. **Divisão em chunks:** o texto é dividido em trechos menores, normalmente de algumas centenas de palavras. Usar uma pequena sobreposição entre trechos evita que uma informação seja cortada ao meio.
3. **Embeddings:** cada chunk é convertido em um vetor.
4. **Armazenamento:** os vetores, os textos e os metadados (nome do arquivo, disciplina, página) são salvos em um banco vetorial, como o ChromaDB.
5. **Recuperação:** quando o usuário faz uma pergunta, ela também é convertida em embedding, e o banco vetorial retorna os chunks mais próximos.
6. **Geração:** o LLM recebe a pergunta e os chunks recuperados e gera uma resposta baseada neles, de preferência citando a fonte.

Boas práticas: instruir o modelo a responder apenas com base nos trechos fornecidos e a dizer que não sabe quando a informação não estiver nos documentos. Usar metadados para filtrar a busca, por exemplo, só documentos de uma disciplina.

---

## Aula 13 — Function calling

**Function calling** (chamada de funções) permite que um LLM use ferramentas externas. O desenvolvedor descreve as funções disponíveis (nome, descrição e parâmetros), e o modelo decide quando chamar cada uma e com quais argumentos. O código da aplicação executa a função de verdade e devolve o resultado ao modelo, que então monta a resposta final.

Exemplo em um assistente acadêmico: para a pergunta "qual é o conteúdo da prova e qual é minha média atual?", o modelo pode chamar duas ferramentas:
- uma função de busca nos documentos (RAG) para encontrar o conteúdo da prova;
- uma função que consulta o banco de dados relacional e retorna a média do aluno.

O modelo nunca acessa o banco diretamente: ele só pede a chamada da função, e quem executa é o código. Isso permite controlar o que o modelo pode fazer, por exemplo, deixando-o consultar apenas a média do próprio aluno.

---

## Exercícios de revisão para a P2

1. Explique o que é um embedding e por que textos com significado parecido ficam próximos.
2. Descreva as seis etapas de um sistema RAG.
3. Por que dividir os documentos em chunks? O que acontece se os chunks forem grandes demais ou pequenos demais?
4. Qual a diferença entre RAG e function calling? Dê um exemplo em que os dois são usados juntos.
5. O que é alucinação em LLMs e como o RAG ajuda a reduzi-la?
