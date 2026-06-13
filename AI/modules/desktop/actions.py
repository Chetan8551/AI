import re
from .controller import DesktopController

desktop = DesktopController()


def extract_coordinates(command: str):
    match = re.search(r"(\d+)\s*(?:,|\s)\s*(\d+)", command)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def extract_number(command: str, default=5):
    match = re.search(r"(\d+)", command)
    if match:
        return int(match.group(1))
    return default


def is_risky_command(cmd: str):
    risky_words = [
        "delete file",
        "format",
        "shutdown",
        "restart",
        "remove all",
        "close all",
        "kill all"
    ]
    return any(word in cmd for word in risky_words)


def handle_desktop_command(command: str):
    if not command:
        return "No desktop command given."

    cmd = command.lower().strip()

    if is_risky_command(cmd):
        return "Blocked risky desktop command."

    x, y = extract_coordinates(cmd)

    if "open start" in cmd or "start menu" in cmd:
        return desktop.open_start_menu()

    if "open run" in cmd or "run dialog" in cmd:
        return desktop.open_run()

    if "show desktop" in cmd or "minimize all" in cmd:
        return desktop.show_desktop()

    if "switch window" in cmd or "next window" in cmd:
        return desktop.switch_window()

    if "close window" in cmd or "close this window" in cmd:
        return desktop.close_window()

    if cmd == "copy" or "copy this" in cmd:
        return desktop.copy()

    if cmd == "paste" or "paste here" in cmd:
        return desktop.paste()

    if cmd == "cut" or "cut this" in cmd:
        return desktop.cut()

    if "select all" in cmd:
        return desktop.select_all()

    if cmd == "save" or "save file" in cmd:
        return desktop.save()

    if "undo" in cmd:
        return desktop.undo()

    if "redo" in cmd:
        return desktop.redo()

    if "press enter" in cmd or cmd == "enter":
        return desktop.enter()

    if "backspace" in cmd:
        return desktop.backspace()

    if cmd == "delete":
        return desktop.delete()

    if "volume up" in cmd:
        steps = extract_number(cmd, 5)
        return desktop.volume_up(steps)

    if "volume down" in cmd:
        steps = extract_number(cmd, 5)
        return desktop.volume_down(steps)

    if "mute" in cmd and "volume" in cmd:
        return desktop.mute_volume()

    if "play pause" in cmd or "pause music" in cmd or "resume music" in cmd:
        return desktop.media_play_pause()

    if "next track" in cmd or "next song" in cmd:
        return desktop.next_track()

    if "previous track" in cmd or "prev track" in cmd or "last song" in cmd:
        return desktop.prev_track()

    if "scroll up" in cmd:
        amount = extract_number(cmd, 500)
        return desktop.scroll_up(amount)

    if "scroll down" in cmd:
        amount = extract_number(cmd, 500)
        return desktop.scroll_down(amount)

    if "take screenshot" in cmd or "capture screen" in cmd:
        path = desktop.screenshot()
        return f"Screenshot saved at {path}"

    if "move mouse to" in cmd and x is not None and y is not None:
        return desktop.move_mouse(x, y)

    if "drag mouse to" in cmd and x is not None and y is not None:
        return desktop.drag_mouse(x, y)

    if "double click" in cmd:
        if x is not None and y is not None:
            return desktop.double_click(x, y)
        return desktop.double_click()

    if "right click" in cmd:
        if x is not None and y is not None:
            return desktop.right_click(x, y)
        return desktop.right_click()

    if "click" in cmd:
        if x is not None and y is not None:
            return desktop.click(x, y)
        return desktop.click()

    if cmd.startswith("type "):
        text = command[5:].strip()
        return desktop.type_text(text)

    if cmd.startswith("press "):
        key = cmd.replace("press ", "").strip()
        return desktop.press_key(key)

    if cmd.startswith("open "):
        app_name = command[5:].strip()
        return desktop.open_app(app_name)

    if cmd.startswith("kill "):
        process_name = command[5:].strip()
        return desktop.kill_app(process_name)

    return "Desktop command not recognized."