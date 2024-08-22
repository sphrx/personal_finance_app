import json
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent / "data" / "settings.json"

DEFAULT_SETTINGS = {
    "currency": "USD",
    "budget_limit": 1000,
    "categories": ["Продукты", "Транспорт", "Развлечения", "Счета", "Прочее"]
}

def load_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_SETTINGS

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)