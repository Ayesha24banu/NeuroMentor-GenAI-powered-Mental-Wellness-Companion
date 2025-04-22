# agent/neuromentor_agent.py
from utils.llm import get_gemini_response
from agent.tools import default_mood_response
from utils.guardrails import is_within_scope

def generate_response(query: str) -> str:
    """
    Generates a supportive response using Gemini Pro.
    
    If the user's message is within the mental wellness scope, this function 
    instructs the Gemini model to respond in a WhatsApp chatting style—casual, supportive,
    and friendly. If the query is off-topic, it returns a default caring message.
    """
    try:
        if not is_within_scope(query):
            return default_mood_response()
        
        # Add a prompt instruction for a WhatsApp chatting style response.
        whatsapp_prompt = (
            "Please answer like you're chatting on WhatsApp—casual, friendly, "
            "and supportive with a natural tone. "
            "Include any relevant emojis to add warmth when appropriate. "
            f"User's message: {query}\n\n"
            "Response:"
        )
        
        response = get_gemini_response(whatsapp_prompt)
        return response
    except Exception:
        return "I'm here for you, but I'm having a little trouble understanding. Could you try asking that in another way?"
