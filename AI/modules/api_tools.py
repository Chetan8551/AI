import requests
import requests
from requests.exceptions import RequestException, Timeout

from config import OPEN_LIBRARY_SEARCH_URL, GOOGLE_BOOKS_API_URL


from config import (
    OPEN_METEO_GEOCODE,
    OPEN_METEO_FORECAST,
    WIKIPEDIA_API_URL,
    EXCHANGE_API_URL,
    GITHUB_API_URL,
    JIKAN_API_URL,
    NAGER_DATE_API_URL,
    DICTIONARY_API_URL,
    OPEN_LIBRARY_SEARCH_URL,
    JOKE_API_URL,
    IP_API_URL,
    GOOGLE_MAPS_API_KEY
)


def get_weather(city):
    try:
        geo_response = requests.get(
            OPEN_METEO_GEOCODE,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            },
            timeout=15
        )
        geo_data = geo_response.json()

        if "results" not in geo_data or not geo_data["results"]:
            return f"Weather error: Could not find location '{city}'."

        place = geo_data["results"][0]
        lat = place["latitude"]
        lon = place["longitude"]
        location_name = f"{place['name']}, {place.get('country', '')}".strip(", ")

        weather_response = requests.get(
            OPEN_METEO_FORECAST,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,apparent_temperature,wind_speed_10m,weather_code",
                "timezone": "auto"
            },
            timeout=15
        )
        weather_data = weather_response.json()
        current = weather_data.get("current", {})

        temp = current.get("temperature_2m", "N/A")
        feels = current.get("apparent_temperature", "N/A")
        wind = current.get("wind_speed_10m", "N/A")
        code = current.get("weather_code", "N/A")

        return (
            f"Weather in {location_name}: "
            f"temperature {temp}°C, feels like {feels}°C, "
            f"wind speed {wind} km/h, weather code {code}."
        )
    except Exception as e:
        return f"Weather error: {e}"


def get_wikipedia_summary(topic):
    try:
        headers = {"User-Agent": "JarvisAI/1.0 (Chetan personal assistant project)"}
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "titles": topic
        }

        response = requests.get(
            WIKIPEDIA_API_URL,
            params=params,
            headers=headers,
            timeout=15
        )

        if response.status_code != 200:
            return f"Wikipedia error: HTTP {response.status_code}"

        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        if not pages:
            return f"Wikipedia error: No page found for '{topic}'."

        page = next(iter(pages.values()))
        if "missing" in page:
            return f"Wikipedia error: No page found for '{topic}'."

        title = page.get("title", topic)
        extract = page.get("extract", "").strip()

        if not extract:
            return f"Wikipedia error: No summary found for '{topic}'."

        short_summary = " ".join(extract.split()[:80])
        return f"{title}: {short_summary}"
    except Exception as e:
        return f"Wikipedia error: {e}"


def convert_currency(base, target, amount):
    try:
        response = requests.get(EXCHANGE_API_URL + base.upper(), timeout=15)
        data = response.json()

        if data.get("result") != "success":
            return "Currency error: Could not fetch exchange rates."

        rates = data.get("rates", {})
        if target.upper() not in rates:
            return f"Currency error: Target currency '{target}' not found."

        rate = rates[target.upper()]
        converted = float(amount) * float(rate)

        return f"{amount} {base.upper()} = {converted:.2f} {target.upper()} (rate: {rate})"
    except Exception as e:
        return f"Currency error: {e}"


def get_github_user(username):
    try:
        url = f"{GITHUB_API_URL}/users/{username}"
        headers = {"Accept": "application/vnd.github+json"}

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return "GitHub error: User not found."

        data = response.json()
        bio = data.get("bio") or "No bio available"
        name = data.get("name") or data.get("login")

        return (
            f"GitHub user {data.get('login')}: "
            f"name {name}, bio {bio}, public repos {data.get('public_repos')}, "
            f"followers {data.get('followers')}, profile {data.get('html_url')}."
        )
    except Exception as e:
        return f"GitHub error: {e}"


