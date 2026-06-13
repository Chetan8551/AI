import os
import subprocess
import datetime
import pyautogui


def execute_command(command):

    command = command.lower()

    # Open Chrome
    if "open chrome" in command:

        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen(path)
                return "Opening Chrome."

        return "Chrome not found."

    # Open Notepad
    elif "open notepad" in command:

        subprocess.Popen("notepad")
        return "Opening Notepad."

    # Open Calculator
    elif "open calculator" in command:

        subprocess.Popen("calc")
        return "Opening Calculator."

    # Open VS Code
    elif "open vscode" in command or "open vs code" in command:

        subprocess.Popen("code")
        return "Opening VS Code."

    # Screenshot
    elif "take screenshot" in command:

        filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        pyautogui.screenshot(filename)

        return f"Screenshot saved as {filename}"

    # Time
    elif "time" in command:

        current_time = datetime.datetime.now().strftime("%I:%M %p")

        return f"Current time is {current_time}"

    return None