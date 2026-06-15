from brain.memory_engine import (
    load_memories
)


def get_all_memories():

    memories = load_memories()

    return [
        item["memory"]
        for item in memories
    ]