#utils/analytics.py
import streamlit as st
from transformers import pipeline

# ---- Sentiment pipeline ----
@st.cache_resource
def _sentiment_pipeline():
    return pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

sentiment_analyzer = _sentiment_pipeline()

# ---- Emotion pipeline ----
@st.cache_resource
def _emotion_pipeline():
    # model that returns scores for multiple emotions
    return pipeline("text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    return_all_scores=True)

emotion_analyzer = _emotion_pipeline()

def analyze_sentiment(text: str) -> dict:
    if not text.strip():
        return {"label":"neutral","score":0.5}
    r = sentiment_analyzer(text[:512])[0]
    score = r["score"] if r["label"]=="POSITIVE" else 1 - r["score"]
    return {"label": r["label"].lower(), "score": score}

def analyze_emotions(text: str) -> dict:
    if not text.strip():
        return {}
    results = emotion_analyzer(text[:512])[0]  # list of dicts
    return { r["label"].lower(): r["score"] for r in results }
