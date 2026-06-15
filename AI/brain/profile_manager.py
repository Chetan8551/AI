import json
from pathlib import Path

PROFILE_FILE = Path(
    "data/profile.json"
)


def load_profile():

    if not PROFILE_FILE.exists():
        return {}

    try:

        with open(
            PROFILE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except:
        return {}


def save_profile(profile):

    with open(
        PROFILE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            profile,
            f,
            indent=4,
            ensure_ascii=False
        )


def update_profile(
    key,
    value
):

    profile = load_profile()

    profile[key] = value

    save_profile(profile)

def get_name():
    profile = load_profile()
    return profile.get("name")


def get_preferred_name():
    profile = load_profile()
    return profile.get("preferred_name")