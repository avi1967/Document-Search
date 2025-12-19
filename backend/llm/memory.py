chat_memory = {}

def add_message(session_id, role, content):
    chat_memory.setdefault(session_id, []).append({
        "role": role,
        "content": content
    })

def get_history(session_id, limit=5):
    return chat_memory.get(session_id, [])[-limit:]
