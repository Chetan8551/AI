import ollama


MEMORY_MODEL = "llama3.2:3b"


def extract_memory_meaning(user_input):

    prompt = f"""
You are a memory extraction engine.

Determine if the user said something
worth remembering permanently.

Examples:

"My name is Chetan"
=> YES|profile|User's first name is Chetan

"Call me Boss from now on"
=> YES|preference|User prefers to be called Boss

"I am working on a project named Jarvis"
=> YES|project|User is building a project called Jarvis

"I like Python"
=> YES|preference|User likes Python

"Open Chrome"
=> NO

Return ONLY:

YES|category|memory

or

NO

User:
{user_input}
"""

    try:

        response = ollama.chat(
            model=MEMORY_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response["message"]["content"].strip()

        if not answer.startswith("YES|"):
            return None

        parts = answer.split("|", 2)

        if len(parts) != 3:
            return None

        return {
            "category": parts[1].strip(),
            "memory": parts[2].strip()
        }

    except Exception:
        return None