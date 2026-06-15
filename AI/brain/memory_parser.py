import ollama
from brain.profile_manager import update_profile
from brain.memory_engine import save_memory

MODEL = "phi4-mini"

def process_memory(user_input):

    prompt = f"""
You are a memory extraction engine.

User message:
{user_input}

Extract ONLY explicit facts.

Rules:
- Never guess.
- Never infer.
- Never invent.
- Only store information directly stated by the user.
- If nothing should be remembered return NONE.

Output formats:

PROFILE|field|value

Examples:

"My name is Chetan"
PROFILE|name|Chetan

"Call me Boss"
PROFILE|preferred_name|Boss

"Mujhe Mr Stark bulao"
PROFILE|preferred_name|Mr Stark

"I am building an AI called Jarvis"
MEMORY|project|User is building an AI called Jarvis

"I love Python"
MEMORY|preference|User loves Python

Output only.
"""

    try:

        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0
            }
        )

        result = response["message"]["content"].strip()

        if result.upper() == "NONE":
            return False

        parts = result.split("|")

        if len(parts) != 3:
            return False

        kind = parts[0].strip()
        field = parts[1].strip()
        value = parts[2].strip()

        if kind == "PROFILE":
            update_profile(field, value)
            return True

        if kind == "MEMORY":
            save_memory(value, field)
            return True

        return False

    except Exception as e:
        print("Memory Parser Error:", e)
        return False