# Plano de Ensino — Banco de Dados

**Instituição:** Faculdade Smart Campus (documento fictício para fins acadêmicos)
**Cursos:** Engenharia da Computação e Sistemas de Informação
**Disciplina:** Banco de Dados
**Código:** SC-BD01
**Período letivo:** 2026/2 (de 03/08/2026 a 12/12/2026)
**Carga horária:** 80 horas (4 aulas semanais)
**Professor responsável:** Prof. André
**Horário:** segundas e quartas-feiras, das 19h00 às 20h40
**Sala:** Laboratório 3, Bloco B

## Ementa

Conceitos de sistemas gerenciadores de banco de dados (SGBD). Modelo entidade-relacionamento. Modelo relacional. Normalização. Linguagem SQL: DDL, DML e consultas. Junções e subconsultas. Views, stored procedures, functions e triggers. Transações e controle de concorrência. Noções de bancos NoSQL e bancos vetoriais.

## Objetivos

Ao final da disciplina, o aluno deverá ser capaz de:

- modelar um banco de dados a partir de requisitos, usando o modelo entidade-relacionamento;
- converter o modelo conceitual em modelo relacional normalizado até a 3ª forma normal;
- criar e manipular bancos de dados em MySQL usando SQL;
- escrever consultas com junções, agrupamentos e subconsultas;
- implementar regras de negócio no banco com stored procedures e triggers;
- reconhecer quando um banco não relacional ou vetorial é mais adequado.

## Conteúdo programático

**Unidade 1 — Fundamentos e modelagem (agosto e setembro)**
1. Introdução a bancos de dados e SGBDs
2. Modelo entidade-relacionamento: entidades, atributos, relacionamentos e cardinalidade
3. Modelo relacional: tabelas, chaves primárias e chaves estrangeiras
4. Normalização: 1ª, 2ª e 3ª formas normais
5. SQL DDL: CREATE, ALTER e DROP

**Unidade 2 — SQL e programação no banco (outubro e novembro)**
6. SQL DML: INSERT, UPDATE e DELETE
7. Consultas com SELECT, WHERE, ORDER BY, GROUP BY e HAVING
8. Junções (INNER JOIN, LEFT JOIN) e subconsultas
9. Views
10. Stored procedures e functions
11. Triggers
12. Transações e propriedades ACID

**Unidade 3 — Tópicos complementares (novembro e dezembro)**
13. Introdução ao NoSQL
14. Bancos vetoriais e busca por similaridade (ChromaDB)

## Avaliação

A avaliação é composta por três notas, todas de 0 a 10:

| Avaliação | Conteúdo | Data |
|---|---|---|
| P1 — Prova 1 | Unidade 1: modelagem ER, modelo relacional, normalização e SQL DDL | 30/09/2026 |
| P2 — Prova 2 | Unidade 2: SQL DML, consultas, junções, subconsultas, views, procedures, triggers e transações | 25/11/2026 |
| Trabalho | Trabalho prático individual: modelagem e criação de um banco em SQL | entregue em 21/10/2026 |

**Cálculo da média final:**

Média final = (P1 + P2 + Trabalho) / 3

**Critérios de aprovação:**

- Média final igual ou superior a **6,0** e frequência mínima de **75%**: aprovado.
- Média final entre **4,0 e 5,9**, com frequência mínima de 75%: o aluno pode fazer o **exame final**.
- Média final abaixo de **4,0** ou frequência abaixo de 75%: reprovado.

**Prova substitutiva:** o aluno que faltar à P1 ou à P2 pode fazer a prova substitutiva em **09/12/2026**, que substitui a prova perdida. O conteúdo da substitutiva é o mesmo da prova que ela substitui. O pedido deve ser feito pelo portal do aluno, conforme o Regulamento Acadêmico.

**Exame final:** **14/12/2026**, sobre todo o conteúdo da disciplina. A média após o exame é (média final + nota do exame) / 2, e o aluno é aprovado se o resultado for igual ou superior a 5,0.

## Conteúdo detalhado da P2 (25/11/2026)

A P2 é individual, sem consulta, com duração de 1h40. Ela cobre:

- comandos INSERT, UPDATE e DELETE;
- consultas com filtros, ordenação, agrupamento (GROUP BY) e funções de agregação (COUNT, SUM, AVG, MAX, MIN);
- INNER JOIN e LEFT JOIN entre duas ou três tabelas;
- subconsultas no WHERE;
- criação de views;
- criação e chamada de stored procedures com parâmetros IN e OUT;
- criação de triggers BEFORE e AFTER para INSERT e UPDATE;
- conceitos de transação: COMMIT, ROLLBACK e propriedades ACID.

A prova terá 4 questões práticas de escrita de SQL e 6 questões objetivas. Bancos NoSQL e vetoriais **não** caem na P2.

## Bibliografia

**Básica**
- ELMASRI, R.; NAVATHE, S. B. *Sistemas de Banco de Dados*. 7. ed. Pearson.
- SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. *Sistema de Banco de Dados*. 7. ed. Elsevier.

**Complementar**
- HEUSER, C. A. *Projeto de Banco de Dados*. 6. ed. Bookman.
- Documentação oficial do MySQL 8.0.

## Atendimento ao aluno

O professor atende às quartas-feiras, das 18h00 às 19h00, na sala dos professores do Bloco B, ou pelo fórum da disciplina no portal do aluno. Dúvidas sobre notas devem ser abertas como chamado no portal.