def get_github_repo(owner, repo):
    try:
        url = f"{GITHUB_API_URL}/repos/{owner}/{repo}"
        headers = {"Accept": "application/vnd.github+json"}

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return "GitHub error: Repository not found."

        data = response.json()
        description = data.get("description") or "No description available"
        language = data.get("language") or "Unknown"

        return (
            f"Repository {data.get('full_name')}: {description}, "
            f"stars {data.get('stargazers_count')}, forks {data.get('forks_count')}, "
            f"language {language}, url {data.get('html_url')}."
        )
    except Exception as e:
        return f"GitHub error: {e}"


def get_top_anime():
    try:
        response = requests.get(f"{JIKAN_API_URL}/top/anime", params={"limit": 5}, timeout=15)
        data = response.json().get("data", [])

        if not data:
            return "Anime error: Could not fetch top anime."

        items = []
        for anime in data[:5]:
            title = anime.get("title", "Unknown")
            score = anime.get("score", "N/A")
            items.append(f"{title} (score: {score})")

        return "Top anime right now: " + ", ".join(items) + "."
    except Exception as e:
        return f"Anime error: {e}"


def get_anime_info(query):
    try:
        response = requests.get(
            f"{JIKAN_API_URL}/anime",
            params={"q": query, "limit": 1},
            timeout=15
        )
        data = response.json().get("data", [])

        if not data:
            return f"Anime error: No anime found for '{query}'."

        anime = data[0]
        title = anime.get("title", "Unknown")
        synopsis = (anime.get("synopsis") or "No synopsis available").replace("\n", " ")
        episodes = anime.get("episodes", "N/A")
        score = anime.get("score", "N/A")
        status = anime.get("status", "N/A")

        short_synopsis = " ".join(synopsis.split()[:60])

        return (
            f"Anime {title}: episodes {episodes}, score {score}, status {status}. "
            f"Synopsis: {short_synopsis}"
        )
    except Exception as e:
        return f"Anime error: {e}"


def get_character_info(query):
    try:
        response = requests.get(
            f"{JIKAN_API_URL}/characters",
            params={"q": query, "limit": 1},
            timeout=15
        )
        data = response.json().get("data", [])

        if not data:
            return f"Character error: No character found for '{query}'."

        char = data[0]
        name = char.get("name", "Unknown")
        about = (char.get("about") or "No details available").replace("\n", " ")
        short_about = " ".join(about.split()[:60])

        return f"Character {name}: {short_about}"
    except Exception as e:
        return f"Character error: {e}"


def get_holidays(country_code="IN", year=2026):
    try:
        url = f"{NAGER_DATE_API_URL}/PublicHolidays/{year}/{country_code}"
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return f"Holiday error: API returned HTTP {response.status_code} for {country_code} in {year}."

        data = response.json()

        if not isinstance(data, list) or not data:
            return f"Holiday error: No holidays returned for {country_code} in {year}."

        top = data[:5]
        items = []

        for x in top:
            date = x.get("date", "unknown date")
            local_name = x.get("localName") or x.get("name") or "unknown holiday"
            items.append(f"{date}: {local_name}")

        return f"Public holidays for {country_code} in {year}: " + ", ".join(items) + "."
    except Exception as e:
        return f"Holiday error: {e}"

def get_word_meaning(word):
    try:
        response = requests.get(f"{DICTIONARY_API_URL}/{word}", timeout=15)

        if response.status_code != 200:
            return f"Dictionary error: Could not find meaning for '{word}'."

        data = response.json()
        if not isinstance(data, list) or not data:
            return f"Dictionary error: No meaning found for '{word}'."

        entry = data[0]
        word_text = entry.get("word", word)
        phonetic = entry.get("phonetic", "")

        meanings = entry.get("meanings", [])
        if not meanings:
            return f"Dictionary error: No meaning found for '{word}'."

        first_meaning = meanings[0]
        part_of_speech = first_meaning.get("partOfSpeech", "unknown")
        definitions = first_meaning.get("definitions", [])

        if not definitions:
            return f"Dictionary error: No definition found for '{word}'."

        definition = definitions[0].get("definition", "No definition available")
        example = definitions[0].get("example", "")

        result = f"{word_text}"
        if phonetic:
            result += f" ({phonetic})"
        result += f": {part_of_speech}. {definition}"

        if example:
            result += f" Example: {example}"

        return result
    except Exception as e:
        return f"Dictionary error: {e}"


