# utils/chat_memory.py

import os
import json
from datetime import datetime
from fpdf import FPDF

# Base folder for all chat session data
CHAT_DIR = "data/chat_sessions"

def save_message_to_history(username: str, role: str, content: str, source: str = "chat"):
    """
    Saves a single chat or voice message to a JSON file organized by user and date.
    Args:
        username: The username of the user.
        role: "user" or "neuromentor"
        content: The text content of the message.
        source: "chat" or "voice" (default is chat)
    """
    # Prepare directory path
    date_today = datetime.now().strftime("%Y-%m-%d")
    base_dir = os.path.join(CHAT_DIR, username, date_today)
    os.makedirs(base_dir, exist_ok=True)

    # Prepare filename (one file per session day)
    filename = os.path.join(base_dir, f"session_{date_today}.json")

    # Load existing messages
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            chat_data = json.load(f)
    else:
        chat_data = []

    # Append new message
    chat_data.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "type": "text",         # Indicating it's a text message
        "source": source,       # "chat" or "voice"
        "content": content
    })

    # Save back
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=2)

def load_chat_history(username: str, date: str) -> list:
    """
    Loads all chat and/or voice messages for a user on a specific date.
    """
    filepath = os.path.join(CHAT_DIR, username, date, f"session_{date}.json")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def delete_session(username: str, date: str, session_file: str):
    """
    Delete a specific chat session by date and filename.
    """
    session_path = os.path.join(CHAT_DIR, username, date, session_file)
    if os.path.exists(session_path):
        os.remove(session_path)

def summarize_session(chat_session: list) -> str:
    """
    Generate a simple summary of a chat session.
    Args:
        chat_session: List of messages (each message is a dict)
    Returns:
        A string summary of user and neuromentor exchanges.
    """
    user_msgs = [msg["content"] for msg in chat_session if msg.get("role") == "user"]
    neuromentor_msgs = [msg["content"] for msg in chat_session if msg.get("role") == "neuromentor"]

    summary = "Summary of the session:\n"
    summary += "\n".join([f"User: {u}" for u in user_msgs]) + "\n\n"
    summary += "\n".join([f"NeuroMentor: {n}" for n in neuromentor_msgs])

    return summary

def export_chat_to_pdf(chat_session: list, output_filename="chat_summary.pdf"):
    """
    Export a chat session to a PDF file.
    Args:
        chat_session: List of messages (each message is a dict)
        output_filename: Path to output PDF
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 10, txt="Chat Session Summary", ln=True, align="C")
    pdf.ln(10)

    # Add each message
    for msg in chat_session:
        role = msg.get("role", "unknown").capitalize()
        text = msg.get("content", "")
        pdf.multi_cell(0, 10, f"{role}: {text}")
        pdf.ln(5)

    # Save the PDF
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    pdf.output(output_filename)
