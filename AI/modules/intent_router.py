import re
from datetime import datetime


LIVE_SEARCH_WORDS = [
    "latest",
    "today",
    "current",
    "recent",
    "live",
    "now",
    "price",
    "rate",
    "stock",
    "market",
    "news",
    "breaking",
    "update",
    "updates",
    "gold price",
    "gold rate",
    "silver price",
    "share price",
    "exchange rate"
]


def is_live_query(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in LIVE_SEARCH_WORDS)


def detect_api_intent(user_input):
    text = user_input.lower().strip()

    if any(x in text for x in ["weather", "temperature", "rain", "forecast"]):
        return "weather"

    if "convert" in text and re.search(r"\b[A-Z]{3}\b", user_input.upper()):
        return "currency"

    if "github user" in text:
        return "github_user"

    if "github repo" in text or "repository" in text:
        return "github_repo"

    if "top anime" in text or "best anime" in text:
        return "top_anime"

    if any(x in text for x in ["anime", "manga", "character"]) and not is_live_query(text):
        return "anime"

    if any(x in text for x in ["holiday", "holidays", "public holiday"]):
        return "holidays"

    if any(x in text for x in ["meaning of", "define", "definition of", "dictionary"]):
        return "dictionary"

    if any(x in text for x in ["book", "books", "author", "novel"]):
        return "books"

    if any(x in text for x in ["joke", "funny joke"]):
        return "joke"

    if any(x in text for x in ["my ip", "ip address", "my location by ip", "where am i from ip"]):
        return "ip_info"

    if "news" in text or "headline" in text:
        return "web_search"

    if "youtube" in text or "video" in text:
        return "web_search"

    if "send email" in text or "mail" in text:
        return "email"

    if "calendar" in text or "schedule" in text or "meeting" in text:
        return "calendar"

    if "map" in text or "route" in text or "location" in text:
        return "maps"

    if (
        text.startswith("who is")
        or text.startswith("what is")
        or text.startswith("tell me about")
        or "wikipedia" in text
    ):
        if is_live_query(text):
            return "web_search"
        return "wikipedia"

    return None


def extract_city(user_input):
    text = user_input.lower()
    patterns = [
        r"weather in ([a-zA-Z\s]+)",
        r"temperature in ([a-zA-Z\s]+)",
        r"rain in ([a-zA-Z\s]+)",
        r"forecast for ([a-zA-Z\s]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip().title()
    return None


def extract_wiki_topic(user_input):
    text = user_input.strip()
    prefixes = ["who is", "what is", "tell me about", "wikipedia"]
    lower = text.lower()

    for p in prefixes:
        if lower.startswith(p):
            return text[len(p):].strip(" :?-").strip()

    return text


def extract_currency(user_input):
    text = user_input.upper()
    match = re.search(r"(\d+(?:\.\d+)?)\s+([A-Z]{3})\s+(?:TO|INTO)\s+([A-Z]{3})", text)
    if match:
        amount = float(match.group(1))
        base = match.group(2)
        target = match.group(3)
        return amount, base, target
    return None


def extract_github_user(user_input):
    match = re.search(r"github user\s+([A-Za-z0-9_-]+)", user_input, re.IGNORECASE)
    return match.group(1) if match else None


def extract_github_repo(user_input):
    match = re.search(r"github repo\s+([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1), match.group(2)
    return None


def extract_anime_query(user_input):
    text = user_input.strip()
    prefixes = [
        "anime",
        "manga",
        "character",
        "tell me about anime",
        "tell me about manga",
        "who is"
    ]
    lower = text.lower()

    for p in prefixes:
        if lower.startswith(p):
            return text[len(p):].strip(" :?-").strip()

    return text


def extract_holiday_country_and_year(user_input):
    text = user_input.lower()
    year_match = re.search(r"\b(20\d{2})\b", text)
    year = int(year_match.group(1)) if year_match else datetime.now().year

    country_map = {
        "india": "IN",
        "united states": "US",
        "usa": "US",
        "uk": "GB",
        "united kingdom": "GB",
        "japan": "JP",
        "germany": "DE",
        "france": "FR",
        "canada": "CA",
        "australia": "AU"
    }

    for name, code in country_map.items():
        if name in text:
            return code, year

    return "IN", year


def extract_dictionary_word(user_input):
    text = user_input.lower().strip()
    prefixes = ["meaning of", "define", "definition of", "dictionary"]
    original = user_input.strip()

    for p in prefixes:
        if text.startswith(p):
            return original[len(p):].strip(" :?-").strip()

    return original


def extract_book_query(user_input):
    original = user_input.strip()
    text = original.lower()

    cleanup_phrases = [
        "tell me about the book",
        "tell me about book",
        "tell me about",
        "find book",
        "book",
        "books",
        "novel",
        "muze",
        "mujhe",
        "ke baremai batao",
        "ke bare mein batao",
        "ke bare me batao",
        "ke baremai",
        "ke bare mein",
        "ke bare me",
        "batao",
        "about the book",
        "about book",
    ]

    result = text
    for phrase in cleanup_phrases:
        result = result.replace(phrase, " ")

    result = " ".join(result.split())
    return result.strip(" ?!.,:-")


def extract_author_book_query(user_input):
    text = user_input.lower().strip()

    cleanup_phrases = [
        "author of",
        "writer of",
        "who wrote",
        "who is the author of",
        "harry potter ke author kon hai",
        "ke author kon hai",
        "ke author kaun hai",
        "author kon hai",
        "author kaun hai",
        "kisne likhi",
        "kisne likha",
        "kon likha",
        "kaun likha",
    ]

    result = text
    for phrase in cleanup_phrases:
        result = result.replace(phrase, " ")

    result = " ".join(result.split())
    return result.strip(" ?!.,:-")