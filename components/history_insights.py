# components/history_insights.py

import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Ensure these imports are valid and available in your utils module
from utils.analytics import analyze_sentiment, analyze_emotions
from utils.file_ops import get_all_session_paths, load_chat_from_file
from utils.voice_memory import load_voice_messages
from utils.pdf_export import export_history_pdf

def show_history_page():
    # --- Ensure user is logged in ---
    if "username" not in st.session_state or not st.session_state.username:
        st.error("🚫 You must log in to access History & Insights.")
        st.stop()

    # --- intro ---
    st.title("📊 NeuroMentor - History & Insights")
    st.subheader("🧠 Your Emotional Journey & Reflections")
    st.write("✨ Reflect on your growth—track moods, conversations, and topics over time!")
    st.divider()

    # ——— Top Bar Controls ———
    top_col1, top_col2, top_col3, top_col4 = st.columns([2, 2, 2, 1])

    with top_col1:
        start_date = st.date_input("🗓️ Start Date", datetime.today().replace(day=1), key="history_start_date")
    with top_col2:
        end_date = st.date_input("🗓️ End Date", datetime.today(), key="history_end_date")
    with top_col3:
        username = st.session_state["username"]
        st.text_input("👭 Username", value=username, disabled=True)
    
    st.divider()

    # ——— Load Session Data ———
    sessions = []
    all_paths = get_all_session_paths()

    # Iterate through all session paths and filter by date
    for chat_path in all_paths:
        date_str = os.path.basename(os.path.dirname(chat_path))
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if not (start_date <= date_obj <= end_date):
            continue

        # Load chat and voice messages
        try:
            chat_msgs = load_chat_from_file(chat_path)
        except Exception as e:
            st.error(f"Error loading chat session from {chat_path}: {e}")
            continue

        voice_msgs = load_voice_messages(username)

        # Ensure that chat_msgs is a list and contains the expected data structure
        if not isinstance(chat_msgs, list):
            st.error(f"Expected 'chat_msgs' to be a list, but got {type(chat_msgs)}.")
            continue

        # Combine text from chat and voice
        combined_text = " ".join(m["content"] for m in chat_msgs) + " " + " ".join(v["content"] for v in voice_msgs if v["type"] == "text")

        # Sentiment and emotion analysis
        sent = analyze_sentiment(combined_text)
        emos = analyze_emotions(combined_text)
        primary = max(emos, key=emos.get) if emos else "neutral"

        sessions.append({
            "date": date_obj,
            "sentiment_score": sent["score"],
            "primary_emotion": primary,
            "raw_text": combined_text,
            **emos
        })

    if not sessions:
        st.warning("⚠️ No session data available for this date range.")
        return

    df = pd.DataFrame(sessions).sort_values("date")
    df["date"] = pd.to_datetime(df["date"])

    # ——— Tabs Layout ———
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📈 Trends", "🎭 Emotions", "🌀 Word Cloud", "📚 Logs", "📥 Download", "💬 Chat History", "🎙️ Voice History"])

    with tab1:
        st.subheader("📈 Sentiment Over Time")
        fig = px.line(
            df, x="date", y="sentiment_score",
            markers=True,
            title="📈 Select a range to explore sessions",
            labels={"date": "🗓️ Date", "sentiment_score": "😊 Sentiment Score"}
        )
        fig.update_layout(dragmode='select')
        st.plotly_chart(fig, use_container_width=True)

        st.caption("🎯 Tip: Drag your mouse to select sessions on the chart!")

        # Metrics Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Sessions", len(df))
        with col2:
            st.metric("💬 Avg Sentiment", f"{df.sentiment_score.mean():.2f}")
        with col3:
            st.metric("🎭 Top Emotion", df.primary_emotion.mode()[0].capitalize())
        with col4:
            st.metric("📅 Active Range", f"{df.date.min().date()} → {df.date.max().date()}")

        st.divider()

    with tab2:
        st.subheader("🎭 Emotion Insights")
    
        # Ensure 'date' is in datetime format
        df["date"] = pd.to_datetime(df["date"])
    
        # Create Pie chart for Primary Emotion Distribution
        pie = px.pie(
            df, names="primary_emotion",
            title="🎭 Primary Emotion Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(pie, use_container_width=True)

        # Create Weekly Emotion Trend
        # Get emotion-related columns
        emotion_cols = [col for col in df.columns if col not in ["date", "sentiment_score", "primary_emotion", "raw_text"]]
    
        # Resample by week and calculate mean for each emotion
        weekly_emotions = df.set_index("date")[emotion_cols].resample("W").mean().reset_index()

        # Create area chart for weekly emotion trends
        fig2 = px.area(
            weekly_emotions, x="date", y=emotion_cols,
            title="📆 Weekly Emotion Fluctuations",
            labels={"date": "🗓️ Date"},
            groupnorm="percent"  # Normalize to percent for better visualization
        )
        st.plotly_chart(fig2, use_container_width=True) 
         
    with tab3:
        st.subheader("🌀 Word Cloud from Conversations")
        text_corpus = " ".join(df["raw_text"].tolist())

        wc = WordCloud(width=800, height=400, background_color="white").generate(text_corpus)

        fig_wc, ax_wc = plt.subplots(figsize=(8, 4))
        ax_wc.imshow(wc, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

    with tab4:
        st.subheader("📚 Session Text Logs")
        for idx, row in df.iterrows():
            with st.expander(f"🗓️ {row['date'].date()} — {row['primary_emotion'].capitalize()}"):
                st.markdown(row["raw_text"])

    with tab5:
        st.subheader("📥 Download Filtered Data")
        # Filter data based on selected start and end date
        filtered_chat = df[df['date'].dt.date.between(start_date, end_date)]
        filtered_voice = df[df['date'].dt.date.between(start_date, end_date)]
    
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Download Chat Data**")
            if not filtered_chat.empty:
                # Download Chat CSV
                chat_csv = filtered_chat.drop(columns=["raw_text"]).to_csv(index=False).encode('utf-8')
                st.download_button("Download Chat CSV", data=chat_csv, file_name="chat_data.csv", mime="text/csv")

                # Download Chat JSON
                chat_json = filtered_chat.drop(columns=["raw_text"]).to_json(orient="records", indent=2)
                st.download_button("Download Chat JSON", data=chat_json, file_name="chat_data.json", mime="application/json")

                # Download Chat PDF
                pdf_bytes = export_history_pdf(start_date, end_date, filtered_chat, export_type="chat")
                st.download_button(
                "Download Chat PDF",
                    data=pdf_bytes,
                    file_name="chat_data.pdf",
                    mime="application/pdf"
                )

            else:
                st.info(f"No chat data available for the selected date range ({start_date} → {end_date}).")

        with col2:
            st.markdown("**Download Voice Data**")
            if not filtered_voice.empty:
                # Download Voice CSV
                voice_csv = filtered_voice.drop(columns=["raw_text"]).to_csv(index=False).encode('utf-8')
                st.download_button("Download Voice CSV", data=voice_csv, file_name="voice_data.csv", mime="text/csv")

                # Download Voice PDF
                pdf_bytes = export_history_pdf(start_date, end_date, filtered_voice, export_type="voice")
                st.download_button(
                    "Download Voice PDF",
                    data=pdf_bytes,
                    file_name="voice_data.pdf",
                    mime="application/pdf"
                ) 
            else:
                st.info(f"No voice data available for the selected date range ({start_date} → {end_date}).")

    # Tab 6: Chat History filtered by selected date range
    with tab6:
        st.subheader("💬 Chat History")
        
        # Filter chat data based on selected start and end date
        filtered_chat = df[df['date'].dt.date.between(start_date, end_date)]
        
        if not filtered_chat.empty:
            for idx, row in filtered_chat.iterrows():
                with st.expander(f"🗓️ {row['date'].date()} — Chat Session"):
                    st.markdown(row["raw_text"])
        else:
            st.info(f"No chat history available for the selected date range ({start_date} → {end_date}).")

    # Tab 7: Voice History filtered by selected date range
    with tab7:
        st.subheader("🎙️ Voice Message History")
        
        # Filter voice data based on selected start and end date
        filtered_voice = df[df['date'].dt.date.between(start_date, end_date)]
        
        if not filtered_voice.empty:
            for idx, row in filtered_voice.iterrows():
                with st.expander(f"🗓️ {row['date'].date()} — Voice Session"):
                    st.markdown(row["raw_text"])
        else:
            st.info(f"No voice message history available for the selected date range ({start_date} → {end_date}).")
