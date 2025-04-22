# components/Documents_images.py
import streamlit as st
import os
import shutil
from utils.vision_utils import analyze_image
from utils.file_utils import (
    query_document_rag, save_uploaded_file, read_pdf,
    summarize_document, merge_texts, save_text_as_file
)

def render_gradient_card(content, title="Answer"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
            margin-top: 1rem;
            font-size: 1.1rem;
            color: #333;
            line-height: 1.6;
        ">
            <strong>{title}:</strong><br><br>{content}
        </div>
        """,
        unsafe_allow_html=True
    )

def render():
    st.title("📄 Documents & 🖼️ Images")
    st.subheader("Upload files for analysis, chatting, or summarizing!")

    if "username" not in st.session_state:
        st.error("🔒 Please log in to use this feature.")
        return

    uploaded_files = st.file_uploader(
        "Choose one or more files (Image, PDF, or TXT):", 
        type=["jpg", "jpeg", "png", "pdf", "txt"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        all_texts = []
        temp_folder = "temp_uploads"
        os.makedirs(temp_folder, exist_ok=True)

        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            st.info(f"Uploaded: {uploaded_file.name} ({file_type})")

            temp_path = os.path.join(temp_folder, uploaded_file.name)
            save_uploaded_file(uploaded_file, temp_path)

            if "image" in file_type:
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                analysis = analyze_image(temp_path)
                render_gradient_card(analysis, title="Image Analysis")
            elif "pdf" in file_type or "text" in file_type:
                if "pdf" in file_type:
                    text = read_pdf(temp_path)
                else:
                    with open(temp_path, "r", encoding="utf-8") as f:
                        text = f.read()
                all_texts.append(text)
            else:
                st.error(f"Unsupported file type: {file_type}")

        if all_texts:
            merged_text = merge_texts(all_texts)
            st.text_area("📄 Extracted Document Content:", merged_text, height=300)

            # Download button for extracted text
            if st.button("⬇️ Download Extracted Text"):
                save_path = save_text_as_file(merged_text, "merged_document.txt")
                with open(save_path, "rb") as f:
                    st.download_button(
                        label="Download Text File",
                        data=f,
                        file_name="merged_document.txt",
                        mime="text/plain"
                    )

            # Choose mode
            mode = st.radio("Select Mode:", ["Chat about Document", "Summarize Document"])

            if mode == "Chat about Document":
                question = st.text_input("Ask a question about the document:")
                if st.button("Submit Question"):
                    if question.strip():
                        answer = query_document_rag(merged_text, question)
                        render_gradient_card(answer, title="Chat Response")
                    else:
                        st.error("❗ Please enter a valid question.")
            elif mode == "Summarize Document":
                if st.button("📝 Auto Summarize"):
                    summary = summarize_document(merged_text)
                    render_gradient_card(summary, title="Document Summary")

        # Clean up temp uploads folder
        shutil.rmtree(temp_folder)
