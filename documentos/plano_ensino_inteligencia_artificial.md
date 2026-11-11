# Plano de Ensino — Inteligência Artificial

**Instituição:** Faculdade Smart Campus (documento fictício para fins acadêmicos)
**Cursos:** Engenharia da Computação e Sistemas de Informação
**Disciplina:** Inteligência Artificial
**Código:** SC-IA01
**Período letivo:** 2026/2 (de 03/08/2026 a 12/12/2026)
**Carga horária:** 80 horas (4 aulas semanais)
**Professor responsável:** Prof. Luiz
**Horário:** terças e quintas-feiras, das 19h00 às 20h40
**Sala:** Laboratório 5, Bloco B

## Ementa

Histórico e fundamentos da inteligência artificial. Agentes inteligentes. Resolução de problemas por busca. Aprendizado de máquina supervisionado e não supervisionado. Redes neurais. Processamento de linguagem natural. Modelos de linguagem de grande escala (LLMs). Embeddings, busca semântica e RAG (Retrieval-Augmented Generation). Function calling e agentes. Ética e uso responsável de IA.

## Objetivos

Ao final da disciplina, o aluno deverá ser capaz de:

- explicar os principais conceitos e áreas da inteligência artificial;
- aplicar algoritmos básicos de aprendizado de máquina em Python;
- avaliar modelos usando métricas como acurácia, precisão e revocação;
- explicar como funcionam embeddings, bancos vetoriais e RAG;
- construir um assistente que combine um LLM com documentos próprios e com funções externas;
- discutir riscos, vieses e limites dos sistemas de IA.

## Conteúdo programático

**Unidade 1 — Fundamentos e aprendizado de máquina (agosto e setembro)**
1. O que é IA: histórico, áreas e aplicações
2. Agentes inteligentes e ambientes
3. Busca em espaço de estados (busca em largura, em profundidade e A*)
4. Aprendizado supervisionado: regressão linear, árvores de decisão e k-NN
5. Avaliação de modelos: treino e teste, acurácia, precisão, revocação e matriz de confusão
6. Aprendizado não supervisionado: k-means

**Unidade 2 — Redes neurais e linguagem (outubro e novembro)**
7. Redes neurais: perceptron, camadas e função de ativação
8. Noções de deep learning
9. Processamento de linguagem natural: tokenização
10. Embeddings e similaridade de cosseno
11. Modelos de linguagem de grande escala (LLMs) e engenharia de prompt
12. RAG: divisão em chunks, banco vetorial, recuperação e geração
13. Function calling e agentes com ferramentas

**Unidade 3 — IA responsável (dezembro)**
14. Vieses, alucinações, privacidade e ética em IA

## Avaliação

A avaliação é composta por três notas, todas de 0 a 10:

| Avaliação | Conteúdo | Data |
|---|---|---|
| P1 — Prova 1 | Unidade 1: fundamentos, agentes, busca, aprendizado supervisionado e não supervisionado, métricas | 01/10/2026 |
| P2 — Prova 2 | Unidade 2: redes neurais, PLN, embeddings, LLMs, RAG e function calling | 26/11/2026 |
| Trabalho | Trabalho prático individual: classificação com árvore de decisão e k-NN em Python | entregue em 22/10/2026 |

**Cálculo da média final:**

Média final = (P1 + P2 + Trabalho) / 3

**Critérios de aprovação:**

- Média final igual ou superior a **6,0** e frequência mínima de **75%**: aprovado.
- Média final entre **4,0 e 5,9**, com frequência mínima de 75%: o aluno pode fazer o **exame final**.
- Média final abaixo de **4,0** ou frequência abaixo de 75%: reprovado.

**Prova substitutiva:** em **10/12/2026**, para o aluno que faltou à P1 ou à P2, com o mesmo conteúdo da prova perdida.

**Exame final:** **15/12/2026**, sobre todo o conteúdo da disciplina. A média após o exame é (média final + nota do exame) / 2, e o aluno é aprovado se o resultado for igual ou superior a 5,0.

## Conteúdo detalhado da P2 (26/11/2026)

A P2 é individual, sem consulta, com duração de 1h40. Ela cobre:

- estrutura de uma rede neural: neurônios, pesos, camadas e funções de ativação;
- diferença entre aprendizado de máquina tradicional e deep learning;
- tokenização e o que é um token;
- embeddings: o que são, para que servem e como medir similaridade com o cosseno;
- funcionamento de um LLM em alto nível e técnicas de engenharia de prompt;
- etapas de um sistema RAG: ingestão, divisão em chunks, geração de embeddings, armazenamento em banco vetorial, recuperação e geração da resposta;
- function calling: como o modelo decide chamar uma função e como o resultado volta para a resposta.

A prova terá 5 questões discursivas e 5 questões objetivas. O conteúdo de ética (Unidade 3) **não** cai na P2, mas cai no exame final.

## Bibliografia

**Básica**
- RUSSELL, S.; NORVIG, P. *Inteligência Artificial: uma abordagem moderna*. 4. ed. GEN LTC.
- GÉRON, A. *Mãos à obra: aprendizado de máquina com Scikit-Learn, Keras e TensorFlow*. 2. ed. Alta Books.

**Complementar**
- JURAFSKY, D.; MARTIN, J. H. *Speech and Language Processing*. 3. ed. (versão online).
- Documentação oficial do ChromaDB.

## Atendimento ao aluno

O professor atende às terças-feiras, das 18h00 às 19h00, na sala dos professores do Bloco B, ou pelo fórum da disciplina no portal do aluno.
