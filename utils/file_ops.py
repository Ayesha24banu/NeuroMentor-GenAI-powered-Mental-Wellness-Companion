# utils/file_ops.py

import os
import json
from datetime import datetime

def get_all_session_paths(base_dir='data/chat_sessions'):
    """
    Get all the session paths under the specified base directory.
    This will return paths for all individual chat session files.
    """
    all_paths = []
    
    # Walk through the directory and subdirectories
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".json"):  # assuming each session is stored as a .json file
                all_paths.append(os.path.join(root, file))
    
    return all_paths

def load_chat_from_file(file_path):
    """
    Load chat session data from a JSON file.
    Auto-fix common problems like missing 'content' field.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_data = json.load(file)

        # If chat_data is a dict, it means it's not structured as expected
        if isinstance(chat_data, dict):
            chat_data = chat_data.get('messages', [])
            if not isinstance(chat_data, list):
                raise ValueError(f"Expected 'messages' to be a list in {file_path}, but got {type(chat_data)}.")

        cleaned_chat_data = []
        for idx, message in enumerate(chat_data):
            if "content" in message:
                # Content is properly available
                cleaned_chat_data.append(message)
            elif "response" in message and isinstance(message["response"], str):
                # Try to extract from messy Gemini response string
                content_start = message["response"].find('content="') + len('content="')
                content_end = message["response"].find('"', content_start)
                if content_start != -1 and content_end != -1 and content_end > content_start:
                    extracted_content = message["response"][content_start:content_end]
                else:
                    extracted_content = ""  # fallback if extraction fails

                cleaned_chat_data.append({
                    "role": message.get("role", "neuromentor"),
                    "content": extracted_content
                })
            elif "message" in message:
                # Old style 'message' key
                cleaned_chat_data.append({
                    "role": message.get("role", "unknown"),
                    "content": message["message"]
                })
            else:
                raise ValueError(f"Message at index {idx} is missing usable 'content' or 'response': {message}")

        return cleaned_chat_data  # Always return list of clean messages

    except FileNotFoundError:
        raise FileNotFoundError(f"Session file {file_path} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON in session file {file_path}.")
    except Exception as e:
        raise ValueError(f"Error loading chat session from {file_path}: {str(e)}")
