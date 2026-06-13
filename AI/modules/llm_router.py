import json
import ollama

ROUTER_MODEL = "llama3.2:3b"

ROUTER_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "enum": [
                "chat",
                "dictionary",
                "books",
                "weather",
                "wikipedia",
                "currency",
                "github_user",
                "github_repo",
                "anime",
                "holidays",
                "joke",
                "ip_info",
                "web_search",
                "email",
                "calendar",
                "maps"
            ]
        },
        "sub_intent": {"type": "string"},
        "entity": {"type": "string"},
        "extra": {"type": "string"},
        "country_code": {"type": "string"},
        "year": {"type": "integer"},
        "amount": {"type": "number"},
        "base_currency": {"type": "string"},
        "target_currency": {"type": "string"},
        "owner": {"type": "string"},
        "repo": {"type": "string"},
        "needs_web_search": {"type": "boolean"},
        "confidence": {"type": "number"}
    },
    "required": [
        "intent",
        "sub_intent",
        "entity",
        "extra",
        "country_code",
        "year",
        "amount",
        "base_currency",
        "target_currency",
        "owner",
        "repo",
        "needs_web_search",
        "confidence"
    ]
}

ROUTER_PROMPT = """
You are a routing model for a local AI assistant called Jarvis.

Your job is to classify the user's message and extract structured fields.

Return valid JSON only.
Do not answer the user.
Do not explain anything.
Always follow the schema exactly.

Rules:
- Understand English, Hindi, and Hinglish.
- If user asks for a meaning/definition, use intent = "dictionary".
- If user asks about a book, author, novel, writer, or book details, use intent = "books".
- If user asks for weather, use intent = "weather".
- If user asks for biography/general encyclopedia-style facts, use intent = "wikipedia".
- If user asks for conversion like 100 USD to INR, use intent = "currency".
- If user asks for GitHub user info, use intent = "github_user".
- If user asks for GitHub repository info, use intent = "github_repo".
- If user asks for anime, manga-like anime info, top anime, or anime character, use intent = "anime".
- If user asks for public holidays, use intent = "holidays".
- If user asks for a joke, use intent = "joke".
- If user asks for IP or IP-based location, use intent = "ip_info".
- If user asks for maps, routes, directions, or place navigation, use intent = "maps".
- If user asks for email sending, use intent = "email".
- If user asks for calendar/meeting/schedule, use intent = "calendar".
- If user asks for latest/current/live/news/recent information, use intent = "web_search" and set needs_web_search = true.
- If the message is casual conversation, opinion, feedback, or does not map cleanly to a tool, use intent = "chat".

Field rules:
- sub_intent examples: "definition", "summary", "author", "top_list", "character", "forecast", "biography".
- entity should contain the main subject, cleaned of filler words.
- extra can contain a short secondary detail if useful, otherwise empty string.
- For holidays, use country_code like IN, US, GB if inferable, otherwise IN. Use year if given, otherwise 2026.
- For currency, fill amount, base_currency, target_currency when available; otherwise defaults: 0, "", "".
- For github_repo, fill owner and repo separately if possible.
- For all unused string fields return "".
- For all unused numeric fields return 0, except year can default to 2026.
- confidence should be between 0 and 1.
"""

def route_query(user_input: str):
    response = ollama.chat(
        model=ROUTER_MODEL,
        messages=[
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": user_input}
        ],
        format=ROUTER_SCHEMA,
        options={
            "temperature": 0
        }
    )

    content = response["message"]["content"]
    data = json.loads(content)

    return {
        "intent": data.get("intent", "chat"),
        "sub_intent": data.get("sub_intent", ""),
        "entity": data.get("entity", ""),
        "extra": data.get("extra", ""),
        "country_code": data.get("country_code", "IN") or "IN",
        "year": data.get("year", 2026) or 2026,
        "amount": data.get("amount", 0) or 0,
        "base_currency": data.get("base_currency", "") or "",
        "target_currency": data.get("target_currency", "") or "",
        "owner": data.get("owner", "") or "",
        "repo": data.get("repo", "") or "",
        "needs_web_search": data.get("needs_web_search", False),
        "confidence": data.get("confidence", 0.0) or 0.0
    }