def get_book_info(query):
    openlibrary_error = None

    try:
        response = requests.get(
            OPEN_LIBRARY_SEARCH_URL,
            params={"q": query, "limit": 3},
            timeout=8
        )

        if response.status_code == 200:
            data = response.json()
            docs = data.get("docs", [])

            if docs:
                book = docs[0]
                title = book.get("title", "Unknown")
                authors = book.get("author_name", ["Unknown author"])
                year = book.get("first_publish_year", "N/A")

                return (
                    f"Book result: {title} by {', '.join(authors[:3])}, "
                    f"first published in {year}."
                )
            else:
                openlibrary_error = "No results from Open Library."
        else:
            openlibrary_error = f"Open Library HTTP {response.status_code}"

    except Timeout:
        openlibrary_error = "Open Library timeout."
    except RequestException as e:
        openlibrary_error = f"Open Library request failed: {e}"

    try:
        response = requests.get(
            GOOGLE_BOOKS_API_URL,
            params={
                "q": query,
                "maxResults": 3,
                "printType": "books"
            },
            timeout=8
        )

        if response.status_code != 200:
            return f"Books error: Open Library failed ({openlibrary_error}) and Google Books returned HTTP {response.status_code}."

        data = response.json()
        items = data.get("items", [])

        if not items:
            return f"Books error: No book found for '{query}'. Open Library status: {openlibrary_error}"

        volume = items[0].get("volumeInfo", {})
        title = volume.get("title", "Unknown")
        authors = volume.get("authors", ["Unknown author"])
        published = volume.get("publishedDate", "N/A")
        description = volume.get("description", "")
        short_description = " ".join(description.split()[:35]) if description else ""

        result = f"Book result: {title} by {', '.join(authors[:3])}, published {published}."
        if short_description:
            result += f" Summary: {short_description}"

        return result

    except Timeout:
        return f"Books error: Open Library failed ({openlibrary_error}) and Google Books also timed out."
    except RequestException as e:
        return f"Books error: Open Library failed ({openlibrary_error}) and Google Books failed: {e}"
    except Exception as e:
        return f"Books error: fallback parsing failed: {e}"

def get_random_joke():
    try:
        response = requests.get(JOKE_API_URL, timeout=15)

        if response.status_code != 200:
            return "Joke error: Could not fetch a joke."

        data = response.json()
        setup = data.get("setup", "").strip()
        punchline = data.get("punchline", "").strip()

        if not setup and not punchline:
            return "Joke error: Joke data was empty."

        return f"Here's a joke: {setup} ... {punchline}"
    except Exception as e:
        return f"Joke error: {e}"


def get_ip_info():
    try:
        response = requests.get(IP_API_URL, timeout=15)

        if response.status_code != 200:
            return "IP error: Could not fetch IP information."

        data = response.json()
        if data.get("status") != "success":
            return "IP error: Could not fetch IP information."

        return (
            f"Your public IP seems to be {data.get('query')}. "
            f"Location: {data.get('city')}, {data.get('regionName')}, {data.get('country')}. "
            f"ISP: {data.get('isp')}."
        )
    except Exception as e:
        return f"IP error: {e}"


def send_email_stub():
    return "Email integration is not added yet. It needs an OAuth-based provider."


def calendar_stub():
    return "Calendar integration is not added yet. It needs an OAuth-based provider."


def maps_stub(query):
    if not GOOGLE_MAPS_API_KEY:
        return "Maps integration is not added yet. For now use web search for routes and places."
    return f"Maps placeholder ready for query: {query}"