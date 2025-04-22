# utils/web_search.py
import json
import requests
import streamlit as st
from config.settings import settings
from utils.llm import get_gemini_response

def live_search(query):
    """
    Performs a live web search via Serper.dev and returns a list of organic results.
    """
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json().get("organic", [])
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return []

def generate_hybrid_answer(query):
    """
    Combines top web search results + Gemini response for a richer answer.
    """
    try:
        search_results = live_search(query)
        if not search_results:
            return "Couldn't find anything useful right now.", []

        # Extract top 3 contents for context
        context_text = ""
        references = []
        for result in search_results[:3]:
            snippet = result.get("snippet", "")
            link = result.get("link", "")
            if snippet:
                context_text += f"- {snippet}\n"
            if link:
                references.append(link)

        # Prepare hybrid prompt
        hybrid_prompt = (
            "You are a helpful assistant.\n"
            "Here is some web search context:\n"
            f"{context_text}\n\n"
            "Based on this, answer the user's query in a clear, concise, and friendly way.\n"
            f"User's question: {query}\n\n"
            "Answer:"
        )

        answer = get_gemini_response(hybrid_prompt)
        return answer, references
    except Exception as e:
        return "⚠️ Oops, something went wrong while generating the answer.", []
