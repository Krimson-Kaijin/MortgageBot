# memory.py
from datetime import datetime

# In-memory storage
user_chat_memory = {}

# Get the full chat context for a user
def get_user_context(user_id):
    return user_chat_memory.get(user_id, [])

# Add a new message to the user's memory
def append_user_message(user_id, role, content):
    if user_id not in user_chat_memory:
        user_chat_memory[user_id] = []
    user_chat_memory[user_id].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })

# Clear a user's context (for logout or reset)
def clear_user_context(user_id):
    user_chat_memory.pop(user_id, None)


