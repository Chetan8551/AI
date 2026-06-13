import json
import sqlite3
from pathlib import Path

DB_PATH = Path("data/state.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS assistant_state (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    state_json TEXT NOT NULL
)
""")
conn.commit()

DEFAULT_STATE = {
    "mode": "neutral",
    "user_mood": "unknown",
    "conversation_style": "normal",
    "sarcasm_detected": False,
    "humor_detected": False,
    "seriousness": "medium",
    "last_topic": "",
    "last_user_intent": "",
    "last_emotion_note": ""
}


def _normalize_state(data):
    state = DEFAULT_STATE.copy()
    if isinstance(data, dict):
        state.update(data)
    return state


def get_state():
    cursor.execute("SELECT state_json FROM assistant_state WHERE id = 1")
    row = cursor.fetchone()

    if not row:
        set_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()

    try:
        data = json.loads(row[0])
        return _normalize_state(data)
    except Exception:
        set_state(DEFAULT_STATE)
        return DEFAULT_STATE.copy()


def set_state(state):
    state = _normalize_state(state)
    payload = json.dumps(state, ensure_ascii=False)

    cursor.execute("""
    INSERT INTO assistant_state (id, state_json)
    VALUES (1, ?)
    ON CONFLICT(id) DO UPDATE SET state_json = excluded.state_json
    """, (payload,))
    conn.commit()


def reset_state():
    set_state(DEFAULT_STATE)


def update_state_from_user_input(user_input: str):
    text = (user_input or "").strip().lower()
    state = get_state()

    sarcasm_markers = [
        "wah", "haan haan", "yeah right", "sure", "obviously",
        "great", "amazing", "kya baat", "very funny", "nice joke"
    ]

    humor_markers = [
        "joke", "funny", "lol", "lmao", "haha", "hehe", "meme"
    ]

    bored_markers = [
        "bore", "boring", "nothing to do", "mood off"
    ]

    serious_markers = [
        "important", "serious", "career", "job", "interview",
        "problem", "help", "issue", "error", "bug"
    ]

    recommendation_markers = [
        "suggest", "recommend", "which one", "what should i",
        "movie", "anime", "watch", "best one"
    ]

    sarcasm_detected = any(marker in text for marker in sarcasm_markers)
    humor_detected = any(marker in text for marker in humor_markers)

    if any(marker in text for marker in bored_markers):
        state["user_mood"] = "bored"
    elif any(marker in text for marker in serious_markers):
        state["user_mood"] = "serious"
    else:
        state["user_mood"] = "normal"

    if sarcasm_detected:
        state["conversation_style"] = "playful"
        state["sarcasm_detected"] = True
    else:
        state["sarcasm_detected"] = False

    if humor_detected:
        state["humor_detected"] = True
        state["conversation_style"] = "playful"
    else:
        state["humor_detected"] = False

    if state["user_mood"] == "serious":
        state["seriousness"] = "high"
    elif state["user_mood"] == "bored":
        state["seriousness"] = "low"
    else:
        state["seriousness"] = "medium"

    if any(marker in text for marker in recommendation_markers):
        state["last_user_intent"] = "recommendation"
    else:
        state["last_user_intent"] = "general"

    state["last_topic"] = text[:120]
    state["last_emotion_note"] = f"mood={state['user_mood']}, style={state['conversation_style']}"

    set_state(state)
    return state


def build_state_prompt():
    state = get_state()

    return f"""
Current conversation state:
- user mood: {state['user_mood']}
- conversation style: {state['conversation_style']}
- sarcasm detected: {state['sarcasm_detected']}
- humor detected: {state['humor_detected']}
- seriousness: {state['seriousness']}
- last user intent: {state['last_user_intent']}
- last emotion note: {state['last_emotion_note']}

Use this state naturally.
Do not mention the state explicitly.
Adjust tone accordingly.
If sarcasm or humor is detected, understand the tone before answering literally.
If recommendation intent is detected, be decisive.
"""