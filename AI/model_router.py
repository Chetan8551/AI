from config import MODELS


def choose_model(prompt):

    prompt = prompt.lower()

    coding_keywords = [
        "code",
        "python",
        "html",
        "css",
        "javascript",
        "django",
        "flask",
        "react",
        "sql",
        "bug",
        "error"
    ]

    reasoning_keywords = [
        "solve",
        "logic",
        "reason",
        "math",
        "calculate",
        "equation"
    ]

    if any(word in prompt for word in coding_keywords):
        return MODELS["coder"]

    if any(word in prompt for word in reasoning_keywords):
        return MODELS["reasoning"]

    return MODELS["chat"]