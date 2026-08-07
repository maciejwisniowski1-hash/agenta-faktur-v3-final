import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="Agent Faktur v3.4",
    layout="wide"
)

st.title("Agent Faktur v3.4")

excel = st.file_uploader(
    "Wybierz plik Excel",
    type=["xlsx"]
)

pdf = st.file_uploader(
    "Wybierz wyciąg PDF",
    type=["pdf"]
)


def extract_invoices(pdf_text):

    invoices = []

    amount_pattern = re.compile(
        r'(\d{1,3}(?:\.\d{3})*,\d{2})'
    )

    transfer_pattern = re.compile(
        r'PRZELEW.*?(?=20\d{2}|$)',
        re.IGNORECASE | re.DOTALL
    )

    matches = transfer_pattern.findall(
        pdf_text
    )

    for fragment in matches:

        numer = ""

        match_number = re.search(
            r'ONLINE\s+(.{0,80})',
            fragment,
            flags=re.IGNORECASE
        )

        if match_number:

            line = match_number.group(1)

            dokumenty = re.findall(
                r'[A-Z0-9()\-]+(?:/[A-Z0-9()\-]+)+',
                line,
                flags=re.IGNORECASE
            )

            if dokumenty:

                dokumenty = sorted(
                    dokumenty,
                    key=len,
                    reverse=True
                )

                numer = dokumenty[0]

        if "/" not in numer:
            continue

        kwoty = amount_pattern.findall(
            fragment
        )

        kwota = ""

        if len(kwoty) >= 2:
            kwota = kwoty[-2]

        elif len(kwoty) == 1:
            kwota = kwoty[0]

        invoices.append({
            "Numer faktury": numer,
            "Kwota": kwota,
            "Fragment": fragment[:250]
        })

    return invoices


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

        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

    st.subheader("PDF")

    st.write(
        "Długość tekstu PDF:",
        len(pdf_text)
    )

    st.download_button(
        "📥 Pobierz tekst PDF",
        data=pdf_text,
        file_name="wyciag.txt",
        mime="text/plain"
    )

    invoices = extract_invoices(
        pdf_text
    )

    st.subheader(
        "Faktury znalezione w wyciągu"
    )

    st.write(
        "Liczba rekordów:",
        len(invoices)
    )

    st.dataframe(
        pd.DataFrame(invoices),
        use_container_width=True
    )
