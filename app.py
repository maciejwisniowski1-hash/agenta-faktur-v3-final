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

    transfers = []

    for i, match in enumerate(matches[:50]):

        start = max(
            0,
            match.start() - 120
        )

        end = min(
            len(pdf_text),
            match.start() + 300
        )

        fragment = pdf_text[start:end]

        fragment = fragment.replace(
            "\n",
            " "
        )

        transfers.append({
            "Nr": i + 1,
            "Fragment": fragment
        })

    st.dataframe(
        pd.DataFrame(transfers),
        use_container_width=True
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

    pdf_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            pdf_text += page_text + "\n"

    show_transfer_contexts(
        pdf_text
    )
