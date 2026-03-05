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
    st.title("Adicionar Mood")
    
    mood_list = mood_df["incomodo"].unique().tolist()

    if "mood_options" not in st.session_state:
        st.session_state.mood_options = mood_list

    with st.popover("Adicionar Novo Mood"):
        new_cat = st.text_input("New category")
        if st.button("Add", use_container_width=True):
            v = new_cat.strip()
            if v and v not in st.session_state.mood_options:
                st.session_state.mood_options.append(v)
            st.rerun()

    novo_mood = pd.DataFrame({
        "incomodo": [""],
        "observacao": [""],
        "intensidade": [0],
    })

    new_mood_editor = st.data_editor(
        novo_mood,
        num_rows="dynamic",
        column_config={
            "incomodo": st.column_config.SelectboxColumn("Incomodo", options=st.session_state.mood_options,required=False),
            "observacao": st.column_config.TextColumn("Observação"),
            "intensidade": st.column_config.SelectboxColumn("Intensidade", options=[0,1,2,3,4,5],
                                                            format_func=lambda x: "😢" * int(x) if x > 0 else "👍(Problema Resolvido)",
                                                            required=True),
        },
        hide_index=True,
    )

    salvar_botao = st.button("Salvar")

    if salvar_botao:
        new_mood_editor["data"] = pd.to_datetime("today").strftime("%Y-%m-%d")
        new_mood_editor = new_mood_editor[["data","incomodo","observacao","intensidade"]]
        mood_lista = new_mood_editor.values.tolist()
        append_sheet_data("mood_base", mood_lista)
        st.success("Base de moods atualizada com sucesso!")
        st.balloons()

else:
    st.error("Senha incorreta. Acesso negado.")
    caixa_de_autenticacao()