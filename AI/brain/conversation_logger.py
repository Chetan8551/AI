import json
from pathlib import Path

FILE = Path("data/conversations.jsonl")

FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


def save_conversation(user, assistant):

    record = {
        "user": user,
        "assistant": assistant
    }

    with open(
        FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(
                record,
                ensure_ascii=False
            ) + "\n"
        )


def get_recent(limit=20):

    if not FILE.exists():
        return []

    with open(
        FILE,
        "r",
        encoding="utf-8"
    ) as f:

        lines = f.readlines()

    records = []

    for line in lines[-limit:]:

        try:
            records.append(
                json.loads(line)
            )
        except:
            pass

    return records