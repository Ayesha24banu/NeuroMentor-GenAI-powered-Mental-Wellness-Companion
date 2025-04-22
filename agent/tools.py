# agents/tools.py

def analyze_mood(text: str) -> str:
    """
    Basic keyword-based mood analysis.
    Returns: 'happy', 'sad', 'anxious', 'stressed', or 'neutral'.
    """
    text_lower = text.lower()
    if any(word in text_lower for word in ["happy", "joy", "excited", "grateful"]):
        return "happy"
    elif any(word in text_lower for word in ["sad", "down", "depressed"]):
        return "sad"
    elif any(word in text_lower for word in ["anxious", "nervous", "worried"]):
        return "anxious"
    elif any(word in text_lower for word in ["stressed", "overwhelmed", "tense"]):
        return "stressed"
    else:
        return "neutral"

def default_mood_response() -> str:
    """
    Returns a default supportive response for off-topic queries.
    """
    return ("I'm here to support your mental wellness. Could you please tell me more about "
            "how you're feeling or ask a wellness-related question?")
