import ollama

MEMORY_MODEL = "phi4-mini"


def retrieve_memories(user_input, memories):

    if not memories:
        return []

    memory_text = "\n".join(
        f"{i+1}. {fact}"
        for i, (fact, category) in enumerate(memories)
    )

    prompt = f"""
You are a memory retrieval engine.

User message:
{user_input}

Stored memories:

{memory_text}

Return the numbers of the memories
that are useful for answering the user.

Example:

1,4

If none are useful return:

NONE

Output only.
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

        if answer.upper() == "NONE":
            return []

        selected = []

        for x in answer.split(","):

            x = x.strip()

            if x.isdigit():

                idx = int(x) - 1

                if 0 <= idx < len(memories):
                    selected.append(
                        memories[idx][0]
                    )

        return selected

    except Exception:
        return []