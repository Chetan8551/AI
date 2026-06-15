import ollama

MODEL = "phi4-mini"


def understand_memory(text):

    prompt = f"""
User said:

{text}

Determine whether the user is giving personal information.

Possible categories:

name
preferred_name
project
preference
goal
location
general

If memory exists return:

YES|category|memory

Examples:

My name is Chetan

YES|name|User's first name is Chetan

Call me Boss

YES|preferred_name|User prefers to be called Boss

I am working on a project called Jarvis

YES|project|User is building an AI project named Jarvis

I love Python

YES|preference|User likes Python

Return:

NO

if no memory should be stored.

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

    except:
        return None