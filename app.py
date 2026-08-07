import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Agent Faktur v3 FINAL",
    layout="wide"
)

st.title("Agent Faktur v3 FINAL")

excel = st.file_uploader(
    "Wybierz plik Excel",
    type=["xlsx"]
)

if excel:

    df = pd.read_excel(excel)

    st.success(
        f"Odczytano {len(df)} rekordów"
    )

    st.dataframe(
        df,
        use_container_width=True
    )
