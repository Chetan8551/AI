import os
import time
import subprocess
from datetime import datetime

import pyautogui

try:
    import psutil
except ImportError:
    psutil = None

from .apps import APP_MAP

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2


class DesktopController:
    def __init__(self, screenshot_dir="screenshots"):
        self.screenshot_dir = screenshot_dir
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def screen_size(self):
        width, height = pyautogui.size()
        return {"width": width, "height": height}

    def mouse_position(self):
        x, y = pyautogui.position()
        return {"x": x, "y": y}

    def move_mouse(self, x, y, duration=0.3):
        pyautogui.moveTo(int(x), int(y), duration=duration)
        return f"Mouse moved to {x}, {y}"

    def drag_mouse(self, x, y, duration=0.5, button="left"):
        pyautogui.dragTo(int(x), int(y), duration=duration, button=button)
        return f"Dragged mouse to {x}, {y}"

    def click(self, x=None, y=None, clicks=1, button="left"):
        if x is not None and y is not None:
            pyautogui.click(x=int(x), y=int(y), clicks=clicks, button=button)
        else:
            pyautogui.click(clicks=clicks, button=button)
        return f"{button} click done"

    def double_click(self, x=None, y=None):
        if x is not None and y is not None:
            pyautogui.doubleClick(x=int(x), y=int(y))
        else:
            pyautogui.doubleClick()
        return "Double click done"

    def right_click(self, x=None, y=None):
        if x is not None and y is not None:
            pyautogui.rightClick(x=int(x), y=int(y))
        else:
            pyautogui.rightClick()
        return "Right click done"

    def scroll_up(self, amount=500):
        pyautogui.scroll(int(amount))
        return f"Scrolled up {amount}"

    def scroll_down(self, amount=500):
        pyautogui.scroll(-int(amount))
        return f"Scrolled down {amount}"

    def type_text(self, text, interval=0.02):
        pyautogui.write(text, interval=interval)
        return f"Typed: {text}"

    def press_key(self, key):
        pyautogui.press(key)
        return f"Pressed {key}"

    def hotkey(self, *keys):
        pyautogui.hotkey(*keys)
        return f"Pressed hotkey: {' + '.join(keys)}"

    def open_start_menu(self):
        pyautogui.press("win")
        return "Start menu opened"

    def open_run(self):
        pyautogui.hotkey("win", "r")
        return "Run dialog opened"

    def show_desktop(self):
        pyautogui.hotkey("win", "d")
        return "Desktop toggled"

    def switch_window(self):
        pyautogui.hotkey("alt", "tab")
        return "Switched window"

    def close_window(self):
        pyautogui.hotkey("alt", "f4")
        return "Close window shortcut pressed"

    def copy(self):
        pyautogui.hotkey("ctrl", "c")
        return "Copied selected content"

    def paste(self):
        pyautogui.hotkey("ctrl", "v")
        return "Pasted clipboard content"

    def cut(self):
        pyautogui.hotkey("ctrl", "x")
        return "Cut selected content"

    def select_all(self):
        pyautogui.hotkey("ctrl", "a")
        return "Selected all"

    def save(self):
        pyautogui.hotkey("ctrl", "s")
        return "Save shortcut pressed"

    def undo(self):
        pyautogui.hotkey("ctrl", "z")
        return "Undo shortcut pressed"

    def redo(self):
        pyautogui.hotkey("ctrl", "y")
        return "Redo shortcut pressed"

    def enter(self):
        pyautogui.press("enter")
        return "Enter pressed"

    def backspace(self):
        pyautogui.press("backspace")
        return "Backspace pressed"

    def delete(self):
        pyautogui.press("delete")
        return "Delete pressed"

    def volume_up(self, times=5):
        for _ in range(times):
            pyautogui.press("volumeup")
        return f"Volume increased {times} step(s)"

    def volume_down(self, times=5):
        for _ in range(times):
            pyautogui.press("volumedown")
        return f"Volume decreased {times} step(s)"

    def mute_volume(self):
        pyautogui.press("volumemute")
        return "Volume mute toggled"

    def media_play_pause(self):
        pyautogui.press("playpause")
        return "Media play/pause pressed"

    def next_track(self):
        pyautogui.press("nexttrack")
        return "Next track pressed"

    def prev_track(self):
        pyautogui.press("prevtrack")
        return "Previous track pressed"

    def screenshot(self, name=None):
        if name is None:
            name = datetime.now().strftime("shot_%Y%m%d_%H%M%S.png")

        if not name.lower().endswith(".png"):
            name += ".png"

        path = os.path.join(self.screenshot_dir, name)
        image = pyautogui.screenshot()
        image.save(path)
        return path

    def open_app(self, app_name):
        app_name = app_name.strip().lower()
        target = APP_MAP.get(app_name, f"start {app_name}")

        try:
            subprocess.Popen(target, shell=True)
            return f"Opened {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    def kill_app(self, process_name):
        if psutil is None:
            return "psutil is not installed. Run: pip install psutil"

        process_name = process_name.strip().lower()
        killed = []

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                name = (proc.info["name"] or "").lower()
                if process_name in name:
                    proc.kill()
                    killed.append(name)
            except Exception:
                pass

        if killed:
            return f"Killed: {', '.join(sorted(set(killed)))}"
        return f"No running process found for {process_name}"

    def wait(self, seconds=1):
        time.sleep(seconds)
        return f"Waited {seconds} second(s)"