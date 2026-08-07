import streamlit as st
import pandas as pd
from pypdf import PdfReader
import re

st.set_page_config(
    page_title="Agent Faktur v3.2",
    layout="wide"
)

st.title("Agent Faktur v3.2")

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

    invoice_pattern = re.compile(
        r'([A-Z0-9()\-]+(?:/[A-Z0-9()\-]+)+)',
        re.IGNORECASE
    )

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

        faktury = invoice_pattern.findall
