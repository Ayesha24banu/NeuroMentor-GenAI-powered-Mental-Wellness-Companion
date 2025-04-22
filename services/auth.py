# services/auth.py
import os
import json

USER_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    os.makedirs("data", exist_ok=True)
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_or_create_user(username: str):
    users = load_users()
    if username not in users:
        # Create a new user entry with an empty chat history structure
        users[username] = {
            "username": username,
            "chat_sessions": {}  # to be populated later
        }
        save_users(users)
    return users[username]
