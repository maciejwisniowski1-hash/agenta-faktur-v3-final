import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="Agent Faktur v3.6",
    layout="wide"
)

st.title("Agent Faktur v3.6")

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
        r'PRZELEW.*?(?=PRZELEW|$)',
        re.IGNORECASE | re.DOTALL
    )

    matches = transfer_pattern.findall(
        pdf_text
    )

    for fragment in matches:

        numer = ""

        match_number = re.search(
            r'ONLINE\s+(.{0,120})',
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
            "Numer faktury": numer.upper(),
            "Kwota": kwota,
            "Fragment": fragment[:250]
        })

    return invoices


def build_payment_report(df, invoices):

    invoice_map = {}

    for item in invoices:

        numer = str(
            item["Numer faktury"]
        ).upper().strip()

        invoice_map[numer] = item

    wynik = []

    for _, row in df.iterrows():

        numer_excel = str(
            row["Numer dokumentu"]
        ).upper().strip()

        kwota_faktury = float(
            row["Brutto"]
        )

        zaplacono = 0

        if numer_excel in invoice_map:

            kwota_txt = (
                str(
                    invoice_map[numer_excel]["Kwota"]
                )
                .replace(".", "")
                .replace(",", ".")
            )

            try:
                zaplacono = float(
                    kwota_txt
                )
            except:
                pass

        roznica = round(
            zaplacono - kwota_faktury,
            2
        )

        if zaplacono == 0:

            status = "BRAK PŁATNOŚCI"

        elif abs(roznica) <= 0.01:

            status = "OPŁACONA"

        elif zaplacono < kwota_faktury:

            status = "CZĘŚCIOWO OPŁACONA"

        else:

            status = "NADPŁATA"

        wynik.append({
            "Numer dokumentu": numer_excel,
            "Kwota faktury": kwota_faktury,
            "Zapłacono": zaplacono,
            "Różnica": roznica,
            "Status": status
        })

    return pd.DataFrame(wynik)


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
        "
