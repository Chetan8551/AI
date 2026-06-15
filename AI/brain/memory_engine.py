import json
from pathlib import Path

MEMORY_FILE = Path(
    "data/memories.json"
)


def load_memories():

    if not MEMORY_FILE.exists():
        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:
        return []


def save_memory(
    memory,
    category="general"
):
    if memory_exists(memory):
        return

    memories = load_memories()

    item = {
        "memory": memory,
        "category": category
    }

    if item not in memories:

        memories.append(item)

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                memories,
                f,
                indent=4,
                ensure_ascii=False
            )
def memory_exists(memory):

    memories = load_memories()

    for item in memories:

        if item["memory"].lower() == memory.lower():
            return True

    return False