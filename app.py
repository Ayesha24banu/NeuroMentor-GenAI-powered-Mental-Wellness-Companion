#app.py 
import streamlit as st

# -------------------- Page Configuration --------------------
st.set_page_config(
    page_title="NeuroMentor - AI Wellness Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from components import home, chat, voice, documents_images, websearch, history_insights
from config.settings import settings  # Loads API keys from .env
from services.auth import get_or_create_user  # Simple username-based authentication

# -------------------- Load Custom CSS --------------------
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")  # Linking to the external style.css file

# -------------------- Session Auth Check --------------------
if "username" not in st.session_state or not st.session_state.username:
    home.render_home()
    st.stop()

# -------------------- Sidebar with Logo, Profile, Navigation --------------------
# -------------------- Sidebar --------------------
st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #f7f9fc;
        }
        .sidebar-title {
            font-size: 22px;
            color: #5A67D8;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .section-header {
            margin-top: 1.5rem;
            font-weight: bold;
            color: #5A67D8;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)  

# Profile Info
st.sidebar.markdown("<div class='sidebar-title'>🧠 NeuroMentor</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='section-header'>👤 Profile</div>", unsafe_allow_html=True)
st.sidebar.markdown(f"**Username:** `{st.session_state.username}`")

# Navigation Title
st.sidebar.markdown("<div class='section-header'>📂 Navigation</div>", unsafe_allow_html=True)

# Navigation Radio Buttons
page = st.sidebar.radio(
    "Select a section:",
    options=[
        "🏠 Home",
        "💬 ChatterBox",
        "🎤 Voice Lounge",
        "📄 Documents & 🖼️ Images",
        "🌐 Search Solutions",
        "📊 History & Insights"
    ],
    index=0,
    label_visibility="collapsed"
)

# Logout button
with st.sidebar:
    st.markdown("<div class='section-header'>🔐 Session</div>", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_button"):
        st.session_state.clear()
        st.success("You have been logged out.")
        st.experimental_rerun()

# -------------------- Page Routing --------------------

if page == "🏠 Home":
    home.render_home()
elif page == "💬 ChatterBox":
    chat.render_chat()
elif page == "🎤 Voice Lounge":
    voice.render_voice()
elif page == "📄 Documents & 🖼️ Images":
    documents_images.render()
elif page == "🌐 Search Solutions":
    websearch.render_web_search()
elif page == "📊 History & Insights":
    history_insights.show_history_page()
else:
    st.error("Section not found.")

# ——— Footer ———————————————————————————————————————————
st.sidebar.divider()
st.sidebar.caption("🚀 Powered by NeuroMentor • Built with ❤️")