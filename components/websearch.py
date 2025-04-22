# components/websearch.py
import streamlit as st
from utils.web_search import live_search
from agent.neuromentor_agent import generate_response  # Make sure folder is 'agents' not 'agent'

def summarize_links(links):
    """Send top links to Gemini to summarize for the user."""
    context = "Summarize the following pages into simple, clear, helpful tips for a student or professional:\n"
    for idx, link in enumerate(links, 1):
        context += f"{idx}. {link}\n"

    # Call Gemini to summarize
    summary = generate_response(context)

    # Extract only the text part if summary is an object
    if hasattr(summary, 'content'):
        summary = summary.content

    return summary.strip()

def render_web_search():
    st.title("🌐 NeuroMentor Web Search")
    st.subheader("Ask your questions, get smart, supportive answers!")

    if "username" not in st.session_state:
        st.error("🔒 Please log in from the Home page first.")
        return

    query = st.text_input("What's your question? (Ask clearly):")
    if st.button("🔎 Search"):
        if not query.strip():
            st.error("❗ Please enter a valid question.")
            return

        with st.spinner("Searching the web and preparing your personalized answer..."):
            results = live_search(query)

            if results:
                # Take top 3 links
                top_links = [r.get("link") for r in results[:3] if r.get("link")]

                # Summarize using Gemini
                summarized_answer = summarize_links(top_links)

                # Show summarized answer nicely
                st.success("✅ NeuroMentor's Summarized Answer:")
                st.markdown(f"""
                <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; font-size: 16px;">
                <b>🧠 NeuroMentor says:</b><br><br>
                {summarized_answer}
                </div>
                """, unsafe_allow_html=True)

                # Show helpful reference links
                if top_links:
                    st.markdown("---")
                    st.markdown("**🔗 Helpful References:**")
                    for link in top_links:
                        st.markdown(f"- [{link}]({link})")
            else:
                st.warning("⚠️ No results found or an error occurred. Try rephrasing your question!")
