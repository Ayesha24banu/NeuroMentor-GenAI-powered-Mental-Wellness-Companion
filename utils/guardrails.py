# utils/guardrails.py

from utils.llm import get_gemini_response

INTENT_CHECK_PROMPT = """
You are a mental wellness assistant.
Please decide if the following message is related to feelings, stress, or personal challenges,
or if it's off-topic (like coding questions or sports news).

Just reply with one word: relevant or irrelevant.

Message: "{query}"
"""

def is_within_scope(query: str) -> bool:
    """
    Determines if the query is about mental wellness.
    Returns True if it is, and False otherwise.
    """
    prompt = INTENT_CHECK_PROMPT.format(query=query.strip())
    try:
        response = get_gemini_response(prompt).lower().strip()
        return "relevant" in response
    except Exception:
        return False  # If something goes wrong, treat it as off-topic.