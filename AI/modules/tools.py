from memory import get_context_text

from modules.router_stage1 import route_stage1
from modules.router_stage2 import route_stage2

from modules.api_tools import (
    get_weather,
    get_wikipedia_summary,
    convert_currency,
    get_github_user,
    get_github_repo,
    get_top_anime,
    get_anime_info,
    get_character_info,
    get_holidays,
    get_word_meaning,
    get_book_info,
    get_random_joke,
    get_ip_info,
    send_email_stub,
    calendar_stub,
    maps_stub
)


def handle_small_talk(text: str):
    t = text.lower().strip()

    positive = [
        "badiya", "bdhiya", "badhiya",
        "accha", "achha",
        "nice", "good", "great", "awesome",
        "mast", "sahi hai", "working now",
        "yes", "yess", "haha", "hehe"
    ]

    negative = [
        "maja nahi aaya",
        "maza nahi aaya",
        "not funny",
        "bakwas",
        "boring",
        "bad"
    ]

    if any(p in t for p in positive):
        return "Glad you liked it."

    if any(p in t for p in negative):
        return "Okay Boss, I will improve it."

    return None


def handle_dynamic_tools(user_input):
    small_talk_reply = handle_small_talk(user_input)
    if small_talk_reply:
        return small_talk_reply

    memory_text = get_context_text(limit=8)

    try:
        stage1 = route_stage1(user_input, memory_text)
    except Exception:
        return None

    route = stage1.get("route", "chat")
    confidence1 = stage1.get("confidence", 0.0)

    if route in ["chat", "web_search"]:
        return None

    if confidence1 < 0.40:
        return None

    try:
        stage2 = route_stage2(user_input, memory_text)
    except Exception:
        return None

    intent = stage2.get("intent", "")
    sub_intent = stage2.get("sub_intent", "")
    entity = stage2.get("entity", "")
    country_code = stage2.get("country_code", "IN")
    year = stage2.get("year", 2026)
    amount = stage2.get("amount", 0)
    base_currency = stage2.get("base_currency", "")
    target_currency = stage2.get("target_currency", "")
    owner = stage2.get("owner", "")
    repo = stage2.get("repo", "")
    confidence2 = stage2.get("confidence", 0.0)

    if confidence2 < 0.45:
        return None

    if intent == "dictionary":
        if not entity:
            return "Please tell me the word you want defined."
        return get_word_meaning(entity)

    if intent == "books":
        if not entity:
            return "Please tell me the book name."
        return get_book_info(entity)

    if intent == "weather":
        return get_weather(entity or "Dhule")

    if intent == "wikipedia":
        if not entity:
            return "Please tell me the topic you want to know about."
        return get_wikipedia_summary(entity)

    if intent == "currency":
        if amount and base_currency and target_currency:
            return convert_currency(base_currency, target_currency, amount)
        return "Please say it like: convert 100 USD to INR"

    if intent == "github_user":
        username = entity or owner
        if username:
            return get_github_user(username)
        return "Please provide the GitHub username."

    if intent == "github_repo":
        if owner and repo:
            return get_github_repo(owner, repo)
        return "Please provide the GitHub repository in owner slash repo format."

    if intent == "anime":
        if sub_intent == "top_list":
            return get_top_anime()

        if sub_intent == "character":
            if not entity:
                return "Please tell me the character name."
            return get_character_info(entity)

        if not entity:
            return "Please tell me the anime name."
        return get_anime_info(entity)

    if intent == "holidays":
        return get_holidays(country_code or "IN", year or 2026)

    if intent == "joke":
        return get_random_joke()

    if intent == "ip_info":
        return get_ip_info()

    if intent == "email":
        return send_email_stub()

    if intent == "calendar":
        return calendar_stub()

    if intent == "maps":
        return maps_stub(entity or user_input)

    return None


def is_web_search(query: str) -> bool:
    memory_text = get_context_text(limit=8)

    try:
        stage1 = route_stage1(query, memory_text)
        return stage1.get("route") == "web_search"
    except Exception:
        q = query.lower()
        fallback_words = [
            "latest", "news", "current", "today",
            "price", "live", "recent", "update",
            "trending", "score"
        ]
        return any(word in q for word in fallback_words)