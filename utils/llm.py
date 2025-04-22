# utils/llm.py

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import settings

# Initialize Gemini 1.5 Pro via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.6,
)

def get_gemini_response(query: str) -> str:
    """
    Sends the user query to Gemini 1.5 Pro and returns a text response.
    """
    try:
        response = llm.invoke(query)

        # Check if response contains the 'text' property and return it without any additional metadata.
        if hasattr(response, "text"):
            return response.text.strip()
        elif isinstance(response, dict) and 'text' in response:
            # If the response is a dictionary and contains the 'text' field
            return response['text'].strip()
        else:
            # Fallback to string conversion if 'text' attribute is absent
            return str(response).strip()
        
    except Exception as e:
        st.error(f"Gemini response error: {e}")
        raise e
