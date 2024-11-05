
from pathlib import Path
import webbrowser


def chrome_playback(file_path:Path):
    webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(file_path.as_uri())
