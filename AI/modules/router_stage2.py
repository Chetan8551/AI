import json
import ollama

STAGE2_MODEL = "llama3.2:3b"

STAGE2_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "enum": [
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
        "confidence"
    ]
}

STAGE2_SYSTEM_PROMPT = """
You are the second-stage tool router for Jarvis.

Your job is to choose the exact tool intent and extract structured fields.

Return valid JSON only.
Do not answer the user's question.

Supported intents:
- dictionary
- books
- weather
- wikipedia
- currency
- github_user
- github_repo
- anime
- holidays
- joke
- ip_info
- email
- calendar
- maps

Rules:
- Understand English, Hindi, and Hinglish.
- For word meaning, definition, meaning of a word => dictionary
- For books, novels, writer, author, publication => books
- For encyclopedia/factual summary about a person, place, concept => wikipedia
- For currency conversion => currency
- For GitHub profile/user => github_user
- For GitHub repository/project => github_repo
- For anime list => anime with sub_intent=top_list
- For anime character => anime with sub_intent=character
- For anime show title/details => anime with sub_intent=anime_info
- For holidays/festivals by year/country => holidays
- For IP address/info => ip_info
- For directions/places/location => maps
- For email sending => email
- For calendar-related scheduling => calendar
- For fields not used, return empty string.
- For amount if unused return 0.
- For year if unused return 2026.
- For country_code if unknown return IN.
"""

def route_stage2(user_input: str, memory_text: str = ""):
    prompt = STAGE2_SYSTEM_PROMPT.strip()

    if memory_text.strip():
        prompt += f"\n\nRecent conversation:\n{memory_text}"

    response = ollama.chat(
        model=STAGE2_MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        format=STAGE2_SCHEMA,
        options={"temperature": 0}
    )

    content = response["message"]["content"].strip()
    data = json.loads(content)

    return {
        "intent": data.get("intent", ""),
        "sub_intent": data.get("sub_intent", ""),
        "entity": (data.get("entity", "") or "").strip(),
        "extra": (data.get("extra", "") or "").strip(),
        "country_code": (data.get("country_code", "IN") or "IN").strip().upper(),
        "year": int(data.get("year", 2026) or 2026),
        "amount": float(data.get("amount", 0) or 0),
        "base_currency": (data.get("base_currency", "") or "").strip().upper(),
        "target_currency": (data.get("target_currency", "") or "").strip().upper(),
        "owner": (data.get("owner", "") or "").strip(),
        "repo": (data.get("repo", "") or "").strip(),
        "confidence": float(data.get("confidence", 0.0) or 0.0)
    }