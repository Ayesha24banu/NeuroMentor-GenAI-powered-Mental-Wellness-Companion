# voice_memory.py

import os
import json
import datetime

# Path where voice messages will be saved
BASE_PATH = "data/voice_sessions/"  # Updated folder name to voice_sessions

# Ensure the base directory exists
os.makedirs(BASE_PATH, exist_ok=True)

# Function to save voice messages (both text and audio)
def save_voice_message(username, role, audio_bytes=None, text_message=None):
    """
    Save voice messages in a session-based directory for each user.
    Audio is saved as WAV, and text is saved as JSON for each session.
    """
    try:
        # Create a directory for the user if it doesn't exist
        user_dir = os.path.join(BASE_PATH, username)
        os.makedirs(user_dir, exist_ok=True)

        # Generate a timestamp for the current date
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        session_file_path = os.path.join(user_dir, f"{date_str}_session.json")

        # Create the session file if it doesn't exist
        if not os.path.exists(session_file_path):
            with open(session_file_path, "w") as session_file:
                json.dump([], session_file)

        # Load the existing session data
        with open(session_file_path, "r") as session_file:
            voice_history = json.load(session_file)

        # Prepare the message entry
        message_entry = {
            "role": role,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # If it's an audio message, save it as a WAV file and store the file path
        if audio_bytes:
            audio_filename = f"{datetime.datetime.now().strftime('%H%M%S')}_audio.wav"
            audio_path = os.path.join(user_dir, audio_filename)
            with open(audio_path, "wb") as audio_file:
                audio_file.write(audio_bytes)
            message_entry["type"] = "audio"
            message_entry["content"] = audio_path

        # If it's a text message, store the text
        if text_message:
            message_entry["type"] = "text"
            message_entry["content"] = text_message

        # Append the new message to the voice history
        voice_history.append(message_entry)

        # Save the updated voice history
        with open(session_file_path, "w") as session_file:
            json.dump(voice_history, session_file, indent=2)  # pretty print

        print(f"Saved {role} message for {username}.")
        return True
    
    except Exception as e:
        print(f"Error saving voice message: {e}")
        return False


# Function to load previous voice messages
def load_voice_messages(username):
    """
    Load voice messages (text and audio) for a specific user from today's session.
    Returns a list of messages (text or audio) for the user.
    """
    try:
        user_dir = os.path.join(BASE_PATH, username)
        if not os.path.exists(user_dir):
            return []

        # Find the session for today's date
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        session_file_path = os.path.join(user_dir, f"{date_str}_session.json")

        if os.path.exists(session_file_path):
            with open(session_file_path, "r") as session_file:
                voice_history = json.load(session_file)
            return voice_history
        else:
            return []

    except Exception as e:
        print(f"Error loading voice messages: {e}")
        return []


# Function to delete a voice session
def delete_voice_session(username, date):
    """
    Delete the voice session file for a specific user on a specific date.
    """
    try:
        session_file_path = os.path.join(BASE_PATH, username, f"{date}_session.json")
        if os.path.exists(session_file_path):
            os.remove(session_file_path)
            print(f"Deleted session for {username} on {date}")
            return True
        else:
            print(f"Session file for {username} on {date} not found.")
            return False
    except Exception as e:
        print(f"Error deleting voice session: {e}")
        return False
