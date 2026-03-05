import streamlit as st
import pandas as pd
from auxiliar.google_sheets import get_sheet_data,append_sheet_data
from auxiliar.athentication import caixa_de_autenticacao
from auxiliar.tratar_bases import pegar_moods_nao_resolvidos

password = st.secrets["PASSWORD"]
password_parametro = st.query_params.get("password",None)

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if password == password_parametro:
    st.session_state["autenticado"] = True

autenticado = st.session_state["autenticado"]

if "mood_base" not in st.session_state:
    st.session_state["mood_base"] = get_sheet_data("mood_base")

mood_df = st.session_state["mood_base"]

if autenticado:
    st.title("Mood Tracker")

    moods_ativos = pegar_moods_nao_resolvidos(mood_df)

    mood_editor = st.data_editor(
        moods_ativos,
        num_rows="fixed",
        column_config={
            "incomodo": st.column_config.TextColumn("Incomodo"),
            "observacao": st.column_config.TextColumn("Observação"),
            "intensidade": st.column_config.SelectboxColumn("Intensidade", options=[0,1,2,3,4,5],
                                                            format_func=lambda x: "😢" * int(x) if x > 0 else "👍(Problema Resolvido)",
                                                            required=True),
        },
        hide_index=True,
    )

    salvar_botao = st.button("Salvar")

    if salvar_botao:
        mood_editor["data"] = pd.to_datetime("today").strftime("%Y-%m-%d")
        mood_editor = mood_editor[["data","incomodo","observacao","intensidade"]]
        mood_lista = mood_editor.values.tolist()
        append_sheet_data("mood_base", mood_lista)
        st.success("Base de moods atualizada com sucesso!")
        st.balloons()
    
    atualizar_pagina_botao = st.button("Atualizar Página")

    if atualizar_pagina_botao:
        st.session_state.pop("mood_base", None)
        st.rerun()


else:
    st.error("Senha incorreta. Acesso negado.")
    caixa_de_autenticacao()