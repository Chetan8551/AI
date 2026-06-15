import ollama

MODEL = "phi4-mini"


def translate_to_english(text):

    prompt = f"""
Translate this sentence into natural English.

Rules:
- Keep the meaning exactly same.
- Return only translated sentence.
- No explanations.

Sentence:
{text}
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

        return response["message"]["content"].strip()

    except:
        return text