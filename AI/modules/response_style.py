import ollama
from config import MODELS
from modules.persona import build_persona_prompt
from modules.state_manager import build_state_prompt

HUMANIZER_MODEL = MODELS["chat"]

HUMANIZER_SYSTEM_PROMPT = """
You are Jarvis's final response writer.

Rewrite responses so they sound like Jarvis: human, sharp, calm, and naturally conversational.

Rules:
- Always answer in English only.
- Keep replies short to medium.
- Sound like a real human assistant with personality.
- Understand humor, context, and light sarcasm.
- If the user is playful, you may respond with light wit.
- If the user is serious, reduce humor.
- Do not sound like a chatbot, therapist, article, or search engine.
- Remove robotic filler and weak generic lines.
- Remove unnecessary follow-up questions.
- If a direct recommendation is better, give it.
- If the answer is too long, compress it.
- Do not add facts not present in the raw answer.
- Make the answer easy to hear in voice mode.

Output only the final rewritten reply.
"""

def humanize_response(user_input: str, raw_answer: str) -> str:
    if not raw_answer or not raw_answer.strip():
        return raw_answer

    system_prompt = "\n\n".join([
        HUMANIZER_SYSTEM_PROMPT,
        build_persona_prompt(),
        build_state_prompt()
    ])

    try:
        response = ollama.chat(
            model=HUMANIZER_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
User message:
{user_input}

Raw answer:
{raw_answer}

Rewrite this into Jarvis's final natural reply.
"""
                }
            ],
            options={"temperature": 0.4}
        )

        final_text = response["message"]["content"].strip()
        return final_text if final_text else raw_answer

    except Exception:
        return raw_answer


def format_web_results_for_prompt(search_results):
    if not search_results:
        return ""

    lines = []
    for i, item in enumerate(search_results[:5], start=1):
        title = item.get("title", "").strip()
        body = item.get("body", "").strip()
        url = item.get("url", "").strip()

        lines.append(
            f"""Result {i}
Title: {title}
Snippet: {body}
URL: {url}"""
        )

    return "\n\n".join(lines)