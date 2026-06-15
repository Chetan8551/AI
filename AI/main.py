import ollama
from memory import (
    save_fact,
    get_all_facts
)
from brain.memory_parser import process_memory
from brain.semantic_memory import extract_memory_meaning
from brain.memory_engine import load_memories
from memory_commands import handle_memory_commands
from config import SYSTEM_PROMPT
from model_router import choose_model
from memory import save_conversation, get_recent_messages, clear_memory
from brain.translator import translate_to_english
from brain.memory_understanding import understand_memory
from brain.profile_manager import update_profile
from brain.memory_engine import save_memory
from modules.action import execute_command
from modules.web_search import search_web
from modules.tools import handle_dynamic_tools, is_web_search
from modules.voice_mode import listen
from modules.tts import speak
from modules.response_style import humanize_response, format_web_results_for_prompt


EXIT_COMMANDS = {"exit", "quit", "bye"}
CLEAR_MEMORY_COMMANDS = {"clear memory", "reset memory", "forget chat"}


def print_banner():
    print("=" * 60)
    print("JARVIS INITIALIZED")
    print("Memory + Actions + Web Search + Voice + APIs")
    print("=" * 60)
    print("\n1. Text Mode")
    print("2. Voice Mode")


def get_mode():
    mode = input("\nChoose mode: ").strip()
    return "2" if mode == "2" else "1"


def build_chat_messages(user_input, extra_system_prompt=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    all_memories = load_memories()

    relevant_facts = []

    for item in all_memories:
        relevant_facts.append(
            item["memory"]
        )

    if relevant_facts:

        memory_text = "\n".join(
            f"- {fact}"
            for fact in relevant_facts
        )

        messages.append(
            {
                "role": "system",
                "content": f"""
        Known information about the user:

        {memory_text}

        Rules:
        - Use this information only when relevant.
        - Maintain conversation continuity.
        - If the user asks about themselves, projects, preferences or past discussions, use these memories.
        - Do not repeat memories unless useful.
        """
            }
        )

    if extra_system_prompt:

        messages.append(
            {
                "role": "system",
                "content": extra_system_prompt
            }
        )

    history = get_recent_messages(limit=10)

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    return messages

def ask_llm(user_input, extra_system_prompt=None, temperature=0.6):
    model = choose_model(user_input)
    messages = build_chat_messages(user_input, extra_system_prompt)

    response = ollama.chat(
        model=model,
        messages=messages,
        options={"temperature": temperature}
    )

    raw_answer = response["message"]["content"].strip()
    return humanize_response(user_input, raw_answer)


def ask_llm_with_memory(user_input):
    extra_prompt = """
Reply in English only.
Do not use Hindi.
Keep the reply natural, human-like, and not robotic.
""".strip()

    return ask_llm(user_input, extra_system_prompt=extra_prompt, temperature=0.6)


def handle_web_query(user_input):
    speak("Searching the internet")

    search_results = search_web(user_input)

    if not search_results:
        return "I could not find anything useful right now."

    if len(search_results) == 1 and search_results[0].get("title") == "Search Error":
        return f"Web search failed. {search_results[0].get('body', 'Unknown error')}"

    context = format_web_results_for_prompt(search_results)

    extra_prompt = f"""
Use the web results below to answer the user's query.

Rules:
- Answer in English only.
- Do not use Hindi.
- Do not copy the search snippets directly.
- Extract only the important and useful points.
- Keep the answer short to medium by default.
- Make it sound like natural conversation.
- Mention source links only if really useful.

Web results:
{context}
""".strip()

    return ask_llm(user_input, extra_system_prompt=extra_prompt, temperature=0.4)


def get_user_input(mode):
    if mode == "2":
        print("\nPress ENTER and speak...")
        input()

        user_input = listen()
        if user_input and user_input.strip():
            print(f"\nBoss: {user_input}")
        return user_input

    return input("\nBoss: ")


def handle_special_commands(user_input):
    lowered = user_input.lower()

    if lowered in EXIT_COMMANDS:
        speak("Goodbye Boss")
        return "EXIT"

    if lowered in CLEAR_MEMORY_COMMANDS:
        clear_memory()
        answer = "Memory cleared."
        print(f"Jarvis: {answer}")
        speak(answer)
        return "CONTINUE"

    return None


def respond_and_save(user_input, answer):
    print(f"Jarvis: {answer}")
    speak(answer)
    save_conversation(user_input, answer)


def process_user_input(user_input):
    memory_response = handle_memory_commands(
        user_input
    )

    if memory_response:
        return memory_response

    english_text = translate_to_english(
        user_input
    )

    memory = understand_memory(
        english_text
    )

    if memory:

        category = memory["category"]
        value = memory["memory"]

        if category == "name":

            update_profile(
                "name",
                value.replace(
                    "User's first name is ",
                    ""
                )
            )

        elif category == "preferred_name":

            update_profile(
                "preferred_name",
                value.replace(
                    "User prefers to be called ",
                    ""
                )
            )

        else:

            save_memory(
                value,
                category
            )

    action_result = execute_command(
        user_input
    )

    if action_result:
        return humanize_response(
            user_input,
            str(action_result)
        )

    api_result = handle_dynamic_tools(
        user_input
    )

    if api_result:
        return humanize_response(
            user_input,
            str(api_result)
        )

    if is_web_search(user_input):
        return handle_web_query(user_input)

    return ask_llm_with_memory(
        user_input
    )
def main():
    print_banner()
    mode = get_mode()

    while True:
        user_input = get_user_input(mode)

        if not user_input or not user_input.strip():
            continue

        user_input = user_input.strip()

        special = handle_special_commands(user_input)
        if special == "EXIT":
            break
        if special == "CONTINUE":
            continue

        answer = process_user_input(user_input)
        respond_and_save(user_input, answer)


if __name__ == "__main__":
    main()