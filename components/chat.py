import streamlit as st
from agent.neuromentor_agent import generate_response
from utils.chat_memory import save_message_to_history
import time
from datetime import datetime

def render_chat():
    # --- Ensure user is logged in ---
    if "username" not in st.session_state or not st.session_state.username:
        st.error("🚫 You must log in to access ChatterBox.")
        st.stop()

    st.title("💬 ChatterBox")
    st.subheader("Chat freely with your AI wellness companion! 🤗🧠")
    st.write("I’m here to listen, support, and guide you. If you're feeling a bit overwhelmed, or simply want to chat, I’m here for you. You’re not alone! 💬")

    # --- Initialize chat history ---
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # --- Display previous chat messages ---
    for message in st.session_state.chat_messages:
        alignment = "flex-end" if message["role"] == "user" else "flex-start"
        bg_color = "#DCF8C6" if message["role"] == "user" else "#E6E6FA"
        sender = (
            f"🧑‍💻 {st.session_state.username}" if message["role"] == "user" else "🧠 NeuroMentor"
        )
        timestamp = message.get("timestamp", "")

        st.markdown(
            f"""
            <div style="display: flex; justify-content: {alignment}; margin-bottom: 12px; animation: fadeIn 0.5s;">
                <div style="background-color: {bg_color}; padding: 14px 20px; border-radius: 18px; max-width: 75%; word-wrap: break-word; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
                    <div style="font-size: 12px; color: gray;">{sender} · {timestamp}</div>
                    <div style="margin-top: 6px; font-size: 16px;">{message["content"]}</div>
                </div>
            </div>

            <style>
                @keyframes fadeIn {{
                    from {{ opacity: 0; }}
                    to {{ opacity: 1; }}
                }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # --- User input box ---
    user_query = st.chat_input("Share your thoughts here... 🤔💬")

    if user_query:
        # 1. Save and display the user's message immediately
        user_message = {
            "role": "user",
            "content": user_query,
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.chat_messages.append(user_message)
        save_message_to_history(
            username=st.session_state.username,
            role="user",
            content=user_query
        )

        # 2. Display "typing..." animation
        typing_placeholder = st.empty()
        dots = ""
        for _ in range(6):  # Show animation for ~3 seconds
            dots = dots + "." if len(dots) < 3 else ""
            typing_placeholder.markdown(f"🧠 NeuroMentor is typing{dots}")
            time.sleep(0.5)
            if len(dots) == 3:
                dots = ""
                typing_placeholder.empty()
                typing_placeholder = st.empty()

        # 3. Generate AI response
        ai_response = generate_response(user_query)

        # 4. Save AI response
        ai_message = {
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now().strftime("%I:%M %p")
        }
        st.session_state.chat_messages.append(ai_message)
        save_message_to_history(
            username=st.session_state.username,
            role="assistant",
            content=ai_response
        )

        # 5. Clear typing animation
        typing_placeholder.empty()

        # 6. Force rerun to display updated chat (optional)
        st.experimental_rerun()

