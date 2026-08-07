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

    pattern = r"PRZELEW.*?(?=PRZELEW|$)"

    matches = re.findall(
        pattern,
        pdf_text,
        flags=re.IGNORECASE | re.DOTALL
    )

    transfers = []

    amount_pattern = re.compile(
        r"(\d+,\d{2})"
    )

    for i, fragment in enumerate(matches):

        fragment_clean = (
            fragment
            .replace("\n", " ")
            .replace("  ", " ")
        )

        kwoty = amount_pattern.findall(
            fragment_clean
        )

        transfers.append({
            "Nr": i + 1,
            "Ilość kwot": len(kwoty),
            "Kwoty znalezione": " | ".join(kwoty[:10]),
            "Fragment": fragment_clean[:500]
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

        page_text = page.extract_text
