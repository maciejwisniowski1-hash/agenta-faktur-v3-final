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


def extract_payments(pdf_text):

    payments = []

    st.subheader(
        "Diagnostyka parsera"
    )

    st.write(
        "Długość tekstu PDF:",
        len(pdf_text)
    )

    st.text_area(
        "Pierwsze 10000 znaków PDF",
        pdf_text[:10000],
        height=500
    )

    return payments


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

    payments = extract_payments(
        pdf_text
    )

    st.subheader(
        "Rozpoznane przelewy"
    )

    st.write(
        "Liczba przelewów:",
        len(payments)
    )

    st.dataframe(
        pd.DataFrame(payments),
        use_container_width=True
    )
