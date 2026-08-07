import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

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


def show_transfer_contexts(pdf_text):

    st.write(
        "Długość tekstu PDF:",
        len(pdf_text)
    )

    matches = list(
        re.finditer(
            r"PRZELEW",
            pdf_text,
            flags=re.IGNORECASE
        )
    )

    st.subheader(
        "Wyszukiwanie słowa PRZELEW"
    )

    st.write(
        "Liczba znalezionych słów PRZELEW:",
        len(matches)
    )

