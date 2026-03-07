import streamlit as st
import pandas as pd
from auxiliar.google_sheets import get_sheet_data,set_sheet_data
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
    base_limpa = get_sheet_data("mood_base")
    base_limpa = base_limpa.drop_duplicates(keep="last").reset_index(drop=True)
    st.session_state["mood_base"] = base_limpa

mood_df = st.session_state["mood_base"]

if autenticado:
    st.title("Analisar Moods")
    mood_list = mood_df["incomodo"].dropna().unique().tolist()

    selected_mood = st.multiselect(
        "Selecione um incômodo para analisar:",
        options=mood_list
    )

    if selected_mood:
        mood_data = mood_df[mood_df["incomodo"].isin(selected_mood)].copy()
        mood_data["data"] = pd.to_datetime(mood_data["data"]).dt.date

        groupby_mood = (
            mood_data.groupby(["data", "incomodo"], as_index=False)["intensidade"]
            .mean()
            .sort_values("data")
        )

        st.subheader(f"Análise do incômodo: {', '.join(selected_mood)}")

        st.line_chart(
            groupby_mood,
            x="data",
            y="intensidade",
            color="incomodo",
        )

        st.subheader("Observações:")
        st.dataframe(mood_data[["data","incomodo","observacao","intensidade"]]
                     .sort_values(["data","incomodo"], ascending=[False,True]))

        
else:
    st.error("Senha incorreta. Acesso negado.")
    caixa_de_autenticacao()