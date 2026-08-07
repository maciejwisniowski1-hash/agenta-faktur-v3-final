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


def extract_payments(pdf_text):

    payments = []

    lines = pdf_text.split("\n")

    amount_pattern = re.compile(
        r"(\d{1,3}(?:\.\d{3})*,\d{2})"
    )

    for line in lines:

        upper = line.upper()

        if not (
            "PRZELEW" in upper
            or "PRZELEW24" in upper
        ):
            continue

        amounts = amount_pattern.findall(
            upper
        )

        if len(amounts) == 0:
            continue

        try:

            amount = float(
                amounts[0]
                .replace(".", "")
                .replace(",", ".")
            )

            payments.append({
                "Opis": upper,
                "Kwota": amount
            })

        except:
            pass

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

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    payments = extract_payments(
        text
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
