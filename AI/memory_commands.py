from brain.memory_engine import load_memories
from brain.profile_manager import load_profile


def handle_memory_commands(text):

    lowered = text.lower().strip()

    if lowered == "show memory":

        lines = []

        profile = load_profile()

        for key, value in profile.items():
            lines.append(f"- {key}: {value}")

        memories = load_memories()

        for item in memories:
            lines.append(
                f"- {item['memory']}"
            )

        if not lines:
            return "Memory is empty."

        return "\n".join(lines)

    return None