import streamlit as st

st.set_page_config(layout="wide")

# --- PAGE SETUP ---
mood_page = st.Page(
    "views/atualizar_mood.py",
    title="Atualizar Moods",
    icon=":material/mood:",
    default=True,
)

analysis_page = st.Page(
    "views/analizar_mood.py",
    title="Analisar Moods",
    icon=":material/analytics:",
)

about_page = st.Page(
    "views/about.py",
    title="About",
    icon=":material/info:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Controle de moods": [mood_page, analysis_page,about_page],
    }
)

# --- SHARED ON ALL PAGES ---
st.sidebar.caption("Version 1.0")

# --- RUN NAVIGATION ---
pg.run()