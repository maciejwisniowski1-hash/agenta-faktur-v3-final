import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="Agent Faktur v3.1",
    layout="wide"
)

st.title("Agent Faktur v3.1")

excel = st.file_uploader(
    "Wybierz plik Excel",
    type=["xlsx"]
)

pdf = st.file_uploader(
    "Wybierz wyciąg PDF",
    type=["pdf"]
)


def extract_bank_operations(pdf_text):

    patterns = [
        "PRZELEW ELIXIR",
        "PRZELEW NA RACHUNEK",
        "PRZELEW24"
    ]

    operations = []

    upper_text = pdf_text.upper()

    for pattern in patterns:

        pos = 0

        while True:

            idx = upper_text.find(
                pattern,
                pos
            )

            if idx == -1:
                break

            start = max(
                0,
                idx - 150
            )

            end = min(
                len(pdf_text),
                idx + 500
            )

            fragment = pdf_text[
                start:end
            ]

            fragment = (
                fragment
                .replace("\n", " ")
                .replace("  ", " ")
            )

            operations.append({
                "Typ": pattern,
                "Fragment": fragment
            })

            pos = idx + 1

    return operations


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

        t = page.extract_text()

        if t:
            pdf_text += t + "\n"

    st.write(
        "Długość tekstu PDF:",
        len(pdf_text)
    )

    operations = extract_bank_operations(
        pdf_text
    )

    st.subheader(
        "Operacje bankowe"
    )

    st.write(
        "Liczba znalezionych operacji:",
        len(operations)
    )

    st.dataframe(
        pd.DataFrame(operations),
        use_container_width=True
    )
