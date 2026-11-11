CREATE DATABASE IF NOT EXISTS Smart;

USE Smart;

CREATE TABLE alunos (
    id_aluno INT AUTO_INCREMENT PRIMARY KEY,
    ra VARCHAR(10) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    curso VARCHAR(80) NOT NULL
);

CREATE TABLE disciplinas (
    id_disciplina INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    professor VARCHAR(100) NOT NULL
);

CREATE TABLE matriculas (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_disciplina INT NOT NULL,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno),
    FOREIGN KEY (id_disciplina) REFERENCES disciplinas(id_disciplina)
);

CREATE TABLE notas (
    id_nota INT AUTO_INCREMENT PRIMARY KEY,
    id_matricula INT NOT NULL,
    avaliacao VARCHAR(50)  NOT NULL,
    valor DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (id_matricula) REFERENCES matriculas(id_matricula)
);

CREATE TABLE chamados (
    id_chamado INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    pergunta TEXT NOT NULL,
    resposta TEXT,
    status VARCHAR(20) DEFAULT 'ABERTO',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno)
);

-- Tabelas  triggers
CREATE TABLE log_notas (
    id_log INT AUTO_INCREMENT PRIMARY KEY,
    id_nota INT,
    valor_antigo DECIMAL(4,2),
    valor_novo DECIMAL(4,2),
    alterado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alertas (
    id_alerta INT AUTO_INCREMENT PRIMARY KEY,
    id_matricula INT,
    mensagem VARCHAR(255),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

-- Calcula a média das notas de uma matrícula
CREATE PROCEDURE sp_calcular_media(IN p_id_matricula INT, OUT p_media DECIMAL(4,2))
BEGIN
    SELECT ROUND(AVG(valor), 2) INTO p_media
      FROM notas
     WHERE id_matricula = p_id_matricula;
END //

-- Gera o boletim de um aluno pelo RA
CREATE PROCEDURE sp_gerar_boletim(IN p_ra VARCHAR(10))
BEGIN
    SELECT a.nome AS aluno,
           d.nome AS disciplina,
           ROUND(AVG(n.valor), 2) AS media,
           CASE WHEN AVG(n.valor) >= 6 THEN 'Aprovado' ELSE 'Em risco' END AS situacao
      FROM alunos a
      JOIN matriculas  m ON m.id_aluno = a.id_aluno
      JOIN disciplinas d ON d.id_disciplina = m.id_disciplina
      LEFT JOIN notas  n ON n.id_matricula = m.id_matricula
     WHERE a.ra = p_ra
     GROUP BY a.nome, d.nome;
END //

-- Registra no lOG toda alteração de nota
CREATE TRIGGER trg_log_nota AFTER UPDATE ON notas
FOR EACH ROW
BEGIN
    INSERT INTO log_notas (id_nota, valor_antigo, valor_novo)
    VALUES (OLD.id_nota, OLD.valor, NEW.valor);
END //

-- Dispara alerta se a média ficar abaixo de 6 ao lançar uma nota
CREATE TRIGGER trg_alerta_media_baixa AFTER INSERT ON notas
FOR EACH ROW
BEGIN
    DECLARE v_media DECIMAL(4,2);

    SELECT AVG(valor) INTO v_media
      FROM notas
     WHERE id_matricula = NEW.id_matricula;

    IF v_media < 6 THEN
        INSERT INTO alertas (id_matricula, mensagem)
        VALUES (NEW.id_matricula, CONCAT('Média baixa: ', ROUND(v_media, 2)));
    END IF;
END //

DELIMITER ;

INSERT INTO alunos (ra, nome, curso) VALUES
('2026001', 'Ana Souza','Engenharia da Computação'),
('2026002', 'Bruno Lima','Sistemas de Informação'),
('2026003', 'Carla Mendes','Sistemas de Informação');

INSERT INTO disciplinas (nome, professor) VALUES
('Banco de Dados','Prof. André'),
('Inteligência Artificial','Prof. Luiz');

INSERT INTO matriculas (id_aluno, id_disciplina) VALUES
(1, 1),
(1, 2), 
(2, 1), 
(3, 2);

INSERT INTO notas (id_matricula, avaliacao, valor) VALUES
(1, 'P1', 4.50),
(1, 'Trabalho', 5.00),  
(2, 'P1', 8.00), 
(2, 'Trabalho', 9.00),
(3, 'P1', 9.00),
(3, 'Trabalho', 4.00),
(4, 'P1', 6.50),
(4, 'Trabalho', 7.00);

INSERT INTO chamados (id_aluno, pergunta) VALUES
(1, 'Quais conteúdos caem na prova de Banco de Dados?'),
(2, 'Qual a frequência mínima para aprovação?');