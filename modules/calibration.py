import json
import threading
import time
from pathlib import Path
from typing import Tuple

import pyautogui


def _mouse_stream(stop_event: threading.Event) -> None:
    while not stop_event.is_set():
        x, y = pyautogui.position()
        print(f"\rSouris -> X: {x:4d} | Y: {y:4d}", end="", flush=True)
        time.sleep(0.05)


def _load_or_create_config(config_path: Path) -> dict:
    if not config_path.exists():
        return {
            "tesseract_path": "",
            "columns": {
                "name": {"x": None, "y": None},
                "price": {"x": None, "y": None},
            },
        }

    raw = config_path.read_text(encoding="utf-8").strip()
    if not raw:
        return {
            "tesseract_path": "",
            "columns": {
                "name": {"x": None, "y": None},
                "price": {"x": None, "y": None},
            },
        }

    return json.loads(raw)


def _capture_point(label: str) -> Tuple[int, int]:
    input(f"\nPlace la souris sur la colonne {label} puis appuie sur Entree...")
    x, y = pyautogui.position()
    print(f"{label}: X={x}, Y={y}")
    return x, y


def calibrate_columns(config_path: Path) -> None:
    print("Calibration en cours. Ctrl+C pour quitter.")

    stop_event = threading.Event()
    stream_thread = threading.Thread(target=_mouse_stream, args=(stop_event,), daemon=True)
    stream_thread.start()

    try:
        name_x, name_y = _capture_point("NOM")
        price_x, price_y = _capture_point("PRIX")
    finally:
        stop_event.set()
        stream_thread.join(timeout=1)
        print()

    config = _load_or_create_config(config_path)
    config.setdefault("columns", {})
    config["columns"]["name"] = {"x": name_x, "y": name_y}
    config["columns"]["price"] = {"x": price_x, "y": price_y}

    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"[OK] Coordonnees enregistrees dans {config_path}")
