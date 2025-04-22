# components/home.py
import streamlit as st
from services.auth import get_or_create_user

def render_home():
    # -------------------- Title with Logo on Side --------------------
    st.markdown("""
        <div style='margin-top: -60px; text-align: center;'>
            <h1 style='font-size: 48px; color: #5A67D8;'>🧠 Welcome to NeuroMentor</h1>
        </div>
    """, unsafe_allow_html=True)
    st.subheader("Your AI-Powered Mental Wellness Companion")
    st.markdown(
    "<h4 style='text-align: center;'>Advanced AI meets compassionate mental wellness.</h4>",
    unsafe_allow_html=True
    )
    st.write("""
NeuroMentor helps you manage stress and improve your mental wellness through multi-modal interactions.
Please enter your unique username to continue. All your data will remain private.
    """)
    
# -------------------- Auth Area --------------------
    if "username" not in st.session_state or not st.session_state.username:
        st.markdown("### 🔐 Login or Register")
        username = st.text_input("Enter your username to login or register:", key="username_input")

        # Centered buttons with spacing
        col_space, col_login, col_register, col_space2 = st.columns([1.5, 1, 1, 1.5])
        login_clicked = False
        register_clicked = False

        with col_login:
            login_clicked = st.button("🔓 Login", use_container_width=True)

        with col_register:
            register_clicked = st.button("📝 Register", use_container_width=True)

        if login_clicked:
            if username.strip() == "":
                st.error("Username cannot be empty.")
            else:
                get_or_create_user(username.strip())
                st.session_state.username = username.strip()
                st.success(f"Welcome back, {username.strip()}!")
                st.experimental_rerun()

        if register_clicked:
            if username.strip() == "":
                st.error("Username cannot be empty.")
            else:
                get_or_create_user(username.strip())
                st.success(f"New user created: {username.strip()}. Please log in now.")
                st.experimental_rerun()

        st.warning("⚠️ You must log in to access all features.")

    else:
        st.success(f"✅ You're logged in as: `{st.session_state.username}`")

    # Display the markdown heading as left-aligned by default
    st.markdown("<h3 style='text-align: left;'> 🧭 Use the sidebar to explore:</h3>", unsafe_allow_html=True)

    
    st.write("""
- **ChatterBox:** Chat with our supportive AI.
- **Voice Lounge:** Speak your thoughts and listen to responses.
- **Documents & Images:** Upload files or images for analysis.
- **Search Solutions:** Retrieve the latest information.
- **History & Insights:** Review your chats and view analytics.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
