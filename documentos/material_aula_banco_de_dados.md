# Material de Aula — Banco de Dados

**Disciplina:** Banco de Dados (SC-BD01) — Prof. André
**Faculdade Smart Campus** (material fictício para fins acadêmicos)
**Assuntos:** Normalização, junções, stored procedures e triggers

---

## Aula 4 — Normalização

Normalização é o processo de organizar as tabelas de um banco para reduzir a redundância de dados e evitar anomalias de inserção, atualização e exclusão.

**Primeira forma normal (1FN):** uma tabela está na 1FN quando todos os atributos são atômicos, ou seja, cada coluna guarda um único valor. Uma coluna "telefones" com vários números separados por vírgula viola a 1FN. A solução é criar uma tabela separada de telefones.

**Segunda forma normal (2FN):** a tabela está na 2FN quando está na 1FN e todo atributo que não é chave depende da chave primária inteira, e não só de parte dela. Isso só é um problema em tabelas com chave composta. Exemplo: numa tabela de matrículas com chave (id_aluno, id_disciplina), o nome da disciplina depende só de id_disciplina, então deve ficar na tabela de disciplinas.

**Terceira forma normal (3FN):** a tabela está na 3FN quando está na 2FN e nenhum atributo não chave depende de outro atributo não chave (dependência transitiva). Exemplo: guardar a cidade e o estado do aluno junto com o CEP cria dependência transitiva, porque cidade e estado dependem do CEP.

Na prática, a maioria dos sistemas trabalha com tabelas na 3FN.

---

## Aula 8 — Junções (JOIN)

Junções combinam linhas de duas ou mais tabelas a partir de uma coluna relacionada, normalmente uma chave estrangeira.

**INNER JOIN** retorna só as linhas que têm correspondência nas duas tabelas:

```sql
SELECT a.nome, d.nome AS disciplina
FROM alunos a
INNER JOIN matriculas m ON m.id_aluno = a.id_aluno
INNER JOIN disciplinas d ON d.id_disciplina = m.id_disciplina;
```

**LEFT JOIN** retorna todas as linhas da tabela da esquerda, mesmo sem correspondência na da direita. As colunas da tabela da direita vêm como NULL quando não há correspondência. É útil, por exemplo, para listar alunos que ainda não têm notas lançadas.

Dica de prova: sempre identifique qual coluna liga as tabelas antes de escrever o JOIN. Esquecer a condição ON gera um produto cartesiano, com todas as combinações possíveis de linhas.

---

## Aula 10 — Stored procedures

Uma stored procedure é um bloco de comandos SQL salvo no banco com um nome, que pode ser executado várias vezes. Ela pode receber parâmetros de entrada (IN) e devolver valores por parâmetros de saída (OUT).

Vantagens: centraliza regras de negócio no banco, reduz repetição de código na aplicação e pode melhorar a segurança, porque a aplicação chama a procedure sem acessar as tabelas diretamente.

Exemplo de estrutura no MySQL:

```sql
DELIMITER $$
CREATE PROCEDURE calcular_media(IN p_id_aluno INT, IN p_id_disciplina INT, OUT p_media DECIMAL(4,2))
BEGIN
    SELECT AVG(valor) INTO p_media
    FROM notas
    WHERE id_aluno = p_id_aluno AND id_disciplina = p_id_disciplina;
END $$
DELIMITER ;

CALL calcular_media(1, 1, @media);
SELECT @media;
```

O comando DELIMITER troca o delimitador para que o MySQL não interprete o ponto e vírgula de dentro da procedure como o fim do comando CREATE.

---

## Aula 11 — Triggers

Um trigger (gatilho) é um bloco de código executado automaticamente quando ocorre um evento em uma tabela: INSERT, UPDATE ou DELETE. Ele pode rodar antes (BEFORE) ou depois (AFTER) do evento.

Dentro do trigger, OLD representa a linha antes da alteração e NEW representa a linha depois da alteração. Em um INSERT só existe NEW; em um DELETE só existe OLD; em um UPDATE existem os dois.

Usos comuns:
- registrar um histórico (log) de alterações, como guardar a nota antiga e a nova sempre que uma nota é alterada;
- validar dados antes de gravar, como impedir nota menor que 0 ou maior que 10;
- gerar alertas automáticos, como registrar um alerta quando a média de um aluno fica abaixo de 6,0.

Cuidado: no MySQL, um trigger não pode alterar a própria tabela que o disparou. Para registrar logs ou alertas, use tabelas separadas.

Exemplo:

```sql
CREATE TRIGGER trg_log_nota
AFTER UPDATE ON notas
FOR EACH ROW
INSERT INTO log_notas (id_nota, valor_antigo, valor_novo, data_alteracao)
VALUES (OLD.id_nota, OLD.valor, NEW.valor, NOW());
```

---

## Exercícios de revisão para a P2

1. Explique a diferença entre INNER JOIN e LEFT JOIN e dê um exemplo de quando usar cada um.
2. Escreva uma consulta que mostre a média de notas de cada disciplina, usando GROUP BY.
3. Crie uma procedure que receba o id de um aluno e liste todas as suas disciplinas e notas.
4. Crie um trigger que impeça a inserção de notas fora do intervalo de 0 a 10.
5. Explique o que acontece com uma transação quando o comando ROLLBACK é executado.
