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

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_facts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fact TEXT UNIQUE,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def save_fact(fact, category="general"):
    fact = _clean_text(fact)

    if not fact:
        return

    try:
        cursor.execute(
            """
            INSERT OR IGNORE INTO user_facts(fact, category)
            VALUES(?, ?)
            """,
            (fact, category)
        )
        conn.commit()

    except Exception:
        pass


def get_facts(limit=20):
    cursor.execute(
        """
        SELECT fact, category
        FROM user_facts
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    return cursor.fetchall()


def get_facts_text(limit=20):
    rows = get_facts(limit)

    if not rows:
        return ""

    return "\n".join(
        f"- {fact}"
        for fact, _ in rows
    )

def get_all_facts():

    cursor.execute("""
    SELECT fact, category
    FROM user_facts
    """)

    return cursor.fetchall()


def delete_fact(keyword):

    cursor.execute(
        """
        DELETE FROM user_facts
        WHERE fact LIKE ?
        """,
        (f"%{keyword}%",)
    )

    conn.commit()