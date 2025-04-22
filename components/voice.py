# components/voice.py
import os
import sys
import time
import random
import tempfile

import sounddevice as sd
import wavio
import pyttsx3
import speech_recognition as sr
import streamlit as st

from playsound import playsound
from utils.voice_memory import save_voice_message, load_voice_messages
from agent.neuromentor_agent import generate_response

# ------------------- Voice Utility Functions ------------------- #

def record_audio(duration=6, fs=44100):
    """Record audio for a given duration and save to a WAV file."""
    save_dir = os.path.join("data", "voice_sessions")
    os.makedirs(save_dir, exist_ok=True)

    filename = f"user_recording_{int(time.time())}.wav"
    save_path = os.path.join(save_dir, filename)

    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        wavio.write(save_path, recording, fs, sampwidth=2)
        return save_path
    except Exception as e:
        print(f"[Error] Recording audio failed: {str(e)}")
        return None

def speech_to_text(audio_path):
    """Convert recorded audio to text using Google's Speech Recognition API."""
    if not audio_path or not os.path.exists(audio_path):
        return "Sorry, the audio file was not found."

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
        os.remove(audio_path)  # Delete file after recognition
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError as e:
        return f"Speech recognition error: {str(e)}"
    except Exception as e:
        return f"Speech-to-text processing failed: {str(e)}"

def text_to_speech(text):
    """Convert text to speech and save the output as a WAV file."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Platform-specific voice selection
        if "linux" in sys.platform:
            engine.setProperty("voice", "english")
        elif "darwin" in sys.platform:
            engine.setProperty("voice", "com.apple.speech.synthesis.voice.Alex")
        elif "win" in sys.platform:
            engine.setProperty('voice', random.choice(voices).id)

        # Randomize speech rate slightly
        base_rate = engine.getProperty('rate')
        varied_rate = random.choice([base_rate - 20, base_rate, base_rate + 20])
        engine.setProperty('rate', varied_rate)

        save_dir = os.path.join("data", "voice_sessions")
        os.makedirs(save_dir, exist_ok=True)

        filename = f"neuromentor_tts_{int(time.time())}.wav"
        audio_path = os.path.join(save_dir, filename)

        engine.save_to_file(text, audio_path)
        engine.runAndWait()

        if os.path.exists(audio_path):
            return audio_path
        else:
            st.error("Text-to-speech audio file was not created.")
            return None
    except Exception as e:
        st.error(f"Text-to-Speech Error: {str(e)}")
        st.info(f"Generated Text: {text}")
        return None

# ------------------- Main Voice Chat Interface ------------------- #

def render_voice():
    st.title("🎙️ NeuroMentor Voice Chat")

    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = []

    if "username" not in st.session_state:
        st.session_state.username = "Guest"

    # Load previous messages
    previous_messages = load_voice_messages(st.session_state.username)
    if previous_messages:
        st.session_state.voice_messages.extend(previous_messages)

    # Centered Mic Button
    st.markdown("""
        <style>
        .center-button { display: flex; justify-content: center; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            record = st.button("🎙️ Tap to Speak", key="record_button", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if record:
        st.toast("Recording... 🎙️")
        audio_path = record_audio()

        if audio_path and os.path.exists(audio_path):
            # First read the user audio
            with open(audio_path, "rb") as audio_file:
                user_audio_bytes = audio_file.read()

            text = speech_to_text(audio_path)

            if text:
                # Save user message (text + audio bytes)
                st.session_state.voice_messages.append({
                    "role": "user",
                    "content": text,
                    "audio_path": audio_path
                })
                save_voice_message(st.session_state.username, "user", audio_bytes=user_audio_bytes, text_message=text)

                # Display user message
                st.markdown(f"🧑‍💻 **{st.session_state.username}:** {text}")
                st.audio(user_audio_bytes, format="audio/wav")

                # Generate AI response
                ai_response = generate_response(text)
                ai_audio_path = text_to_speech(ai_response)

                if ai_audio_path and os.path.exists(ai_audio_path):
                    with open(ai_audio_path, "rb") as ai_audio_file:
                        ai_audio_bytes = ai_audio_file.read()

                    st.session_state.voice_messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "audio_path": ai_audio_path
                    })
                    save_voice_message("NeuroMentor", "assistant", audio_bytes=ai_audio_bytes, text_message=ai_response)

                    # Display AI response
                    st.markdown(f"🤖 **NeuroMentor:** {ai_response}")
                    st.audio(ai_audio_bytes, format="audio/wav")

    