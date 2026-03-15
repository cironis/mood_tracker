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

    mood_list = mood_df.loc[mood_df["incomodo"].notnull(), "incomodo"].unique().tolist()

    if "mood_options" not in st.session_state:
        st.session_state.mood_options = mood_list

    with st.popover("Adicionar Novo Mood"):
        new_cat = st.text_input("Novo Incômodo")
        if st.button("Add", use_container_width=True):
            v = new_cat.strip()
            if v and v not in st.session_state.mood_options:
                st.session_state.mood_options.append(v)
            st.rerun()
    
    moods_ativos = pegar_moods_nao_resolvidos(mood_df)
    
    date_picker = st.date_input("Selecione a data para adicionar o mood:", value=pd.Timestamp.now(tz="America/Sao_Paulo").date())
    
    mood_editor = st.data_editor(
        moods_ativos,
        num_rows="dynamic",
        column_config={
            "incomodo": st.column_config.SelectboxColumn("Incomodo", options=st.session_state.mood_options),
            "observacao": st.column_config.TextColumn("Observação"),
            "intensidade": st.column_config.SelectboxColumn("Intensidade", options=[0,1,2,3,4,5],
                                                            format_func=lambda x: "😢" * int(x) if x > 0 else "👍(Problema Resolvido)",
                                                            required=True),
        },
        hide_index=True,
    )

    salvar_botao = st.button("Salvar")

    if salvar_botao:
        data = date_picker.strftime("%Y-%m-%d")
        mood_editor["data"] = data
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