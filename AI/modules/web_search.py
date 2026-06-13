from ddgs import DDGS

def search_web(query, max_results=5):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

        if not results:
            return []

        formatted = []
        for item in results[:5]:
            formatted.append({
                "title": item.get("title", "").strip(),
                "body": item.get("body", "").strip(),
                "url": item.get("href", "").strip()
            })

        return formatted

    except ImportError:
        return [{
            "title": "Search Error",
            "body": "DDGS package is not installed. Run: pip install ddgs",
            "url": ""
        }]
    except Exception as e:
        return [{
            "title": "Search Error",
            "body": str(e),
            "url": ""
        }]