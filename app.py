import streamlit as st
import pandas as pd
from pypdf import PdfReader

st.set_page_config(
    page_title="Agent Faktur v3 FINAL",
    layout="wide"
)

st.title("Agent Faktur v3 FINAL")

excel = st.file_uploader(
    "Wybierz plik Excel",
    type=["xlsx"]
)

pdf = st.file_uploader(
    "Wybierz wyciąg PDF",
    type=["pdf"]
)

if excel:

    df = pd.read_excel(excel)

    st.success(
        f"Odczytano {len(df)} rekordów"
    )

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

if pdf:

    reader = PdfReader(pdf)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    st.subheader(
        "Podgląd PDF"
    )

    st.text_area(
        "Pierwsze 5000 znaków",
        text[:5000],
        height=300
    )
