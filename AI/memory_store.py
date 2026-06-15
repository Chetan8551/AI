import json
from pathlib import Path

BASE = Path("data")
BASE.mkdir(exist_ok=True)

MEMORY_FILE = BASE / "memories.json"
CHAT_FILE = BASE / "conversations.json"
PROFILE_FILE = BASE / "profile.json"


# -------------------------
# Helpers
# -------------------------

def _load(file, default):
    if not file.exists():
        return default
    try:
        return json.loads(file.read_text(encoding="utf-8"))
    except:
        return default


def _save(file, data):
    file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# -------------------------
# PROFILE
# -------------------------

def update_profile(key, value):
    profile = _load(PROFILE_FILE, {})
    profile[key] = value
    _save(PROFILE_FILE, profile)


def get_profile():
    return _load(PROFILE_FILE, {})


def get_name():
    return get_profile().get("name")


def get_preferred_name():
    return get_profile().get("preferred_name")


# -------------------------
# CONVERSATIONS
# -------------------------

def save_conversation(user, assistant):
    chats = _load(CHAT_FILE, [])

    chats.append({
        "user": user.strip(),
        "assistant": assistant.strip()
    })

    _save(CHAT_FILE, chats)


def get_recent_messages(limit=10):
    chats = _load(CHAT_FILE, [])[-limit:]

    messages = []
    for c in chats:
        messages.append({"role": "user", "content": c["user"]})
        messages.append({"role": "assistant", "content": c["assistant"]})

    return messages


def clear_memory():
    _save(CHAT_FILE, [])


# -------------------------
# FACT MEMORY
# -------------------------

def save_memory(memory, category="general"):
    memories = _load(MEMORY_FILE, [])

    item = {
        "memory": memory.strip(),
        "category": category
    }

    # prevent duplicates (case insensitive)
    for m in memories:
        if m["memory"].lower() == item["memory"].lower():
            return

    memories.append(item)
    _save(MEMORY_FILE, memories)


def get_all_facts():
    return _load(MEMORY_FILE, [])


def get_facts_text(limit=20):
    facts = _load(MEMORY_FILE, [])[-limit:]
    return "\n".join(f"- {f['memory']}" for f in facts)


def delete_fact(keyword):
    memories = _load(MEMORY_FILE, [])

    memories = [
        m for m in memories
        if keyword.lower() not in m["memory"].lower()
    ]

    _save(MEMORY_FILE, memories)