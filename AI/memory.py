import sqlite3
from pathlib import Path

DB_PATH = Path("data/memory.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    assistant TEXT NOT NULL
)
""")
conn.commit()


def _clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = " ".join(text.split())
    return text


def save_conversation(user, assistant):
    user = _clean_text(user)
    assistant = _clean_text(assistant)

    if not user or not assistant:
        return

    cursor.execute(
        """
        INSERT INTO conversations(user, assistant)
        VALUES(?, ?)
        """,
        (user, assistant)
    )
    conn.commit()


def get_recent(limit=8):
    cursor.execute(
        """
        SELECT user, assistant
        FROM conversations
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )
    rows = cursor.fetchall()
    return rows[::-1]


def get_recent_messages(limit=8):
    rows = get_recent(limit)
    messages = []

    for user, assistant in rows:
        messages.append({
            "role": "user",
            "content": user
        })
        messages.append({
            "role": "assistant",
            "content": assistant
        })

    return messages


def get_context_text(limit=8):
    rows = get_recent(limit)
    lines = []

    for user, assistant in rows:
        lines.append(f"User: {user}")
        lines.append(f"Assistant: {assistant}")

    return "\n".join(lines)


def clear_memory():
    cursor.execute("DELETE FROM conversations")
    conn.commit()