#utils/ file_utils.py
import os
import fitz  # PyMuPDF
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from config.settings import settings

# Load models once
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Fast and lightweight
genai.configure(api_key=settings.GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel('models/gemini-1.5-pro')

def save_uploaded_file(uploaded_file, save_path):
    try:
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return save_path
    except Exception as e:
        raise Exception(f"File could not be saved: {str(e)}")

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def merge_texts(text_list):
    return "\n\n".join(text_list)

def save_text_as_file(text, filename):
    save_path = os.path.join("temp_uploads", filename)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)
    return save_path

def chunk_text(text, chunk_size=300):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def build_faiss_index(chunks):
    embeddings = embedding_model.encode(chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    return index, embeddings, chunks

def query_document_rag(document_text, user_query, top_k=3):
    chunks = chunk_text(document_text)
    index, embeddings, raw_chunks = build_faiss_index(chunks)
    query_embedding = embedding_model.encode([user_query])

    D, I = index.search(np.array(query_embedding), top_k)
    retrieved_chunks = [raw_chunks[i] for i in I[0]]

    context = "You are helping based on the following extracted document sections:\n\n"
    for idx, chunk in enumerate(retrieved_chunks, 1):
        context += f"Section {idx}:\n{chunk}\n\n"
    context += f"Now answer the user's question clearly:\nQ: {user_query}\nA:"

    response = gemini_model.generate_content(context)
    return response.text

def summarize_document(document_text):
    prompt = f"Summarize the following document clearly, concisely, and beautifully:\n\n{document_text}\n\nSummary:"
    response = gemini_model.generate_content(prompt)
    return response.text
