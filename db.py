"""Acesso ao banco relacional (MySQL, schema do grupo): chama procedures e consulta tabelas."""
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "Smart"),
    )


def listar_alunos():
    with conectar() as con:
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT id_aluno, ra, nome FROM alunos ORDER BY nome")
        return cur.fetchall()


def consultar_media(ra, nome_disciplina):
    """Chama a procedure sp_calcular_media e devolve também as notas lançadas."""
    with conectar() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """SELECT m.id_matricula, d.nome AS disciplina
                 FROM matriculas m
                 JOIN alunos a ON a.id_aluno = m.id_aluno
                 JOIN disciplinas d ON d.id_disciplina = m.id_disciplina
                WHERE a.ra = %s AND d.nome LIKE %s""",
            (ra, f"%{nome_disciplina}%"),
        )
        mat = cur.fetchone()
        if not mat:
            return {"erro": "Aluno não matriculado nessa disciplina."}
        cur.fetchall()  # limpa resultados pendentes
        cur2 = con.cursor()
        resultado = cur2.callproc("sp_calcular_media", [mat["id_matricula"], 0])
        media = resultado[1]
        cur.execute(
            "SELECT avaliacao, valor FROM notas WHERE id_matricula = %s",
            (mat["id_matricula"],),
        )
        return {"disciplina": mat["disciplina"], "media": media, "notas": cur.fetchall()}


def gerar_boletim(ra):
    """Chama a procedure sp_gerar_boletim (recebe o RA)."""
    with conectar() as con:
        cur = con.cursor(dictionary=True)
        cur.callproc("sp_gerar_boletim", [ra])
        linhas = []
        for rs in cur.stored_results():
            linhas = rs.fetchall()
        return {"boletim": linhas}


def abrir_chamado(ra, pergunta):
    """Registra uma dúvida na tabela chamados."""
    with conectar() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO chamados (id_aluno, pergunta) SELECT id_aluno, %s FROM alunos WHERE ra = %s",
            (pergunta, ra),
        )
        con.commit()
        if cur.rowcount == 0:
            return {"erro": "Aluno não encontrado."}
        return {"id_chamado": cur.lastrowid, "status": "ABERTO"}


def listar_alertas(ra):
    with conectar() as con:
        cur = con.cursor(dictionary=True)
        cur.execute(
            """SELECT d.nome AS disciplina, al.mensagem, al.criado_em
                 FROM alertas al
                 JOIN matriculas m ON m.id_matricula = al.id_matricula
                 JOIN alunos a ON a.id_aluno = m.id_aluno
                 JOIN disciplinas d ON d.id_disciplina = m.id_disciplina
                WHERE a.ra = %s ORDER BY al.criado_em DESC""",
            (ra,),
        )
        return {"alertas": cur.fetchall()}
