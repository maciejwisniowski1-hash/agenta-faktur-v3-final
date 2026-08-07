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


def extract_transfers(pdf_text):

    transfers = []

    matches = list(
        re.finditer(
            r"20\d{2}[‑-]\d{2}[‑-]\d{2}",
            pdf_text
        )
    )

    for i, match in enumerate(matches[:100]):

        start = match.start()

        end = min(
            len(pdf_text),
            start + 500
        )

        fragment = pdf_text[start:end]

        fragment_clean = (
            fragment
            .replace("\n", " ")
            .replace("  ", " ")
        )

        transfers.append({
            "Nr": i + 1,
            "Operacja": fragment_clean[:500]
        })

    return transfers


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

    st.write(
        "Długość tekstu PDF:",
        len(pdf_text)
    )

    transfers = extract_transfers(
        pdf_text
    )

    st.subheader(
        "Rozpoznane przelewy"
    )

    st.write(
        "Liczba operacji:",
        len(transfers)
    )

    st.dataframe(
        pd.DataFrame(transfers),
        use_container_width=True
    )
