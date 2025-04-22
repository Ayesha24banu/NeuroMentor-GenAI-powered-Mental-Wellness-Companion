# utils/pdf_export.py

import os
import re
from fpdf import FPDF
from datetime import datetime
from utils.file_ops import get_all_session_paths, load_chat_from_file
from utils.analytics import analyze_sentiment, analyze_emotions
import streamlit as st
from io import BytesIO


def clean_text(text):
    """
    Removes emojis and non-latin1 characters to prevent PDF encoding errors.
    Also replaces common symbols.
    """
    if not text:
        return ""
    text = text.replace('→', '->').replace('—', '-')
    return re.sub(r'[^\x00-\xFF]', '', text)

def export_history_pdf(start_date, end_date, data, export_type="chat"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    title = f"{export_type.capitalize()} Data ({start_date} to {end_date})"
    pdf.cell(200, 10, txt=title, ln=True, align="C")
    pdf.ln(10)

    for idx, row in data.iterrows():
        pdf.multi_cell(0, 10, f"Date: {row['date'].date()}")
        pdf.multi_cell(0, 10, f"Primary Emotion: {row['primary_emotion'].capitalize()}")
        pdf.multi_cell(0, 10, f"Sentiment Score: {row['sentiment_score']:.2f}")
        pdf.ln(5)

    # ⭐ Correct: Return as bytes for download
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes