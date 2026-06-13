import json
import ollama

STAGE1_MODEL = "llama3.2:3b"

STAGE1_SCHEMA = {
    "type": "object",
    "properties": {
        "route": {
            "type": "string",
            "enum": ["chat", "tool", "web_search"]
        },
        "reason": {
            "type": "string"
        },
        "confidence": {
            "type": "number"
        }
    },
    "required": ["route", "reason", "confidence"]
}

STAGE1_SYSTEM_PROMPT = """
You are the first-stage router for Jarvis.

Your job is to classify the user's message into exactly one route:
- chat
- tool
- web_search

Return valid JSON only.
Do not answer the user's question.

Rules:
- Use "web_search" for latest, current, live, recent, breaking, news, price, update, today, trending, score, stock, match.
- Use "tool" for weather, books, authors, word meanings, dictionary, GitHub, anime, holidays, currency conversion, IP info, joke, maps, email, calendar.
- Use "chat" for normal conversation, greeting, thanks, opinions, vague follow-up conversation, and casual talk.
- Understand English, Hindi, and Hinglish.
- If live/current information is needed, prefer "web_search".
- If the request clearly matches an internal tool, prefer "tool".
"""

def route_stage1(user_input: str, memory_text: str = ""):
    prompt = STAGE1_SYSTEM_PROMPT.strip()

    if memory_text.strip():
        prompt += f"\n\nRecent conversation:\n{memory_text}"

    response = ollama.chat(
        model=STAGE1_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        format=STAGE1_SCHEMA,
        options={"temperature": 0}
    )

    content = response["message"]["content"].strip()
    data = json.loads(content)

    return {
        "route": data.get("route", "chat"),
        "reason": data.get("reason", ""),
        "confidence": float(data.get("confidence", 0.0) or 0.0)
    }