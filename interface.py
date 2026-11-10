"""Interface web (Streamlit). Execute: streamlit run src/app.py"""
import streamlit as st
import db
import chatbot

st.set_page_config(page_title="SmartCampus RAG", page_icon="🎓")
st.title("🎓 SmartCampus — Assistente Acadêmico")

alunos = db.listar_alunos()
escolhido = st.sidebar.selectbox("Aluno (simula login)", alunos, format_func=lambda a: f"{a['nome']} ({a['ra']})")
ra, nome = escolhido["ra"], escolhido["nome"]

if st.session_state.get("ra") != ra:
    st.session_state.ra = ra
    st.session_state.historico = []   # histórico da API
    st.session_state.mensagens = []   # histórico visual

with st.sidebar:
    st.subheader("Alertas")
    alertas = db.listar_alertas(ra)["alertas"]
    if alertas:
        for a in alertas:
            st.warning(f"{a['disciplina']}: {a['mensagem']}")
    else:
        st.success("Sem alertas.")
    st.caption("Exemplos: 'Qual é o conteúdo da P1 e qual é minha média em Banco de Dados?' • 'Mostre meu boletim' • 'Qual a frequência mínima?'")

for m in st.session_state.mensagens:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if pergunta := st.chat_input("Pergunte algo..."):
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        with st.status("Consultando...", expanded=False) as status:
            resposta = chatbot.responder(
                st.session_state.historico, pergunta, ra, nome,
                on_tool=lambda n, a: status.write(f"🔧 `{n}` {a}"),
            )
            status.update(label="Pronto", state="complete")
        st.markdown(resposta)
    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
